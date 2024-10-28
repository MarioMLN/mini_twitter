from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

from user.models import Follow


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ['id', 'follower', 'following', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate(self, attrs):
        if attrs['follower'] == attrs['following']:
            raise serializers.ValidationError("Você não pode seguir a si mesmo.")
        return attrs

    def create(self, validated_data):
        follower = validated_data['follower']
        following = validated_data['following']

        follow_instance, created = Follow.objects.get_or_create(follower=follower, following=following)

        if not created:
            raise serializers.ValidationError("Você já está seguindo este usuário.")

        return follow_instance
