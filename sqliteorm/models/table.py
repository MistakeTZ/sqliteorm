from ..enums.filters import *
from ..filters import Q


class Table():
    def __init__(self, db, name: str):
        self.db = db
        self.table_name = name
        self.filters = []
        self.params = []

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

    def get_dict(self, cursor):
        keys = cursor.description
        value = cursor.fetchone()
        if not value:
            return {}

        return dict(zip([k[0] for k in keys], value))

    def all(self, **kwargs):
        conditions = self.get_conditions()
        print(conditions, self.params)

        cursor = self.db.execute(f'SELECT * FROM {self.table_name} ' + conditions, self.params)
        return self.get_dict_list(cursor)

    def one(self, **kwargs):
        conditions = self.get_conditions()

        cursor = self.db.execute(f'SELECT * FROM {self.table_name} ' + conditions, self.params)
        return self.get_dict(cursor)

    def insert(self, **kwargs):
        self.db.execute(f'INSERT INTO {self.table_name} (' +
            f'{", ".join(kwargs.keys())}) ' +
            f'VALUES ({('?, ' * len(kwargs))[:-2]})',
                tuple(kwargs.values()))

    def delete(self, **kwargs):
        conditions = self.get_conditions()

        self.db.execute(f'DELETE FROM {self.table_name} ' + conditions, self.params)

    def filter(self, *args, **kwargs):
        new_table = Table(self.db, self.table_name)
        new_table.filters = self.filters[:]

        for expr, value in kwargs.items():
            if "__" in expr:
                field, lookup = expr.split("__", 1)
            else:
                field, lookup = expr, "exact"

            op = LOOKUPS.get(lookup)
            if not op:
                raise ValueError(f"Unknown lookup: {lookup}")

            if lookup == "contains":
                value = f"%{value}%"
            elif lookup == "startswith":
                value = f"{value}%"
            elif lookup == "endswith":
                value = f"%{value}"
            elif lookup == "icontains":
                value = f"%{value.lower()}%"
                expr_sql = f"LOWER({field}) {op} ?"
                new_table.filters.append((expr_sql, value))
                continue

            expr_sql = f"{field} {op} ?"
            new_table.filters.append((expr_sql, value))

        for q in args:
            if not isinstance(q, Q):
                raise ValueError("filter() args must be Q objects")
            for sql, params in q.children:
                new_table.filters.append((sql, *params))

        return new_table

    def get_conditions(self):
        if self.filters:
            where_clauses = [f[0] for f in self.filters]
            
            self.params = []
            for filter in self.filters:
                self.params.extend(filter[1:])
            
            return " WHERE " + " AND ".join(where_clauses)
        return ""
