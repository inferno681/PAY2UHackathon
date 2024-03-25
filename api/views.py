from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import mixins, status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView

from .filters import CoverFilter
from .serializers import (
    CategorySerializer,
    CoverRetrieveSerializer,
    CoverSerializer,
    GetTokenSerializer,
    UserSerializer,
    SubscriptionReadSerializer,
    SubscriptionWriteSerializer
)
from subscriptions.models import (
    Category,
    Cover,
    User,
    Subscription,
    UserSubscription
)


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


class CategoryViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CoverViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Cover.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CoverFilter

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


class SubscriptionViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = SubscriptionReadSerializer
    queryset = Subscription.objects.all()
    http_method_names = ('get', 'post', 'patch')

    @extend_schema(tags=['Subscriptions'])
    def get_queryset(self):
        if self.action in ('retrieve',):
            return Subscription.objects.all()
        return UserSubscription.objects.all()

    def get_serializer_class(self):
        if self.action in ('retrieve',):
            return SubscriptionReadSerializer
        return SubscriptionWriteSerializer
