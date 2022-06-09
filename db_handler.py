import sqlite3


class DatabaseHandler:
    def __init__(self, db_name) -> None:
        self._db_path = db_name
        self.con = sqlite3.connect(f'{db_name}.db')
        self.cur = self.con.cursor()
        self.table_name = 'users'
        self.__create_table()

    def __create_table(self):
        self.cur.execute(f'''
                        CREATE TABLE IF NOT EXISTS {self.table_name} (id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT,
                        age INTEGER,
                        password TEXT,
                        UNIQUE(username))
                        ''')

    def create(self, instance):
        attributes = instance.get_attribute_dict()
        fields = tuple(attributes.keys())
        values = tuple(attributes.values())

        self.cur.execute(f'INSERT INTO {self.table_name} {fields} VALUES {values}')
        self.con.commit()

    def get(self, id, fields):
        fields = ', '.join(fields)
        self.cur.execute(f'SELECT {fields} from {self.table_name} WHERE id=:id', {'id': id})
        return self.cur.fetchall()

    def get_all(self, fields):
        fields = ', '.join(fields)
        self.cur.execute(f'SELECT {fields} from {self.table_name}')
        return self.cur.fetchall()

    def update(self, instance):
        attributes = instance.get_attribute_dict()
        fields = ', '.join([f"{key}='{value}'" for key, value in attributes.items()])

        self.cur.execute(f'UPDATE {self.table_name} SET {fields} WHERE id=:id', {'id': instance.id})
        self.con.commit()

    def delete(self, id):
        self.cur.execute(f'DELETE from {self.table_name} WHERE id=:id', {'id': id})
        self.con.commit()

    def __del__(self):
        self.con.close()
