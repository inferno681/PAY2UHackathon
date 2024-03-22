from django.urls import include, path
from rest_framework import routers

from .views import GetTokenView, SubscriptionViewSet

router_v1 = routers.DefaultRouter()
router_v1.register(
    r'subscription',
    SubscriptionViewSet,
    basename='subscription'
)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('auth/token/', GetTokenView.as_view(), name='signup'),
]