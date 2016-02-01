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

from peewee import *
import logging
from db.fields import OauthField
import db.database
from settings.settings import LINTWEB_SETTINGS
from urllib.parse import urlparse
from simplecrypt import decrypt, encrypt

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
    id = PrimaryKeyField(primary_key='true')
    username = CharField(unique='true', null='True')
    github_id = CharField(unique='true')
    token = OauthField(unique='True')

    def get_oauth_token(self) -> str:
        """

        :return decrypted oauth token as a string:
        """
        return decrypt(LINTWEB_SETTINGS['simple-crypt']['ENCRYPTION_KEY'],
                       self.token).decode('utf8')

    def save(self):
        if db.database.database_handler.get_user(self.username) is None:
            try:
                # has this value been encrypted?
                decrypt(LINTWEB_SETTINGS['simple-crypt']['ENCRYPTION_KEY'], self.token)
            except Exception as e:
                self.token = encrypt(LINTWEB_SETTINGS['simple-crypt']['ENCRYPTION_KEY'], self.token)
        return super(User, self).save()


class Repo(BaseModel):
    id = ForeignKeyField(User, related_name='repos')
    url = CharField(unique='true')
    token = ForeignKeyField(User)


class Jobs(BaseModel):
    id = ForeignKeyField(User, related_name='jobs', to_field='id')
    jobId = PrimaryKeyField()
    url = ForeignKeyField(Repo, to_field='url')
    startTime = DateTimeField()
    endTime = DateTimeField(null=True)
    commentNumber = IntegerField()
    status = CharField()
