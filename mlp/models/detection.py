from ultralytics import YOLO
import os
import torch
from ultralytics import YOLO
import os

class DetectionModel:
    def __init__(self, config):
        self.config = config
        self.model = None  # Модель будет загружена позже

    def train_model(self):
        self.model = YOLO(self.config['model'])
        rt = os.path.exists("configs/data.yaml")
        if(not rt):
            print("\nNNOONON\n\n\n")
        
        self.model.train(
            data='configs/data.yaml',
            epochs=self.config['epochs'],
            batch=self.config['batch'],
            imgsz=self.config['img_size'],
            optimizer=self.config['optimizer'],
            lr0=self.config['learning_rate'],
            weight_decay=self.config['weight_decay'],
            iou = self.config['iou'],
            conf=self.config['conf'],
            val=False,
            verbose=True,
            save=True,
            project=self.config['model_save_path'],  # Используем 'project' вместо 'save_dir'
            name='train_results',  # Можно задать любое имя
            exist_ok = True
        )
        print(f"YOLOv8 обучение завершено. Модель сохранена в {self.config['model_save_path']}")

    def load_model(self, model_path):
        # Загружаем модель напрямую из файла
        self.model = YOLO(model_path)
        print(f"Модель загружена из {model_path}")

    def detect(self, image_path):
        results = self.model.predict(source=image_path)
        return results

