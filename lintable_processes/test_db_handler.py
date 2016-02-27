# Copyright 201016 Capstone Team G
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

import logging
import shutil
import tempfile
import unittest

# create and initialize a local test database in memory
from uuid import uuid4

import git
from peewee import SqliteDatabase
from playhouse.test_utils import test_database
from cryptography.fernet import Fernet

from lintable_db.database import DatabaseHandler
from lintable_db.models import User, Jobs, Repo, Report, ReportSummary
from lintable_lintball.lint_error import LintError
from lintable_lintball.lint_report import LintReport, create_from_db_query
from lintable_processes.db_handler import DBHandler
from lintable_settings.settings import LINTWEB_SETTINGS

test_db = SqliteDatabase(':memory:')

# just put the log messages into a file
logging.basicConfig(filename='./db_handler_tests.log', level=logging.DEBUG)


class DBHandlerTests(unittest.TestCase):
    def setUp(self):
        # Override our default encryption key.
        LINTWEB_SETTINGS['simple-crypt']['ENCRYPTION_KEY'] = Fernet.generate_key()

        self.db = DatabaseHandler()
        User._meta.database = test_db
        Jobs._meta.database = test_db
        Repo._meta.database = test_db
        Report._meta.database = test_db
        ReportSummary._meta.database = test_db

        # Create local objects that can be written
        # written to the database during a test
        self.user1 = User(token='dummyToken', github_id=1)
        self.repo1 = Repo(repo_id=1, owner=self.user1,
                          url='https://github.com/user/repo.git')

        for i in [User, Jobs, Repo, Report, ReportSummary]:
            if not i.table_exists():
                test_db.create_table(i)

        self.user1.save()
        self.repo1.save()

        self.db_handler = DBHandler(repo_id=self.repo1.repo_id)
        self.uuid = uuid4()
        self.tmp_dir = tempfile.mkdtemp()
        self.git_repo = git.Repo.init(path=self.tmp_dir, mkdir=False)
        self.db_handler.started(self.uuid)

    def tearDown(self):

        self.user1.delete_instance()
        self.repo1.delete_instance()

        shutil.rmtree(self.tmp_dir)

    def get_and_check_job_status(self, status: str)-> Jobs:
        job = DatabaseHandler.get_job(identifier=self.uuid)
        self.assertIsNotNone(job, 'Job row with uuid {uuid} doesn\'t exist'.format(uuid=self.uuid))
        self.assertTrue(job.status == status,
                        'Job status after started call should be {expected} not \'{actual}\''.format(expected=status,
                                                                                                     actual=job.status))

        return job

    def test_started(self):
        with test_database(test_db, ()):
            self.db_handler.started(self.uuid)
            self.get_and_check_job_status(status='STARTED')

    def test_clone_repo(self):
        with test_database(test_db, ()):
            self.db_handler.clone_repo(self.uuid, self.git_repo, self.tmp_dir)
            self.get_and_check_job_status('CLONE_REPO')

    def test_retrieve_files(self):
        with test_database(test_db, ()):
            commit = self.git_repo.head
            self.db_handler.retrieve_file_from_commit(self.uuid, 'file', commit)
            job = self.get_and_check_job_status(status='RETRIEVE_FILES')

            report_summary = job.summaries

            self.assertTrue(len(report_summary) == 1, 'report_summary should contain 1 row')
            self.assertTrue(report_summary[0].file_name == 'file', 'file_name should be file')
            self.assertTrue(report_summary[0].error_count == 0, 'error_count should be 0')

    def test_lint_files(self):
        with test_database(test_db, ()):
            self.db_handler.lint_file(self.uuid, 'linter', 'file')
            self.get_and_check_job_status(status='LINT_FILES')

    def test_report(self):
        report = LintReport(errors=dict(a_file=[LintError(line_number=1,
                                                          column=2,
                                                          msg='Some error message')]))  # type: LintReport
        a_file = 'a_file'

        with test_database(test_db, ()):
            self.db_handler.retrieve_file_from_commit(self.uuid, file=a_file, commit=self.git_repo.head)
            self.db_handler.report(self.uuid, report)
            job = self.get_and_check_job_status(status='REPORT')

            # now check that the lint_report got saved

            retrieved_report = create_from_db_query(job.reports)
            summaries = job.summaries

            self.assertIsNotNone(retrieved_report)
            self.assertEqual(report,
                             retrieved_report,
                             'The original lint_report and the retrieved lint_report should be the same')

            self.assertIsNotNone(summaries)
            self.assertTrue(len(summaries) == 1 and
                            summaries[0].file_name == a_file and
                            summaries[0].error_count == 1,
                            'ReportSummary should contain 1 row, with file_name == {a_file} and error_count == 1'
                            .format(a_file=a_file))

    def test_finished(self):
        with test_database(test_db, ()):
            self.db_handler.finish(self.uuid)
            self.get_and_check_job_status(status='FINISHED')

if __name__ == '__main__':
    unittest.main()
