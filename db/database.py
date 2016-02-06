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
from db.models import User, Repo, Jobs
from typing import Union

logger = logging.getLogger(__name__)


class database_handler():
    def get_repo(self, identifier: Union[int, str]) -> Repo:
        """
        Finds a repo for a given URL

        :param url:
        :return Repo or None:
        """
        try:
            if isinstance(identifier, int):
                user = Repo.get(Repo.repo_id == identifier)
            if isinstance(identifier, str):
                user = Repo.get(Repo.url == identifier)
        except Repo.DoesNotExist as e:
            repo = None
            logger.error(
                'No repo found for identifier: {0} .\nException:\n\t{1}'.format(
                    identifier, e))
        except Exception as e:
            repo = None
            logger.error(e)
        return repo

    @staticmethod
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
                user = User.get(User.github_id == identifier)
        except User.DoesNotExist as e:
            user = None
            logger.error(
                'No user found for identifier: {0}.\nException:\n\t{1}'.format(
                    identifier, e))
        except Exception as e:
            user = None
            logger.error(e)
        return user

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
                'No job found with job id: {0}.\nException:\n\t{1}'.format(
                    job_id,
                    e))
            success = None
        except Exception as e:
            logger.error(e)
            success = None
        return success

    def get_job(self, identifier: int) -> Jobs:
        """
        Finds a job for a given job ID.

        :param identifier:
        :return Jobs or None:
        """
        try:
            job = Jobs.get(Jobs.job_id == identifier)
        except Jobs.DoesNotExist as e:
            job = None
            logger.error(
                'No job found for identifier: {0}.\nException:\n\t{1}'.format(
                    identifier, e))
        except Exception as e:
            job = None
            logger.error(e)

        return job

    def get_repos_for_user(self, identifier: Union[int, str]) -> Iterable[Repo]:
        """
        Finds any repos associated with a given username or user ID.

        :param identifier:
        :return Iterable object of Repo or None:
        """
        try:
            repos = self.get_user(identifier).repos
        except Exception as e:
            logger.warn(e)
            repos = None
        return repos

    def get_jobs_for_user(self, identifier: Union[int, str]) -> Iterable[Jobs]:
        """
        Finds any jobs currently in the system for a given username or user ID.
        :param identifier:
        :return Iterable object of Jobs or None:
        """
        try:
            jobs = self.get_user(identifier).jobs
        except Exception as e:
            jobs = None
        return jobs
