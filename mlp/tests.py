

import torch
from torch.utils.data import Dataset
from PIL import Image
import os







# label_name = os.path.splitext(img_name)[0] + '.txt'
# label_path = os.path.join(self.label_dir, label_name)


label_path = "/home/andrey/Документы/Хакатон_13.10.24/Detecting_defects_laptops/mlp/data/train/labels"
label_name = "-223014448_jpeg.rf.323117e65584713e63b75346badfb05e.txt"


label_path = "data/train/labels/photo_2023-11-08_13-06-52_jpg.rf.0fbe7940136e28e6492c39adef47c8c8.txt"
label_name = "photo_2023-11-08_13-06-52_jpg.rf.0fbe7940136e28e6492c39adef47c8c8.txt"


pr = os.path.exists(label_path)
print(pr, os.path.getsize(label_path))

if os.path.exists(label_path) and os.path.getsize(label_path) > 0:
    print("True")