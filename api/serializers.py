from datetime import timedelta

from django.db.models import Exists, Max, Min, OuterRef
from django.utils import timezone
from drf_spectacular.utils import extend_schema_field
from drf_spectacular.types import OpenApiTypes
from rest_framework import serializers
from sms import send_sms

from .functions import promocode_generator
from subscriptions.models import (
    Category,
    Cover,
    Subscription,
    User,
    UserSubscription,
    ANNUAL,
    LENGTH_LIMIT_PHONE_NUMBER_FIELD,
    MONTH,
    SEMI_ANNUAL
)

ADDITION_SUBSCRIPTION_DAYS = {
    MONTH: 30,
    SEMI_ANNUAL: 180,
    ANNUAL: 365
}

SUBSCRIPTION_EXIST_ERROR = {'error': 'Вы уже подписаные на один из тарифов'}
INSUFFICIENT_FUNDS = {'error': 'Недостаточно средств на счете'}


class GetTokenSerializer(serializers.Serializer):
    phone_number = serializers.CharField(
        max_length=LENGTH_LIMIT_PHONE_NUMBER_FIELD,
        required=True)


class CategorySerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Category
        fields = ('id', 'name')


class CoverSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField()
    cashback_percent = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()
    categories = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        many=True
    )

    class Meta:
        model = Cover
        fields = (
            'id',
            'name',
            'preview',
            'logo_link',
            'price',
            'cashback_percent',
            'categories',
            'is_subscribed'
        )

    @extend_schema_field(OpenApiTypes.DECIMAL)
    def get_price(self, obj):
        return min(obj.subscriptions.aggregate(
            min_monthly_price=Min('monthly_price'),
            min_semi_annual_price=Min('semi_annual_price'),
            min_annual_price=Min('annual_price')
        ).values())

    @extend_schema_field(OpenApiTypes.DECIMAL)
    def get_cashback_percent(self, obj):
        return obj.subscriptions.aggregate(
            Max('cashback_percent')
        ).get('cashback_percent__max')

    @extend_schema_field(OpenApiTypes.BOOL)
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

    @extend_schema_field(OpenApiTypes.BOOL)
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
            'categories',
            'subscriptions'
        )


class UserSubscriptionSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        read_only=True, source='subscription.id')
    name = serializers.StringRelatedField(source='subscription.name')
    logo_link = serializers.StringRelatedField(
        source='subscription.cover.logo_link')
    is_active = serializers.SerializerMethodField()
    categories = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        many=True,
        source='subscription.cover.categories'
    )

    class Meta:
        model = UserSubscription
        fields = (
            'id',
            'name',
            'end_date',
            'price',
            'period',
            'logo_link',
            'categories',
            'promocode',
            'is_active',
        )

    @extend_schema_field(OpenApiTypes.BOOL)
    def get_is_active(self, obj):
        return obj.end_date >= timezone.now().date()


class UserSerializer(serializers.ModelSerializer):
    subscriptions = UserSubscriptionSerializer(
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


class SubscriptionReadSerializer(SubscriptionSerializer):
    logo_link = serializers.StringRelatedField(
        read_only=True, source='cover.logo_link')
    service_link = serializers.StringRelatedField(
        read_only=True, source='cover.service_link')
    categories = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        many=True,
        source='cover.categories'
    )
    period = serializers.StringRelatedField(
        allow_null=True,
        read_only=True,
        source='usersubscriptions.first.period'
    )
    autorenewal = serializers.BooleanField(
        allow_null=True,
        read_only=True,
        source='usersubscriptions.first.autorenewal'
    )
    promocode = serializers.StringRelatedField(
        allow_null=True,
        read_only=True,
        source='usersubscriptions.first.promocode'
    )

    class Meta:
        model = Subscription
        exclude = (*SubscriptionSerializer.Meta.exclude,)


class SubscriptionWriteSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Subscription.objects.all(), source='subscription.id')
    autorenewal = serializers.BooleanField(write_only=True, required=False)

    class Meta:
        model = UserSubscription
        fields = (
            'id',
            'period',
            'autorenewal'
        )

    def validate(self, data):
        subscription = data['subscription']['id']
        if (self.context.get('request').method == 'POST'
            and UserSubscription.objects.filter(
            Exists(
                UserSubscription.objects.filter(
                    subscription=OuterRef('subscription'),
                    subscription__cover=subscription.cover
                )
            )
        ).exists()):
            raise serializers.ValidationError(SUBSCRIPTION_EXIST_ERROR)
        return data

    def create(self, validated_data):
        period = validated_data['period']
        user = self.context.get('request').user
        subscription = validated_data['subscription']['id']
        period_accordance = {
            MONTH: subscription.monthly_price,
            SEMI_ANNUAL: subscription.semi_annual_price,
            ANNUAL: subscription.annual_price
        }
        if user.account_balance <= period_accordance[period]:
            raise serializers.ValidationError(INSUFFICIENT_FUNDS)
        user.account_balance -= period_accordance[period]
        user.cashback += period_accordance[period] * (
            subscription.cashback_percent / 100
        )
        user.save()
        send_sms(
            (
                'Вам оформлена подписка: '
                f'Название: {subscription.name} '
                f'Цена: {period_accordance[period]} '
                f'Описание: {subscription.description}'

            ),
            'PAY2U_phone_number',
            ['+7' + user.phone_number],
            fail_silently=False
        )
        return UserSubscription.objects.create(
            start_date=timezone.now().date(),
            end_date=(timezone.now().date() + timedelta(
                days=ADDITION_SUBSCRIPTION_DAYS[period]
            )),
            period=period,
            price=period_accordance[period],
            user=user,
            subscription=subscription,
            promocode=promocode_generator()
        )

    def update(self, usersubscription, validated_data):
        period = validated_data['period']
        if usersubscription.period != period:
            period_accordance = {
                MONTH: usersubscription.subscription.monthly_price,
                SEMI_ANNUAL: usersubscription.subscription.semi_annual_price,
                ANNUAL: usersubscription.subscription.annual_price
            }
            usersubscription.period = period
            usersubscription.price = period_accordance[period]
            usersubscription.save()
        return usersubscription

    def to_representation(self, subscription):
        return SubscriptionReadSerializer(
            subscription.subscription,
            context={'request': self.context.get('request')}).data
