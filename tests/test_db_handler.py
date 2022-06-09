import os
import sqlite3
import unittest

from db_handler import DatabaseHandler
from helpers import get_hash
from manager import Manager
from models import User


class TestDatabaseHandler(unittest.TestCase):
    def setUp(self):
        self.test_db_name = 'test_database'
        self.db_handler = DatabaseHandler(db_name=self.test_db_name)
        self.user_manager = Manager(model=User, db_name=self.test_db_name)

    def tearDown(self):
        del self.db_handler
        del self.user_manager

        db = f'{self.test_db_name}.db'
        if os.path.exists(db):
            os.remove(db)

    def test_create_raises_error_for_duplicate_username(self):
        username = 'test'
        age = 10
        password = '123'
        user = User(username=username, age=age, password=password)

        self.db_handler.create(user)
        self.assertRaises(sqlite3.IntegrityError, lambda: self.db_handler.create(user))

    def test_length_of_get_is_zero_initially(self):
        self.assertEqual(len(self.db_handler.get(1, User.FIELDS)), 0)

    def test_get(self):
        test_user = self.__create_test_user()
        user = self.db_handler.get(id=1, fields=User.FIELDS)[0]
        self.assertEqual(user, test_user)

    def test_length_of_get_all_is_zero_initially(self):
        user = self.db_handler.get_all(fields=User.FIELDS)
        self.assertEqual(len(user), 0)

    def test_get_all(self):
        test_user = self.__create_test_user()
        user = self.db_handler.get_all(fields=User.FIELDS)[0]
        self.assertEqual(user, test_user)

    def test_update(self):
        test_user = self.__create_test_user()
        test_user_data = self.db_handler.get(id=1, fields=User.FIELDS)[0]

        age = 20
        password = '1234'
        test_user.age = age
        test_user.password = get_hash(password)

        self.db_handler.update(test_user)
        updated_data = self.db_handler.get(id=1, fields=User.FIELDS)[0]

        self.assertEqual(test_user_data[0], updated_data[0])
        self.assertEqual(test_user_data[1], updated_data[1])
        self.assertEqual(test_user_data[2], updated_data[2])

    def test_delete(self):
        self.__create_test_user()
        self.db_handler.delete(id=1)
        users = self.db_handler.get(id=1, fields=User.FIELDS)

        self.assertEqual(len(users), 0)

    def __create_test_user(self):
        username = 'test'
        age = 10
        password = '123'
        user = self.user_manager.create(username=username, age=age, password=password)
        return user


if __name__ == '__main__':
    unittest.main()
