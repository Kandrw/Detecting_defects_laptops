import torch
from models.classification import ClassificationModel
from models.detection import DetectionModel
from utils.data_loader import get_data_loaders
from utils.train_helper import save_model, load_model
import json

def load_configs(config_path):
    with open(config_path, 'r') as f:
        return json.load(f)

def main():
    classification_config = load_configs('configs/classification/hyperparams.json')
    detection_config = load_configs('configs/detection/hyperparams.json')

    model_save_path = 'models/save_model'
    os.makedirs(model_save_path, exist_ok=True)

    # Дообучение классификационной модели
    train_loader_class, _ = get_data_loaders(task="classification", batch_size=classification_config['batch_size'])
    classification_model = load_model(ClassificationModel, os.path.join(model_save_path, 'classification_model.pth'), classification_config)
    classification_model.train_model(train_loader_class)

    save_model(classification_model, os.path.join(model_save_path, 'classification_model.pth'))

    # Дообучение YOLO модели
    detection_model = DetectionModel(detection_config)
    detection_model.load_model(os.path.join(model_save_path, 'detection_model.pth'))
    detection_model.train_model()

    detection_model.save_model(os.path.join(model_save_path, 'detection_model.pth'))

if __name__ == "__main__":
    main()
