"""Tests for DatabaseHandler."""

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

from datetime import datetime
import logging
import unittest
from uuid import uuid4

from peewee import SqliteDatabase
from playhouse.test_utils import test_database
from cryptography.fernet import Fernet

from lintable_db.database import DatabaseHandler, User, Repo, Jobs
from lintable_settings.settings import LINTWEB_SETTINGS

# create and initialize a local test database in memory
test_db = SqliteDatabase(':memory:')

# just put the log messages into a file
logging.basicConfig(filename='./db_tests.log', level=logging.DEBUG)


class dbTests(unittest.TestCase):
    """Tests for DatabaseHandler."""

    def setUp(self):
        # Override our default encryption key.
        LINTWEB_SETTINGS['simple-crypt']['ENCRYPTION_KEY'] = Fernet.generate_key()

        self.db = DatabaseHandler()
        User._meta.database = test_db
        Jobs._meta.database = test_db
        Repo._meta.database = test_db

        # Create local objects that can be written
        # written to the database during a test
        self.user1 = User(token='dummyToken', github_id=1)
        self.user2 = User(token='badToken', github_id=2)
        self.repo1 = Repo(repo_id=1, owner=self.user1,
                          url='https://github.com/user/repo.git')
        self.repo2 = Repo(repo_id=2, owner=self.user1,
                          url='https://github.com/user/repo2.git')

        for i in [User, Jobs, Repo]:
            if not i.table_exists():
                test_db.create_table(i)

    def tearDown(self):
        self.user1.delete_instance()
        self.user2.delete_instance()
        self.repo1.delete_instance()
        self.repo2.delete_instance()

    def test_shouldHaveUser(self):
        """Make sure that the database has at least one user."""

        with test_database(test_db, ()):
            self.assertIsNotNone(User())

    def test_shouldHaveJob(self):
        """Make sure that the database has at least one job."""

        with test_database(test_db, ()):
            self.assertIsNotNone(Jobs())

    def test_shouldHaveRepo(self):
        """Make sure that the database has at least repo."""

        with test_database(test_db, ()):
            self.assertIsNotNone(Repo())

    def test_returns_none_for_missing_user(self):
        """Make sure that a user query with no results returns None."""

        with test_database(test_db, ()):
            self.assertIsNone(self.db.get_user(''))

    def test_find_user_by_id(self):
        """Make sure that a valid user query returns a user."""

        with test_database(test_db, ()):
            # SUT
            self.user1.save()

            # exercise
            person = self.db.get_user(1)
            twin = self.db.get_user(person.github_id)

            self.assertEqual(self.assertEqual(person, self.user1),
                             self.assertEqual(self.user1, twin))

            # clean up
            person.delete_instance()
            self.assertIsNone(self.db.get_user(2))
            self.assertEqual(person.id, twin.id)
            twin.delete_instance()

    def test_get_missing_repo(self):
        """Make sure that a repo query with no results returns empty iter."""

        with test_database(test_db, ()):
            self.user2.save()
            for repo in self.user2.repos:
                self.assertTrue(False)

    def test_get_repos(self):
        """Make sure that a valid repo query returns an iter with contents."""

        with test_database(test_db, ()):
            # SUT
            self.user1.save()
            self.user2.save()
            self.repo1.save()
            self.repo2.save()

            repo3 = self.repo2 = Repo(repo_id=123, owner=self.user1,
                                 url='https://github.com/user/repo2.git')

            repo3.save()

            # exercise
            # uses native peewee
            for repo in self.user1.repos:
                self.assertEqual(repo.owner.github_id, self.user1.github_id)
                self.assertTrue(repo.url == self.repo1.url or
                                repo.url == self.repo2.url)

            self.assertTrue(self.user1.repos == 2)

            # clean up
            repo3.delete_instance()

    def test_get_job(self):
        """Make sure that a valid single job query returns the job."""

        with test_database(test_db, ()):
            # SUT
            self.user1.save()
            self.repo1.save()
            job = Jobs(job_id=uuid4(), repo_owner=self.user1, repo=self.repo1,
                       start_time=datetime.now(), comment_number=1,
                       status='pending')
            job.save()

            # Exercise
            self.assertEqual(self.db.get_job(job.job_id), job)

            # Cleanup
            job.delete_instance()

    def test_get_all_jobs(self):
        """Make sure that a valid job search returns all jobs for user."""

        with test_database(test_db, ()):
            # SUT
            self.user1.save()
            self.repo1.save()
            job1 = Jobs(job_id=uuid4(), repo_owner=self.user1, repo=self.repo1,
                        start_time=datetime.now(),status='pending')
            job2 = Jobs(job_id=uuid4(), repo_owner=self.user1, repo=self.repo1,
                        start_time=datetime.now(),status='pending')
            job1.save()
            job2.save()

            # exercise
            self.assertTrue(self.user1.jobs == 2)

            # clean up
            job1.delete_instance()
            job2.delete_instance()

    def test_sucessfully_adds_user(self):
        """Make sure that adding a user works."""

        with test_database(test_db, ()):
            # SUT
            self.assertIsNone(self.db.get_user(1))

            # exercise
            self.user1.save()
            self.assertTrue(
                self.db.get_user(1).get_oauth_token() == 'dummyToken')



if __name__ == '__main__':
    unittest.main()
