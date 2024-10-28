from django.urls import path
from user.views import FollowUserView, TokenRefreshView, UserLoginView, UserRegistrationView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('follow/<int:user_id>/', FollowUserView.as_view(), name='follow'),
]
