import torch
from PIL import Image
from models.classification import ClassificationModel
from models.detection import DetectionModel
from utils.train_helper import load_model
import json
import torchvision.transforms as transforms
import os

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
    detection_model.load_model('models/save_model/detection_model/train_results/weights/best.pt')

    transform = transforms.Compose([
        transforms.Resize((640, 480)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                             std=[0.229, 0.224, 0.225])
    ])

    output_txt_folder = 'output_txt_files'  # Папка для txt-файлов
    os.makedirs(output_txt_folder, exist_ok=True)

    report = {
        'serial_number': serial_number,
        'defects': []
    }
    defect_found = False

    for image_path in image_paths:
        image = Image.open(image_path).convert('RGB')

        classification_result = classify_image(image, classification_model, transform)
        detection_results = detect_defects(image_path, detection_model)

        # Получение детекций
        detections = detection_results[0]  # Обрабатываем по одному изображению
        boxes = detections.boxes  # Объект с детекциями

        # Подготовка имени файла для сохранения
        image_filename = os.path.basename(image_path)
        image_name = os.path.splitext(image_filename)[0]
        txt_filename = image_name + ".txt"
        txt_filepath = os.path.join(output_txt_folder, txt_filename)

        if boxes is not None and len(boxes) > 0:
            # Получение классов и координат
            class_ids = boxes.cls.cpu().numpy().astype(int)
            coordinates = boxes.xyxy.cpu().numpy().astype(int)

            # Подготовка строк для записи в txt-файл
            lines = []
            for cls_id, coord in zip(class_ids, coordinates):
                x1, y1, x2, y2 = coord
                line = f"{cls_id} {x1} {y1} {x2} {y2}"
                lines.append(line)

            # Сохранение в txt-файл
            with open(txt_filepath, 'w') as f:
                for line in lines:
                    f.write(line + '\n')
        else:
            print(f"На изображении {image_path} дефекты не обнаружены.")
            # Записываем в txt-файл информацию об отсутствии дефекта
            width, height = image.size
            # Если хотите записать координаты, охватывающие всё изображение
            x1, y1, x2, y2 = 0, 0, width, height
            with open(txt_filepath, 'w') as f:
                f.write(f"{7} {x1} {y1} {x2} {y2}\n")  # Используем класс 7 и координаты всего изображения

        # Анализ результатов
        if classification_result != 7 or (boxes is not None and len(boxes) > 0):
            defect_found = True

        report['defects'].append({
            'image': image_path,
            'classification_result': classification_result,
            'detection_results': detection_results
        })

    report['quality_passed'] = not defect_found

    # Возвращаем отчёт
    return report

if __name__ == "__main__":
    # Пример использования
    image_paths = ['data/train/images/2024-01-15 14-34-26.jpg', 'data/train/images/2024-01-15 14-32-34.jpg']
    serial_number = 'ABC123456'
    result = main(image_paths, serial_number)
    print(result)


