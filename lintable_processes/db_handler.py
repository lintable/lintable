"""Updates the database based on a job's progress."""

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

from typing import Optional
from uuid import UUID

import datetime
from git import Commit, Repo

from lintable_db import models
from lintable_db.database import DatabaseHandler
from lintable_db.models import Jobs, Report
from lintable_lintball.lint_report import LintReport
from lintable_processes.do_nothing_handler import DoNothingHandler


class DBHandler(DoNothingHandler):
    """Updates the database based on a job's progress."""

    def __init__(self, repo_id: int):
        super().__init__()
        self.job = None  # type: Optional[Jobs]
        self.repo_id = repo_id
        self.repo_fk = None  # type: Optional[models.Repo]

    def report(self, uuid: UUID, lint_report: LintReport):
        """Called when the linting process has produced a LintReport."""

        super().report(uuid, lint_report)

        for filename, errors in lint_report.errors.items():
            for error in errors:
                line = Report.create(report_number=self.job,
                                     file_name=filename,
                                     column_number=error.column,
                                     line_number=error.line_number,
                                     error_message=error.msg)
                line.save()

        self.job.status = 'REPORT'
        self.job.save()

    def started(self, uuid: UUID, comment_id: int = None):
        """Kicks off the process."""

        super().started(uuid, comment_id)
        self.repo_fk = DatabaseHandler.get_repo(identifier=self.repo_id)
        self.job = Jobs.create(job_id=uuid,
                               repo_owner=self.repo_fk.owner_id,
                               repo=self.repo_fk,
                               start_time=datetime.datetime.now(),
                               end_time=None,
                               comment_number=comment_id,
                               status='STARTED')
        self.job.save()

    def lint_file(self, uuid: UUID, linter: str, file: str):
        """Called when each file is linted."""

        super().lint_file(uuid, linter, file)
        if self.job.status != 'LINT_FILES':
            self.job.status = 'LINT_FILES'
            self.job.save()

    def finish(self, uuid: UUID):
        """Called as a last step to clean up the linting process."""

        super().finish(uuid)
        self.job.end_time = datetime.datetime.now()
        self.job.status = 'FINISHED'
        self.job.save()

    def retrieve_file_from_commit(self, uuid: UUID, file: str, commit: Commit):
        """Called for each file being retrieved."""

        super().retrieve_file_from_commit(uuid, file, commit)
        self.job.status = 'RETRIEVE_FILES'
        self.job.save()

    def retrieve_changed_file_set(self, uuid: UUID, a_commit: Commit, b_commit: Commit):
        """Indicates what files are going to be retrieved for the 2 commits."""

        super().retrieve_changed_file_set(uuid, a_commit, b_commit)

    def clone_repo(self, uuid: UUID, repo: Repo, local_path: str):
        """Indicates a repo has been cloned and where that clone is located."""

        super().clone_repo(uuid, repo, local_path)
        self.job.status = 'CLONE_REPO'
        self.job.save()
