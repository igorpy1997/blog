from django.conf import settings
from django.contrib import admin
from django.core.mail import send_mail

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
    list_display = ('post', 'temporary_name', 'author', 'text', 'created_at')
    list_filter = ('post', 'temporary_name', 'author', 'created_at')

    def send_comment_approval_email(comment):
        subject = f'Your comment has been approved'
        message = f'Hi {comment.post.author.username},\n\n{comment.temporary_name} has commented on your post.'
        from_email = 'webmaster@example.com'  # Замените на ваш реальный адрес отправителя
        recipients = [comment.post.author.email]  # Список получателей (в данном случае, автор поста)


        recipient_emails = [user.email for user in recipients]
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_emails, fail_silently=False)


    def approve_comments(self, request, queryset):
        queryset.update(approval_status='approved')

        # Отправка письма после одобрения комментария
        for comment in queryset:
            self.send_comment_approval_email(comment)

    approve_comments.short_description = 'Approve selected comments'






@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('author', 'post')
