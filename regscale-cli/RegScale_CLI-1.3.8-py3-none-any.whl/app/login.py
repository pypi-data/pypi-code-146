#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Standard Imports """
import logging
import sys
from datetime import datetime
from json import JSONDecodeError
from ssl import SSLCertVerificationError

import requests
from typing_extensions import Self

from app.api import Api
from app.application import Application
from app.logz import create_logger

logger = create_logger()


def login(
    str_user: str, str_password: str, host: str = None, app: Application = None
) -> str:
    """Wrapper for Login to RegScale"""
    config = app.config
    jwt = None
    # load the config from YAML
    # with open("init.yaml", "r") as stream:
    #     config = yaml.safe_load(stream)
    if config["domain"] is None:
        raise ValueError("ERROR: No domain set in the initilization file.")
    if config["domain"] == "":
        raise ValueError("ERROR: The domain is blank in the initialization file.")
    # set the catalog URL for your Atlasity instance
    if host is None:
        url_login = config["domain"] + "/api/authentication/login"
    else:
        url_login = host + "/api/authentication/login"
    logger.info("Logging into: %s", url_login)

    # create object to authenticate
    auth = {"userName": str_user, "password": str_password, "oldPassword": ""}
    logging.debug(auth)
    if auth["password"]:
        try:
            user_id, jwt = regscale_login(url_login=url_login, auth=auth, app=app)

            # update init file from login
            config["token"] = jwt
            config["userId"] = user_id
            # write the changes back to file
            app.save_config(config)
            # set variables
            logger.info("User ID: %s", user_id)
            logger.info("New RegScale Token: %s", jwt)
        except TypeError as ex:
            logger.error("TypeError: %s", ex)
        except SSLCertVerificationError as sslex:
            logger.error(
                "SSLError, python requests requires a valid ssl certificate\n%s", sslex
            )
            sys.exit(1)
    return jwt


def regscale_login(url_login, auth, app):
    """Login to RegScale"""
    api = Api(app=app)
    try:
        # login and get token
        response = api.post(url=url_login, json=auth)
        auth_response = response.json()
        user_id = auth_response["id"]
        jwt = "Bearer " + auth_response["auth_token"]

    except ConnectionError:
        logger.error(
            "ConnectionError: Unable to login user to RegScale, check the server domain"
        )
        sys.exit(1)
    except JSONDecodeError:
        logger.error(
            "Login Error: Unable to login user to instance: %s\n", app.config["domain"]
        )
        sys.exit(1)
    return user_id, jwt


def is_valid(host=None, app=None) -> bool:
    """Quick endpoint to check login status"""
    config = app.config
    login_status = False
    api = Api(app=app)
    try:
        # Make sure url isn't default
        # login with token
        token = config["token"]
        headers = {"Authorization": token}
        if host is None:
            url_login = config["domain"] + "/api/logging/filterLogs/0/0"
        else:
            url_login = host + "/api/logging/filterLogs/0/0"
        logger.debug("config: %s", config)
        logger.debug("is_valid url: %s", url_login)
        logger.debug("is_valid headers: %s", headers)
        response = api.get(url=url_login, headers=headers)
        if response:
            if response.status_code == 200:
                login_status = True
    except KeyError as ex:
        if str(ex).replace("'", "") == "token":
            logger.debug("Token is missing, we will generate this")
    except ConnectionError:
        logger.error(
            "ConnectionError: Unable to login user to RegScale, check the server domain"
        )
    except JSONDecodeError as decode_ex:
        logger.error(
            "Login Error: Unable to login user to RegScale instance:  %s/n",
            config["domain"],
        )
        logger.error(decode_ex)

    finally:
        logger.debug("login status: %s", login_status)
    return login_status


def is_licensed(app: Application) -> bool:
    """Check license status.

    Returns:
        bool: license status
    """
    status = False
    api = Api(app=app)
    try:
        lic = app.get_regscale_license(appl=app, api=api).json()
        license_date = datetime.strptime(lic["expirationDate"], "%Y-%m-%d")
        if lic["licenseType"] == "Enterprise" and license_date > datetime.now():
            status = True
    except requests.RequestException:
        pass  # TODO: Need to account for versions of the API with no license endpoint
    return status
