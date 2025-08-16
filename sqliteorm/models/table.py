class Table():
    def __init__(self, db, name: str):
        self.db = db
        self.table_name = name

        if not db.check_table(name):
            db.create_table(name)

    def check_column(self, column_name):
        return self.db.check_column(self.table_name, column_name)

    def get_dict_list(self, cursor):
        keys = cursor.description
        values = cursor.fetchall()

        if not values:
            return []
        keys = [k[0] for k in keys]

        data = []
        while values:
            data.append(dict(zip(keys, values.pop())))
        return data

    def values(self):
        cursor = self.db.execute(f'SELECT * FROM {self.table_name}')
        return self.get_dict_list(cursor)

    def get_dict(self, cursor):
        keys = cursor.description
        value = cursor.fetchone()

        return dict(zip([k[0] for k in keys], value))

    def value(self):
        cursor = self.db.execute(f'SELECT * FROM {self.table_name}')
        return self.get_dict(cursor)

    def filter(self, **kwargs):
        conditions, condition_formats = Table.get_conditions(list(kwargs.keys()))
        values = [condition_formats[i].format(v) for i, v in enumerate(kwargs.values())]

        cursor = self.db.execute(f'SELECT * FROM {self.table_name} ' +
            f'WHERE {" AND ".join(conditions)}', values)
        return self.get_dict_list(cursor)

    def filter_one(self, **kwargs):
        conditions, condition_formats = Table.get_conditions(list(kwargs.keys()))
        values = [condition_formats[i].format(v) for i, v in enumerate(kwargs.values())]

        cursor = self.db.execute(f'SELECT * FROM {self.table_name} ' +
            f'WHERE {" AND ".join(conditions)}', values)
        return self.get_dict(cursor)

    def insert(self, **kwargs):
        self.db.execute(f'INSERT INTO {self.table_name} (' +
            f'{", ".join(kwargs.keys())}) ' +
            f'VALUES ({('?, ' * len(kwargs))[:-2]})',
                tuple(kwargs.values()))

    def delete(self, **kwargs):
        conditions, condition_formats = Table.get_conditions(list(kwargs.keys()))
        values = [condition_formats[i].format(v) for i, v in enumerate(kwargs.values())]

        self.db.execute(f'DELETE FROM {self.table_name} ' +
            f'WHERE {" AND ".join(conditions)}', values)

    staticmethod
    def get_conditions(data):
        conditions = []
        condition_formats = []
        for key in data:
            if not '__' in key:
                conditions.append(f'{key} = ?')
                condition_formats.append('{}')
            else:
                key, condition = key.split('__')
                match (condition):
                    case 'gt':
                        conditions.append(f'{key} > ?')
                        condition_formats.append('{}')
                    case 'lt':
                        conditions.append(f'{key} < ?')
                        condition_formats.append('{}')
                    case 'gte':
                        conditions.append(f'{key} >= ?')
                        condition_formats.append('{}')
                    case 'lte':
                        conditions.append(f'{key} <= ?')
                        condition_formats.append('{}')
                    case 'startswith':
                        conditions.append(f'{key} LIKE ?')
                        condition_formats.append('{}%')
                    case 'endswith':
                        conditions.append(f'{key} LIKE ?')
                        condition_formats.append('%{}')
                    case 'contains':
                        conditions.append(f'{key} LIKE ?')
                        condition_formats.append('%{}%')
                    case _:
                        raise Exception(f'Unknown condition: {condition}')
                        
        return conditions, condition_formats
