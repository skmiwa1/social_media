from django.contrib.auth import get_user_model
from rest_framework import viewsets, generics, permissions
from rest_framework.response import Response

from SM.models import Post, Like
from SM.permissions import IsAdminOrIfAuthenticatedReadOnly, IsAuthorOrReadOnly
from SM.serializers import PostSerializer, OwnPostSerializer, LikeSerializer

User = get_user_model()


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorOrReadOnly,
        IsAdminOrIfAuthenticatedReadOnly,
    )

    @staticmethod
    def _params_to_ints(qs):
        return [int(str_id) for str_id in qs.split(",")]

    def get_queryset(self):
        queryset = Post.objects.all()
        content = self.request.query_params.get("content")
        authors = self.request.query_params.get("author")
        if content:
            queryset = queryset.filter(content__icontains=content)
        if authors:
            authors_id = self._params_to_ints(authors)
            queryset = queryset.filter(author_id__in=authors_id)
        return queryset

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user == request.user:
            serializer = self.get_serializer(
                instance,
                data=request.data,
                partial=True,
            )
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
        else:
            return Response(
                {"error": "You are not authorized to update this post."},
                status=403,
            )


class MyPostsView(generics.ListAPIView):
    serializer_class = OwnPostSerializer

    def get_queryset(self):
        user_id = self.request.user.id
        posts = Post.objects.filter(user_id=user_id)
        return posts


class LikeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)