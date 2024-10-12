 




import os
from PIL import Image

# def resize_images(input_dir, output_dir, new_size):
#     os.makedirs(output_dir, exist_ok=True)

#     for filename in os.listdir(input_dir):
#         if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
#             image_path = os.path.join(input_dir, filename)
 
#             with Image.open(image_path) as img:
#                 resized_img = img.resize(new_size)

#                 resized_img.save(os.path.join(output_dir, filename))
#                 print(f"{filename} изменён и сохранён в {output_dir}")

# input_dir = '/Users/mikhailkatsuro/Downloads/train_data/train/images'
# output_dir = '/Users/mikhailkatsuro/Downloads/train_data/size'
# new_image_size = (640, 480)

# resize_images(input_dir, output_dir, new_image_size)




result_data = {
    "Scratches": "Detected",
    "BrokenPixels": "Not Detected",
    "ProblemsWithButtons": "Detected",
    "Zamok": "Not Detected",
    "MissingScrew": "Detected",
    "Chips": "Not Detected",
    # "ImgRes": img_data
}








def Train():
    print("TEst")
    return 123


















