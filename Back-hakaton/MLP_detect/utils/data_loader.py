import os
from torch.utils.data import DataLoader
from torchvision import transforms
from utils.custom_image_dataset import CustomImageDataset

def get_data_loaders(task="classification", batch_size=32, image_dir='data/train/images', label_dir='data/train/labels'):
    if task == "classification":
        transform = transforms.Compose([
            # Предполагаем, что изображения уже нужного размера
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                 std=[0.229, 0.224, 0.225])
        ])

        train_dataset = CustomImageDataset(
            image_dir=image_dir,
            label_dir=label_dir,
            transform=transform
        )

        train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)

        return train_loader

    elif task == "detection":
        transform = transforms.Compose([
            transforms.ToTensor(),  # Преобразуем изображение в тензор без изменения размера
        ])

        train_dataset = CustomImageDataset(
            image_dir=image_dir,
            label_dir=label_dir,
            transform=transform,
            task="detection"
        )

        train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)

        return train_loader

    else:
        raise ValueError(f"Unknown task: {task}. Supported tasks: 'classification', 'detection'.")
