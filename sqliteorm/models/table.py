class Table():
    def __init__(self, db, name: str):
        self.db = db
        self.table_name = name

        if not db.check_table(name):
            db.create_table(name)

    def check_column(self, column_name):
        return self.db.check_column(self.table_name, column_name)

    def values(self):
        return self.db.execute(f'SELECT * FROM {self.table_name}').fetchall()

    def insert(self, **kwargs):
        self.db.execute(f'INSERT INTO {self.table_name} (' +
            f'{", ".join(kwargs.keys())})' +
            f'VALUES ({('?, ' * len(kwargs))[:-2]})',
                tuple(kwargs.values()))
