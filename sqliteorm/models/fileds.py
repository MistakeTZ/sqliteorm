from .table import Table

class BaseColumn():
    def __init__(self, name: str, default_value = None, is_null = False, type = 'UNKNOWN'):
        self.name = name
        self.default_value = default_value
        self.is_null = is_null
        self.type = type

    def get_default(self):
        return self.default_value
    
    def params(self):
        attribute_list = []
        if self.default_value is not None:
            attribute_list.append(f'DEFAULT {self.get_default()}')
            

        if not self.is_null:
            attribute_list.append('NOT NULL')

        return ' '.join(attribute_list)

    def create_column(self, table):
        if not table.check_column(self.name):
            params = self.params()
            table.db.execute(f'ALTER TABLE {table.table_name} ADD COLUMN {self.name} {self.type} {params}')


class IntegerColumn(BaseColumn):
    def __init__(self, name: str, default_value = None, is_null = False):
        super().__init__(name, default_value, is_null, 'INTEGER')

class BooleanColumn(BaseColumn):
    def __init__(self, name: str, default_value = None, is_null = False):
        super().__init__(name, default_value, is_null, 'BOOLEAN')

class TextColumn(BaseColumn):
    def __init__(self, name: str, default_value = None, is_null = False):
        super().__init__(name, default_value, is_null, 'TEXT')

    def get_default(self):
        return f"'{self.default_value}'"

class DateTimeColumn(BaseColumn):
    def __init__(self, name: str, default_value = None, is_null = False):
        super().__init__(name, default_value, is_null, 'DATETIME')