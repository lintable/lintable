import os

"""
Settings dictionary for lintweb.
"""

LINTWEB_SETTINGS = {
    'peewee': {
        'DATABASE_URL': os.environ.get('DATABASE_URL', 'postgres://user@localhost:5432/postgres')
    }
}

"""
Settings dictionary for lintball.
"""

LINTBALL_SETTINGS = {
    'celery': {
        'BROKER': os.environ.get('CELERY_BROKER', 'amqp://'),
        'BACKEND': os.environ.get('CELERY_BACKEND', 'redis://')
    },

    'peewee': {
        'HOST': os.environ.get('LINTBALL_DB_HOST', 'localhost'),
        'PORT': os.environ.get('LINTBALL_DB_PORT', '1234'),
        'USER': os.environ.get('LINTBALL_DB_USER', ''),
        'PASS': os.environ.get("LINTBALL_DB_PASS", '')
    }
}
