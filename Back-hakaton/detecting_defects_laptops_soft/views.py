from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from django.http import JsonResponse
import time

from detecting_defects_laptops_soft.models import ImageModel

class ImageUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        serial_number = request.data.get('serial_number')
        images = request.FILES.getlist('images')

        for image in images:
            ImageModel.objects.create(image=image, serial_number=serial_number)

        
        result_data = {
            "Scratches": "Detected",
            "BrokenPixels": "Not Detected",
            "ProblemsWithButtons": "Detected",
            "Zamok": "Not Detected",
            "MissingScrew": "Detected",
            "Chips": "Not Detected",
        }

        # result_data = {
        #     "Scratches": "",
        #     "BrokenPixels": "",
        #     "ProblemsWithButtons": "",
        #     "Zamok": "",
        #     "MissingScrew": "",
        #     "Chips": "",
        # }


        return JsonResponse(result_data, status=200)

from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.core.files.storage import default_storage
from docx import Document

# @api_view(['POST'])
# def submit_report(request):
#     serial_number = request.data.get('serialNumber')
#     defects = request.data.get('defects')

    
#     doc = Document()
#     doc.add_heading('Отчет по дефектам', level=1)
#     doc.add_paragraph(f'Серийный номер: {serial_number}')
    
#     for key, value in defects.items():
#         doc.add_paragraph(f'{key}: {value}')

    
#     file_path = f'reports/report_{serial_number}.docx'
#     doc.save(file_path)

    
#     with open(file_path, 'rb') as f:
#         response = JsonResponse({'status': 'success'})
#         response['Content-Disposition'] = f'attachment; filename="report_{serial_number}.docx"'
#         response.write(f.read())
#         return response

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
