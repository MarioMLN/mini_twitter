from rest_framework import viewsets, generics, status
from rest_framework.response import Response

from django.contrib.auth.models import User
from user.models import Follow
from user.serializers import UserSerializer
from .models import Post, Likes
from .serializers import PostSerializer, LikesSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination


class FeedPagination(PageNumberPagination):
    page_size = 10


class PostViewSet(generics.CreateAPIView, generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args,**kwargs):
        post = self.get_object()

        if request.user != post.user:
            return Response(
                {"error": "You are not the author of this post."},
                status=status.HTTP_403_FORBIDDEN
            )

        return Response(
            {"action": "You edited your post."},
            status=status.HTTP_200_OK
        )

    def delete(self, request, *args, **kwargs):
        post = self.get_object()

        if request.user != post.user:
            return Response(
                {"error": "You are not the author of this post."},
                status=status.HTTP_403_FORBIDDEN
            )

        post.delete()
        return Response(
            {"action": "You deleted your post."},
            status=status.HTTP_204_NO_CONTENT
        )


class LikesView(generics.CreateAPIView):
    queryset = Likes.objects.all()
    serializer_class = LikesSerializer
    permission_classes = [IsAuthenticated]


class FeedView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = FeedPagination

    def get_queryset(self):
        following_users_ids = Follow.objects.filter(follower=self.request.user).values_list(
            'id',
            flat=True
        )
        queryset = Post.objects.filter(user__id__in=following_users_ids)

        return queryset
