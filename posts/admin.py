from django.contrib import admin
from .models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'content_preview', 'comments_count', 'created_at', 'is_active')
    list_filter = ('is_active', 'created_at')
    search_fields = ('author__phone_number', 'content')
    readonly_fields = ('created_at', 'updated_at')
    list_per_page = 20
    
    def content_preview(self, obj):
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content Preview'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'post_id', 'content_preview', 'created_at', 'is_active')
    list_filter = ('is_active', 'created_at')
    search_fields = ('author__phone_number', 'content', 'post__content')
    readonly_fields = ('created_at', 'updated_at')
    list_per_page = 20
    
    def content_preview(self, obj):
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content Preview'
