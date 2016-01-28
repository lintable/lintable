from peewee import *
import logging
from settings.settings import LINTWEB_SETTINGS
from urllib.parse import urlparse

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
    username = CharField(unique='true', null=True)
    github_id = CharField(unique='true')
    token = CharField(unique='true')


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
