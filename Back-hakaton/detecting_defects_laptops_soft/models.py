from django.db import models
import os

def upload_to(instance, filename):
    return os.path.join(f"images/{instance.serial_number}", filename)

class ImageModel(models.Model):
    image = models.ImageField(upload_to=upload_to) 
    serial_number = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        directory = f'media/images/{self.serial_number}/'
        os.makedirs(directory, exist_ok=True)
        super().save(*args, **kwargs)  