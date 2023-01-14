import os
import sqlite3
from celestis.model import exceptions

class Model:
    def __init__(self, table_name, path):
        self.table_name = table_name
        self.db_file = os.path.join(path, "db.sqlite3")
    
    def add(self, record):
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()

        c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (self.table_name,))
        result = c.fetchone()

        if result:
            columns = ', '.join(record.keys())
            placeholders = ', '.join('?' for _ in record.values())

            c.execute("INSERT INTO {} ({}) VALUES ({})".format(self.table_name, columns, placeholders), tuple(record.values()))
        else:
            raise exceptions.TableNotFoundError(self.table_name)
        
        conn.commit()
        conn.close()

    def find(self, conditions):
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()

        query = f"SELECT * FROM {self.table_name} WHERE "
        args = []
        for key, value in conditions.items():
            query += f"{key} = ? AND "
            args.append(value)
        query = query[:-4]
        c.execute(query, tuple(args))
        result = c.fetchall()
        conn.close()
        if len(result) > 1:
            fields = [i[0] for i in c.description]
            return [{fields[i]: row[i] for i in range(len(fields))} for row in result]
        elif len(result) == 1:
            fields = [i[0] for i in c.description]
            return {fields[i]: result[0][i] for i in range(len(fields))}
        else:
            return None
    
    def delete(self, record):
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()

        query = f"DELETE FROM {self.table_name} WHERE "
        args = []
        for key, value in record.items():
            query += f"{key} = ? AND "
            args.append(value)
        query = query[:-4]
        c.execute(query, tuple(args))
        conn.commit()
        conn.close()
    
    def update(self, record, **kwargs):
        self.delete(record)

        for key, value in kwargs.items():
            try:
                record[key] = value
            except KeyError:
                self.add(record)
                raise exceptions.FieldNotFoundError(key)
        
        self.add(record)

    