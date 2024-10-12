from ultralytics import YOLO
import os

class DetectionModel:
    def __init__(self, config):
        self.model = YOLO(config['model'])
        self.config = config

    def train_model(self):
        self.model.train(
            data='configs/data.yaml',
            epochs=self.config['epochs'],
            batch=self.config['batch'],
            imgsz=self.config['img_size'],
            optimizer=self.config['optimizer'],
            lr0=self.config['learning_rate'],
            momentum=self.config['momentum'],
            weight_decay=self.config['weight_decay'],
            val=False
        )
        print(f"YOLOv8 training completed. Model saved to {self.config['model_save_path']}")

    def save_model(self, path):
        self.model.save(path)

    def detect(self, image_path):
        results = self.model.predict(source=image_path)
        return results

    def load_model(self, model_path):
        self.model = YOLO(model_path)
        return self.model
