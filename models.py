import manager
from helpers import get_hash


class User:
    FIELDS = ['username', 'age', 'password', 'id']

    def __init__(self, username, age, password, id=None) -> None:
        self.username = username
        self.age = age
        self.password = password
        self.id = id

    def update(self, age=None, password=None):
        if self.id is None:
            print("Can't update a user whose id=None")
            return

        if age is not None:
            self.age = age

        if password is not None:
            self.password = get_hash(password)

        instance = self.manager.get(id=self.id)
        if instance is not None:
            self.manager.db_handler.update(self)

    def delete(self):
        if self.id is None:
            print("Can't delete a user whose id=None")
            return

        instance = self.manager.get(id=self.id)
        if instance is not None:
            self.manager.db_handler.delete(self.id)
            self.username = None
            self.age = None
            self.password = None

    def get_attribute_dict(self):
        return {'username': self.username, 'age': self.age, 'password': self.password}

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, self.__class__):
            return self.username == __o.username and self.age == __o.age and self.password == __o.password

        elif isinstance(__o, tuple):
            return self.username == __o[0] and self.age == __o[1] and self.password == __o[2]

    def __repr__(self):
        if self.id is not None:
            return f'Id: {self.id:<15} Username: {self.username:<15}  Age: {self.age:<15}'
        return f'Username: {self.username:<15}  Age: {self.age:<15}'


setattr(User, 'manager', manager.Manager(User))
