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
import simplecrypt

# create and initialize a local test database in memory
test_db = SqliteDatabase(':memory:')

# just put the log messages into a file
logging.basicConfig(filename='./model_tests.log', level=logging.DEBUG)


class ModelTests(unittest.TestCase):
    def setUp(self):
        self.db = database_handler()
        User._meta.database = test_db
        Jobs._meta.database = test_db
        Repo._meta.database = test_db
        for i in [User, Jobs, Repo]:
            if not i.table_exists():
                test_db.create_table(i)

    def test_encrypts_token(self):
        with test_database(test_db, ()):
            # SUT
            self.assertIsNone(self.db.get_user('new_user'))
            new_user = User(username='new_user', token='dummyToken',
                            github_id='badId')

            # Exercise
            new_user.save()
            self.assertNotEqual(new_user.token, 'dummyToken')
            user = self.db.get_user('badId')
            self.assertNotEqual(user.token, 'dummyToken')

            # Clean up
            user.delete_instance()

    def test_encrypts_token_only_once(self):
        with test_database(test_db, ()):
            # SUT
            self.assertIsNone(self.db.get_user('badId'))
            new_user = User(username='new_user', token='dummyToken',
                            github_id='badId')
            new_user.save()

            # Exercise
            user = self.db.get_user('badId')
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
            self.assertIsNone(self.db.get_user('badId'))
            new_user = User(username='new_user', token='dummyToken',
                            github_id='badId')
            new_user.save()

            # Exercise
            user = self.db.get_user('badId')
            self.assertEqual(user.get_oauth_token(), 'dummyToken')
            self.assertNotEqual(user.token, 'dummyToken')

            # Clean up
            user.delete_instance()


    def test_get_token_from_repo(self):
        # SUT
        user = User(username='this', github_id='that', token='dummyToken')
        user.save()
        repo = Repo(owner=user, url='a')
        repo.save()
        self.assertEqual(user.get_oauth_token(), repo.get_oauth_token())


if __name__ == '__main__':
    unittest.main()
