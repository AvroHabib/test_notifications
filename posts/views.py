from rest_framework import generics, permissions, status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from .models import Post, Comment
from .serializers import (
    PostSerializer,
    PostCreateSerializer,
    CommentSerializer,
    CommentCreateSerializer
)
from notifications.tasks import send_post_notification, send_comment_notification


@extend_schema(
    request=PostCreateSerializer,
    responses={201: PostSerializer}
)
class PostCreateView(generics.CreateAPIView):
    serializer_class = PostCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        post = serializer.save()
        
        # Send push notification to all users
        send_post_notification.delay(post.id)
        
        # Return detailed post data
        response_serializer = PostSerializer(post, context={'request': request})
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


@extend_schema(responses={200: PostSerializer})
class PostListView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Post.objects.filter(is_active=True).select_related('author')


@extend_schema(responses={200: PostSerializer})
class PostDetailView(generics.RetrieveAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'
    
    def get_queryset(self):
        return Post.objects.filter(is_active=True).select_related('author')


@extend_schema(
    request=CommentCreateSerializer,
    responses={201: CommentSerializer}
)
class CommentCreateView(generics.CreateAPIView):
    serializer_class = CommentCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        comment = serializer.save()
        
        # Send push notification to post author (if not the same user)
        if comment.post.author != comment.author:
            send_comment_notification.delay(comment.id)
        
        # Return detailed comment data
        response_serializer = CommentSerializer(comment, context={'request': request})
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


@extend_schema(responses={200: CommentSerializer})
class CommentListView(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        return Comment.objects.filter(
            post_id=post_id,
            is_active=True
        ).select_related('author', 'post')


@extend_schema(responses={200: CommentSerializer})
class CommentDetailView(generics.RetrieveAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'
    
    def get_queryset(self):
        return Comment.objects.filter(is_active=True).select_related('author', 'post')
