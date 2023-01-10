"""
create.py

Create upload database template.
"""
import os
import sqlite3


CURRENT_DIRECTORY = os.path.dirname(__file__)
TEMPLATE_DB = os.path.join(CURRENT_DIRECTORY, "template.db")
TEMPLATE_SQL_SCRIPT = os.path.join(CURRENT_DIRECTORY, "manifest.sql")

# Register adapter and converter for "BOOLEAN" type.
sqlite3.register_adapter(bool, int)
sqlite3.register_converter("BOOLEAN", lambda db_value: bool(int(db_value)))


def create_template(db_path=TEMPLATE_DB):
    """
    Create a template database.

    This function only needs to be called when changes are made
    to manifest.sql.

    Parameters
    ----------
    db_path : str
        The path to the template database file.

    Result
    ------
    A new template database file will be created.
    """
    # Remove the template database file if it already exists.
    if os.path.exists(db_path):
        os.remove(db_path)

    # Open a connection to the database file.
    # Detect types like DATETIME, which will then be treated as datetime
    # objects instead of strings.
    detect_types = sqlite3.PARSE_DECLTYPES

    with sqlite3.connect(db_path, detect_types=detect_types) as conn:
        # Allow values in records to be retrieved using column names as keys.
        conn.row_factory = sqlite3.Row

        # Enforce referential integrity.
        conn.execute("PRAGMA foreign_keys = ON")

        # Run the SQL script.
        with open(TEMPLATE_SQL_SCRIPT) as f:
            sql = f.read()

        conn.executescript(sql)
        conn.commit()
