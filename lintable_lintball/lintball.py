"""Handles linter tasks for a given repo."""

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

import json
import logging
import os
from typing import List
from uuid import uuid4

from lintable_db.database import DatabaseHandler
from lintable_db.models import User
from lintable_git.git_handler import GitHandler
from lintable_lintball.lint_error import LintError
from lintable_lintball.lint_report import LintReport
from lintable_lintball.lint_wrapper import LintWrapper
from lintable_lintball.runner import runner
from lintable_linters.whitespace_file_linter import WhitespaceFileLinter
from lintable_processes.db_handler import DBHandler
from lintable_processes.log_handler import LogHandler
from lintable_processes.process_handler import ProcessHandler


@runner.task(serializer='json')
def lint_github(payload: json, task_id=uuid4()):
    """Receive a task to lint a Github repo."""

    logger = logging.getLogger()

    if payload['action'] != 'opened' and payload['action'] != 'synchronized':
        return

    github_id = payload['repository']['owner']['id']

    owner = DatabaseHandler.get_user(github_id)

    oauth_key = owner.get_oauth_token() if isinstance(owner, User) else None

    if oauth_key is None:
        logger.error('Unable to locate oauth_token for {user} with id of {id}'.format(user=owner, id=github_id))
        return

    repo_url = 'https://{oauth_key}@github.com/{full_name}.git'.format(
        oauth_key=oauth_key,
        full_name=payload['repository']['full_name'])

    sha1_a = payload['pull_request']['head']['sha']
    sha1_b = payload['pull_request']['base']['sha']

    repo_id = payload['pull_request']['repository']['id']

    process_handler = ProcessHandler(repo=repo_url,
                                     uuid=task_id,
                                     logger=LogHandler(logger),
                                     db=DBHandler(repo_id=repo_id))

    git_handler = GitHandler(process_handler=process_handler,
                             repo_url=repo_url,
                             sha1_a=sha1_a,
                             sha1_b=sha1_b)

    lint_process(git_handler, process_handler)

    return


def lint_process(git_handler: GitHandler,
                 process_handler: ProcessHandler,
                 linters=None):
    """Get the files we're interested in, then start the linter."""

    if linters is None:
        linters = [WhitespaceFileLinter()]

    git_handler.started()

    git_handler.clone_repo()

    git_handler.retrieve_changed_files_from_commit()

    lintball(process_handler, linters)

    return


def lintball(handler: ProcessHandler, linters: List[LintWrapper]):
    """Run a linter or linters."""

    a_path = os.path.join(handler.local_path, 'a')
    b_path = os.path.join(handler.local_path, 'b')

    lint_errors = {}

    for filename in handler.files:
        a_file = os.path.join(a_path, filename)
        b_file = os.path.join(b_path, filename)

        a_results = lint(a_file, linters, handler) if os.path.exists(
            a_file) else []
        b_results = lint(b_file, linters, handler) if os.path.exists(
            b_file) else []
        lint_errors[filename] = [results for results in b_results if
                                 results not in a_results]

    lint_report = LintReport(errors=lint_errors)

    handler.report(lint_report)

    handler.finish()

    return


def lint(filename: str, linters: List[LintWrapper], handler: ProcessHandler) -> List[LintError]:
    """Run a linter or linters."""

    lint_errors = []

    for linter in linters:
        handler.lint_file(linter=str(linter), file=filename)
        lint_errors.extend(linter.lint(filename))

    return lint_errors
