import os
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    photo = models.ImageField(upload_to="user_photos/", null=True, blank=True)

    def save(self, *args, **kwargs):
        # Check if the object is already in the database
        if self.pk:
            try:
                # Retrieve the old photo associated with the user_forms
                old_photo = CustomUser.objects.get(pk=self.pk).photo
                # Check if there"s a new photo and it"s different from the old photo
                if self.photo and old_photo and self.photo != old_photo:
                    # Delete the old photo from storage
                    old_photo.delete(save=False)
            except CustomUser.DoesNotExist:
                pass

        super(CustomUser, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Удаление файла фотографии при удалении объекта пользователья
        if self.photo:
            # Получить путь к файлу фотографии
            file_path = self.photo.path
            # Удалить файл из системы хранения файлов
            if os.path.exists(file_path):
                os.remove(file_path)
        # Вызвать метод delete() базового класса для выполнения обычного удаления объекта
        super().delete(*args, **kwargs)


class Image(models.Model):
    IMAGE_TYPES = (
        ("header", "Header Image"),
        ("profile", "Profile Image"),
    )
    title = models.CharField(max_length=100)
    photo = models.ImageField(upload_to="images/")
    type = models.CharField(max_length=10, choices=IMAGE_TYPES)


class Post(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, default="No title")  # Добавляем поле заголовка
    text = models.TextField()
    likes = models.ManyToManyField(CustomUser, related_name="liked_posts", through="Like")
    description = models.CharField(max_length=500, default="No description")
    photo = models.ImageField(upload_to="post_photos/", blank=True, null=True)  # Поле для фотографии
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return f"Post by {self.author.username} at {self.created_at}"

    def save(self, *args, **kwargs):
        # Check if the object is already in the database
        if self.pk:
            try:
                # Retrieve the old photo associated with the user_forms
                old_photo = Post.objects.get(pk=self.pk).photo
                # Check if there"s a new photo and it"s different from the old photo
                if self.photo and old_photo and self.photo != old_photo:
                    # Delete the old photo from storage
                    old_photo.delete(save=False)
            except CustomUser.DoesNotExist:
                pass

        super(Post, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Удаление файла фотографии при удалении объекта пользователья
        if self.photo:
            # Получить путь к файлу фотографии
            file_path = self.photo.path
            # Удалить файл из системы хранения файлов
            if os.path.exists(file_path):
                os.remove(file_path)
        # Вызвать метод delete() базового класса для выполнения обычного удаления объекта
        super().delete(*args, **kwargs)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True, default=None)

    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    temporary_name = models.CharField(max_length=255, null=True, blank=True, default=None)

    APPROVAL_CHOICES = (
        ("pending", "Pending Approval"),
        ("approved", "Approved"),
    )

    approval_status = models.CharField(
        max_length=10,
        choices=APPROVAL_CHOICES,
        default="pending",
    )

    class Meta:
        ordering = ["created_at"]  # Упорядочиваем комментарии по дате создания

    def __str__(self):
        if self.author:
            return f"Comment by fgdfgfdg {self.author.username}"
        else:
            return f"Comment by anonym_user"


class Like(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
