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

import logging
from urllib.parse import urlparse

from peewee import (Model, PrimaryKeyField, IntegerField, ForeignKeyField,
                    DateTimeField, CharField, PostgresqlDatabase, UUIDField)
from simplecrypt import decrypt, encrypt, EncryptionException
from cryptography.fernet import Fernet

from lintable_db.fields import OauthField
from lintable_settings.settings import LINTWEB_SETTINGS

logger = logging.getLogger(__name__)


class BaseModel(Model):
    class Meta:
        try:
            db_url = urlparse(LINTWEB_SETTINGS['peewee']['DATABASE_URL'])
            database = PostgresqlDatabase(
                db_url.path[1:],
                user=db_url.username,
                password=db_url.password,
                host=db_url.hostname
            )
        except Exception as e:
            logger.error("Unable to connect.\nException: {0}".format(e))


class User(BaseModel):
    id = PrimaryKeyField()
    github_id = IntegerField(unique=True)
    username = CharField(null=True)
    token = OauthField()

    def get_oauth_token(self) -> str:
        """

        :return decrypted oauth token as a string:
        """
        decrypter = Fernet(LINTWEB_SETTINGS['simple-crypt']['ENCRYPTION_KEY'])
        return decrypter.decrypt(self.token).decode('utf8')

    def save(self, *args, **kwargs):
        if self.token.__class__ == str:
            try:
                encrypter = Fernet(LINTWEB_SETTINGS['simple-crypt']['ENCRYPTION_KEY'])
                self.token = encrypter.encrypt(bytes(self.token, 'utf8'))
            except EncryptionException as e:
                print('Unable to encrypt OAuth token. User not saved'\
                      'Exception: \n{}'.format(e))
                return None
        return super(User, self).save(*args, **kwargs)


class Repo(BaseModel):
    id = PrimaryKeyField()
    repo_id = IntegerField(unique=True)
    owner = ForeignKeyField(User, related_name='repos')
    url = CharField()

    def get_oauth_token(self) -> str:
        """
        Get the unencrypted OAuth token for the owner of this repo

        :return decrypted oauth token as a string:
        """
        return self.owner.get_oauth_token()


class Jobs(BaseModel):
    job_id = UUIDField(unique=True)
    repo_owner = ForeignKeyField(User, related_name='jobs')
    repo = ForeignKeyField(Repo)
    start_time = DateTimeField()
    end_time = DateTimeField(null=True)
    comment_number = IntegerField()
    status = CharField()


class Report(BaseModel):
    report_number = ForeignKeyField(Jobs, related_name='reports')
    file_name = CharField()
    column_number = IntegerField()
    line_number = IntegerField()
    error_message = CharField()


class GithubString(BaseModel):
    state_string = CharField()
