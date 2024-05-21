from django.shortcuts import get_object_or_404
from .models import *


class WarmUpService:

    def clean_image(self, user):
        processed_image = user.processed_image
        if processed_image:
            user.processed_image = None
            user.save()
            processed_image.delete()

    def initialize_analyze(self, user, image_data):
        #Очищаем прошлое изображение
        self.clean_image(user)
        #Присваиваем новое изображение
        user.processed_image = image_data
        image_data.user = user


        #Обработка фото
        image_data.result_file = image_data.source_file

        #Сохраняем изменения
        image_data.save()
        user.save()



    def get_result(self, user) -> dict:
        context = {}
        context['processed_image'] = user.processed_image
        return context


deepForest_service = WarmUpService()  # Инициализируем общий экземпляр сервиса
