from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListCreateAPIView
from rest_framework.filters import SearchFilter
from rest_framework import permissions
from .permissions import IsAuthorOrReadOnly
from .models import Post, Comment, Group, Follow
from .serializers import PostSerializer, CommentSerializer, GroupSerializer, FollowSerializer


class PostViewSet(ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnly, permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Post.objects.all()
        group_id = self.request.query_params.get('group', None)
        if group_id and self.action == 'list':
            queryset = queryset.filter(group__id=group_id)
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)  


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly, permissions.IsAuthenticatedOrReadOnly]

    def get_post(self):
        post = get_object_or_404(Post, id=self.kwargs['post_id'])
        return post

    def get_queryset(self):
        queryset = Comment.objects.filter(post=self.get_post()).all()
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user, post=self.get_post())

    def perform_update(self, serializer):
        serializer.save(author=self.request.user, post=self.get_post())


class GroupView(ListCreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class FollowView(ListCreateAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    filter_backends = [SearchFilter]
    search_fields = ['=user__username', '=following__username']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
