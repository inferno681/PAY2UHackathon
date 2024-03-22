from django.shortcuts import get_object_or_404
from rest_framework import mixins, status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from .serializers import (
    GetTokenSerializer,
    SubscriptionSerializer,
    ShortSubscriptionSerializer,
    UserSerializer,
)
from subscriptions.models import Subscription, User


class GetTokenView(APIView):
    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        request_body=GetTokenSerializer,
        responses={
            200: openapi.Response(
                "Token obtained successfully",
                openapi.Schema(
                    type=openapi.TYPE_OBJECT, properties={
                        'token': openapi.Schema(type=openapi.TYPE_STRING)
                    }
                )),
            404: openapi.Response("User not found")
        }
    )
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

    def get_serializer_class(self):
        if self.action in ('retrieve',):
            return SubscriptionSerializer
        return ShortSubscriptionSerializer


class UserView(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = (AllowAny,)
    queryset = User.objects.all()
    serializer_class = UserSerializer
