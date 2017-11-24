import os
from clockwork.settings import BASE_DIR


SECRET_KEY = os.environ['DJANGO_SECRET_KEY']

DEBUG = False

ALLOWED_HOSTS = ['ams.osaarchivum.org']

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'public', 'static')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static', 'components'),
    os.path.join(BASE_DIR, 'static', 'django_select2')
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'public]', 'media')

CSRF_COOKIE_SECURE = True
X_FRAME_OPTIONS = 'DENY'
SESSION_COOKIE_SECURE = True
