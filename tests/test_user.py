import os
import unittest

from db_handler import DatabaseHandler
from helpers import get_hash
from manager import Manager
from models import User


class TestUser(unittest.TestCase):
    def setUp(self):
        self.test_db_name = 'test_database'
        self.db_handler = DatabaseHandler(db_name=self.test_db_name)
        self.user_manager = Manager(model=User, db_name=self.test_db_name)

        self.username = 'test'
        self.age = 10
        self.password = '123'
        self.user_manager.create(username=self.username, age=self.age, password=self.password)
        self.user = self.user_manager.get_all()[0]
        self.user.manager = self.user_manager

    def tearDown(self):
        del self.db_handler
        del self.user
        del self.user_manager

        db = f'{self.test_db_name}.db'
        if os.path.exists(db):
            os.remove(db)

    def test_user_update(self):
        age = 20
        password = '1234'
        self.user.update(age=age, password=password)

        self.assertEqual(self.user.age, age)
        self.assertEqual(self.user.password, get_hash(password))

    def test_user_delete(self):
        self.user.delete()

        self.assertEqual(self.user.username, None)
        self.assertEqual(self.user.age, None)
        self.assertEqual(self.user.password, None)

    def test_get_attribute_dict(self):
        self.assertDictEqual(self.user.get_attribute_dict(), {'username': self.username,
                                                              'age': self.age,
                                                              'password': get_hash(self.password)})


if __name__ == '__main__':
    unittest.main()
