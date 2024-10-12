from django.urls import path
from .views import ImageUploadView
from .views import submit_report

urlpatterns = [
    path('upload/', ImageUploadView.as_view(), name='image-upload'),
    path('submit-report/', submit_report, name='submit_report')
]
