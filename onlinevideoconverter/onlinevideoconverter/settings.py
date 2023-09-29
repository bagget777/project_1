# Настройки Django для проекта onlinevideoconverter.

# Построение путей внутри проекта, например: BASE_DIR / 'подкаталог'.
from pathlib import Path
import os
from celery import Celery

# Определение базовой директории проекта
BASE_DIR = Path(__file__).resolve().parent.parent

# Быстрый старт настроек разработки - не подходит для продакшена
# СМЕНИТЕ СЕКРЕТНЫЙ КЛЮЧ НА СЛУЧАЙНЫЙ И СТРОГО ЗАДЕРЖИВАЙТЕ ЕГО В ТАЙНЕ!
SECRET_KEY = 'django-insecure-4$_o4!95^os@65@@=d-#h$j^(4g%v_u(4+0k8b*u%m0%rsps)1'

# Включение/отключение режима отладки (DEBUG) в продакшене выключите
DEBUG = True

# Разрешенные хосты для приложения (установите для продакшена)
ALLOWED_HOSTS = []

# Определение установленных приложений
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'converter',
    'onlinevideoconverter',
    'django.contrib.staticfiles',
    'rest_framework',
]

# Настройки для Django Rest Framework
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
}

# Промежуточное ПО (Middleware)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Корневая конфигурация URL
ROOT_URLCONF = 'onlinevideoconverter.urls'

# Настройки шаблонов
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Настройка приложения WSGI
WSGI_APPLICATION = 'onlinevideoconverter.wsgi.application'

# Конфигурация базы данных
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Настройки проверки пароля
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Международная локализация и временные зоны
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Обработка статических файлов (CSS, JavaScript, изображения)
STATIC_URL = 'static/'

# Тип поля для первичных ключей по умолчанию
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Настройки Celery
celery = Celery('myapp')
celery.config_from_object('django.conf:settings', namespace='CELERY')
celery.autodiscover_tasks()

# Настройки Redis для Celery
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
