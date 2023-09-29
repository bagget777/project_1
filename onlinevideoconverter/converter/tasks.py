# converter/tasks.py

# Задачи Celery для приложения converter.

from celery import shared_task
from .models import ConversionRequest
from .utils import download_video, convert_video_to_mp3, create_zip_archive, send_mp3_email

# Задача Celery для обработки конверсионного запроса.
@shared_task
def process_conversion_request(request_id):
    request = ConversionRequest.objects.get(pk=request_id)

    # Изменение статуса задачи на "в процессе"
    request.status = 'In Progress'
    request.save()

    # Сначала скачиваем видео
    video_file_path = download_video(request.video_url)

    if video_file_path:
        mp3_file_path = convert_video_to_mp3(video_file_path)

        if mp3_file_path:
            archive_path = create_zip_archive(mp3_file_path)

            sender_email = "your_email@example.com"
            sender_password = "your_email_password"
            subject = "Converted Video"
            body = "Here is your converted video."

            if send_mp3_email(sender_email, sender_password, request.email, subject, body, mp3_file_path):
                # Если отправка прошла успешно, обновите статус задачи
                request.status = 'Completed'
                request.mp3_file = mp3_file_path
            else:
                # Если возникла ошибка при отправке почты, обновите статус задачи
                request.status = 'Error'
        else:
            # Если возникла ошибка в конвертации или создании архива, обновите статус задачи
            request.status = 'Error'
    else:
        # Если возникла ошибка при скачивании видео, также обновите статус задачи
        request.status = 'Error'

    request.save()
