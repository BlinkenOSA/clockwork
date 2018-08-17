# Application definition
PREREQ_APP = [
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'bootstrap3',
    'django_select2',
    'widget_tweaks',
    'crispy_forms',
    'fm',
    'userena',
    'guardian',
    'easy_thumbnails',
    'session_security',
    'rest_framework',
    'rest_framework.authtoken',
]

PROJECT_APPS = [
    'accounts',
    'authority',
    'controlled_list',
    'dashboard',
    'archival_unit',
    'accession',
    'donor',
    'isaar',
    'isad',
    'container',
    'finding_aids',
    'mlr',
    'migration'
]

INSTALLED_APPS = PREREQ_APP + PROJECT_APPS