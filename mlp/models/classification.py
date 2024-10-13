import torch
import torch.nn as nn
import torch.cuda.amp as amp
from torchvision import models
from utils.log_visualization import log_metrics

class ClassificationModel(nn.Module):
    def __init__(self, config):
        super(ClassificationModel, self).__init__()
        self.device = torch.device(config['device'] if torch.cuda.is_available() else 'cpu')
        self.model = models.efficientnet_b0(pretrained=True)
        self.model.classifier[1] = nn.Linear(self.model.classifier[1].in_features, config['output_size'])
        self.model.to(self.device)
        self.config = config
        self.scaler = amp.GradScaler()

    def forward(self, x):
        x = x.to(self.device)
        return self.model(x)

    def train_model(self, train_loader, valid_loader=None):
        optimizer = torch.optim.Adam(self.model.parameters(), 
                                     lr=self.config['learning_rate'], d=self.config['dropout'])
        criterion = nn.CrossEntropyLoss()

        for epoch in range(self.config['epochs']):
            self.model.train()
            running_loss = 0.0
            correct = 0
            total = 0

            for images, labels in train_loader:
                images, labels = images.to(self.device), labels.to(self.device)
                optimizer.zero_grad()

                with amp.autocast():
                    outputs = self.forward(images)
                    loss = criterion(outputs, labels)

                self.scaler.scale(loss).backward()
                self.scaler.step(optimizer)
                self.scaler.update()

                running_loss += loss.item()
                _, predicted = outputs.max(1)
                total += labels.size(0)
                correct += predicted.eq(labels).sum().item()

            accuracy = 100 * correct / total
            avg_loss = running_loss / len(train_loader)

            print(f'Epoch {epoch + 1}/{self.config["epochs"]}, Loss: {avg_loss}, Accuracy: {accuracy}%')

            # Логирование метрик
            log_metrics(epoch + 1, avg_loss, accuracy)

            # Проверяем, передан ли valid_loader, прежде чем вызывать валидацию
            if valid_loader is not None:
                self.validate_model(valid_loader)

    def validate_model(self, valid_loader):
        self.model.eval()
        criterion = nn.CrossEntropyLoss()
        val_loss = 0.0
        correct = 0
        total = 0

        with torch.no_grad():
            for images, labels in valid_loader:
                images, labels = images.to(self.device), labels.to(self.device)
                outputs = self.forward(images)
                loss = criterion(outputs, labels)
                val_loss += loss.item()

                _, predicted = outputs.max(1)
                total += labels.size(0)
                correct += predicted.eq(labels).sum().item()

        accuracy = 100 * correct / total
        avg_val_loss = val_loss / len(valid_loader)

        print(f'Validation Loss: {avg_val_loss}, Validation Accuracy: {accuracy}%')
