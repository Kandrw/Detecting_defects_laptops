import logging
import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from django.http import HttpResponse, JsonResponse
import time


import base64
from django.core.files.base import ContentFile

from detecting_defects_laptops_soft.models import ImageModel


import subprocess
from subprocess import Popen, PIPE
# from MLP_detect.mlp.mlp_api import Predict

# from detecting_defects_laptops_soft.mlp.run_predictions import Predict_

# from mlp_api import Predict
# from models.detection import DetectionModel
# from MLP_detect.mlp.run_predictions import Predict_

# from MLP_detect.mlp.test import Predict

# from mlp.mlp_api import Predict_
from pathlib import Path

class ImageUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        serial_number = request.data.get('serial_number')
        images = request.FILES.getlist('images')
        ARGS_img = ""
        PATH_OUTPUT = "/home/andrey/Документы/Хакатон_13.10.24/Detecting_defects_laptops/mlp/output_txt_files/"
        RESULTS = []
        for image in images:
            ImageModel.objects.create(image=image, serial_number=serial_number)
            print("[get] image", image)
            abs_path = "/home/andrey/Документы/Хакатон_13.10.24/Detecting_defects_laptops/Back-hakaton/"
            dir = abs_path + f'media/images/{serial_number}/'
            ARGS_img += str(dir)+str(image) + " "
            RESULTS.append(PATH_OUTPUT + str(Path(image).stem))

        # Здесь будет правка при готовой нейросети
        if images:
            with images[0].open() as img_file:
                img_content = img_file.read()
                encoded_img = base64.b64encode(img_content).decode('utf-8')
                img_format = images[0].content_type  # Получаем формат изображения (например, image/png)

                # Форматируем изображение в нужный вид
                img_data = f"data:{img_format};base64,{encoded_img}"
        else:
            img_data = None

        # Predict(images)
        # subprocess.run(["python", "./mlp/run_predictions.py"])
        # PATH_ML = "/home/andrey/Документы/Хакатон_13.10.24/Detecting_defects_laptops/mlp/run_predictions.py"
        
        # os.environ["PYTHONPATH"] = "$PYTHONPATH:../mlp"


        # result = subprocess.run(['export', 'PYTHONPATH'], capture_output=True, text=True)
        # print(result.stdout)


        PATH_ML = "../mlp/run_predictions.py"
        PATH_RUN = "/home/andrey/Документы/Хакатон_13.10.24/Detecting_defects_laptops/mlp"
        
        # ARGS = images

        out, err = Popen('python3 ' + PATH_ML + " " + ARGS_img, cwd=PATH_RUN, shell=True, stdout=PIPE).communicate()
        # print("DDDDDDDDF: ", str(out, 'utf-8'))
        # path_res = Path().stem
        result_data_s = []
        for i in range(len(RESULTS)):
            str1 = "Not Detected"
            str2 = "Not Detected"
            str3 = "Not Detected"
            str4 = "Not Detected"
            str5 = "Not Detected"
            str6 = "Not Detected"
            
            
            if():
            str1 = asdasdd
            result_data = {
                "Scratches": str1,
                "BrokenPixels": "Not Detected",
                "ProblemsWithButtons": "Detected",
                "Zamok": "Not Detected",
                "MissingScrew": "Detected",
                "Chips": "Not Detected",
                "ImgRes": img_data
            }
            result_data_s.append(result_data)
        

        return JsonResponse(result_data, status=200)

from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.core.files.storage import default_storage
from docx import Document

@api_view(['POST'])
def submit_report(request):
    serial_number = request.data.get('serialNumber')
    defects = request.data.get('defects')

    if not defects:
        return JsonResponse({'error': 'Defects data is missing or empty'}, status=400)

    doc = Document()
    doc.add_heading('Отчет по дефектам', level=1)
    doc.add_paragraph(f'Серийный номер: {serial_number}')

    for key, value in defects.items():
        doc.add_paragraph(f'{key}: {value}')

    file_path = f'reports/report_{serial_number}.docx'
    doc.save(file_path)

    with open(file_path, 'rb') as f:
        response = JsonResponse({'status': 'success'})
        response['Content-Disposition'] = f'attachment; filename="report_{serial_number}.docx"'
        response.write(f.read())
        return response

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

@api_view(['POST'])
def submit_report_pdf(request):
    serial_number = request.data.get('serialNumber')
    defects = request.data.get('defects')

    if not defects:
        return JsonResponse({'error': 'Defects data is missing or empty'}, status=400)

    file_path = f'reports/report_{serial_number}.pdf'
    c = canvas.Canvas(file_path, pagesize=letter)
    c.drawString(100, 750, f'Report about Laptop defects')
    c.drawString(100, 735, f'Serial Number: {serial_number}')

    y = 700
    for key, value in defects.items():
        c.drawString(100, y, f'{key}: {value}')
        y -= 20

    c.save()

    with open(file_path, 'rb') as f:
        response = JsonResponse({'status': 'success'})
        response['Content-Disposition'] = f'attachment; filename="report_{serial_number}.pdf"'
        response.write(f.read())
        return response
