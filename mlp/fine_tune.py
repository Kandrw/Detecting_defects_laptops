import torch
from models.classification import ClassificationModel
from models.detection import DetectionModel
from utils.data_loader import get_data_loaders
from utils.train_helper import save_model, load_model
import json
import os
import shutil
import logging
from PIL import Image

# Логирование
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# Функция для обновления тренировочного набора для классификации
def update_classification_data(new_images, new_labels, classification_image_dir):
    """
    Добавляет новые изображения и их метки классов в классификационный датасет.
    """
    if not os.path.exists(classification_image_dir):
        os.makedirs(classification_image_dir)

    for img, label in zip(new_images, new_labels):
        label_dir = os.path.join(classification_image_dir, str(label))
        os.makedirs(label_dir, exist_ok=True)

        img_name = os.path.basename(img)
        img_path = os.path.join(label_dir, img_name)

        if not os.path.exists(img):
            logging.error(f"Файл {img} не существует. Пропуск...")
            continue

        if os.path.exists(img_path):
            logging.info(f"Файл {img_path} уже существует, пропуск...")
        else:
            shutil.copyfile(img, img_path)
            logging.info(f"Файл {img} скопирован в {img_path}")

# Функция для обновления тренировочного набора для детекции
def update_detection_data(new_images, new_labels, new_bboxes, image_dir, label_dir):
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)
    if not os.path.exists(label_dir):
        os.makedirs(label_dir)

    for img, label, bbox in zip(new_images, new_labels, new_bboxes):
        img_name = os.path.basename(img)
        img_path = os.path.join(image_dir, img_name)

        if not os.path.exists(img):
            logging.error(f"Файл {img} не существует. Пропуск...")
            continue

        image = Image.open(img)
        img_width, img_height = image.size

        if os.path.exists(img_path):
            logging.info(f"Файл {img_path} уже существует, пропуск...")
        else:
            shutil.copyfile(img, img_path)
            logging.info(f"Файл {img} скопирован в {img_path}")

        x1, y1, x2, y2 = bbox
        x_center = (x1 + x2) / 2 / img_width
        y_center = (y1 + y2) / 2 / img_height
        width = (x2 - x1) / img_width
        height = (y2 - y1) / img_height

        label_path = os.path.join(label_dir, img_name.replace('.jpg', '.txt'))
        with open(label_path, 'w') as f:
            f.write(f"{label} {x_center} {y_center} {width} {height}\n")
        logging.info(f"Метка сохранена в {label_path}")

# Функция для загрузки конфигураций
def load_configs(config_path):
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError as e:
        logging.error(f"Ошибка загрузки конфигурации: {e}")
        return {}

# Основная функция дообучения моделей
def main(front_data):
    classification_config = load_configs('configs/classification/hyperparams.json')
    detection_config = load_configs('configs/detection/hyperparams.json')

    model_save_path = 'models/save_model'
    os.makedirs(model_save_path, exist_ok=True)

    classification_image_dir = 'data/train/classification_images'
    image_dir = 'data/train/images'
    label_dir = 'data/train/labels'

    # Обновление данных
    update_classification_data(front_data['images'], front_data['labels'], classification_image_dir)
    update_detection_data(front_data['images'], front_data['labels'], front_data['bboxes'], image_dir, label_dir)

    logging.info("Начало дообучения классификационной модели...")
    train_loader_class = get_data_loaders(task="classification", batch_size=classification_config['batch_size'])

    # Загрузка и дообучение классификационной модели
    classification_model = load_model(ClassificationModel, os.path.join(model_save_path, 'classification_model.pth'), classification_config)
    classification_model.train_model(train_loader_class)
    save_model(classification_model, os.path.join(model_save_path, 'classification_model.pth'))
    logging.info("Дообучение классификационной модели завершено.")

    # Дообучение YOLO модели
    logging.info("Начало дообучения YOLO модели...")
    detection_model = DetectionModel(detection_config)
    detection_model.load_model('models/save_model/detection_model/train_results/weights/best.pt')
    detection_model.train_model()
    detection_model.save_model('models/save_model/detection_model/train_results/weights/best.pt')
    logging.info("Дообучение YOLO модели завершено.")

    # Валидация
    logging.info("Запуск валидации классификационной модели...")
    classification_model.validate_model(train_loader_class)
    logging.info("Валидация классификационной модели завершена.")

if __name__ == "__main__":
    # Пример данных с фронта
    front_data = {
        'images': ['data/train/classification_images/1/photo_2023-11-08_11-03-59_jpg.rf.b6f8a42a4a5bc001521d585106d227a2.jpg',
                   'data/train/classification_images/2/2024-01-15-16-30-36_flipped_rotated_90_jpg.rf.a0a42adf3567f5aa403360772a4aa907.jpg'],
        'labels': [1, 2],
        'bboxes': [(50, 50, 200, 200), (30, 40, 100, 150)]
    }

    main(front_data)
