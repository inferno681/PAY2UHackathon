from django.db.models import Max, Min
from django.utils import timezone
from rest_framework import serializers

from subscriptions.models import LENGTH_LIMIT_PHONE_NUMBER_FIELD
from subscriptions.models import Subscription, User, Cover, UserSubscription


class GetTokenSerializer(serializers.Serializer):
    phone_number = serializers.CharField(
        max_length=LENGTH_LIMIT_PHONE_NUMBER_FIELD,
        required=True)


class CoverSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField()
    cashback_percent = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Cover
        fields = (
            'id',
            'name',
            'preview',
            'logo_link',
            'price',
            'cashback_percent',
            'is_subscribed'
        )

    def get_price(self, obj):
        return min(obj.subscriptions.aggregate(
            min_monthly_price=Min('monthly_price'),
            min_semi_annual_price=Min('semi_annual_price'),
            min_annual_price=Min('annual_price')
        ).values())

    def get_cashback_percent(self, obj):
        return obj.subscriptions.aggregate(
            Max('cashback_percent')
        ).get('cashback_percent__max')

    def get_is_subscribed(self, obj):
        return UserSubscription.objects.filter(
            subscription__in=obj.subscriptions.all(),
            user=self.context.get('request').user,
            end_date__gte=timezone.now()
        ).exists()


class SubscriptionSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()
    end_date = serializers.DateField(
        allow_null=True,
        source='usersubscriptions.first.end_date'
    )

    class Meta:
        model = Subscription
        exclude = ('users',)

    def get_is_subscribed(self, obj):
        return UserSubscription.objects.filter(
            subscription=obj,
            user=self.context.get('request').user,
            end_date__gte=timezone.now()
        ).exists()


class CoverRetrieveSerializer(serializers.ModelSerializer):
    subscriptions = SubscriptionSerializer(many=True, read_only=True)

    class Meta:
        model = Cover
        fields = (
            'name',
            'logo_link',
            'subscriptions'
        )


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
