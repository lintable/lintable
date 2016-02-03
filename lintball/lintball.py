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
from typing import List, Dict
from uuid import uuid4, UUID

from functools import partial
from git.github import github_pull_hook
from lintball.lint_error import LintError
from lintball.lint_report import LintReport
from lintball.runner import runner
from linters.whitespace_file_linter import WhitespaceFileLinter


@runner.task(serializer='json')
def lint_github(payload: json, task_id=uuid4()):
    github = github_pull_hook(task_id, payload)

    lintball(github, task_id)

    return


def lintball(git: (partial, partial, partial), task_id: UUID):
    retrieve_files, ab_files, process_results = git

    retrieve_files()

    lint_errors = Dict(str, List(LintError))

    linter = WhitespaceFileLinter()

    for filename, a, b in ab_files:
        a_results = linter.lint(a)
        b_results = linter.lint(b)
        lint_errors[filename] = [results for results in b_results if results not in a_results]

    return process_results(lint_report=LintReport(errors=lint_errors))
