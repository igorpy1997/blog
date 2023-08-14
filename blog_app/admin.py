from django.contrib import admin
from .models import CustomUser, Image, Post, Comment, Like
from blog_app.tasks import send_comment_approval_email


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("username", "first_name", "last_name", "email", "photo")


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ("title", "type")


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("author", "text", "get_likes_count")

    def get_likes_count(self, obj):
        return obj.likes.count()

    get_likes_count.short_description = "Likes"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("post", "temporary_name", "author", "text", "created_at")
    list_filter = ("post", "temporary_name", "author", "created_at")

    def save_model(self, request, obj, form, change):
        if change and obj.approval_status == "approved" and obj.post.author is not None:
            send_comment_approval_email.delay(obj.id)
        super().save_model(request, obj, form, change)


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ("author", "post")
