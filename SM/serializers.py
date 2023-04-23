from rest_framework import serializers

from SM.models import Post


class PostSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        source="user.email",
        read_only=True,
    )
    likes = serializers.SerializerMethodField()
    media = serializers.ImageField(required=False)

    class Meta:
        model = Post
        fields = (
            "id",
            "content",
            "created_at",
            "email",
            "likes",
            "media",
        )

    def get_likes(self, obj):
        return [like.user.email for like in obj.likes.all()]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.pop("user", None)
        return representation
