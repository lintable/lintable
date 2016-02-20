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

from uuid import UUID
from github.Commit import Commit as GithubCommit

from lintable_lintball.lint_report import LintReport
from lintable_processes.do_nothing_handler import DoNothingHandler
import logging

LINTABLE = 'Lintable'


class StatusHandler(DoNothingHandler):
    """
    This is status_updater that the ProcessHandler can delegate to.
    This allows us to update status to GitHub at key points during linting process
    """
    def __init__(self, github_commit: GithubCommit, target_url: str):
        super().__init__()
        self.github_commit = github_commit # type: GitHubCommit
        self.target_url = target_url
        self.linting_files = False
        self.logger=logging.getLogger()

    def lint_file(self, uuid: UUID, linter: str, file: str):
        super().lint_file(uuid, linter, file)
        if self.linting_files == False:
            self.linting_files = True
            self.github_commit.create_status(state='pending',
                                             target_url=self.target_url,
                                             description='Linting files',
                                             context=LINTABLE)

    def report(self, uuid: UUID, report: LintReport):
        super().report(uuid, report)
        num_of_files = len(report.errors)
        files_with_errors = dict((filename, errors) for filename, errors in report.errors.items() if len(errors) > 0)

        if len(files_with_errors) == 0:
            self.github_commit.create_status(state='success',
                                             target_url=self.target_url,
                                             description='Total number of files processed: {nof}\t Files with errors: {fwe}'.format(nof=num_of_files,fwe=len(files_with_errors)),
                                             context=LINTABLE)
        else:
            self.github_commit.create_status(state='failure',
                                             target_url=self.target_url,
                                             description='Total number of files processed: {nof}\t Files with errors: {fwe}'.format(nof=num_of_files,fwe=len(files_with_errors)),
                                             context=LINTABLE)

    def started(self, uuid: UUID, comment_id: int = None):
        self.logger.error('target_url= {url}'.format(url=self.target_url))
        super().started(uuid, comment_id)
        self.github_commit.create_status(state='pending',
                                         target_url=self.target_url,
                                         description='Starting linting process',
                                         context=LINTABLE)
