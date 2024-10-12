import torch
from PIL import Image
from models.classification import ClassificationModel
from models.detection import DetectionModel
from utils.train_helper import load_model
import json
import torchvision.transforms as transforms

def load_configs(config_path):
    with open(config_path, 'r') as f:
        return json.load(f)

def classify_image(image, classification_model, transform):
    image = transform(image).unsqueeze(0)
    outputs = classification_model(image)
    _, preds = torch.max(outputs, 1)
    return preds.item()

def detect_defects(image_path, detection_model):
    results = detection_model.detect(image_path)
    return results

def main(image_paths, serial_number):
    classification_config = load_configs('configs/classification/hyperparams.json')
    detection_config = load_configs('configs/detection/hyperparams.json')

    device = torch.device(classification_config['device'] if torch.cuda.is_available() else 'cpu')

    classification_model = load_model(ClassificationModel, 'models/save_model/classification_model.pth', classification_config)
    classification_model.to(device)

    detection_model = DetectionModel(detection_config)
    detection_model.load_model('models/save_model/detection_model.pth')

    transform = transforms.Compose([
        transforms.Resize((640, 480)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                             std=[0.229, 0.224, 0.225])
    ])

    report = {
        'serial_number': serial_number,
        'defects': []
    }
    defect_found = False

    for image_path in image_paths:
        image = Image.open(image_path).convert('RGB')

        classification_result = classify_image(image, classification_model, transform)
        detection_results = detect_defects(image_path, detection_model)

        # Анализ результатов
        if classification_result != 7 or len(detection_results) > 0:
            defect_found = True

        report['defects'].append({
            'image': image_path,
            'classification_result': classification_result,
            'detection_results': detection_results
        })

    report['quality_passed'] = not defect_found

    # Возвращаем отчет
    return report

if __name__ == "__main__":
    # Пример использования
    image_paths = ['data/test/image1.jpg', 'data/test/image2.jpg']
    serial_number = 'ABC123456'
    result = main(image_paths, serial_number)
    print(result)
