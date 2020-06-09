from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Post, Comment, Group, Follow, User


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field="username", read_only=True
    )

    class Meta:
        fields = ("id", "text", "author", "pub_date")
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field="username", read_only=True
    )

    class Meta:
        fields = ("id", "author", "post", "text", "created")
        model = Comment


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            "id",
            "title",
        )
        model = Group


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field="username", read_only=True)
    following = serializers.SlugRelatedField(
        slug_field="username", queryset=User.objects.all()
    )

    class Meta:
        fields = (
            "id",
            "user",
            "following",
        )
        model = Follow

    def validate(self, data):
        user = self.context["request"].user
        following = data["following"]
        if user == following:
            raise serializers.ValidationError("You can not follow yourself")
        follow = Follow.objects.filter(user=user, following=following)
        if follow.exists():
            raise serializers.ValidationError(
                "You are already following this user"
            )
        return data
