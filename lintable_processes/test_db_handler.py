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

from lintable_db.database import DatabaseHandler
from lintable_db.models import User, Jobs, Repo
from lintable_lintball.lint_report import LintReport
from lintable_processes.db_handler import DBHandler
from lintable_settings.settings import LINTWEB_SETTINGS

test_db = SqliteDatabase(':memory:')

# just put the log messages into a file
logging.basicConfig(filename='./db_handler_tests.log', level=logging.DEBUG)


class DBHandlerTests(unittest.TestCase):
    def setUp(self):
        # Override our default encryption key.
        LINTWEB_SETTINGS['simple-crypt']['ENCRYPTION_KEY'] = "donotusethis"

        self.db = DatabaseHandler()
        User._meta.database = test_db
        Jobs._meta.database = test_db
        Repo._meta.database = test_db

        # Create local objects that can be written
        # written to the database during a test
        self.user1 = User(token='dummyToken', github_id=1)
        self.repo1 = Repo(repo_id=1, owner=self.user1,
                          url='https://github.com/user/repo.git')

        for i in [User, Jobs, Repo]:
            if not i.table_exists():
                test_db.create_table(i)

        self.user1.save()
        self.repo1.save()

        self.db_handler = DBHandler(repo_id=self.repo1.repo_id)
        self.uuid = uuid4()
        self.comment_number = 42
        self.tmp_dir = tempfile.mkdtemp()
        self.git_repo = git.Repo.init(path=self.tmp_dir, mkdir=False)
        self.db_handler.started(self.uuid, self.comment_number)

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
            self.db_handler.started(self.uuid, self.comment_number)
            self.get_and_check_job_status(status='STARTED')

    def test_clone_repo(self):
        with test_database(test_db, ()):
            self.db_handler.clone_repo(self.uuid, self.git_repo, self.tmp_dir)
            self.get_and_check_job_status('CLONE_REPO')

    def test_retrieve_files(self):
        with test_database(test_db, ()):
            commit = self.git_repo.head
            self.db_handler.retrieve_file_from_commit(self.uuid, 'file', commit)
            self.get_and_check_job_status(status='RETRIEVE_FILES')

    def test_lint_files(self):
        with test_database(test_db, ()):
            self.db_handler.lint_file(self.uuid, 'linter', 'file')
            self.get_and_check_job_status(status='LINT_FILES')

    def test_report(self):
        report = {}  # type: LintReport
        with test_database(test_db, ()):
            self.db_handler.report(self.uuid, report)
            self.get_and_check_job_status(status='REPORT')

    def test_finished(self):
        with test_database(test_db, ()):
            self.db_handler.finish(self.uuid)
            self.get_and_check_job_status(status='FINISHED')

if __name__ == '__main__':
    unittest.main()
