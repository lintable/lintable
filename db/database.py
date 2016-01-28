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
from db.models import User
from db.models import Repo
from db.models import Jobs
logger = logging.getLogger(__name__)

class database_handler():
    def get_repo(self, url: str) -> Repo:
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


    def get_user(self, username: str) -> User:
        """
        Finds a user for a given user name

        :param username:
        :return User or None:
        """
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


    def get_jobs_for_user(self, username: str) -> Iterable[Jobs]:
        """
        Finds any jobs currently in the system for a given user name.

        :param username:
        :return Iterable object of Jobs or None:
        """
        try:
            jobs = SelectQuery(Jobs).join(User).where(User.id == Jobs.id,
                                                      User.username == username)
        except Exception as e:
            jobs = None
            logger.error(
                'No jobs found for user with username:{0}.\nException:\n\t{'
                '1}'.format(username, e))
        return jobs


    def set_job_status(self, job_id: int, status: str) -> int:
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
