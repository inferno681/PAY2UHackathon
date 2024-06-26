from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView

from .filters import CoverFilter
from .functions import pdf_receipt_generator
from .serializers import (
    CategorySerializer,
    CoverRetrieveSerializer,
    CoverSerializer,
    GetTokenSerializer,
    SubscriptionReadSerializer,
    SubscriptionWriteSerializer,
    UserSerializer
)
from subscriptions.models import (
    Category,
    Cover,
    Subscription,
    User,
    UserSubscription
)


class GetTokenView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = GetTokenSerializer
    pagination_class = None

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


@extend_schema(tags=['Categories'])
class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = None


@extend_schema(tags=['Covers'])
class CoverViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Cover.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CoverFilter

    def get_serializer_class(self):
        if self.action in ('retrieve',):
            return CoverRetrieveSerializer
        return CoverSerializer


class UserView(APIView):
    serializer_class = UserSerializer
    pagination_class = None

    @extend_schema(tags=['Users'])
    def get(self, request):
        return Response(UserSerializer(request.user).data)


@extend_schema(
    tags=['Subscriptions'],
    responses={200: SubscriptionReadSerializer}
)
class SubscriptionViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = SubscriptionReadSerializer
    queryset = Subscription.objects.all()
    http_method_names = ('get', 'post', 'patch')

    def get_serializer_class(self):
        if self.action in ('retrieve',):
            return SubscriptionReadSerializer
        return SubscriptionWriteSerializer

    @extend_schema(
        description='Get the receipt for the subscription',
        responses={
            200: OpenApiResponse(
                description='Receipt for the subscription',
            )
        }
    )
    @action(methods=['get'], detail=True)
    def get_reciept(self, request, pk=None):
        usersubscription = get_object_or_404(
            UserSubscription, subscription_id=pk, user=request.user)
        return pdf_receipt_generator(
            id=usersubscription.id,
            phone_number=request.user.phone_number,
            name=usersubscription.subscription.name,
            end_date=usersubscription.end_date,
            promocode=usersubscription.promocode,
            price=usersubscription.price
        )
