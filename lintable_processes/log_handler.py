"""Logger that the ProcessHandler can delegate to. Logs linting output."""

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

from logging import Logger
from uuid import UUID

from git import Commit, Repo

from lintable_lintball.lint_report import LintReport
from lintable_processes.do_nothing_handler import DoNothingHandler

class LogHandler(DoNothingHandler):
    """Logger that the ProcessHandler can delegate to. Logs linting output."""

    def __init__(self, logger: Logger):
        super().__init__()
        self.logger = logger

    def lint_file(self, uuid: UUID, linter: str, file: str):
        """Called when each file is linted."""

        super().lint_file(uuid, linter, file)
        self.logger.info('Linting {file} with linter {linter}'.format(file=file, linter=linter))

    def retrieve_changed_file_set(self, uuid: UUID, a_commit: Commit, b_commit: Commit):
        """Indicates what files are going to be retrieved for the 2 commits."""

        super().retrieve_changed_file_set(uuid, a_commit, b_commit)
        self.logger.info('Retrieving files from {a_commit} and {b_commit}'.format(a_commit=a_commit, b_commit=b_commit))

    def report(self, uuid: UUID, lint_report: LintReport):
        """Called when the linting process has produced a LintReport."""

        super().report(uuid, lint_report)
        num_of_files = len(lint_report.errors)
        files_with_errors = dict((filename, errors) for filename, errors in lint_report.errors.items() if len(errors) > 0)

        self.logger.info('Total number of files processed: {nof}\t Files with errors: {fwe}'.format(nof=num_of_files,
                                                                                     fwe=len(files_with_errors)))
        for file, errors in lint_report.errors.items():

            if len(errors) > 0:
                self.logger.info('File {file} contains {error_count} errors.'.format(file=file, error_count=len(errors)))
                for line, column, message in errors:
                    self.logger.info('[{line}, {column}] - {message}'.format(line=line, column=column, message=message))
            else:
                self.logger.info('{file} contained no errors.'.format(file=file))

    def started(self, uuid: UUID, comment_id: int = None):
        """Kicks off the process."""

        super().started(uuid, comment_id)
        self.logger.info('Starting linting process with id: {uuid}'.format(uuid=uuid))
        if type(comment_id) is int and comment_id >= 0:
            self.logger.debug('Comment id is {comment_id}'.format(comment_id=comment_id))

    def clone_repo(self, uuid: UUID, repo: Repo, local_path: str):
        """Indicates a repo has been cloned and where that clone is located."""

        super().clone_repo(uuid, repo, local_path)
        self.logger.info('Cloning repo {repo}'.format(repo=str(repo)))

    def retrieve_file_from_commit(self, uuid: UUID, file: str, commit: Commit):
        """Return the given file from the given commit."""

        super().retrieve_file_from_commit(uuid, file, commit)
        self.logger.info('Retrieving {file} from {commit}'.format(file=file, commit=commit))
