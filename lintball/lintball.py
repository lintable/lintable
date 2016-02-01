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
