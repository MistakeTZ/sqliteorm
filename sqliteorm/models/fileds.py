from .table import Table

class BaseColumn():
    def __init__(self, name: str, default_value = None, is_null = False, type = 'TEXT'):
        self.name = name
        self.default_value = default_value
        self.is_null = is_null
        self.type = type

    def create_column(self, table):
        if not table.check_column(self.name):
            if self.default_value is not None:
                default_value_text = f' DEFAULT {self.default_value}'
            else:
                default_value_text = ''

            if self.is_null:
                is_null_text = ''
            else:
                is_null_text = ' NOT NULL'
            table.db.execute(f'ALTER TABLE {table.table_name} ADD COLUMN {self.name} {self.type} {default_value_text} {is_null_text}')


class IntegerColumn(BaseColumn):
    def __init__(self, name: str, default_value = None, is_null = False):
        super().__init__(name, default_value, is_null, 'INTEGER')


class IntegerField(BaseColumn):
    def __init__(self, table: Table, name: str, value: int):
        super().__init__(table, name, value)