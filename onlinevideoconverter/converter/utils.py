# converter/utils.py

# Вспомогательные функции для приложения converter.

import os
import subprocess
import zipfile
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from django.http import FileResponse, HttpResponse
from django.shortcuts import get_object_or_404
from .models import ConversionRequest  # Замените на свою модель

# Функция для скачивания видео по URL.
def download_video(request, video_id):
    video = get_object_or_404(ConversionRequest, pk=video_id)
    video_path = video.video_file.path

    response = FileResponse(open(video_path, 'rb'))
    response['Content-Disposition'] = f'attachment; filename="{video.video_file.name}"'
    return response

# Функция для скачивания видео по URL.
def download_video_url(request):
    video_url = request.GET.get('video_url')
    video_file_path = download_video(video_url)
    
    if video_file_path:
        video_file = open(video_file_path, 'rb')
        response = FileResponse(video_file)
        response['Content-Disposition'] = 'attachment; filename="downloaded_video.mp4"'
        return response
    else:
        return HttpResponse('Ошибка загрузки видео')

# Функция для конвертации видео в MP3.
def convert_video_to_mp3(video_file_path):
    # Определите путь для сохранения MP3
    mp3_file_path = 'converted_audio.mp3'  # Пример пути, укажите свой

    # Используйте ffmpeg для конвертации видео в MP3
    try:
        subprocess.run(['ffmpeg', '-i', video_file_path, mp3_file_path], check=True)
        return mp3_file_path
    except subprocess.CalledProcessError as e:
        # Обработайте ошибку, если конвертация не удалась
        print(f"Ошибка конвертации видео в MP3: {e}")
        return None

# Функция для создания архива с MP3-файлом.
def create_zip_archive(mp3_file_path):
    # Определите путь для сохранения архива
    archive_file_path = 'converted_audio.zip'  # Пример пути, укажите свой

    # Создайте архив с MP3-файлом
    try:
        with zipfile.ZipFile(archive_file_path, 'w', zipfile.ZIP_DEFLATED) as archive:
            archive.write(mp3_file_path, os.path.basename(mp3_file_path))
        return archive_file_path
    except Exception as e:
        # Обработайте ошибку, если создание архива не удалось
        print(f"Ошибка создания архива: {e}")
        return None

# Функция для отправки MP3-файла по электронной почте.
def send_mp3_email(sender_email, sender_password, recipient_email, subject, body, mp3_file_path):
    # Отправка MP3-файла по электронной почте
    try:
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        with open(mp3_file_path, 'rb') as mp3_file:
            part = MIMEApplication(mp3_file.read(), Name=os.path.basename(mp3_file_path))
            part['Content-Disposition'] = f'attachment; filename="{os.path.basename(mp3_file_path)}"'
            msg.attach(part)

        server = smtplib.SMTP('smtp.example.com', 587)  # Укажите SMTP-сервер и порт
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()

        return True
    except Exception as e:
        # Обработайте ошибку при отправке почты
        print(f"Ошибка отправки электронной почты: {e}")
        return False

# Функция для скачивания видео по URL с использованием youtube-dl.
def download_video(video_url):
    # Определите путь, куда сохранить видео
    video_file_path = 'downloaded_video.mp4'  # Пример пути, укажите свой

    # Используйте youtube-dl для скачивания видео
    try:
        subprocess.run(['youtube-dl', '-o', video_file_path, video_url], check=True)
        return video_file_path
    except subprocess.CalledProcessError as e:
        # Обработайте ошибку, если скачивание не удалось
        print(f"Ошибка загрузки видео: {e}")
        return None
    except Exception as e:
        # Обработайте другие ошибки
        print(f"Ошибка: {e}")
        return None
