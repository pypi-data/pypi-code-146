##
## Copyright (C) Optumi Inc - All rights reserved.
##
## You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
## To receive a copy of the licensing terms please write to contact@optumi.com or visit us at https://www.optumi.com.
##

from .LoginServer import login as oauth_login
from .HoldoverTime import HoldoverTime
from .Workloads import Workloads
from requests.exceptions import ConnectionError

import phonenumbers

# Generic Operating System Services
import datetime, json, os
from typing import Union

# Optumi imports
import optumi_core as optumi
from optumi_core.exceptions import (
    NotLoggedInException,
    ServiceException,
    OptumiException,
)


def login(
    connection_token=None,
    dnsName=optumi.login.get_portal(),
    port=optumi.login.get_portal_port(),
):
    # On a dynamic machine we do not need to get an okta token
    if optumi.login.is_dynamic():
        if not optumi.login.check_login(dnsName, port, mode="api"):
            login_status, message = optumi.login.login_rest_server(
                dnsName, port, "", mode="api", login_type="dynamic"
            )
    else:
        if not optumi.login.check_login(dnsName, port, mode="api"):
            if connection_token == None:
                login_status, message = optumi.login.login_rest_server(
                    dnsName, port, oauth_login(), mode="api", login_type="oauth"
                )
                if login_status != 1:
                    raise NotLoggedInException("Login failed: " + message)
            else:
                login_status, message = optumi.login.login_rest_server(
                    dnsName, port, connection_token, mode="api", login_type="token"
                )
                if login_status != 1:
                    raise NotLoggedInException("Login failed: " + message)
    ## This is currently necessary in order for the controller to recognize that the user has signed the agreement
    optumi.login.get_new_agreement()


def logout():
    try:
        optumi.login.logout()
    except NotLoggedInException:
        pass


def get_phone_number():
    return json.loads(optumi.core.get_user_information(False).text)["phoneNumber"]


def get_holdover_time():
    res = optumi.core.get_user_information(False)
    return HoldoverTime(
        int(
            json.loads(optumi.core.get_user_information(False).text)["userHoldoverTime"]
        )
        // 60  # Convert to minutes
    )


def set_holdover_time(holdover_time: Union[int, HoldoverTime]):
    optumi.core.set_user_information(
        "userHoldoverTime",
        str(
            holdover_time.seconds
            if type(holdover_time) is HoldoverTime
            else holdover_time * 60  # Convert to seconds
        ),
    )


def get_connection_token():
    return json.loads(optumi.core.get_connection_token().text)


def redeem_signup_code(signupCode):
    optumi.core.redeem_signup_code(signupCode)


def send_notification(message, details=True):
    if get_phone_number():
        optumi.core.send_notification(
            "From " + str(Workloads.current()) + ": " + message
            if details and optumi.login.is_dynamic()
            else message
        )
    else:
        print("Unable to send notification - no phone number specified")


def set_phone_number(phone_number):
    if phone_number == "":
        optumi.core.clear_phone_number()
    else:
        number = phonenumbers.parse(phone_number, "US")
        if not phonenumbers.is_valid_number(number):
            raise OptumiException(
                "The string supplied did not seem to be a valid phone number."
            )

        formatted_number = phonenumbers.format_number(
            number, phonenumbers.PhoneNumberFormat.E164
        )

        optumi.core.send_verification_code(formatted_number)

        while True:
            code = input("Enter code sent to " + formatted_number + ": ")
            text = optumi.core.check_verification_code(formatted_number, code).text

            if text:
                print(text)
                # This is kind of sketchy but wont break if the message changes, it will just continue prompting the user for their code
                if text == 'Max check attempts reached':
                    break
            else:
                optumi.set_user_information("notificationsEnabled", True)
                break


        