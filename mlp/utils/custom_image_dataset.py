import torch
from torch.utils.data import Dataset
from PIL import Image
import os


class CustomImageDataset12(Dataset):
    def __init__(self, image_dir, label_dir, transform=None, task="classification"):
        self.image_dir = image_dir
        self.label_dir = label_dir
        self.image_files = [f for f in os.listdir(image_dir) if f.endswith(('jpg', 'jpeg', 'png'))]
        self.transform = transform
        self.task = task

    def __len__(self):
        return len(self.image_files)

    def __getitem__(self, idx):
        img_name = self.image_files[idx]
        img_path = os.path.join(self.image_dir, img_name)

        image = Image.open(img_path).convert("RGB")

        label_name = os.path.splitext(img_name)[0] + '.txt'
        label_path = os.path.join(self.label_dir, label_name)

        if self.task == "classification":
            class_id = 7  # По умолчанию "без дефектов"
            if os.path.exists(label_path):
                with open(label_path, 'r') as f:
                    class_id = int(f.readline().split()[0])

            if self.transform:
                image = self.transform(image)

            return image, class_id

        elif self.task == "detection":
            labels = []
            if os.path.exists(label_path):
                with open(label_path, 'r') as f:
                    lines = f.readlines()
                    for line in lines:
                        label = line.strip().split()
                        labels.append([float(x) for x in label])

            if self.transform:
                image = self.transform(image)

            return image, torch.tensor(labels)


class CustomImageDataset(Dataset):
    def __init__(self, image_dir, label_dir, transform=None, task="classification"):
        self.image_dir = image_dir
        self.label_dir = label_dir
        self.image_files = [f for f in os.listdir(image_dir) if f.endswith(('jpg', 'jpeg', 'png'))]
        self.transform = transform
        self.task = task

    def __len__(self):
        return len(self.image_files)

    def __getitem__(self, idx):
        img_name = self.image_files[idx]
        img_path = os.path.join(self.image_dir, img_name)

        # Загружаем изображение
        image = Image.open(img_path).convert("RGB")

        # Найдём соответствующий текстовый файл с метками
        label_name = os.path.splitext(img_name)[0] + '.txt'
        label_path = os.path.join(self.label_dir, label_name)

        if self.task == "classification":
            # Проверим, что файл метки не пуст
            # print(label_path, " - ", label_name)
            if os.path.exists(label_path) and os.path.getsize(label_path) > 0:
                with open(label_path, 'r') as f:
                    line = f.readline().strip()
                    if line:  # Убедимся, что строка не пустая
                        class_id = int(line.split()[0])
                    else:
                        raise ValueError(f"Файл метки {label_name} пустой или содержит некорректные данные.")
            else:
                raise FileNotFoundError(f"Файл метки {label_name} не найден или пуст.")
            
            if self.transform:
                image = self.transform(image)

            return image, class_id

        elif self.task == "detection":
            # Если задача детекции, получаем координаты и классы
            labels = []
            if os.path.exists(label_path) and os.path.getsize(label_path) > 0:
                with open(label_path, 'r') as f:
                    lines = f.readlines()
                    for line in lines:
                        label = line.split()
                        if len(label) >= 5:
                            labels.append([float(x) for x in label])
                        else:
                            raise ValueError(f"Файл метки {label_name} содержит некорректные данные.")
            else:
                raise FileNotFoundError(f"Файл метки {label_name} не найден или пуст.")

            if self.transform:
                image = self.transform(image)

            return image, torch.tensor(labels)