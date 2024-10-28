from rest_framework.exceptions import ValidationError
from rest_framework import serializers

from user.serializers import UserSerializer
from .models import Post, Likes


class LikesSerializer(serializers.Serializer):
    class Meta:
        model = Likes
        fields = ['user', 'post']

    def create(self, validated_data):
        post_pk = self.context['request'].parser_context['kwargs'].get('post_pk')
        post = Post.objects.get(pk=post_pk)
        like = Likes.objects.create(
            user=self.context['request'].user,
            post=post
        )
        return like


class PostSerializer(serializers.Serializer):
    text = serializers.CharField(required=False)
    image = serializers.ImageField(required=False)
    created_at = serializers.DateTimeField(required=False)
    like_count = serializers.SerializerMethodField()
    user = UserSerializer(required=False)

    class Meta:
        model = Post
        fields = [
            'user__username',
            'created_at',
            'like_count',
            'image',
            'text',
        ]
        read_only_fields = ['created_at', 'like_count']

    def create(self, validated_data):
        post = Post.objects.create(
            user=self.context['request'].user,
        )
        if 'text' in validated_data:
            post.text = validated_data['text']

        if 'image' in validated_data:
            post.image = validated_data['image']

        post.save()

        return post

    def get_like_count(sel, obj):
        return obj.likes.count()
