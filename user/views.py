from rest_framework import generics
from .models import User
from .serializers import UserSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView
    )


class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class UserLoginView(TokenObtainPairView):
    """View for user login and obtaining a JWT token"""
    permission_classes = [AllowAny]


class TokenRefreshView(TokenRefreshView):
    """View for refreshing JWT token"""
    permission_classes = [AllowAny]
