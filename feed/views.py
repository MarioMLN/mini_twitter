from rest_framework import viewsets, generics, status
from rest_framework.response import Response

from user.models import User
from user.serializers import UserSerializer
from .models import Post, Likes
from .serializers import PostSerializer, LikesSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination


class FeedPagination(PageNumberPagination):
    page_size = 10


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request):
        post = self.get_object()

        if request.user != post.user:
            return Response(
                {"error": "You are not the author of this post."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = self.get_serializer(post, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {"action": "You edited your post."},
            status=status.HTTP_200_OK
        )

    def delete(self, request):
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


class LikesViewSet(viewsets.ModelViewSet):
    queryset = Likes.objects.all()
    serializer_class = LikesSerializer
    permission_classes = [IsAuthenticated]


class FollowView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):

        return self.request.user

    def update(self):
        user_to_follow = User.objects.get(id=self.kwargs['pk'])
        if self.request.user == user_to_follow:
            return Response(
                {
                    "detail": "You can't follow yourself."
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        if self.request.user in user_to_follow.followers.all():
            user_to_follow.followers.remove(self.request.user)
            message = f"You have unfollowed {user_to_follow.username}."

        else:
            user_to_follow.followers.add(self.request.user)
            message = f"You have followed {user_to_follow.username}."

        return Response(
            {
                "detail": message
            },
            status=status.HTTP_200_OK
        )


class FeedView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = FeedPagination

    def get_queryset(self):
        following_users_ids = self.request.user.followers.values_list('id', flat=True)
        queryset = Post.objects.filter(user__id__in=following_users_ids)

        return queryset
