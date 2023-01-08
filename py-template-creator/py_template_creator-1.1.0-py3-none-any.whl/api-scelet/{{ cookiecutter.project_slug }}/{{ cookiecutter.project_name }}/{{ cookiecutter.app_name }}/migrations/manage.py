#!/usr/bin/env python
import os
import logging
from migrate.versioning.shell import main

logger = logging.getLogger(__name__)


if __name__ == '__main__':
    try:
        url = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(
            os.getenv("MYSQL_USER"),
            os.getenv("MYSQL_PASSWORD"),
            os.getenv("MYSQL_HOST"),
            os.getenv("MYSQL_PORT"),
            os.getenv("MYSQL_DB"),
        )
        logger.info(f"Using database url {url}")
        main(repository='./{{cookiecutter.app_name}}/migrations', url=url, debug='True')
    except Exception as e:
        logger.error(f"{str(e)}")
