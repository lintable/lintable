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

# This is needed to set env vars before execution, needs to be first import
from db.local_test_settings import *
import unittest
import logging
from db.database import database_handler
from db.models import User, Repo, Jobs
from peewee import *
from playhouse.test_utils import test_database
import datetime


# create and initialize a local test database in memory
test_db = SqliteDatabase(':memory:')

# just put the log messages into a file
logging.basicConfig(filename='./db_tests.log', level=logging.DEBUG)


class dbTests(unittest.TestCase):
    def setUp(self):
        self.db = database_handler()
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
            user = User(username='this', github_id='that', token='dummyToken')
            user.save()

            # exercise
            person = self.db.get_user('that')
            twin = self.db.get_user(person.id)

            self.assertEqual(self.assertEqual(person, user),
                             self.assertEqual(user, twin))

            # clean up
            user.delete_instance()
            self.assertIsNone(self.db.get_user('that'))
            self.assertEqual(person.id, twin.id)

    def test_get_missing_repo(self):
        with test_database(test_db, ()):
            # SUT
            user = User(username='that', github_id='doeasaurausrex', token='a')
            user.save()

            for repo in user.repos:
                self.assertTrue(False)

            user.delete_instance()

    def test_get_repos(self):
        with test_database(test_db, ()):
            # SUT
            user = User(username='that', github_id='dopeasaurusrex', token='a')
            user.save()
            repo1 = Repo(owner=user, url='https://github.com/user/repo.git')
            repo2 = Repo(owner=user, url='https://github.com/user/repo2.git')
            repo1.save()
            repo2.save()
            user2 = User(username='that2', github_id='dopeasaurusrex', token='a')
            repo3 = repo2 = Repo(owner=user, url='https://github.com/user/repo2.git')
            user2.save()
            repo3.save()


            # exercise
            # check native peewee
            for repo in user.repos:
                self.assertEqual(repo.owner.id, user.id)
                self.assertTrue(repo.url == repo1.url or
                                repo.url == repo2.url)
            # check db_handler function
            for repo in self.db.get_repos_for_user(user.id):
                self.assertEqual(repo.owner.id, user.id)
                self.assertTrue(repo.url == repo1.url or
                                repo.url == repo2.url)

            self.assertTrue(user.repos == 2)
            self.assertTrue(self.db.get_repos_for_user(user.id) == 2)

            #clean up
            user.delete_instance()
            repo1.delete_instance()
            repo2.delete_instance()

    def test_get_job(self):
        with test_database(test_db, ()):
            user = User(username='that', github_id='dopeasaurusrex', token='a')
            user.save()

            repo = Repo(owner=user, url='https://github.com/user/job.git')
            repo.save()

            job = Jobs(repo_owner=user, url=repo,start_time=datetime.datetime.now(),comment_number=1, status = 'pending')
            job.save()

            self.assertEqual(self.db.get_job(job.job_id), job)

    def test_get_all_jobs(self):
        with test_database(test_db, ()):
            # SUT
            user = User(username='that', github_id='dopeasaurusrex', token='a')
            user.save()
            repo = Repo(owner=user, url='https://github.com/user/job.git')
            repo.save()

            job1 = Jobs(repo_owner=user, url=repo,start_time=datetime.datetime.now(),comment_number=1, status = 'pending')
            job2 = Jobs(repo_owner=user, url=repo,start_time=datetime.datetime.now(),comment_number=2, status = 'pending')
            job1.save()
            job2.save()

            # exercise
            # check native peewee
            for job in user.jobs:
                self.assertEqual(job.repo_owner.id, user.id)
                self.assertTrue(job.comment_number == job1.comment_number or
                                job.comment_number == job2.comment_number)
            # check db_handler function
            for job in self.db.get_jobs_for_user(user.id):
                self.assertEqual(job.repo_owner.id, user.id)
                self.assertTrue(job.comment_number == job1.comment_number or
                                job.comment_number == job2.comment_number)

            self.assertTrue(user.jobs == 2)
            self.assertTrue(self.db.get_jobs_for_user(user.id) == 2)

            #clean up
            user.delete_instance()
            job1.delete_instance()
            job2.delete_instance()


    def test_sucessfully_adds_user(self):
        with test_database(test_db, ()):
            # SUT
            self.assertIsNone(self.db.get_user('badId'))

            # exercise
            person = User(username='new_user', token='dummyToken',
                          github_id='badId')
            person.save()
            self.assertTrue(
                self.db.get_user('badId').get_oauth_token() == 'dummyToken')

            # cleanup
            self.assertTrue(person.delete_instance() == 1)

    def test_unique_id_generated(self):
        with test_database(test_db, ()):
            # SUT
            self.assertIsNotNone('user_1')
            self.assertIsNotNone('user_2')
            user_1 = User(username='user_1', token='dummyToken',
                          github_id='badId')
            user_2 = User(username='user_2', token='dummyToken2',
                          github_id='badId2')
            user_2.save()
            user_1.save()

            # exercise
            self.assertNotEqual(self.db.get_user('badId').id,
                                self.db.get_user('badId2').id)

            # cleanup
            self.assertTrue(
                user_1.delete_instance() == user_2.delete_instance() == 1)


if __name__ == '__main__':
    unittest.main()
