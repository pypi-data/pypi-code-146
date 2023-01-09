"""
    SQL implementation for Python. contains The following classes:
    Create, creates a database if one isn't present;
    Connect, opens database and runs function and arguments passed to it;
    CreateTable, creates a table in a given database;
    add, adds data to a table;
    readAll, (not recommended) returns tuple with all rows within the database;
    columnNames, returns list of columns within a table;
    columnsDistinct, gets distinct values for row in table.
    find, to do
"""

import os
import itertools
# Only to access database
import sqlite3
from sqlite3 import Error
# Only needed for access to command line arguments
import sys


class DatabaseSQLite:
    """
    Class
    """
    def __init__(self, db_loc='', name='database.db'):
        self.defaultDBName = name
        self.defaultTable = "Material"
        self.dbPath = False
        self.Create(path=db_loc, name=name)

    def Existence(self, path=None):
        """
        Checks the existence of sql database at location. Requires OS
        :param path: (str) path to check for sqlite3 databases
        :return: (list(str)) or None if path is invalid
        """
        if path is None:
            path = os.path.dirname(os.path.realpath(__file__))
        if path and os.path.exists(path):
            files = [file for file in os.listdir(path) if file.endswith(".db")]
            valid_sqlite = []
            for i in files:
                with sqlite3.connect(f'file:{os.path.join(path, i)}?mode=rw', uri=True) as con:
                    try:
                        curser = con.cursor()
                        curser.execute("SELECT name FROM sqlite_master WHERE type='table';")
                        valid_sqlite += [i]
                    except sqlite3.DatabaseError:
                        pass
            return valid_sqlite

    def Create(self, path=None, name=None):
        """
        Connects to a database in path, default is active file, named database.db. If
        Database does not exist it will be created
        :param path: (str) database folder's path, must be set according to OS
        :param name: (str) database name
        :return: True if database connection is valid
                 str if database connection Failed
        """
        if name is None:
            name = self.defaultDBName
        if path is None:
            self.dbPath = db.Existence(os.path.dirname(os.path.realpath(__file__)))

        try:
            database = sqlite3.connect(path + name)
            if database:
                database.close()
                self.dbPath = path
                return True
        except Error as e:
            return e

    @staticmethod
    def RunCommand(c, inputs, *args):
        """

        :param c: SQLite curser
        :param inputs: SQL command
        :return: bool, depending if error found
        """

        c.execute(inputs, args)
        try:
            return 1
        except Error as e:
            return e

    def Connect(self, command, *args, save=False, **kwargs):
        """
        Input function, args and kwargs.
        print(db.Connect(db.RunCommand, sql_create_tasks_table))

        :param save:
        :param command: function
        :param args: passed function's arguments
        :param kwargs: passed function's keyword arguments
        :return: passed functions return or Error String

        example:
        Connect(self.RunCommand, SQL_command_string, save=True)
        """
        if isinstance(self.dbPath, str):
            try:
                database = sqlite3.connect(self.dbPath + self.defaultDBName)
                curser = database.cursor()
                rt = True
                if callable(command):
                    command(curser, *args, **kwargs)
                    rt = curser.fetchall()
                    if save:
                        database.commit()
                if database:
                    database.close()
                    return rt

            except Error as e:
                return e

    def CreateTable(self, c, table=None, cols=None, types=None, adds=None):
        """

        Creates and sets up a table.

        :param c: SQLite curser
        :param table: (str) Name for the table
        :param cols: list(str) for name of columns
        :param types: list(str) informs SQL data type for columns
        :param adds: additional parameters

        example:
        print(db.Connect(db.CreateTable, "Material",
                   ["id", 'hyperlink', 'level', 'subject'],
                   ["integer", 'text', 'text', 'text'],
                   ["NOT NULL"]))
        """
        if table is None:
            table = self.defaultTable

        if (isinstance(cols, list)) & \
                (isinstance(types, list)) & \
                (isinstance(adds, list)):
            command_string = f'CREATE TABLE IF NOT EXISTS {table}(\n'
            for name, typ, add in list(itertools.zip_longest(cols, types, adds, fillvalue="")):
                command_string += f'{name} {typ} {add},\n'
            command_string = command_string[:-2] + ");"

            return self.RunCommand(c, command_string)

        else:
            return False

    def add(self, table=None, data=None):
        """
        Adds a row of data to database. All data must be in a dictionary
        :param table: (str) name of table
        :param data: (dict) dictionary with column_name : value
        :return: bool or error string

        example:
        db.add("Material", {"id": 2,
                              "hyperlink": "www.google.com",
                              "level": "C2",
                              "subject": "simple Present"})
        """
        if table is None:
            table = self.defaultTable

        if data:
            part1 = f"INSERT INTO {table}("
            part2 = f"VALUES("
            for col, val in zip(data.keys(), data.values()):
                part1 += f"'{col}', "
                part2 += f"'{val}', "

            command_string = part1[:-2] + ") " + part2[:-2] + ");"
            return self.Connect(self.RunCommand, command_string, save=True)

    def readAll(self, table=None, limit=None, offset=None):
        """

        :param table: (str) table name
        :param limit: (int) limits the number of results
        :param offset: (int) offsets the position sql starts listing
        :return: tuple of row in table

        example:
        db.readAll("Material")
        """
        if table is None:
            table = self.defaultTable

        cmd = f"SELECT * FROM {table}"

        if limit:
            cmd += f" LIMIT {limit}"
        if offset:
            cmd += f" OFFSET {offset}"
        return self.Connect(self.RunCommand, cmd)

    def columnNames(self, table=None):
        """
        Gets the name for each column in table
        :param table: (str) table name
        :return: list(str)

        example:
        print(db.columnNames())
        """
        if table is None:
            table = self.defaultTable
        a = self.Connect(self.RunCommand, f"select name from pragma_table_info('{table}')")
        return list(map(lambda x: x[0], a))

    def columnsDistinct(self, col="", table=None):
        """

        :param col: (str) column name
        :param table: (str) table name
        :return: tuple of (str)

        example:
        db.columnsDistinct("Material", "id")
        """
        if table is None:
            table = self.defaultTable

        result = self.Connect(self.RunCommand, f"SELECT DISTINCT  {col} FROM {table}")
        return [item for sublist in result for item in sublist]

    def find(self, values=None, table=None, selection='*', operation='AND', limit=None, offset=None, count=False):
        """
        Find rows with multiple values and or columns

        :param values: Dict{column: list(Values)}
        :param table: (str) table in SQL database
        :param operation: (str) SQL operation (AND, OR, ...) for columns
        :param selection: (str) SQL select statement
        :param limit: (int) limits the number of results
        :param offset: (int) offsets the position sql starts listing
        :param count: (bool) set command to count row count according to other inputs

        Example:
        db.find(values={'Column_1': [1, 2, 3], 'Column_2': ["C2"]})
        SQLite command:
        SELECT * FROM TABLE_NAME WHERE Column_1 IN (?, ?, ?) AND Column_2 IN (?)
        """
        if table is None:
            table = self.defaultTable
        if values is None:
            values = {}

        if isinstance(values, dict):
            condition = ''
            for keys in values.keys():
                val = ', '.join("?" for _ in values[keys])
                condition += f"{keys} IN ({val}) {operation} "
            query = f'SELECT {f"COUNT ({selection})" if count else f"{selection}"} FROM {table} ' \
                    f'{"WHERE" if values else ""} %s' % condition[:-4]

            if limit:
                query += f"LIMIT {limit}"
            if offset and not count:
                query += f" OFFSET {offset}"

            result = self.Connect(self.RunCommand, query,
                                  *[item for sublist in list(values.values()) for item in sublist])

            return result[0] if count else result
