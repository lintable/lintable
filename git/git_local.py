import os
from functools import partial
from logging import getLogger
from typing import Dict
from uuid import UUID, uuid4

from git import Repo

join = os.path.join

local_repo = '$repo'
local_path = './tmp/$uuid'

logger = getLogger('GitHubIntegration')


def git_local_repo(uuid: UUID, repo_path: str, branch: str = 'master', path: str = None)-> (partial, partial, partial):
    path = local_path.format(uuid=uuid)

    partial_functions = (partial(retrieve_files,
                                 uuid=uuid,
                                 repository=repo_path,
                                 branch=branch,
                                 path=path),

                         partial(ab_files, path=path),

                         partial(process_results,
                                 uuid=uuid,
                                 repository=repo_path))

    return partial_functions


def retrieve_files(uuid: UUID, repository: str, branch: str, path: str):
    logger.debug('retrieving $repo from local repository for task $uuid'.format(repo=repository, uuid=uuid))
    repo = Repo(path=repository)
    repo.clone(path=path)
    logger.deubug('retrieval of $repo from local repository for task $uuid complete'.format(repo=repository, uuid=uuid))
    return None


def ab_files(path: str)-> (str, str, str):
    return '', '', ''


def process_results(repository: str, results):
    return None

