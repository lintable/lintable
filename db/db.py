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
from peewee import SelectQuery
from typing import Iterable
import logging
from settings.settings import LINTWEB_SETTINGS
from urllib.parse import urlparse

logger = logging.getLogger(__name__)
db_url = urlparse(LINTWEB_SETTINGS['peewee']['DATABASE_URL'])


database = PostgresqlDatabase(
    db_url.path[1:],
    user=db_url.username,
    password=db_url.password,
    host=db_url.hostname
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

def get_user(identifier: Union[int, str]) -> User:
    """
    Finds a user for a given ID or username.

    :param identifier:
    :return User or None:
    """
    try:
        if isinstance(identifier, int):
            user = User.get(User.id == identifier)
        if isinstance(identifier, str):
            user = User.get(User.username == identifier)
    except User.DoesNotExist as e:
        user = None
        logger.error(
            'No user found for identifier: {0}.\nException:\n\t{1}'.format(
                identifier, e))
    except Exception as e:
        user = None
        logger.error(e)

    return user

def get_job(identifier: int) -> Jobs:
    """
    Finds a job for a given job ID.

    :param identifier:
    :return Jobs or None:
    """
    try:
        job = Jobs.get(Jobs.jobId == identifier)
    except Jobs.DoesNotExist as e:
        job = None
        logger.error(
            'No job found for identifier: {0}.\nException:\n\t{1}'.format(
                identifier, e))
    except Exception as e:
        job = None
        logger.error(e)

    return job

def get_repo(url: str) -> Repo:
    """
    Finds a repo for a given URL

    :param url:
    :return Repo or None:
    """
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

def get_repos_for_user(identifier: Union[int, str]) -> Iterable[Repo]:
    """
    Finds any repos associated with a given username or user ID.

    :param identifier:
    :return Iterable object of Repo or None:
    """
    try:
        if isinstance(identifier, int):
            repos = SelectQuery(Repo).join(User).where(User.id == Repo.id,
                                                       User.id == identifier)
        if isinstance(identifier, str):
            repos = SelectQuery(Repo).join(User).where(User.id == Repo.id,
                                                       User.username == identifier)
    except Exception as e:
        repos = None
        logger.error(
            'No repos found for user with identifier:{0}.\nException:\n\t{'
            '1}'.format(identifier, e))
    return repos

def get_jobs_for_user(identifier: Union[int, str]) -> Iterable[Jobs]:
    """
    Finds any jobs currently in the system for a given username or user ID.

    :param identifier:
    :return Iterable object of Jobs or None:
    """
    try:
        if isinstance(identifier, int):
            jobs = SelectQuery(Jobs).join(User).where(User.id == Jobs.id,
                                                      User.id == identifier)
        if isinstance(identifier, str):
            jobs = SelectQuery(Jobs).join(User).where(User.id == Jobs.id,
                                                      User.username == identifier)
    except Exception as e:
        jobs = None
        logger.error(
            'No jobs found for user with identifier:{0}.\nException:\n\t{'
            '1}'.format(identifier, e))
    return jobs


def set_job_status(job_id: int, status: str) -> int:
    """
    Updates job status to provided string.

    :param job_id:
    :param status:
    :return number of records changed or None:
    """
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
