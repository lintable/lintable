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
    }
}
