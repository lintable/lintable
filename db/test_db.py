import unittest
import db
import logging
from peewee import *
from playhouse.test_utils import test_database

# create and initialize a local test database in memory
test_db = SqliteDatabase(':memory:')

# just put the log messages into a file
logging.basicConfig(filename='./db_tests.log', level=logging.DEBUG)


class dbTests(unittest.TestCase):
    def setUp(self):
        db.User._meta.database = test_db
        db.Jobs._meta.database = test_db
        db.Repo._meta.database = test_db
        for i in [db.User, db.Jobs, db.Repo]:
            if not i.table_exists():
                test_db.create_table(i)

    def test_shouldHaveUser(self):
        with test_database(test_db, (db.User)):
            self.assertIsNotNone(db.User())

    def test_shouldHaveJob(self):
        with test_database(test_db, (db.User)):
            self.assertIsNotNone(db.Jobs())

    def test_shouldHaveRepo(self):
        with test_database(test_db, (db.User)):
            self.assertIsNotNone(db.Repo())

    def test_returns_none_for_missing_user(self):
        with test_database(test_db, (db.User)):
            self.assertIsNone(db.get_user(''))

    def test_sucessfully_adds_user(self):
        with test_database(test_db, (db.User)):
            self.assertIsNone(db.get_user('new_user'))

            # exercise
            person = db.User(username='new_user', token='dummyToken')
            person.save()
            self.assertTrue(db.get_user('new_user').token == 'dummyToken')

            # cleanup
            self.assertTrue(person.delete_instance() == 1)

    def test_unique_id_generated(self):
        with test_database(test_db, (db.User)):
            # SUT
            self.assertIsNotNone('user_1')
            self.assertIsNotNone('user_2')
            user_1 = db.User(username='user_1', token='dummyToken')
            user_2 = db.User(username='user_2', token='dummyToken2')
            user_2.save()
            user_1.save()

            # exercise
            self.assertNotEqual(db.get_user('user_1').id,
                                db.get_user('user_2').id)

            # cleanup
            self.assertTrue(
                user_1.delete_instance() == user_2.delete_instance() == 1)


if __name__ == '__main__':
    unittest.main()
