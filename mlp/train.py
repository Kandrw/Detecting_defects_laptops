import os

# from . import models.classification.ClassificationModel
from models.classification import ClassificationModel
from models.detection import DetectionModel
from utils.data_loader import get_data_loaders
from utils.train_helper import save_model
import json


def load_configs(config_path):
    with open(config_path, 'r') as f:
        return json.load(f)


def main():
    # Загрузка конфигураций для классификации и детекции
    classification_config = load_configs('configs/classification/hyperparams.json')
    detection_config = load_configs('configs/detection/hyperparams.json')

    # Создание директории для сохранения моделей
    model_save_path = 'models/save_model'
    os.makedirs(model_save_path, exist_ok=True)

    # Обучение YOLO модели (детекция)
    detection_model = DetectionModel(detection_config)
    detection_model.train_model()

    # Сохранение детекционной модели
    #detection_model.save_model(os.path.join(model_save_path, 'detection_model.pth'))

    # Обучение классификационной модели
    train_loader_class = get_data_loaders(
        task="classification",
        batch_size=classification_config['batch_size']
    )
    classification_model = ClassificationModel(classification_config)
    classification_model.train_model(train_loader_class)

    # Сохранение классификационной модели
    save_model(classification_model, os.path.join(model_save_path, 'classification_model.pth'))


if __name__ == "__main__":
    main()
