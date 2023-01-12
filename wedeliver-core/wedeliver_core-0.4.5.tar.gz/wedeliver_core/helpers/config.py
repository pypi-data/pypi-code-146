# -*- coding: utf-8 -*-

import os
import json

from dotenv import load_dotenv


class Config(object):
    SQLALCHEMY_DATABASE_URI = None

    def init_database_config(self):
        self.SQLALCHEMY_DATABASE_URI = "{engine}://{username}:{password}@{server}:{port}/{database}?charset=utf8".format(
            engine=os.environ.get("DATABASE_ENGINE"),
            username=os.environ.get("DATABASE_USERNAME"),
            password=os.environ.get("DATABASE_PASSWORD"),
            server=os.environ.get("DATABASE_SERVER"),
            database=os.environ.get("DATABASE_NAME"),
            port=os.environ.get("DATABASE_PORT", 3306),
        )

    def __init__(self):
        if not os.environ.get("DATABASE_ENGINE"):
            load_dotenv()

        self.init_database_config()

        for k, v in os.environ.items():

            if not k:
                continue

            env_val = os.environ.get(k).strip()
            # Convert Null and empty value to None
            env_val = None if env_val.upper() in ["NULL", ""] else env_val
            # Convert True and False value to Boolean
            env_val = (
                json.loads(env_val.lower())
                if env_val and env_val.upper() in ["TRUE", "FALSE"]
                else env_val
            )

            self.__dict__[k] = env_val
