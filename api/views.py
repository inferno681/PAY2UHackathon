from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, OpenApiExample
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView

from .serializers import (
    GetTokenSerializer,
    SubscriptionSerializer,
    ShortSubscriptionSerializer,
    UserSerializer,
)
from subscriptions.models import Subscription, User


class GetTokenView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = GetTokenSerializer

    @extend_schema(tags=['Users'])
    def post(self, request):
        serializer = GetTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            User,
            phone_number=serializer.data['phone_number']
        )
        token = RefreshToken.for_user(user).access_token
        return Response({'token': str(token)}, status=status.HTTP_200_OK)


class SubscriptionViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (AllowAny,)
    queryset = Subscription.objects.all()

    @extend_schema(tags=['Subscriptions'])
    def get_serializer_class(self):
        if self.action in ('retrieve',):
            return SubscriptionSerializer
        return ShortSubscriptionSerializer


class UserView(APIView):
    serializer_class = UserSerializer

    @extend_schema(tags=['Users'],
                   examples=[
        OpenApiExample(
            "example",
            value={
                "phone_number": "9211231212",
                "first_name": "string",
                "middle_name": "string ",
                "last_name": "string",
                "account_balance": "15000.00",
                "cashback": "151.00",
                "active_subscriptions": [
                    {
                            "id": 1,
                            "name": "string",
                            "logo_link": "string",
                            "monthly_price": "100.00",
                            "cashback_procent": "10.00",
                            "start_date": "2024-03-15",
                            "end_date": "2024-04-15",
                            "price": "100.00"
                    }
                ],
                "inactive_subscriptions": [{"id": 51,
                                            "name": "string",
                                            "logo_link": "string",
                                            "monthly_price": "100.00",
                                            "cashback_procent": "10.00",
                                            "start_date": "2024-03-15",
                                            "end_date": "2024-01-15",
                                            "price": "100.00"}]
            },
            response_only=True,
        ),
    ]
    )
    def get(self, request):
        return Response(UserSerializer(request.user).data)
