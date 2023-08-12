from django.contrib import admin
from .models import CustomUser, Image, Post, Comment, Like

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'photo')

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'type')

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'text', 'get_likes_count')

    def get_likes_count(self, obj):
        return obj.likes.count()
    get_likes_count.short_description = 'Likes'

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'text', 'created_at')
    list_filter = ('post', 'author', 'created_at')

    def approve_comments(self, request, queryset):
        queryset.update(approval_status='approved')
    approve_comments.short_description = 'Approve selected comments'

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('author', 'post')
