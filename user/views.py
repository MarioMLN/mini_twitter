from rest_framework import generics
from .serializers import FollowSerializer, UserSerializer
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from .models import Follow

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


class FollowUserView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FollowSerializer

    def post(self, request, user_id):
        user_to_follow = get_object_or_404(User, id=user_id)

        if user_to_follow == request.user:
            return Response({"detail": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data={'follower': request.user.id, 'following': user_to_follow.id})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)

    def delete(self, request, user_id):
        user_to_unfollow = get_object_or_404(User, id=user_id)

        if user_to_unfollow == request.user:
            return Response({"detail": "You cannot unfollow yourself"}, status=status.HTTP_400_BAD_REQUEST)

        deleted_count, _ = Follow.objects.filter(follower=request.user, following=user_to_unfollow).delete()

        if deleted_count > 0:
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"detail": "You are not a follower"}, status=status.HTTP_400_BAD_REQUEST)