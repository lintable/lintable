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

    handler = ProcessHandler(repo=repo_url, uuid=task_id,
                             logger=LogHandler(logging.getLogger()))

    git_handler = GitHandler(handler=handler, repo_url=repo_url)

    git_handler.clone_repo()

    git_handler.retrieve_files()

    linters = [WhitespaceFileLinter()]

    lintball(handler, linters)

    return


def lintball(handler: ProcessHandler,
             linters: List[LintWrapper]):
    a_path = os.path.join(handler.local_path, 'a')
    b_path = os.path.join(handler.local_path, 'b')

    lint_errors = {}

    for filename in handler.files():
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


def lint(filename: str, linters: List[LintWrapper], handler: ProcessHandler) \
    -> \
        List[LintError]:
    lint_errors = []

    for linter in linters:
        handler.lint_file(linter=str(linter), file=filename)
        lint_errors.append(linter.lint(filename))

    return lint_errors
