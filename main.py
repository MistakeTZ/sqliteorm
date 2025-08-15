from sqliteorm import sqliteorm
from sqliteorm.models.table import Table
from sqliteorm.models.fileds import IntegerColumn, BaseColumn
import logging


logging.basicConfig(level=logging.DEBUG)

class Users(Table):
    name = BaseColumn('name')
    age = IntegerColumn('age', is_null=True)


db = sqliteorm.SQLiteORM('test.sqlite3')
users = Users(db, 'users')

db.add_table(users)
db.migrate()

# users.insert(name='John', age=20)
print(users.values())
print(users.value())