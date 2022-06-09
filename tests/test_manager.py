import os
import unittest

from helpers import get_hash
from manager import Manager
from models import User


class TestManager(unittest.TestCase):
    def setUp(self):
        self.test_db_name = 'test_database'
        self.user_manager = Manager(model=User, db_name=self.test_db_name)

    def tearDown(self):
        del self.user_manager

        db = f'{self.test_db_name}.db'
        if os.path.exists(db):
            os.remove(db)

    def test_create(self):
        username = 'test'
        age = 10
        password = '123'
        user = self.user_manager.create(username=username, age=age, password=password)

        self.assertEqual(user.username, username)
        self.assertEqual(user.age, age)
        self.assertEqual(user.password, get_hash(password))

    def test_get(self):
        test_user = self.__create_test_user()
        user = self.user_manager.get(id=1)

        self.assertEqual(user, test_user)

    def test_get_returns_none_if_id_is_not_in_db(self):
        user = self.user_manager.get(id=1)
        self.assertIsNone(user)

    def test_length_of_get_all_is_zero_initially(self):
        users = self.user_manager.get_all()
        self.assertEqual(len(users), 0)

    def test_length_of_get_all_is_one(self):
        user = self.__create_test_user()
        users = self.user_manager.get_all()

        self.assertEqual(len(users), 1)
        self.assertIsInstance(users[0], User)
        self.assertEqual(users[0], user)

    def __create_test_user(self):
        username = 'test'
        age = 10
        password = '123'
        user = self.user_manager.create(username=username, age=age, password=password)
        return user


if __name__ == '__main__':
    unittest.main()
