import torch
from torch.utils.data import Dataset
from PIL import Image
import os

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
