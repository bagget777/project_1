# converter/models.py

# Модели Django для приложения converter.

from django.db import models
from django.contrib.auth.models import User

# Модель для хранения конверсионных запросов.
class ConversionRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video_url = models.URLField()
    email = models.EmailField()
    status = models.CharField(max_length=20, default='Pending')  # Статус задачи
    mp3_file = models.FileField(upload_to='mp3_files/', null=True, blank=True)

    def __str__(self):
        return f'Запрос от {self.user} от {self.timestamp}'

