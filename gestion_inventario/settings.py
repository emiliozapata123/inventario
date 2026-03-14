# gestion_inventario/settings.py
from pathlib import Path
import os
import dj_database_url

# ----------------------------------------
# Base del proyecto
# ----------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# ----------------------------------------
# Seguridad
# ----------------------------------------
# SECRET_KEY = os.environ.get("SECRET_KEY",'django-insecure-qdi!f6da8!r1#5+*b^&63qvlyz$51yn4=x@7%3(21v^4gb80!r')
SECRET_KEY = os.environ.get("SECRET_KEY", "super-secret-key-local")
DEBUG = os.environ.get("DEBUG", "False") == "True"

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    "inventariobackend-va4r.onrender.com",

]

# ----------------------------------------
# Aplicaciones
# ----------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'corsheaders',
    'rest_framework',
    'rest_framework_simplejwt',

    'inventario',
    'accounts',
]


# ----------------------------------------
# Middleware
# ----------------------------------------
MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware', 
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
}

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

ROOT_URLCONF = 'gestion_inventario.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'gestion_inventario.wsgi.application'

# ----------------------------------------
# Base de datos
# ----------------------------------------
if os.environ.get("DATABASE_URL"):
    DATABASES = {
        "default": dj_database_url.parse(os.environ["DATABASE_URL"], conn_max_age=600)
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# ----------------------------------------
# Password validators
# ----------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ----------------------------------------
# Internacionalización
# ----------------------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ----------------------------------------
# Archivos estáticos y media
# ----------------------------------------
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
# ----------------------------------------
# CORS
# ----------------------------------------
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

# ----------------------------------------
# Email (Gmail)
# ----------------------------------------
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get("EMAIL_USER","emiliozapata952@gmail.com")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_PASS","iocutoytxgxrqvca")
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'