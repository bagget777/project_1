# converter/urls.py

# Конфигурация URL для приложения converter.

from django.urls import path
from .views import ConversionRequestCreateView
from . import views
urlpatterns = [
    path('create/', ConversionRequestCreateView.as_view(), name='conversion-request-create'),
    path('download/<int:video_id>/', views.download_video, name='download_video'),
]
