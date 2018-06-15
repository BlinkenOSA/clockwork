import os
from split_settings.tools import optional, include

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

include(
    'components/base.py',
    'components/applications.py',
    'components/database.py',
    'components/extra.py',
    'components/celery.py',
    'components/userena.py',
    'components/production_settings.py',
    optional('components/database_migration.py'),
    optional('components/local_settings.py')
)
