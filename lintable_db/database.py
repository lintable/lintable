"""Provides utility methods for handling the different database Models."""

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
from typing import Union
from uuid import uuid4, UUID

from lintable_db.models import User, Repo, Jobs

logger = logging.getLogger(__name__)

class DatabaseHandler:
    """Provides utility methods for handling the different database Models."""

    @staticmethod
    def get_repo(identifier: Union[int, str]) -> Repo:
        """Finds a repo for a given URL.

        :param identifier:
        :return Repo or None:
        """

        try:
            if isinstance(identifier, int):
                repo = Repo.get(Repo.repo_id == identifier)
            if isinstance(identifier, str):
                repo = Repo.get(Repo.url == identifier)
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
        """Finds a user for a given ID or username.

        :param identifier:
        :return User or None:
        """

        try:
            if isinstance(identifier, int):
                user = User.get(User.github_id == identifier)
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

    def set_job_status(self, job_id: int, status: str) -> int:
        """Updates job status to provided string.

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

    @staticmethod
    def get_job(identifier: UUID) -> Jobs:
        """Finds a job for a given job ID.

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
