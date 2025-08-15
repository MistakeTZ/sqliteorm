from os import path
from sqlite3 import Connection
from .models.fileds import BaseColumn


class SQLiteORM():
    tables = []

    def __init__(self, db_name):
        self.db_name = db_name
        if not path.exists(db_name):
            self.execute('SELECT 1')

    def check_table(self, table_name):
        return table_name in self.execute('SELECT name FROM sqlite_master WHERE type="table"').fetchall()

    def create_table(self, table_name):
        self.execute(f'CREATE TABLE IF NOT EXISTS {table_name} (id INTEGER PRIMARY KEY AUTOINCREMENT)')

    def check_column(self, table_name, column_name):
        return column_name in self.execute(f'PRAGMA table_info({table_name})').fetchall()

    def execute(self, query):
        with Connection(self.db_name) as connection:
            return connection.cursor().execute(query)

    def add_table(self, table):
        self.tables.append(table)

    def migrate(self):
        for table in self.tables:
            columns = {
                name: column 
                for name, column in vars(type(table)).items()  # Получаем атрибуты класса (не экземпляра)
                if isinstance(column, BaseColumn)  # Проверяем, что это экземпляр BaseColumn
            }
            for column in columns:
                exec("table." + column + ".create_column(table)")