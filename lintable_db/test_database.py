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

import datetime
import logging
import unittest

from peewee import SqliteDatabase
from playhouse.test_utils import test_database

from lintable_db.database import DatabaseHandler, User, Repo, Jobs
from lintable_settings.settings import LINTWEB_SETTINGS

# create and initialize a local test database in memory
test_db = SqliteDatabase(':memory:')

# just put the log messages into a file
logging.basicConfig(filename='./db_tests.log', level=logging.DEBUG)

class dbTests(unittest.TestCase):
    def setUp(self):
        # Override our default encryption key.
        LINTWEB_SETTINGS['simple-crypt']['ENCRYPTION_KEY'] = "donotusethis"

        self.db = DatabaseHandler()
        User._meta.database = test_db
        Jobs._meta.database = test_db
        Repo._meta.database = test_db
        for i in [User, Jobs, Repo]:
            if not i.table_exists():
                test_db.create_table(i)

    def test_shouldHaveUser(self):
        with test_database(test_db, ()):
            self.assertIsNotNone(User())

    def test_shouldHaveJob(self):
        with test_database(test_db, ()):
            self.assertIsNotNone(Jobs())

    def test_shouldHaveRepo(self):
        with test_database(test_db, ()):
            self.assertIsNotNone(Repo())

    def test_returns_none_for_missing_user(self):
        with test_database(test_db, ()):
            self.assertIsNone(self.db.get_user(''))

    def test_find_user_by_id(self):
        with test_database(test_db, ()):
            # SUT
            user = User(github_id=2, token='dummyToken')
            user.save()

            # exercise
            person = self.db.get_user(2)
            twin = self.db.get_user(person.github_id)

            self.assertEqual(self.assertEqual(person, user),
                             self.assertEqual(user, twin))

            # clean up
            person.delete_instance()
            self.assertIsNone(self.db.get_user(2))
            self.assertEqual(person.id, twin.id)
            user.delete_instance()
            twin.delete_instance()

    def test_get_missing_repo(self):
        with test_database(test_db, ()):
            # SUT
            user = User(github_id=2, token='a')
            user.save()

            for repo in user.repos:
                self.assertTrue(False)

            user.delete_instance()

    def test_get_repos(self):
        with test_database(test_db, ()):
            # SUT
            user = User(github_id=2, token='a')
            user.save()
            repo1 = Repo(repo_id=1, owner=user,
                         url='https://github.com/user/repo.git')
            repo2 = Repo(repo_id=2, owner=user,
                         url='https://github.com/user/repo2.git')
            repo1.save()
            repo2.save()
            user2 = User(github_id=1, token='a')
            repo3 = repo2 = Repo(repo_id=123, owner=user,
                                 url='https://github.com/user/repo2.git')
            user2.save()
            repo3.save()

            # exercise
            # check native peewee
            for repo in user.repos:
                self.assertEqual(repo.owner.id, user.id)
                self.assertTrue(repo.url == repo1.url or
                                repo.url == repo2.url)

            self.assertTrue(user.repos == 2)

            # clean up
            user.delete_instance()
            user2.delete_instance()
            repo1.delete_instance()
            repo2.delete_instance()
            repo3.delete_instance()

    def test_get_job(self):
        with test_database(test_db, ()):
            user = User(github_id=1, token='a')
            user.save()

            repo = Repo(repo_id=23, owner=user,
                        url='https://github.com/user/job.git')
            repo.save()

            job = Jobs(job_id=1, repo_owner=user, repo=repo,
                       start_time=datetime.datetime.now(), comment_number=1,
                       status='pending')
            job.save()

            self.assertEqual(self.db.get_job(job.job_id), job)

            user.delete_instance()
            repo.delete_instance()
            job.delete_instance()

    def test_get_all_jobs(self):
        with test_database(test_db, ()):
            # SUT
            user = User(github_id=1, token='a')
            user.save()
            repo = Repo(repo_id=24, owner=user,
                        url='https://github.com/user/job.git')
            repo.save()

            job1 = Jobs(job_id=1,repo_owner=user, repo=repo,
                        start_time=datetime.datetime.now(),
                        comment_number=1, status='pending')
            job2 = Jobs(job_id=2,repo_owner=user, repo=repo,
                        start_time=datetime.datetime.now(),
                        comment_number=2, status='pending')
            job1.save()
            job2.save()

            # exercise
            for job in user.jobs:
                self.assertEqual(job.repo_owner.github_id, user.github_id)
                self.assertTrue(job.comment_number == job1.comment_number or
                                job.comment_number == job2.comment_number)

            self.assertTrue(user.jobs == 2)

            # clean up
            user.delete_instance()
            job1.delete_instance()
            job2.delete_instance()
            repo.delete_instance()

    def test_sucessfully_adds_user(self):
        with test_database(test_db, ()):
            # SUT
            self.assertIsNone(self.db.get_user(1))

            # exercise
            person = User(token='dummyToken', github_id=1)
            person.save()
            self.assertTrue(
                self.db.get_user(1).get_oauth_token() == 'dummyToken')

            # cleanup
            person.delete_instance()


if __name__ == '__main__':
    unittest.main()
