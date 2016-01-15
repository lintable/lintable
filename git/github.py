import os
from functools import partial
from logging import getLogger
from typing import Dict, Iterable
from uuid import UUID, uuid4

from git import Repo

join = os.path.join

github_repo = 'git@github.com:$owner/$repo'

logger = getLogger('GitHubIntegration')


def github_pull_hook(uuid: UUID, payload: Dict)-> (partial, partial, partial):
    owner = payload['repo']['owner']
    repo = payload['repo']['name']
    pull_request = payload['pull_request']['id']
    path = './$uuid'.format(uuid=uuid)
    comment_id = 0

    partial_functions = (partial(retrieve_files,
                                 uuid=uuid,
                                 owner=owner,
                                 repository=repo,
                                 pull_request_id=pull_request,
                                 path=path,
                                 comment_id=comment_id),

                         partial(ab_files, path=path),

                         partial(process_results,
                                 uuid=uuid,
                                 owner=owner,
                                 repository=repo,
                                 pull_request_id=pull_request))

    return partial_functions


def retrieve_files(uuid: UUID, owner: str, repository: str, pull_request_id: str, path: str, comment_id: int):
    logger.debug('retrieving $repo from github for task $uuid'.format(repo=repository, uuid=uuid))
    repo = Repo.clone_from(url=github_repo.format(owner=owner, repo=repository), to_path=path)
    logger.deubug('retrieval of $repo from github for task $uuid complete'.format(repo=repository, uuid=uuid))
    return None


def ab_files(path: str)-> Iterable(str, str, str):
    return []


def process_results(repository: str, pull_request_id: str, comment_id: int):
    return None

