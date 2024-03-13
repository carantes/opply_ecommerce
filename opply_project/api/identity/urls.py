from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView
)
from api.identity.views import identity_root, RegisterUserView, SignInUserView, CustomerViewSet

router = routers.DefaultRouter()
router.register(r'customers', CustomerViewSet)

urlpatterns = [
    path('', identity_root, name='identity_root'),
    path('token/', SignInUserView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('register/', RegisterUserView.as_view(), name='register_user'),
    path('', include(router.urls)),
]
