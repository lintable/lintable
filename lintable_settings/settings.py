# Copyright 2015-2016 Capstone Team G
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

"""
Settings dictionary for lintweb.
"""

LINTWEB_SETTINGS = {
    'peewee': {
        'DATABASE_URL': os.environ.get('DATABASE_URL', 'postgres://user@localhost:5432/postgres')
    },
    'simple-crypt': {
        'ENCRYPTION_KEY': os.environ.get('ENCRYPTION_KEY', None)
    },
    'github': {
        'CLIENT_ID': os.environ.get('LINTWEB_CLIENT_ID', ''),
        'CLIENT_SECRET': os.environ.get('LINTWEB_CLIENT_SECRET', ''),
        'CALLBACK': os.environ.get('LINTWEB_FLASK_CALLBACK', 'localhost/callback'),
        'OAUTH_URL': os.environ.get('LINTWEB_OAUTH_URL', 'https://github.com/login/oauth/authorize'),
        'OAUTH_URL_POST': os.environ.get('LINTWEB_OAUTH_URL_POST', 'https://github.com/login/oauth/access_token'),
        'SCOPES': os.environ.get('LINTWEB_SCOPES', 'repo')
    },
    'DEBUG' : os.environ.get('DEBUG', True),
    'SESSIONS_SECRET': os.environ.get('LINTWEB_SESSIONS_SECRET', '')
}

"""
Settings dictionary for lintball.
"""

LINTBALL_SETTINGS = {
    'celery': {
        'broker': os.environ.get('CELERY_BROKER', 'amqp://'),
        'backend': os.environ.get('CELERY_BACKEND', 'redis://')
    }
}
