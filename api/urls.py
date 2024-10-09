from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import UserViewSet, VideoViewSet, SubscriptionViewSet, SubscriptionTypeViewSet, HistoryViewSet, RegisterView, WalletViewSet, CommentViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'videos', VideoViewSet)
router.register(r'subscriptions', SubscriptionViewSet)
router.register(r'subscription-types', SubscriptionTypeViewSet)
router.register(r'history', HistoryViewSet)
router.register(r'wallet', WalletViewSet, basename="wallet")
router.register(r'comment', CommentViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/', include('dj_rest_auth.urls')),
]

