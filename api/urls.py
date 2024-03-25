from django.urls import include, path
from rest_framework import routers

from .views import (
    CategoryViewSet,
    CoverViewSet,
    GetTokenView,
    SubscriptionViewSet,
    UserView
)
router_v1 = routers.DefaultRouter()
router_v1.register(
    r'covers',
    CoverViewSet,
    basename='cover'
)
router_v1.register(
    r'subscriptions',
    SubscriptionViewSet,
    basename='subscription'
)
router_v1.register(
    r'categories',
    CategoryViewSet,
    basename='category'
)


urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('auth/token/', GetTokenView.as_view(), name='signup'),
    path('my/', UserView.as_view(), name='my'),
]
