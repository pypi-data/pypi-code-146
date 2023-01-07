import datetime as dt
import uuid

from flask import current_app
from flask_bcrypt import check_password_hash, generate_password_hash

from soccer_sdk_utils.model.meta import MetaProperty


class User:
    def __init__(self, **kwargs):
        name = kwargs.get("name")

        if name is not None:
            tokens = name.split(" ")
            self.first_name = tokens[0].strip()
            self.last_name = tokens[1].strip()
        else:
            self.first_name = kwargs.get("first_name")
            self.last_name = kwargs.get("last_name")

            if self.first_name is not None:
                self.first_name = self.first_name.strip()

            if self.last_name is not None:
                self.last_name = self.last_name.strip()

        self.id = kwargs.get("id")
        self.email = kwargs.get("email")
        self.username = kwargs.get("username")
        self.password = kwargs.get("password")
        self.phone = kwargs.get("phone")
        self.registered_on = kwargs.get("registered_on")
        self.meta = kwargs.get("meta", [])

    @property
    def slug(self):
        return f"{self.first_name}-{self.last_name}".lower()

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)

    def hash_password(self):
        """Hashes the user's password in place"""
        self.password = generate_password_hash(self.password).decode("utf-8")

    def generate_id(self):
        """Generates a unique ID for the user in place"""
        self.id = str(uuid.uuid4())

    def has_property(self, name: str):
        for meta in self.meta:
            if meta.name == name:
                return True

        return False

    def get_property(self, name: str):
        for meta in self.meta:
            if meta.name == name:
                return meta.value

        return None

    def add_property(self, name: str, value: str):
        self.meta.append(MetaProperty(name=name, value=value))

    @staticmethod
    def get_utc_now():
        return dt.datetime.utcnow()

    @staticmethod
    def get_secret_key():
        return current_app.config.get("SECRET_KEY")

    def __repr__(self):
        return f"<User(email='{self.email}', first_name='{self.first_name}', last_name='{self.last_name}')>"
