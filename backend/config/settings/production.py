from .base import *
import os

DEBUG = False  # Asegurar que DEBUG esté configurado como False
ALLOWED_HOSTS = ['*']  # Permitir todos los hosts
APPEND_SLASH = True  # Asegurar que APPEND_SLASH esté configurado como True

CSRF_TRUSTED_ORIGINS = ['https://.vercel.app', 'https://.onrender.com']
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
