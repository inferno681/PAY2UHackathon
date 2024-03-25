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
            end_date__gte=timezone.now().date()
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
            end_date__gte=timezone.now().date()
        ).exists()


class CoverRetrieveSerializer(serializers.ModelSerializer):
    subscriptions = SubscriptionSerializer(many=True, read_only=True)

    class Meta:
        model = Cover
        fields = (
            'name',
            'logo_link',
            'service_link',
            'subscriptions'
        )


class UserShortSubscriptionSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        read_only=True, source='subscription.id')
    name = serializers.StringRelatedField(source='subscription.name')
    logo_link = serializers.StringRelatedField(
        source='subscription.cover.logo_link')
    is_active = serializers.SerializerMethodField()

    class Meta:
        model = UserSubscription
        fields = (
            'id',
            'name',
            'end_date',
            'price',
            'period',
            'logo_link',
            'is_active',
        )

    def get_is_active(self, obj):
        return obj.end_date >= timezone.now().date()


class UserSerializer(serializers.ModelSerializer):
    subscriptions = UserShortSubscriptionSerializer(
        many=True, source='usersubscriptions')

    class Meta:
        model = User
        fields = (
            'phone_number',
            'first_name',
            'middle_name',
            'last_name',
            'account_balance',
            'cashback',
            'subscriptions',
        )
