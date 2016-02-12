"""Handles the linting process, between the GitHandler and Lintball."""

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

from git import Commit, Repo

from lintable_lintball.lint_report import LintReport
from lintable_processes.do_nothing_handler import DoNothingHandler
from lintable_processes.process_state import ProcessState

class ProcessHandler(object):
    """Handles the linting process, between the GitHandler and Lintball.

    It tracks the state of the process and delegates to side-effecting code
    for logging, db persistence, and website commenting.
    """

    def __init__(self, uuid: UUID, repo: Repo, logger=DoNothingHandler(),
                 status_handler=DoNothingHandler(), db=DoNothingHandler()):
        self.state = ProcessState.STARTED
        self.uuid = uuid
        self.repo = repo
        self.logger = logger
        self.status_updater = status_handler
        self.db = db
        self.a_commit = None
        self.b_commit = None
        self.local_path = None
        self.files = []
        self.comment_id = None

    def started(self):
        """Kicks off the process.

        :return:
        """

        self.comment_id = self.status_updater.started(uuid=self.uuid)
        self.logger.started(uuid=self.uuid, comment_id=self.comment_id)
        self.db.started(uuid=self.uuid, comment_id=self.comment_id)

    def clone_repo(self, local_path: str):
        """Indicates a repo has been cloned and where that clone is located.

        :param local_path: The path of the cloned repo.
        :return:
        """

        self.state = ProcessState.CLONE_REPO
        self.local_path = local_path
        self.logger.clone_repo(self.uuid, self.repo, local_path)
        self.status_updater.clone_repo(self.uuid, self.repo, local_path)
        self.db.clone_repo(self.uuid, self.repo, local_path)
        return

    def retrieve_changed_file_set(self, a_commit: Commit, b_commit: Commit):
        """Indicates what files are going to be retrieved for the 2 commits.

        :param a_commit: The commit we are checking for changed files
        :param b_commit: The commit we are comparing against
        :return:
        """

        self.state = ProcessState.RETRIEVE_FILES
        self.a_commit = a_commit
        self.b_commit = b_commit
        self.logger.retrieve_changed_file_set(self.uuid, a_commit, b_commit)
        self.status_updater.retrieve_changed_file_set(self.uuid, a_commit, b_commit)
        self.db.retrieve_changed_file_set(self.uuid, a_commit, b_commit)
        return

    def retrieve_file_from_commit(self, file: str, commit: Commit):
        """Called for each file being retrieved.

        :param file: The filename being retrieved
        :param commit: The commit it is being retrieved from.
        :return:
        """

        # track which files we have retrieved
        self.files.append(file)
        self.logger.retrieve_file_from_commit(self.uuid, file, commit)
        self.status_updater.retrieve_file_from_commit(self.uuid, file, commit)
        self.db.retrieve_file_from_commit(self.uuid, file, commit)
        return

    def lint_file(self, linter: str, file: str):
        """Called when each file is linted.

        :param linter: The name of the linter being used
        :param file: The filename being linted.
        :return:
        """

        self.state = ProcessState.LINT_FILES
        self.logger.lint_file(self.uuid, linter, file)
        self.status_updater.lint_file(self.uuid, linter, file)
        self.db.lint_file(self.uuid, linter, file)
        return

    def report(self, report: LintReport):
        """Called when the linting process has produced a LintReport.

        :param report: The lint report being produced.
        :return:
        """

        self.state = ProcessState.REPORT
        self.logger.report(self.uuid, report)
        self.status_updater.report(self.uuid, report)
        self.db.report(self.uuid, report)
        return

    def finish(self):
        """Called as a last step to clean up the linting process.

        :return:
        """

        self.state = ProcessState.FINISHED
        self.logger.finish(self.uuid)
        self.status_updater.finish(self.uuid)
        self.db.finish(self.uuid)
        return
