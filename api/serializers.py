from rest_framework import serializers

from subscriptions.models import LENGTH_LIMIT_PHONE_NUMBER_FIELD

from subscriptions.models import Subscription


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