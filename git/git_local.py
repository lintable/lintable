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

import os
from functools import partial
from logging import getLogger
from typing import Dict, Iterable
from uuid import UUID, uuid4

from git import Repo
from lintball.lint_report import LintReport

join = os.path.join

local_repo = '$repo'
local_path = './tmp/$uuid'

logger = getLogger('LocalGitIntegration')


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


def ab_files(path: str)-> Iterable(str, str, str):
    return []


def process_results(repository: str, lint_report: LintReport):
    return None

