import os
import re
import sqlite3
import importlib

def extract_models(path):
    with open(path, 'r') as f:
        content = f.read()
    
    function_names = re.findall(r'def\s(\w+)\(', content)

    spec = importlib.util.spec_from_file_location("models", str(path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    schemas = []
    for item in function_names:
        schema = getattr(module, item)()

        modified_schema = dict()
        modified_schema.update({
            "fields": schema
        })
        modified_schema["table"] = item

        schemas.append(modified_schema)
    
    return schemas

def read_db(project_path):
    models_path = os.path.join(project_path, "models.py")
    db_file = os.path.join(project_path, "db.sqlite3")


    if models_path:
        conn = sqlite3.connect(db_file)
        c = conn.cursor()

        models_info = extract_models(models_path)

        for model in models_info:
            table = model["table"]
            fields = model["fields"]

            c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table,))

            field_str = ', '.join("{} {}".format(field, fields[field]) for field in fields)
            print(field_str)

            try:
                c.execute("CREATE TABLE {} ({})".format(table, field_str))

            except sqlite3.OperationalError:
                print(f"The {table} table already exists in database, skipping creation.")
