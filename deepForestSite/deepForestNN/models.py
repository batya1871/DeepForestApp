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
    name = models.CharField("Название", max_length=15, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Данные по фото"
        verbose_name_plural = "Данные по фото"
