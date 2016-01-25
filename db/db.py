from peewee import *
from peewee import SelectQuery
from typing import Iterable
import logging

logger = logging.getLogger(__name__)


database = PostgresqlDatabase(
    'db_name',
    user='user_name',
    password='password',
    host='db_address'
)


class BaseModel(Model):
    class Meta:
        try:
            database = database
        except Exception as e:
            logger.error("Unable to connect.\nException: {0}".format(e))




class User(BaseModel):
    id = PrimaryKeyField(primary_key='true')
    username = CharField(unique='true')
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


"""Returns a user object matching the supplied user name."""


def get_user(username: str) -> User:
    try:
        user = User.get(User.username == username)
    except User.DoesNotExist as e:
        user = None
        logger.error(
            'No user found for user name: {0}.\nException:\n\t{1}'.format(
                username, e))
    except Exception as e:
        user = None
        logger.error(e)

    return user


"""Returns a repo object matching the supplied URL."""


def get_repo(url: str) -> Repo:
    try:
        repo = Repo.get(Repo.url == url)
    except Repo.DoesNotExist as e:
        repo = None
        logger.error(
            'No repo found for url: {0} .\nException:\n\t{1}'.format(url, e))
    except Exception as e:
        repo = None
        logger.error(e)
    return repo


def get_jobs_for_user(username: str) -> Iterable[Jobs]:
    try:
        jobs = SelectQuery(Jobs).join(User).where(User.id == Jobs.id,
                                                  User.username == username)
    except Exception as e:
        jobs = None
        logger.error(
            'No jobs found for user with username:{0}.\nException:\n\t{'
            '1}'.format(username, e))
    return jobs


"""Updates job status and returns number of records changed. """


def set_job_status(job_id: int, status: str) -> int:
    try:
        job = Jobs.get(Jobs.id == job_id)
        job.status = status
        success = job.save()

    except Jobs.DoesNotExist as e:
        logger.error(
            'No job found with job id: {0}.\nException:\n\t{1}'.format(job_id,
                                                                       e))
        success = None
    except Exception as e:
        logger.error(e)
        success = None
    return success
