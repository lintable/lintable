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

import logging
import unittest

from peewee import SqliteDatabase
from playhouse.test_utils import test_database
from uuid import uuid4
from datetime import datetime
import random
import string

from lintable_db.database import DatabaseHandler
from lintable_db.models import User, Repo, Jobs, GithubString, Report
from lintable_settings.settings import LINTWEB_SETTINGS

# create and initialize a local test database in memory
test_db = SqliteDatabase(':memory:')

# just put the log messages into a file
logging.basicConfig(filename='./model_tests.log', level=logging.DEBUG)


class ModelTests(unittest.TestCase):
    def setUp(self):
        # Override our default encryption key.
        LINTWEB_SETTINGS['simple-crypt']['ENCRYPTION_KEY'] = "donotusethis"

        self.db = DatabaseHandler()
        User._meta.database = test_db
        Jobs._meta.database = test_db
        Repo._meta.database = test_db
        GithubString._meta.database = test_db
        Report._meta.database = test_db

        for i in [User, Jobs, Repo, GithubString, Report]:
            if not i.table_exists():
                test_db.create_table(i)

        self.user1 = User(token='dummyToken', github_id=1)
        self.repo1 = Repo(repo_id=1, owner=self.user1,
                          url='https://github.com/user/repo.git')
        self.job1 = Jobs(job_id=uuid4(), repo_owner=self.user1, repo=self.repo1,
                         start_time=datetime.now(), comment_number=1,
                         status='pending')

    def test_encrypts_token(self):
        with test_database(test_db, ()):
            # SUT
            self.assertIsNone(self.db.get_user('new_user'))
            new_user = User(username='new_user', token='dummyToken',
                            github_id=2)

            # Exercise
            new_user.save()
            self.assertNotEqual(new_user.token, 'dummyToken')
            user = self.db.get_user(2)
            self.assertNotEqual(user.token, 'dummyToken')

            # Clean up
            user.delete_instance()

    def test_encrypts_token_only_once(self):
        with test_database(test_db, ()):
            # SUT
            self.assertIsNone(self.db.get_user(2))
            new_user = User(token='dummyToken', github_id=2)
            new_user.save()

            # Exercise
            user = self.db.get_user(2)
            user.save()
            self.assertEqual(user.get_oauth_token(), 'dummyToken')
            self.assertNotEqual(user.token, 'dummyToken')
            user.username = "changed one field"
            user.save()
            self.assertEqual(user.get_oauth_token(), 'dummyToken')
            self.assertNotEqual(user.token, 'dummyToken')

            # Clean up
            user.delete_instance()

    def test_decrypts_token(self):
        with test_database(test_db, ()):
            # SUT
            self.assertIsNone(self.db.get_user(2))
            new_user = User(username='new_user', token='dummyToken',
                            github_id=2)
            new_user.save()

            # Exercise
            user = self.db.get_user(2)
            self.assertEqual(user.get_oauth_token(), 'dummyToken')
            self.assertNotEqual(user.token, 'dummyToken')

            # Clean up
            user.delete_instance()

    def test_token_type(self):
        with test_database(test_db, ()):
            self.assertTrue(self.user1.token.__class__ == str)
            self.user1.save()
            self.assertFalse(self.user1.token.__class__ == str)
            user = User.get(User.id == self.user1.id)
            self.assertFalse(user.token.__class__ == str)

            user.delete_instance()

    def test_get_token_from_repo(self):
        # SUT
        user = User(github_id=23, token='dummyToken')
        user.save()
        repo = Repo(owner=user, url='a', repo_id=2)
        repo.save()
        self.assertEqual(user.get_oauth_token(), repo.get_oauth_token())

    def test_state(self):
        # SUT
        state = GithubString(state_string='state')

        # Exercise
        self.assertTrue(state.save() == 1)

        # cleanup
        self.assertTrue(state.delete_instance() == 1)

    def test_report(self):
        # SUT
        self.user1.save()
        self.repo1.save()
        self.job1.save()

        # Exercise
        report = Report(report_number=self.job1, file_name='file_a',
                        column_number=10,
                        line_number=15, error_message='V for vendetta')
        report.save()
        for report in self.job1.reports:
            self.assertTrue(report.id == report.id)
            self.assertEqual(report.line_number, 15)

        # Cleanup
        report.delete_instance()

    def test_report_length(self):
        # SUT
        self.user1.save()
        self.repo1.save()
        self.job1.save()

        # Exercise
        comment_string = ''.join(
            random.choice(string.ascii_uppercase + string.digits) for a in
            range(1000000))
        report = Report(report_number=self.job1, file_name='file_a',
                        column_number=10,
                        line_number=15, error_message=comment_string)
        report.save()
        fetched_report = Report.get(Report.line_number == 15)
        self.assertEqual(fetched_report.file_name, report.file_name)
        self.assertTrue(len(fetched_report.error_message) == 1000000)

        # Cleanup
        report.delete_instance()


if __name__ == '__main__':
    unittest.main()
