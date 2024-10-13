import torch
from PIL import Image, ImageDraw
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
    image_tensor = transform(image).unsqueeze(0)
    outputs = classification_model(image_tensor)
    _, preds = torch.max(outputs, 1)
    return preds.item()

def detect_defects(image_path, detection_model):
    results = detection_model.detect(image_path)
    return results

def Predict_(image_paths):
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

    output_txt_folder = 'output_txt_files'  # Папка для txt-файлов и аннотированных изображений
    os.makedirs(output_txt_folder, exist_ok=True)

    report = {
        'defects': []
    }
    defect_found = False

    for image_path in image_paths:
        print("image_path", image_path)
        image = Image.open(image_path).convert('RGB')
        image_draw = image.copy()  # Создаём копию изображения для рисования
        draw = ImageDraw.Draw(image_draw)

        classification_result = classify_image(image, classification_model, transform)
        detection_results = detect_defects(image_path, detection_model)

        # Получение детекций
        detections = detection_results[0]  # Обрабатываем по одному изображению
        boxes = detections.boxes  # Объект с детекциями

        # Подготовка имени файла для сохранения, сохраняем оригинальное имя
        image_filename = os.path.basename(image_path)
        txt_filename = os.path.splitext(image_filename)[0] + ".txt"
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

                # Рисуем прямоугольник на изображении
                draw.rectangle([(x1, y1), (x2, y2)], outline='red', width=2)
                # Добавляем метку класса
                draw.text((x1, y1 - 10), str(cls_id), fill='red')

            # Сохранение в txt-файл
            with open(txt_filepath, 'w') as f:
                for line in lines:
                    f.write(line + '\n')
        else:
            print(f"На изображении {image_path} дефекты не обнаружены.")
            width, height = image.size
            x1, y1, x2, y2 = 0, 0, width, height
            with open(txt_filepath, 'w') as f:
                f.write(f"{7} {x1} {y1} {x2} {y2}\n")  # Используем класс 7 и координаты всего изображения

        # Сохраняем аннотированное изображение с таким же именем, как и оригинал
        annotated_image_path = os.path.join(output_txt_folder, image_filename)
        image_draw.save(annotated_image_path)

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

import sys

if True:
    # print("dir", os.path.abspath(os.curdir))
    # print("dir2", os.path.abspath(__file__))
    # Пример использования
    image_paths = sys.argv[1:]
    print("[] image_paths", image_paths)
    # image_paths = ['data/train/images/2024-01-15 14-41-39.jpg', 'data/train/images/2024-01-15 15-07-43.jpg']
    # image_paths = ['data/test/images/2024-01-15-14-32-34_jpg.rf.ea5c015b66fcd5eff4356034a08a46eb.jpg', 'data/test/images/IMG_7559_JPG.rf.922d0e29361aa049ac2ebee8b534a6fe.jpg']
    result = Predict_(image_paths)
    print(result)
