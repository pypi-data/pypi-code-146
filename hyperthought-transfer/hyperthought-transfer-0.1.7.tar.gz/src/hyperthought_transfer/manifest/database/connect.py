"""
database/upload/connect.py

Means of connecting to upload database.
"""

import json
import os
import shutil
import sqlite3


# Register adapter and converter for "BOOLEAN" type.
sqlite3.register_adapter(bool, int)
sqlite3.register_converter("BOOLEAN", lambda db_value: bool(int(db_value)))

# Register adapter and converter for "METADATA" type.
sqlite3.register_adapter(dict, json.dumps)  # TODO:  Is this needed?
sqlite3.register_adapter(list, json.dumps)
sqlite3.register_adapter(tuple, json.dumps)  # TODO:  Is this needed?
sqlite3.register_converter("METADATA", lambda db_value: json.loads(db_value))


def get_connection(manifest_path, overwrite=True):
    """
    Get or create a database file for a job.

    Parameters
    ----------
    job_name : str
        The name of the job (usually computer name + datetime stamp).
    directory : str
        Directory path to folder where jobs are stored.
    """
    template_path = os.path.join(
        os.path.dirname(__file__),
        "template/template.db",
    )

    if not os.path.exists(manifest_path) or overwrite:
        shutil.copyfile(template_path, manifest_path)

    # Open a connection to the database file.
    # Detect types like DATETIME, which will then be treated as datetime
    # objects instead of strings.
    conn = sqlite3.connect(manifest_path, detect_types=sqlite3.PARSE_DECLTYPES)

    # Allow values in records to be retrieved using column names as keys.
    conn.row_factory = sqlite3.Row

    # Enforce referential integrity.
    conn.execute("PRAGMA foreign_keys = ON")

    return conn
