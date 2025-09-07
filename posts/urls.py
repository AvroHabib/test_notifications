from django.urls import path
from .views import (
    PostCreateView,
    PostListView,
    PostDetailView,
    CommentCreateView,
    CommentListView,
    CommentDetailView
)

urlpatterns = [
    # Posts
    path('posts/', PostListView.as_view(), name='post-list'),
    path('posts/create/', PostCreateView.as_view(), name='post-create'),
    path('posts/<int:id>/', PostDetailView.as_view(), name='post-detail'),
    
    # Comments
    path('posts/<int:post_id>/comments/', CommentListView.as_view(), name='comment-list'),
    path('comments/create/', CommentCreateView.as_view(), name='comment-create'),
    path('comments/<int:id>/', CommentDetailView.as_view(), name='comment-detail'),
]
