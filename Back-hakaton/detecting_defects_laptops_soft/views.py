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

from MLP_detect.apps import Train





class ImageUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        serial_number = request.data.get('serial_number')
        images = request.FILES.getlist('images')

        for image in images:
            ImageModel.objects.create(image=image, serial_number=serial_number)


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

        Train()

        result_data = {
            "Scratches": "Detected",
            "BrokenPixels": "Not Detected",
            "ProblemsWithButtons": "Detected",
            "Zamok": "Not Detected",
            "MissingScrew": "Detected",
            "Chips": "Not Detected",
            "ImgRes": img_data
        }
        

        return JsonResponse(result_data, status=200)

from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.core.files.storage import default_storage
from docx import Document

@api_view(['POST'])
def submit_report(request):
    serial_number = request.data.get('serialNumber')
    defects = request.data.get('defects')
    images = request.FILES.getlist('images')  

    if not defects:
        return JsonResponse({'error': 'Defects data is missing or empty'}, status=400)

    doc = Document()
    doc.add_heading('Отчет по дефектам', level=1)
    doc.add_paragraph(f'Серийный номер: {serial_number}')
    
    for key, value in list(defects.items())[:-1]:
        doc.add_paragraph(f'{key}: {value}')

    for image in images:
        image_content = ContentFile(image.read(), name=image.name)
        doc.add_picture(image_content)  

    file_path = f'reports/report_{serial_number}.docx'
    doc.save(file_path)

    with open(file_path, 'rb') as f:
        response = JsonResponse({'status': 'success'})
        response['Content-Disposition'] = f'attachment; filename="report_{serial_number}.docx"'
        response.write(f.read())
        return response

# 
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

@api_view(['POST'])
def submit_report_pdf(request):
    serial_number = request.data.get('serialNumber')
    defects = request.data.get('defects')
    images = request.FILES.getlist('images') 

    if not defects:
        return JsonResponse({'error': 'Defects data is missing or empty'}, status=400)

    file_path = f'reports/report_{serial_number}.pdf'
    c = canvas.Canvas(file_path, pagesize=letter)
    
    c.drawString(100, 750, f'Report about Laptop defects')
    c.drawString(100, 735, f'Serial Number: {serial_number}')

    y = 700
    for key, value in list(defects.items())[:-1]:
        c.drawString(100, y, f'{key}: {value}')
        y -= 20

    # 
    # for image in images:
    #     image_reader = ImageReader(image)  
    #     c.drawImage(image_reader, 100, y, width=200, height=200)
    #     y -= 220  # Уменьшите y, чтобы не перекрывать текст

    c.save()

    with open(file_path, 'rb') as f:
        response = JsonResponse({'status': 'success'})
        response['Content-Disposition'] = f'attachment; filename="report_{serial_number}.pdf"'
        response.write(f.read())
        return response
