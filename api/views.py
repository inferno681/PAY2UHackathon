from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView

from .serializers import (
    CoverRetrieveSerializer,
    CoverSerializer,
    GetTokenSerializer,

    UserSerializer,
)
from subscriptions.models import User, Cover


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
    queryset = Cover.objects.all()

    @extend_schema(tags=['Subscriptions'])
    def get_serializer_class(self):
        if self.action in ('retrieve',):
            return CoverRetrieveSerializer
        return CoverSerializer


class UserView(APIView):
    serializer_class = UserSerializer

    @extend_schema(tags=['Users'])
    def get(self, request):
        return Response(UserSerializer(request.user).data)
