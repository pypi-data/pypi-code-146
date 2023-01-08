from pathlib import Path
import typer
import pickledb
import os
import base64

APP_NAME = 'uva-command-line'
CONFIG_FILE_NAME = 'config.db'

DB_KEY_COOKIE = 'COOKIE'
DB_KEY_USERNAME = 'USERNAME'
DB_KEY_UHUNT_UID = 'UHUNT_UID'


def get_database():
    app_dir = typer.get_app_dir(APP_NAME)
    path: Path = Path(app_dir) / CONFIG_FILE_NAME
    if not path.is_file():
        os.makedirs(os.path.dirname(path), exist_ok=True)
    return pickledb.load(path, False)


def read_cookies():
    db = get_database()
    if db.exists(DB_KEY_COOKIE):
        cookies = db.get(DB_KEY_COOKIE)
        return base64.b64decode(cookies)
    else:
        return None


def save_cookies(data):
    encoded = base64.b64encode(data)
    db = get_database()
    db.set(DB_KEY_COOKIE, encoded.decode('ascii'))
    db.dump()


def save_login_data(username, uhunt_uid):
    db = get_database()
    db.set(DB_KEY_USERNAME, username)
    db.set(DB_KEY_UHUNT_UID, uhunt_uid)
    db.dump()


def read_uhunt_uid():
    db = get_database()
    return db.get(DB_KEY_UHUNT_UID)


def purge():
    # app_dir = typer.get_app_dir(APP_NAME)
    # path: Path = Path(app_dir) / CONFIG_FILE_NAME
    # os.remove(os.path.dirname(path))
    db = get_database()
    db.deldb()
    db.dump()
