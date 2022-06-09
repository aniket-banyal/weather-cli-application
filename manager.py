import sqlite3

import db_handler
from helpers import get_hash


class Manager:
    db_handler = None

    def __init__(self, model, db_name='database') -> None:
        self.model = model
        self.model_name = f'{model.__name__}s'
        self.db_handler = db_handler.DatabaseHandler(db_name)

    def create(self, *args, **kwargs):
        instance = self.model(*args, **kwargs)
        instance.password = get_hash(instance.password)

        try:
            self.db_handler.create(instance)
        except sqlite3.IntegrityError:
            return None

        return instance

    def get(self, id):
        fields = self.model.FIELDS
        instances = self.db_handler.get(id, fields)
        if len(instances) < 1:
            return None
        return self.__get_model_instance(instances[0])

    def get_all(self):
        fields = self.model.FIELDS
        data = self.db_handler.get_all(fields=fields)
        return [self.__get_model_instance(user_data) for user_data in data]

    def __get_model_instance(self, data):
        return self.model(*data)
