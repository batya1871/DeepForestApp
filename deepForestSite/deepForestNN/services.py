from django.shortcuts import get_object_or_404
from .models import *


class WarmUpService:

    def clean_image(self, user):
        user.processed_image = None

    def initialize_analyze(self, user):
        self.clean_image(user)

        #Обработка фото
        #...




    def get_result(self, user) -> dict:
        context = {}
        context['results'] = "ОБРАБОТАННОЕ ФОТО"
        return context


deepForest_service = WarmUpService()  # Инициализируем общий экземпляр сервиса
