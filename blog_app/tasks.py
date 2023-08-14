from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from .models import CustomUser, Post


@shared_task
def send_notification_task(post_id):
    post = Post.objects.get(id=post_id)
    subject = "New post"
    message = (
        f"New post was created: {post.title}\n"
        f"Author: {post.author.username}\n"
        f"Creation date: {timezone.now().strftime('%B %d, %Y %H:%M')}"
    )
    recipients = CustomUser.objects.filter(is_superuser=True)
    recipient_emails = [user.email for user in recipients]
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_emails, fail_silently=False)


@shared_task
def send_comment_approval_email(comment_id):
    from blog_app.models import Comment

    comment = Comment.objects.get(id=comment_id)
    subject = f"Your comment has been approved"
    message = f"Hi {comment.post.author.username},\n\n{comment.temporary_name} has commented on your post."
    from_email = "webmaster@example.com"  # Замените на ваш реальный адрес отправителя
    recipient_emails = [comment.post.author.email]

    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_emails, fail_silently=False)
