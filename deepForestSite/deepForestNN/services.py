from .models import *
import cv2
import deepforest.main
import torch
import numpy as np
import io
import os
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.conf import settings


# Метод, проверяющий наслаивается ли площадь обнаруженного дерева на площадь другого дерева
def calculate_iou(box1, box2):
    x1_min, y1_min, x1_max, y1_max = box1
    x2_min, y2_min, x2_max, y2_max = box2

    # Calculate the intersection area
    inter_x_min = max(x1_min, x2_min)
    inter_y_min = max(y1_min, y2_min)
    inter_x_max = min(x1_max, x2_max)
    inter_y_max = min(y1_max, y2_max)

    inter_width = max(0, inter_x_max - inter_x_min)
    inter_height = max(0, inter_y_max - inter_y_min)
    inter_area = inter_width * inter_height

    # Calculate the union area
    box1_area = (x1_max - x1_min) * (y1_max - y1_min)
    box2_area = (x2_max - x2_min) * (y2_max - y2_min)
    union_area = box1_area + box2_area - inter_area

    # Calculate the IoU
    iou = inter_area / union_area
    return iou


def detect_trees(image_path, iou_threshold=0.5):
    # Загрузка изображения
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"Изображение по пути {image_path} не найдено.")

    # Преобразование изображения в RGB и тип float32 для модели
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB).astype('float32')

    # Инициализация модели DeepForest
    my_model = deepforest.main.deepforest()
    my_model.use_release()

    # Определение устройства (GPU или CPU)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    my_model.model.to(device)

    # Выполнение предсказания на устройстве
    with torch.no_grad():
        box_info = my_model.predict_image(img_rgb, return_plot=False)


    filtered_boxes = []
    for index, row in box_info.iterrows():
        x_min, y_min = int(row['xmin']), int(row['ymin'])
        x_max, y_max = int(row['xmax']), int(row['ymax'])
        new_box = (x_min, y_min, x_max, y_max)

        # Check if the new box overlaps with any of the filtered boxes
        keep = True
        for box in filtered_boxes:
            if calculate_iou(new_box, box) > iou_threshold:
                keep = False
                break

        if keep:
            filtered_boxes.append(new_box)
            cv2.rectangle(img, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)

    total_trees = len(filtered_boxes)
    # Возвращаем обработанное изображение и кол-во найденных деревьев
    return img, total_trees


class DeepForestService:

    def clean_image(self, user):
        processed_image = user.processed_image
        if processed_image:
            user.processed_image = None
            user.save()
            processed_image.delete()

    def initialize_analyze(self, user, image_data):
        # Очищаем прошлое изображение
        self.clean_image(user)
        # Присваиваем новое изображение
        user.processed_image = image_data
        image_data.user = user

        # Сохраняем изменения
        image_data.save()
        user.save()

    def get_result(self, user) -> dict:
        image_data = user.processed_image
        if not image_data.result_file:
            source_path = image_data.source_file.url[1:len(image_data.source_file.url)]
            result_image, trees_count = detect_trees(source_path)
            # Конвертируем результат в байтовый формат
            is_success, buffer = cv2.imencode(".jpg", result_image)
            if not is_success:
                raise ValueError("Ошибка при конвертации изображения")

            file_io = io.BytesIO(buffer)
            file_content = ContentFile(file_io.getvalue())

            # Создаем путь для сохранения файла
            result_file_name = f"{image_data.id}_result.jpg"
            image_data.result_file.save(result_file_name, file_content)
            image_data.trees_count = trees_count
            # Сохраняем изменения в базе данных
            image_data.save()

        context = {
            'processed_image': user.processed_image
        }
        return context


deepForest_service = DeepForestService()  # Инициализируем общий экземпляр сервиса
