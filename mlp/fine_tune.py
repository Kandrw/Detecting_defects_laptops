import torch
from models.classification import ClassificationModel
from models.detection import DetectionModel
from utils.data_loader import get_data_loaders
from utils.train_helper import save_model, load_model
import json
import os
import shutil
import logging

# Логирование
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')


# Функция для обновления тренировочного набора для классификации
def update_classification_data(new_images, new_labels, classification_image_dir):
    """
    Добавляет новые изображения и их метки классов в классификационный датасет.
    """
    for img, label in zip(new_images, new_labels):
        label_dir = os.path.join(classification_image_dir, str(label))
        os.makedirs(label_dir, exist_ok=True)

        # Копируем изображение в нужную папку класса
        img_name = os.path.basename(img)
        img_path = os.path.join(label_dir, img_name)
        shutil.copy(img, img_path)


# Функция для обновления тренировочного набора для детекции
def update_detection_data(new_images, new_labels, image_dir, label_dir):
    """
    Добавляет новые изображения и их метки классов в YOLO датасет.
    """
    for img, label in zip(new_images, new_labels):
        img_name = os.path.basename(img)
        img_path = os.path.join(image_dir, img_name)

        # Копируем изображение в папку с тренировочными данными
        shutil.copy(img, img_path)

        # Создаём соответствующий txt файл с метками для YOLO
        label_path = os.path.join(label_dir, img_name.replace('.jpg', '.txt'))
        with open(label_path, 'w') as f:
            f.write(f"{label} 0.5 0.5 0 0")  # Замените координаты по необходимости


# Функция для загрузки конфигураций
def load_configs(config_path):
    """
    Загружает конфигурации из указанного JSON файла.
    """
    with open(config_path, 'r') as f:
        return json.load(f)


# Основная функция дообучения моделей
def main(front_data):
    """
    Основная функция, которая управляет процессом дообучения моделей на основе данных, поступающих с фронта.
    """
    # Загрузка конфигураций для классификации и детекции
    classification_config = load_configs('configs/classification/hyperparams.json')
    detection_config = load_configs('configs/detection/hyperparams.json')

    # Путь для сохранения моделей
    model_save_path = 'models/save_model'
    os.makedirs(model_save_path, exist_ok=True)

    # Папки для хранения новых тренировочных данных
    classification_image_dir = 'data/train/classification_images'
    image_dir = 'data/train/images'
    label_dir = 'data/train/labels'

    # Обновление классификационного набора данными с фронта
    update_classification_data(front_data['images'], front_data['labels'], classification_image_dir)

    # Обновление детекционного набора данными с фронта (YOLO)
    update_detection_data(front_data['images'], front_data['labels'], image_dir, label_dir)

    # --- ДООбучение классификационной модели ---
    logging.info("Начало дообучения классификационной модели...")

    # Загрузка обновленного тренировочного датасета
    train_loader_class, valid_loader_class = get_data_loaders(task="classification",
                                                              batch_size=classification_config['batch_size'])

    # Загрузка предварительно обученной классификационной модели
    classification_model = load_model(ClassificationModel, os.path.join(model_save_path, 'classification_model.pth'),
                                      classification_config)

    # Дообучение модели
    classification_model.train_model(train_loader_class, valid_loader_class)

    # Сохранение дообученной классификационной модели
    save_model(classification_model, os.path.join(model_save_path, 'classification_model.pth'))
    logging.info("Дообучение классификационной модели завершено.")

    # --- ДООбучение YOLO модели ---
    logging.info("Начало дообучения YOLO модели...")

    # Загрузка YOLO модели
    detection_model = DetectionModel(detection_config)
    detection_model.load_model('models/save_model/detection_model/train_results/weights/best.pt')

    # Дообучение YOLO модели
    detection_model.train_model()

    # Сохранение дообученной YOLO модели
    detection_model.save_model('models/save_model/detection_model/train_results/weights/best.pt')
    logging.info("Дообучение YOLO модели завершено.")

    # Валидация моделей
    logging.info("Запуск валидации моделей...")
    classification_model.validate_model(valid_loader_class)  # Валидация классификационной модели
    logging.info("Валидация классификационной модели завершена.")


if __name__ == "__main__":
    # Пример данных, поступающих с фронта
    front_data = {
        'images': ['new_image_1.jpg', 'new_image_2.jpg'],  # Пути к новым изображениям
        'labels': [1, 2]  # Метки классов для каждого изображения
    }

    # Запуск дообучения моделей на данных с фронта
    main(front_data)
