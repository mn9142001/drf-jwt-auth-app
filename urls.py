from .views import SignupView, JWTLoginView, PasswordChangeView, PasswordResetVerifyView, PasswordResetSendView, PasswordResetConfirmView, PromoteUserPermissionView
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.routers import DefaultRouter

utils_router = DefaultRouter()

utils_router.register('user/promote', PromoteUserPermissionView)

admin_utils = [
] + utils_router.urls


password_urls = [
    path('reset/send/', PasswordResetSendView.as_view()),
    path('reset/verify/', PasswordResetVerifyView.as_view()),
    path('reset/change/', PasswordResetConfirmView.as_view()),
    path('change/', PasswordChangeView.as_view()),
]

auth_urls = [
    path('token/refresh/', TokenRefreshView.as_view()),
    path('signup/', SignupView.as_view()),
    path('login/', JWTLoginView.as_view()),
    path('password/', include(password_urls))
]

urlpatterns = [
    path('auth/', include(auth_urls)),
    path('utils/', include(admin_utils)),
]