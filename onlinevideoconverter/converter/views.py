# converter/views.py

# Представления Django для приложения converter.

from .models import ConversionRequest
from rest_framework import generics
from .serializers import ConversionRequestSerializer
from .utils import download_video, convert_video_to_mp3, create_zip_archive, send_mp3_email

# converter/views.py

# ...

# Представление для создания конверсионного запроса через API.
class ConversionRequestCreateView(generics.CreateAPIView):
    queryset = ConversionRequest.objects.all()
    serializer_class = ConversionRequestSerializer

    def perform_create(self, serializer):
        video_url = serializer.validated_data['video_url']
        email = serializer.validated_data['email']

        # Скачать видео с помощью youtube-dl
        video_file_path = download_video(video_url)

        if video_file_path:
            mp3_file_path = convert_video_to_mp3(video_file_path)

            if mp3_file_path:
                archive_path = create_zip_archive(mp3_file_path)

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
            else:
                print("Ошибка в конвертации видео в MP3")
        else:
            print("Ошибка загрузки видео")

