from .base import *
import os

DEBUG = True  # Cambiar a True para habilitar el modo de depuración
ALLOWED_HOSTS = ['*']  # Permitir todos los hosts
APPEND_SLASH = True  # Asegurar que APPEND_SLASH esté configurado como True

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
