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

import unittest

from db.database import database_handler
from db.models import User,Repo,Jobs
import logging
from peewee import *
from playhouse.test_utils import test_database

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
        with test_database(test_db, (User)):
            self.assertIsNotNone(User())

    def test_shouldHaveJob(self):
        with test_database(test_db, (User)):
            self.assertIsNotNone(Jobs())

    def test_shouldHaveRepo(self):
        with test_database(test_db, (User)):
            self.assertIsNotNone(Repo())

    def test_returns_none_for_missing_user(self):
        with test_database(test_db, (User)):
            self.assertIsNone(self.db.get_user(''))

    def test_sucessfully_adds_user(self):
        with test_database(test_db, ()):
            self.assertIsNone(self.db.get_user('new_user'))

            # exercise
            person = User(username='new_user', token='dummyToken', github_id='badId')
            person.save()
            self.assertTrue(self.db.get_user('new_user').token == 'dummyToken')

            # cleanup
            self.assertTrue(person.delete_instance() == 1)

    def test_unique_id_generated(self):
        with test_database(test_db, ()):
            # SUT
            self.assertIsNotNone('user_1')
            self.assertIsNotNone('user_2')
            user_1 = User(username='user_1', token='dummyToken',github_id='badId')
            user_2 = User(username='user_2', token='dummyToken2',github_id='badId2')
            user_2.save()
            user_1.save()

            # exercise
            self.assertNotEqual(self.db.get_user('user_1').id,
                                self.db.get_user('user_2').id)

            # cleanup
            self.assertTrue(
                user_1.delete_instance() == user_2.delete_instance() == 1)


if __name__ == '__main__':
    unittest.main()
