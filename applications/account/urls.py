from django.urls import path
from .views import RegisterView, ActivationView, ForgotPasswordAPIView, ForgotPasswordCompleteAPIView, CustomUserUpdateAPIView, AccountView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('activate/<uuid:activation_code>/', ActivationView.as_view()),

    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('reset_password', ForgotPasswordAPIView.as_view()),
    path('reset_password_complete', ForgotPasswordCompleteAPIView.as_view()),

    path('update/', CustomUserUpdateAPIView.as_view()),
    path('users/me/', AccountView.as_view()),
]
