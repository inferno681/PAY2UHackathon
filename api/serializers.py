from django.utils import timezone

from rest_framework import serializers

from subscriptions.models import LENGTH_LIMIT_PHONE_NUMBER_FIELD
from subscriptions.models import Subscription, User


class GetTokenSerializer(serializers.Serializer):
    phone_number = serializers.CharField(
        max_length=LENGTH_LIMIT_PHONE_NUMBER_FIELD,
        required=True)


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        exclude = ('users',)


class ShortSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = (
            'id',
            'name',
            'logo_link',
            'monthly_price',
            'cashback_procent'
        )


class UserShortSubscriptionSerializer(ShortSubscriptionSerializer):
    start_date = serializers.DateField(
        source='usersubscriptions__start_date')
    end_date = serializers.DateField(
        read_only=True, source='usersubscriptions__end_date')
    price = serializers.ReadOnlyField(source='usersubscriptions__price')

    class Meta:
        model = Subscription
        fields = (
            *ShortSubscriptionSerializer.Meta.fields,
            'start_date',
            'end_date',
            'price')


class UserSerializer(serializers.ModelSerializer):
    active_subscriptions = serializers.SerializerMethodField()
    inactive_subscriptions = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'phone_number',
            'first_name',
            'middle_name',
            'last_name',
            'account_balance',
            'cashback',
            'active_subscriptions',
            'inactive_subscriptions',
        )

    def get_active_subscriptions(self, obj):
        return UserShortSubscriptionSerializer(
            obj.subscription_set.filter(
                usersubscriptions__end_date__gte=timezone.now()).values(
                *ShortSubscriptionSerializer.Meta.fields,
                'usersubscriptions__start_date',
                'usersubscriptions__end_date',
                'usersubscriptions__price'),
            many=True,
            read_only=True
        ).data

    def get_inactive_subscriptions(self, obj):
        return UserShortSubscriptionSerializer(
            obj.subscription_set.filter(
                usersubscriptions__end_date__lt=timezone.now()).values(
                *ShortSubscriptionSerializer.Meta.fields,
                'usersubscriptions__start_date',
                'usersubscriptions__end_date',
                'usersubscriptions__price'),
            many=True,
            read_only=True
        ).data
