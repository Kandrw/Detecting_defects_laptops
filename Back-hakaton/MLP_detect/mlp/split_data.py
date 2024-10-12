import os
import shutil
import random
from pathlib import Path

def create_split_folders(output_dir):
    """
    Создает необходимые директории для тренировочных, валидационных и тестовых данных.
    """
    train_images_dir = os.path.join(output_dir, 'train', 'images')
    valid_images_dir = os.path.join(output_dir, 'valid', 'images')
    test_images_dir = os.path.join(output_dir, 'test', 'images')

    train_labels_dir = os.path.join(output_dir, 'train', 'labels')
    valid_labels_dir = os.path.join(output_dir, 'valid', 'labels')
    test_labels_dir = os.path.join(output_dir, 'test', 'labels')

    os.makedirs(train_images_dir, exist_ok=True)
    os.makedirs(valid_images_dir, exist_ok=True)
    os.makedirs(test_images_dir, exist_ok=True)

    os.makedirs(train_labels_dir, exist_ok=True)
    os.makedirs(valid_labels_dir, exist_ok=True)
    os.makedirs(test_labels_dir, exist_ok=True)

    return (train_images_dir, valid_images_dir, test_images_dir,
            train_labels_dir, valid_labels_dir, test_labels_dir)

def move_files(images_list, image_dir, label_dir, subset_images_dir, subset_labels_dir):
    """
    Перемещает изображения и их соответствующие лейблы в указанные директории.
    """
    for image_name in images_list:
        # Копируем изображение
        image_path = os.path.join(image_dir, image_name)
        if os.path.exists(image_path):
            shutil.copy(image_path, subset_images_dir)
        else:
            print(f"Изображение {image_name} не найдено!")

        # Ищем соответствующий лейбл
        label_name = Path(image_name).stem + '.txt'
        label_path = os.path.join(label_dir, label_name)
        if os.path.exists(label_path):
            shutil.copy(label_path, subset_labels_dir)
        else:
            print(f"Лейбл {label_name} не найден!")

def split_dataset(image_dir, label_dir, output_dir, train_ratio=0.7, valid_ratio=0.15, test_ratio=0.15):
    """
    Разбивает набор данных на тренировочные, валидационные и тестовые данные.
    :param image_dir: Путь к папке с изображениями
    :param label_dir: Путь к папке с лейблами
    :param output_dir: Путь к папке, куда будут сохранены разбитые данные
    :param train_ratio: Доля тренировочных данных
    :param valid_ratio: Доля валидационных данных
    :param test_ratio: Доля тестовых данных
    """
    # Получаем список всех файлов изображений
    images = [f for f in os.listdir(image_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]

    if len(images) == 0:
        print("Не найдено изображений для обработки.")
        return

    # Перемешиваем файлы для случайной выборки
    random.shuffle(images)

    # Вычисляем количество изображений для каждого набора
    total_images = len(images)
    train_count = int(total_images * train_ratio)
    valid_count = int(total_images * valid_ratio)

    train_images = images[:train_count]
    valid_images = images[train_count:train_count + valid_count]
    test_images = images[train_count + valid_count:]

    # Создаем папки для разбиения
    (train_images_dir, valid_images_dir, test_images_dir,
     train_labels_dir, valid_labels_dir, test_labels_dir) = create_split_folders(output_dir)

    # Копируем изображения и лейблы в соответствующие папки
    move_files(train_images, image_dir, label_dir, train_images_dir, train_labels_dir)
    move_files(valid_images, image_dir, label_dir, valid_images_dir, valid_labels_dir)
    move_files(test_images, image_dir, label_dir, test_images_dir, test_labels_dir)

    print(f"Разбиение завершено. Данные сохранены в {output_dir}")

# Пример использования
if __name__ == "__main__":
    image_dir = "data"  # Папка с изображениями
    label_dir = "data/train/labels/"  # Папка с лейблами
    output_dir = "data/train/output/"  # Папка, где будут созданы train, valid, test

    # Запуск процесса
    split_dataset(image_dir, label_dir, output_dir)
