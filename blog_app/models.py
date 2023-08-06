import os

from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):

    photo = models.ImageField(upload_to='user_photos/', null=True, blank=True)

    def save(self, *args, **kwargs):
        # Check if the object is already in the database
        if self.pk:
            try:
                # Retrieve the old photo associated with the user_forms
                old_photo = CustomUser.objects.get(pk=self.pk).photo
                # Check if there's a new photo and it's different from the old photo
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
        ('header', 'Header Image'),
        ('profile', 'Profile Image'),
    )
    title = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='images/')
    type = models.CharField(max_length=10, choices=IMAGE_TYPES)