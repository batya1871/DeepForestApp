import os

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    processed_image = models.OneToOneField('Image_data', on_delete=models.SET_NULL, null=True, blank=True,
                                           related_name="user")

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Image_data(models.Model):
    source_file = models.FileField(upload_to="analyzing_images/source_images", verbose_name="Изначальное фото")
    result_file = models.FileField(upload_to="analyzing_images/result_images", verbose_name="Обработанное фото")
    trees_count = models.IntegerField("Деревьев обнаружено", default=0)

    class Meta:
        verbose_name = "Данные по фото"
        verbose_name_plural = "Данные по фото"

    def delete(self, *args, **kwargs):
        # Удаление файлов с сервера
        if self.source_file:
            if os.path.isfile(self.source_file.path):
                os.remove(self.source_file.path)
        if self.result_file:
            if os.path.isfile(self.result_file.path):
                os.remove(self.result_file.path)
        # Вызов родительского метода delete
        super().delete(*args, **kwargs)
