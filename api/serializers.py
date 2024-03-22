
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
    start_date = serializers.DateTimeField(
        read_only=True, source='usersubscriptions__start_date')
    end_date = serializers.DateTimeField(
        read_only=True, source='usersubscriptions__end_date')
    price = serializers.ReadOnlyField(source='usersubscriptions__price')

    class Meta:
        model = Subscription
        fields = (*ShortSubscriptionSerializer.Meta.fields,
                  'end_date', 'start_date', 'price')


class UserSerializer(serializers.ModelSerializer):
    subscriptions = serializers.SerializerMethodField()

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

    def get_subscriptions(self, obj):

        return UserShortSubscriptionSerializer(
            obj.subscription_set.all(), many=True, read_only=True
        ).data
