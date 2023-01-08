import os
import json
from json import dumps # used later on (load)
import string # outline
from tabulate import tabulate

from config import * # add .
from exceptions import * # add .
# import text for easier text output changes

class Database:
    def __init__(self) -> None:
        """
        Select the save method for the "Database", currently only json file is an option to save
        more databases will be added later
        txt will be the next method added
        """

    class normal: # normal version | the version you should use if you have already experience with databases like mysql, mariadb, sqlite, etc
        def __init__(self, save_method="json", db_path=db_folder_normal) -> None:
            self.path = db_path
            self.basedir = basedir
            self.save_method = save_method
            self.json_indent = 4

            if self.save_method == "json":
                if not os.path.exists(self.path):
                    os.makedirs(self.path) # creates path for databases 

        def filter_input(self, string: str):
            def filter(letter):
                list = ["!", "#", "$", "%", "&", "'", "(", ")", "*", "+", ",", "-", ".", "/", ":", ";", "<", "=", ">", "?", "@", "[ ", "\ ", "]", "^", "`", "{", "|", "}", "~"]
                if letter in list:
                    return False
                else:
                    return True
                
            final_string = ""
            final_bool = False
            for letter in string:
                response = filter(letter)
                if response:
                    final_string = final_string + letter
                else:
                    final_bool = True

            return final_string, final_bool


        def is_path_safe(self, basedir: str, path: str, follow_symlinks=True):
            # resolves symbolic links
            if follow_symlinks:
                matchpath = os.path.realpath(path)
            else:
                matchpath = os.path.abspath(path)
            return basedir == os.path.commonpath((basedir, matchpath))


        def read_db(self, database: str) -> dict:
            if self.save_method == "json":
                path = f"{self.path}{database}.json"
                if self.is_path_safe(basedir, path):
                    try:
                        with open(path, "r") as json_file:
                            data = json.load(json_file)
                            return data
                    except:
                        raise InvalidDatabase
                else:
                    raise NotSavePath(path)


        def overwrite_db(self, database: str, data: dict) -> None:
            if self.save_method == "json":
                path = f"{self.path}{database}.json"
                if self.is_path_safe(basedir, path):
                    try:
                        with open(path, "w") as json_file:
                            json_file.write(dumps(data, indent=self.json_indent))
                            return
                    except:
                        raise InvalidDatabase(database)
                else:
                    raise NotSavePath(path)


        def read_structure(self, database: str, table: str) -> dict:
            if self.save_method == "json":
                data = self.read_db(database)
                
                try:
                    table_structure = data[table]["0"]
                    return table_structure
                except:
                    raise CorruptDatabaseStructure(database, table)


        def list_databases(self) -> list: # should be ok
            if self.save_method == "json":
                data = os.listdir(self.path)
                db_list = []
                for db in data:
                    name, _ = db.split(".")
                    db_list.append(name)
                return db_list


        def list_tables(self, database: str) -> list: # should be ok
            """
            lists all tables in a database
            """
            if self.save_method == "json":
                data = self.read_db(database)
                table_list = list(data)
                return table_list


        def list_table_data(self, database: str, table: str) -> list:
            table_dict = dict(self.read_db(database)[table])
            table_dict.pop("0") # removes structure

            table_structure = list(self.read_structure(database, table))

            header_tab = []

            for struc_name in table_structure:
                #struc_value = table_structure[struc_name]
                header_tab.append(struc_name)

            table_tab = []
            
            for row_num in table_dict:
                list_ = []
                row_value = table_dict[row_num]
                print(row_value)
                for name in row_value:
                    value = row_value[name]
                    list_.append(value)
                table_tab.append(list_)            
            
            print(tabulate(table_tab, header_tab, tablefmt="outline"))


        def next_table_row(self, database: str, table: str) -> int: # should be ok
            if self.save_method == "json":
                table_data = self.read_db(database)[table]
                number_list = list(table_data)
                num = 1

                while True:
                    if not str(num) in number_list:
                        break
                    else:
                        num += 1

                return num


        def create_database(self, database: str) -> int | str:
            """
            database:is the name of the new database
            """
            if self.save_method == "json":
                db_list = self.list_databases()
                db_name, db_bool = self.filter_input(database)
                if db_name in db_list:
                    return 401, "Database already exists"

                path = f"{self.path}/{db_name}.json"

                if self.is_path_safe(basedir, path):

                    with open(path, "w") as f:
                        f.write(dumps({}, indent=self.json_indent))

                    if db_bool:
                        return 201, "Created Database but the name has been slightly changed"
                    else:
                        return 200, "Created Database"
                else:
                    return 410, "Your Database name is not safe !!!"
            else:
                return 401, "error"


        def drop_database(self, database: str) -> int | str:
            db_list = self.list_databases()

            db_name, db_bool = self.filter_input(database)

            if db_bool:
                return 411, "Your Database name is very incorrect"
            elif not database in db_list:
                return 401, "Database doesnt exist"

            path = f"{self.path}/{database}.json"

            if self.is_path_safe(basedir, path):
                os.remove(path)
                return 200,  "Database deleted"
            else:
                return 410, "Something went wrong"


        def check_db_if_exists(self, database: str):
            if self.save_method == "json":
                db_list = self.list_databases
                if database in db_list:
                    return True
                else:
                    return False


        def backup_database(self, database: str, path: str):
            if self.save_method == "json":
                if self.check_db_if_exists(database):
                    data = self.read_db
                    with open(f"{path}") as f:
                        f.write(data)
                    return True
                else:
                    return False


        def create_table(self, database: str, tablename: str, structure: list) -> str | bool:
            """
            tablename
            structure is built with two string and one seperator "::"
            z.b. ["username::str", "age::int"] types allowed:"str, int"
            if you want another type create a github issue
            """
            if self.save_method == "json":
                data = self.read_db(database)
                table_list = self.list_tables(database)

                for table in table_list:
                    if table == tablename:
                        return "Tablename is already in use"

                structure_list = {}

                for struc in structure:
                    try:
                        struc_name, struc_type = str(struc).split("::")
                    except:
                        return "Something went wrong in your structure. Maybe forgot to use the seperator '::' between the name and the type"
                    if not struc_type in ["str", "int"]:
                        return "Invalid type"

                    structure_list[struc_name] = struc_type

                data[tablename] = {"0": structure_list}
                
                # saves it to file
                self.overwrite_db(database, data)
                return True
        

        def drop_table(self, database:str,  tablename: str) -> str:
            if self.save_method == "json":
                data = self.read_db(database)
                table_list = self.list_tables(database)
                if tablename in table_list:
                    data.pop(tablename)

                    self.overwrite_db(database, data)
                return "Table doesnt exist"


        def rename_table(self, database: str, tablename: str, new_name: str):
            if self.save_method == "json":
                data = self.read_db(database)
                try: # checks if tablename exists
                    table = data[tablename]
                except:
                    return "Table couldnt be found"
                
                table_list = self.list_tables(database) # checks if new_name is already in use
                if new_name in table_list:
                    return f"The name you want to give '{tablename}' is already in use"

                data[new_name] = table

                self.overwrite_db(database, data)

                print(self.drop_table(database, tablename))

                return True


        def insert_into_table(self, database: str, tablename: str, value: dict) -> str | bool:
            """
            insert into table | value example {"name": "examplename", "username": "exampleusername"}
            """
            if self.save_method == "json": # remove func and replace it with a normal dict and at the end of insert func overwrite json file
                if not tablename in self.list_tables(database): 
                    return "Tablename is not in use"

                if value == {}:
                    return "Add something to the value dictionary"

                try:
                    data = self.read_db(database)
                except:
                    return "Your file is corrupt"
                #table = data[tablename] # initialies the table data

                try:
                    structure = self.read_structure(database, tablename) # reads the structure of the table
                    # gets the names of the structure
                except:
                    return "Structure doesnt exist in this table ???"

                content_list = {}

                for struc in structure:
                    for value_ in value:
                        content = value[value_] # content to save

                        if str(value_) == struc: # checks if content is the same as the structure list
                            if structure[struc] == "str":
                                if type(content) == str:
                                    content_list[value_] = content
                                else:
                                    return "You got the wrong name or wrong data type"
                            elif structure[struc] == "int":
                                if type(content) == int:
                                    content_list[value_] = content
                                else:
                                    return "You got the wrong name or wrong data type"

                number = self.next_table_row(database, tablename)
                data[tablename][number] = content_list

                self.overwrite_db(database, data)
                return True


        def drop_row_by_number(self, database: str, tablename: str, row: int):
                if self.save_method == "json":
                    data = self.read_db(database)
                    try:
                        data = data[tablename]
                    except:
                        pass

                    if row == 0:
                        return "You cant drop row 0 (stores the structure of the table)"
                    
                    data.pop(str(row))

                    self.overwrite_db(database, data)

                    return True


        def use_sql_lang(self, database: str, code: str, sql_terminal=False):
            """
            translates the sql language and creates everything
            """
            words = str(code).lower()
            if ";" in words:
                words.replace(";", "")
            else:
                raise SQLMissingSemicolon

            args = str(words).split()
            
            def create_func():
                arg1 = words[1]
                if arg1 == "database":
                    self.create_database(words[2])
                elif arg1 == "table":
                    self.create_table(database, words[2])
                elif arg1 == "index":
                    pass
                elif arg1 == "view":
                    pass

            def drop_func():
                arg1 = words[1]
                if arg1 == "database":
                    self.drop_database(words[2])
                elif arg1 == "table":
                    self.drop_table(words[2])
                elif arg1 == "index":
                    pass

            def index_func():
                arg1 = words[1]
                if arg1 == "database":
                    pass
            
            def backup_func():
                if args[1] == "database":
                    if args[3] == "to":
                        if args[4] == "disk":
                            if args[5] == "=":
                                self.backup_database(args[2], args[6])


            try:
                if words[0] == "select": # you have to use use command before or select a db before
                    if words[1] == "*":
                        if words[2] == "from":
                            table = words[3]
                            if table is None:
                                return ""
                            self.read

            



                else:
                    return "No Command"
            except Exception as e:
                #return 401, "You dindnt gave enough arguments", e
                raise SQLMissingArgs(e)
                

        def sql_terminal(self):
            current_database = None
            while True:
                code = input(f"DB_NAME [{current_database}]> ")

                if not code == "": # if input == "" doesnt request
                    response = self.use_sql_lang(database=current_database, code=code, sql_terminal=True)
                    
                    if type(response) == list or type(response) == tuple:
                        if response[0] == "use":
                            current_database = response[1]
                    else:
                        print(response)
                




#elif words[1] == "user": # maybe ill create a user func (which is save) but if then at the end

    
    class simple: # create a second version wich is simplified (lightweight) inspirated by replits builtin database (keystorage)
        """
        NOT USABLE
        """
        def __init__(self, db_folder=db_folder_simple) -> None:
            self.db_folder = db_folder
            
            self.save_method = "json"
            self.json_indent = 4

            #if self.save_method == "json":
            #    if not os.path.exists(self.db_path):

            #        open(self.db_path, "w").write(dumps({}, indent=self.json_indent))

        def setkeytovalue(self, key, value):
            """
            # Set a key to a value
            """
            # file = self.readfiel()
            

        def getkeysvalue(self, key):
            """
            # Get a key's value
            """
            #return value

        def deletekey(self, key):
            """
            # Delete a key
            """


        def listkeys(self):
            """
            # List all keys
            """

        
        def listkeywithprefix(self, prefix):
            """
            # Search for a key/s
        """

    #def create_table(self, tablename):
    #    PATH = f"{DATABASE_DIRECTORY}/{tablename}.txt"
    #
    #    if os.path.exists(PATH):
    #        return "Table already exists"

    #    open(PATH) # creates file

    #    with open(f"{DATABASE_DIRECTORY}/tables.txt") as w:
    #        w.write(f"{tablename}\n")
    #        w.close()
        
    #    return "Table created successfully"

    
    #def list_tables(self):
    #    with open(f"{DATABASE_DIRECTORY}/tables.txt") as w:
    #        table_list = []
    #        for table in w.readlines():
    #            table_list.append(table)
    #        w.close()
    #        return table_list


    #def add(self, key, value):
    #    pass# problem how to save more then one key 
        # create a database in python you can access over http request and 
        # local request with user etc, and select in what file to save it