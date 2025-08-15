from sqliteorm import sqliteorm
from sqliteorm.models.table import Table
from sqliteorm.models.fileds import IntegerColumn, BaseColumn

class Users(Table):
    name = BaseColumn('name')
    age = IntegerColumn('age', is_null=True)


db = sqliteorm.SQLiteORM('test.sqlite3')
db.add_table(Users(db, 'users'))

db.migrate()