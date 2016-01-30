import os

"""
Settings dictionary for lintweb.
"""

LINTWEB_SETTINGS = {
    'peewee': {
        'HOST': os.environ.get('LINTWEB_DB_HOST', 'localhost'),
        'PORT': os.environ.get('LINTWEB_DB_PORT', '1234'),
        'USER': os.environ.get('LINTWEB_DB_USER', ''),
        'PASS': os.environ.get("LINTWEB_DB_PASS", '')
    },
    'github': {
        'CLIENT_ID': os.environ.get('LINTWEB_CLIENT_ID', ''),
        'CLIENT_SECRET': os.environ.get('LINTWEB_CLIENT_SECRET', ''),
        'CALLBACK': os.environ.get('LINTWEB_FLASK_CALLBACK', 'localhost/callback'),
        'OAUTH_URL': os.environ.get('LINTWEB_OAUTH_URL', 'https://github.com/login/oauth/authorize'),
        'OAUTH_URL_POST': os.environ.get('LINTWEB_OAUTH_URL_POST', 'https://github.com/login/oauth/access_token'),
        'SCOPES': os.environ.get('LINTWEB_SCOPES', 'repo:status')
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
