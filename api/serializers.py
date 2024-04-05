from .tasks import send_sms_task
from subscriptions import (
    ANNUAL,
    DONE,
    LENGTH_LIMIT_PHONE_NUMBER_FIELD,
    MONTH,
    SEMI_ANNUAL,
    SUBSCRIPTION_PERIOD
)
from subscriptions.models import (
    Category,
    Cover,
    Subscription,
    User,
    UserSubscription,
)
from .functions import cashback_calculation, payment, promocode_generator
from datetime import timedelta

from django.db.models import Exists, Max, Min, OuterRef, Sum
from django.shortcuts import get_object_or_404
from django.utils import timezone
from drf_spectacular.utils import extend_schema_field
from drf_spectacular.types import OpenApiTypes
from rest_framework import serializers

from .constants import (
    ADDITION_SUBSCRIPTION_DAYS,
    INSUFFICIENT_FUNDS,
    NO_DATA_TRANSFERED,
    PAY2U_PHONE_NUMBER,
    SMS_TEXT,
    SUBSCRIPTION_EXIST_ERROR

)


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
    end_date = serializers.SerializerMethodField()

    class Meta:
        model = Subscription
        exclude = ('users',)

    @extend_schema_field(OpenApiTypes.DATE)
    def get_end_date(self, obj):
        usersubscription = obj.usersubscriptions.filter(
            user=self.context.get('request').user
        ).first()
        return str(usersubscription.end_date) if usersubscription else None

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
    description = serializers.StringRelatedField(
        source='subscription.description')
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
            'description',
            'end_date',
            'price',
            'period',
            'logo_link',
            'categories',
            'autorenewal',
            'promocode',
            'is_active',
        )

    @extend_schema_field(OpenApiTypes.BOOL)
    def get_is_active(self, obj):
        return obj.end_date >= timezone.now().date()


class UserSerializer(serializers.ModelSerializer):
    subscriptions = UserSubscriptionSerializer(
        many=True, source='usersubscriptions')
    current_month_expenses = serializers.SerializerMethodField()

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
            'current_month_expenses'
        )

    @extend_schema_field(OpenApiTypes.DECIMAL)
    def get_current_month_expenses(self, user):
        return user.transactions.filter(
            timestamp__month=timezone.now().month,
            timestamp__year=timezone.now().year,
            status=DONE
        ).aggregate(
            current_month_expenses=Sum('amount')
        )['current_month_expenses']


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
    period = serializers.SerializerMethodField()
    autorenewal = serializers.SerializerMethodField()
    promocode = serializers.SerializerMethodField()
    cover_name = serializers.StringRelatedField(
        read_only=True, source='cover.name'
    )

    class Meta:
        model = Subscription
        exclude = (*SubscriptionSerializer.Meta.exclude,)

    @extend_schema_field(OpenApiTypes.STR)
    def get_period(self, obj):
        usersubscription = obj.usersubscriptions.filter(
            user=self.context.get('request').user
        ).first()
        return usersubscription.period if usersubscription else None

    @extend_schema_field(OpenApiTypes.BOOL)
    def get_autorenewal(self, obj):
        usersubscription = obj.usersubscriptions.filter(
            user=self.context.get('request').user
        ).first()
        return usersubscription.autorenewal if usersubscription else None

    def get_promocode(self, obj):
        usersubscription = obj.usersubscriptions.filter(
            user=self.context.get('request').user
        ).first()
        return usersubscription.promocode if usersubscription else None


class SubscriptionWriteSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Subscription.objects.all(),
        required=False
    )
    autorenewal = serializers.BooleanField(required=False)
    period = serializers.ChoiceField(
        required=False, choices=SUBSCRIPTION_PERIOD)

    class Meta:
        model = Subscription
        fields = (
            'id',
            'period',
            'autorenewal'
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.context.get('request') and self.context[
            'request'
        ].method == 'POST':
            for field in ('id', 'period'):
                self.fields[field].required = True

    def validate(self, data):
        if not data:
            raise serializers.ValidationError(NO_DATA_TRANSFERED)
        subscription = data.get('id', self.instance)
        if (self.context.get('request').method == 'POST'
            and UserSubscription.objects.filter(
            Exists(
                UserSubscription.objects.filter(
                    subscription=OuterRef('subscription'),
                    subscription__cover=subscription.cover,
                    user=self.context.get('request').user

                )
            )
        ).exists()):
            raise serializers.ValidationError(SUBSCRIPTION_EXIST_ERROR)
        return data

    def create(self, validated_data):
        period = validated_data['period']
        user = self.context.get('request').user
        subscription = validated_data['id']
        period_accordance = {
            MONTH: subscription.monthly_price,
            SEMI_ANNUAL: subscription.semi_annual_price,
            ANNUAL: subscription.annual_price
        }
        price = period_accordance[period]
        if not payment(user, subscription, price):
            raise serializers.ValidationError(INSUFFICIENT_FUNDS)
        cashback_calculation(user, price, subscription.cashback_percent)
        promocode = promocode_generator()
        send_sms_task.delay(
            (SMS_TEXT.format(
                name=subscription.name,
                price=period_accordance[period],
                description=subscription.description,
                promocode=promocode)),
            PAY2U_PHONE_NUMBER,
            user.phone_number,
        )
        return UserSubscription.objects.create(
            start_date=timezone.now().date(),
            end_date=(timezone.now().date() + timedelta(
                days=ADDITION_SUBSCRIPTION_DAYS[period]
            )),
            period=period,
            price=price,
            user=user,
            subscription=subscription,
            promocode=promocode
        )

    def update(self, subscription, validated_data):
        usersubscription = get_object_or_404(
            UserSubscription,
            subscription=subscription,
            user=self.context.get('request').user)
        period = validated_data.get('period', usersubscription.period)
        autorenewal = validated_data.get(
            'autorenewal', usersubscription.autorenewal)
        if usersubscription.period != period:
            period_accordance = {
                MONTH: usersubscription.subscription.monthly_price,
                SEMI_ANNUAL: usersubscription.subscription.semi_annual_price,
                ANNUAL: usersubscription.subscription.annual_price
            }
            usersubscription.period = period
            usersubscription.price = period_accordance[period]
        if usersubscription.autorenewal != autorenewal:
            usersubscription.autorenewal = autorenewal

        if usersubscription.end_date < timezone.now().date(
        ) and validated_data.get('autorenewal') is True:
            user = self.context.get('request').user
            period_accordance = {
                MONTH: subscription.monthly_price,
                SEMI_ANNUAL: subscription.semi_annual_price,
                ANNUAL: subscription.annual_price
            }
            price = period_accordance[period]
            if not payment(user, subscription, price):
                raise serializers.ValidationError(INSUFFICIENT_FUNDS)
            cashback_calculation(user, price, subscription.cashback_percent)
            promocode = promocode_generator()
            send_sms_task.delay(
                (SMS_TEXT.format(
                    name=subscription.name,
                    price=period_accordance[period],
                    description=subscription.description,
                    promocode=promocode)),
                PAY2U_PHONE_NUMBER,
                user.phone_number,
            )
            usersubscription.start_date = timezone.now().date()
            usersubscription.price = price
            usersubscription.end_date = (timezone.now().date() + timedelta(
                days=ADDITION_SUBSCRIPTION_DAYS[period]
            ))
            usersubscription.promocode = promocode

        usersubscription.save()
        return usersubscription

    def to_representation(self, subscription):
        return SubscriptionReadSerializer(
            subscription.subscription,
            context={'request': self.context.get('request')}).data
