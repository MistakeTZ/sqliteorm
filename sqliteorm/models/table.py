class Table():
    def __init__(self, db, name: str):
        self.db = db
        self.table_name = name

        if not db.check_table(name):
            db.create_table(name)

    def check_column(self, column_name):
        return self.db.check_column(self.table_name, column_name)

    def values(self):
        cursor = self.db.execute(f'SELECT * FROM {self.table_name}')
        keys = cursor.description
        values = cursor.fetchall()

        if not values:
            return []
        keys = [k[0] for k in keys]

        data = []
        while values:
            data.append(dict(zip(keys, values.pop())))
        return data

    def value(self):
        cursor = self.db.execute(f'SELECT * FROM {self.table_name}')
        keys = cursor.description
        value = cursor.fetchone()

        return dict(zip([k[0] for k in keys], value))

    def insert(self, **kwargs):
        self.db.execute(f'INSERT INTO {self.table_name} (' +
            f'{", ".join(kwargs.keys())}) ' +
            f'VALUES ({('?, ' * len(kwargs))[:-2]})',
                tuple(kwargs.values()))
