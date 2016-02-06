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

from git_handler.git_handler import GitHandler
from lintball.lint_error import LintError
from lintball.lint_report import LintReport
from lintball.lint_wrapper import LintWrapper
from lintball.runner import runner
from linters.whitespace_file_linter import WhitespaceFileLinter
from process_handler.log_handler import LogHandler
from process_handler.process_handler import ProcessHandler


@runner.task(serializer='json')
def lint_github(payload: json, task_id=uuid4()):
    repo_url = 'ssh://git@github.com:{full_name}.git'.format(
        full_name=payload['repo']['full_name'])

    process_handler = ProcessHandler(repo=repo_url, uuid=task_id,
                                     logger=LogHandler(logging.getLogger()))

    git_handler = GitHandler(process_handler=process_handler, repo_url=repo_url)

    lint_process(git_handler, process_handler)

    return


def lint_process(git_handler: GitHandler,
                 process_handler: ProcessHandler,
                 linters=None):

    if linters is None:
        linters = [WhitespaceFileLinter()]

    git_handler.started()

    git_handler.clone_repo()

    git_handler.retrieve_changed_files_from_commit()

    lintball(process_handler, linters)

    return


def lintball(handler: ProcessHandler, linters: List[LintWrapper]):
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
    lint_errors = []

    for linter in linters:
        handler.lint_file(linter=str(linter), file=filename)
        lint_errors.extend(linter.lint(filename))

    return lint_errors
