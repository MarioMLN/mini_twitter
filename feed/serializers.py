from rest_framework.exceptions import ValidationError
from rest_framework import serializers
from .models import Post, PostContent, Likes


class PostContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostContent
        fields = ['image', 'text']


class LikesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Likes
        fields = ['user', 'post']


class PostSerializer(serializers.ModelSerializer):
    post_content_serializer = PostContentSerializer()

    class Meta:
        model = Post
        fields = ['user',
                  'created_at',
                  'like_count',
                  'post_content_serializer']
        read_only_fields = ['user', 'created_at', 'like_count']

    def validate(self, attrs):
        if self.request.user != self.author:
            raise ValidationError(
                "You can't change the post of another user.",
                code="cannot_change_post_of_another_user"
            )

        return super().validate(attrs)
