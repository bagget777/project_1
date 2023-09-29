# converter/serializers.py

# Сериализаторы для приложения converter.

from rest_framework import serializers
from .models import ConversionRequest
from .utils import download_video, convert_video_to_mp3, create_zip_archive, send_mp3_email  # Импортируем send_mp3_email
import smtplib

# Сериализатор для конверсионного запроса.
class ConversionRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConversionRequest
        fields = '__all__'

    def perform_create(self, serializer):
        video_url = serializer.validated_data['video_url']
        email = serializer.validated_data['email']

        # Скачать видео с помощью youtube-dl
        video_file_path = download_video(video_url)

        # Конвертировать видео в MP3
        mp3_file_path = convert_video_to_mp3(video_file_path)

        # Создать архив с MP3-файлом (и другими файлами, если есть)
        archive_path = create_zip_archive(mp3_file_path)

        # Отправить архив по электронной почте
        server = smtplib.SMTP('smtp.gmail.com', 587)  # SMTP-сервер и порт для Gmail

        sender_email = "bagget7777@gmail.com"  # Замените на ваш адрес электронной почты
        sender_password = "bayzak2005"  # Замените на ваш пароль
        subject = "Converted Video"
        body = "Here is your converted video."
        
        if mp3_file_path and archive_path:
            # Если mp3_file_path и archive_path существуют, отправьте MP3-файл по электронной почте
            if send_mp3_email(sender_email, sender_password, email, subject, body, mp3_file_path):
                serializer.save(mp3_file=mp3_file_path)  # Сохраняем путь к MP3-файлу в модели
            else:
                print("Ошибка отправки электронной почты")
        else:
            print("Ошибка в конвертации или создании архива")
