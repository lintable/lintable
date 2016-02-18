"""Provides models for interfacing with the database."""

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
from datetime import date, timedelta
from urllib.parse import urlparse

from peewee import (Model, PrimaryKeyField, IntegerField, ForeignKeyField,
                    DateTimeField, CharField, UUIDField, PostgresqlDatabase)
from simplecrypt import decrypt, encrypt, EncryptionException
from cryptography.fernet import Fernet

from lintable_db.fields import OauthField
from lintable_settings.settings import LINTWEB_SETTINGS

logger = logging.getLogger(__name__)


class BaseModel(Model):
    """Elements that apply to all our models."""

    class Meta:
        """Database access settings for all our models."""

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
    """A user of the website, with repos/tokens."""

    id = PrimaryKeyField()
    github_id = IntegerField(unique=True)
    username = CharField(null=True)
    token = OauthField()

    @property
    def is_authenticated(self):
        """Is the user authenticated? Always true for our User objects."""

        return True

    @property
    def is_active(self):
        """Is this user active? Always true because we don't disable users."""

        return True

    @property
    def is_anonymous(self):
        """Is the user anonymous? Always false because we don't have anons."""

        return False

    def get_id(self) -> str:
        """Returns the user id as a string."""

        return str(self.github_id)

    def get_oauth_token(self) -> str:
        """Return the OAuth token for a user.

        :return decrypted oauth token as a string:
        """
        if isinstance(self.token, str):
            self.token = bytes(self.token, 'utf8')

        decrypter = Fernet(LINTWEB_SETTINGS['simple-crypt']['ENCRYPTION_KEY'])
        return decrypter.decrypt(self.token).decode('utf8')

    def save(self, *args, **kwargs):
        """Override the default save method for a Model."""

        if self.token.__class__ == str:
            try:
                encrypter = Fernet(
                    LINTWEB_SETTINGS['simple-crypt']['ENCRYPTION_KEY'])
                self.token = encrypter.encrypt(bytes(self.token, 'utf8'))
            except EncryptionException as e:
                print('Unable to encrypt OAuth token. User not saved'\
                      'Exception: \n{}'.format(e))
                return None
        return super(User, self).save(*args, **kwargs)


class Repo(BaseModel):
    """A repo, with URL and id."""

    id = PrimaryKeyField()
    repo_id = IntegerField(unique=True)
    owner = ForeignKeyField(User, related_name='repos')
    url = CharField()

    def get_oauth_token(self) -> str:
        """Get the unencrypted OAuth token for the owner of this repo

        :return decrypted oauth token as a string:
        """

        return self.owner.get_oauth_token()


class Jobs(BaseModel):
    """A linting job, currently running or already done."""

    job_id = UUIDField(unique=True)
    repo_owner = ForeignKeyField(User, related_name='jobs')
    repo = ForeignKeyField(Repo)
    start_time = DateTimeField()
    end_time = DateTimeField(null=True)
    status = CharField()

    def finished(self) -> bool:
        """Get whether the job is finished or not."""

        if self.end_time is None:
            return False

        return True

    def duration(self) -> timedelta:
        """Get the duration of the job."""

        if self.finished():
            return (self.end_time - self.start_time)

        return (date.today() - self.start_time)

class Report(BaseModel):
    """A linting results report."""

    report_number = ForeignKeyField(Jobs, related_name='reports')
    file_name = CharField()
    column_number = IntegerField()
    line_number = IntegerField()
    error_message = CharField()

class ReportSummary(BaseModel):
    job_id=ForeignKeyField(Jobs, related_name='summaries')
    file_name = CharField()
    error_count = IntegerField(default=0)

class GithubString(BaseModel):
    """A test state placeholder."""

    state_string = CharField()
