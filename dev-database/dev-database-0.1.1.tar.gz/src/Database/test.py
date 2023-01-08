import main as db
from exceptions import *

db = db.Database.normal()

#print(db.create_table("test", ["name::str", "username::str"]))

#print(db.read_structure("NEXT_FORMAT"))

#print(db.insert_into_table("test", {"name": "testname", "username": "testusername"}))

#print(db.next_number_to_use("NEXT_FORMAT"))

#print(db.drop_table("test"))

#print(db.drop_row_by_number("test", 1))

#print(db.read_structure("test"))

#print(db.rename_table("table2", "table4"))

#print(db.use_sql_lang("create database"))

#print(db.create_database("dsdasda"))

#print(db.drop_database("dsa"))

#print(db.list_databases())

#db.sql_terminal()

#db.filter_input("String")

#database = "db_test"
#path = "/dsada/sfnklafnkad/db_.json"

#raise CorruptDatabaseStructure(database, "table__")


#db.create_database("test")
#db.create_table("test", "test123", ["username::str", "password::str", "age::int"])
#db.insert_into_table("test", "test123", {"username": "luc343221a", "password": "pswd3421123", "age": 2893223411})
db.list_table_data("test", "test123")