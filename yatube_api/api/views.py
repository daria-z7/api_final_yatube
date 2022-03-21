from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, filters
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from posts.models import Post, Group, Follow, User
from api.serializers import PostSerializer, GroupSerializer
from api.serializers import CommentSerializer, FollowSerializer
from api.permissions import OwnerOrReadOnly
from api.mixins import CreateListViewSet


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (OwnerOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (OwnerOrReadOnly,)

    def get_queryset(self):
        post = get_object_or_404(
            Post,
            id=self.kwargs.get("post_id"))
        new_queryset = post.comments.all()
        return new_queryset

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            post=get_object_or_404(Post, id=self.kwargs.get("post_id"))
        )

    def perform_update(self, serializer):
        serializer.save(
            author=self.request.user,
            post=get_object_or_404(Post, id=self.kwargs.get("post_id"))
        )


class FollowViewSet(CreateListViewSet):
    serializer_class = FollowSerializer

    def get_queryset(self):
        user = self.request.user
        # return Follow.objects.filter(user=user)
        return user.follower.all()
    search_fields = ('following__username',)
    filter_backends = (filters.SearchFilter,)

    def perform_create(self, serializer):
        # following = User.objects.get(username=self.request.data.get('following'))
        following=get_object_or_404(User, username=self.request.data.get('following'))
        return serializer.save(
            user=self.request.user,
            following=following,
        )
