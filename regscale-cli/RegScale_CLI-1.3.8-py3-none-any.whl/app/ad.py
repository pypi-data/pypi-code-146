#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# standard python imports

import json
import sys
from os import sep

import click
import msal
import requests
import yaml

from app.api import Api
from app.application import Application
from app.logz import create_logger
from app.utils import check_license

logger = create_logger()


# Create group to handle Active Directory processing
@click.group()
def ad():
    """Performs directory and user synchronization functions with Azure Active Directory"""
    check_license()


#####################################################################################################
#
# AUTHENTICATE TO ACTIVE DIRECTORY
#
#####################################################################################################
@ad.command()
def authenticate():
    """Obtains an access token using the credentials provided"""
    get_access_token()


#####################################################################################################
#
# GET ACTIVE DIRECTORY GROUPS
#
#####################################################################################################
@ad.command()
def listGroups():
    """Prints the lists of available RegScale groups the CLI can read"""
    # authenticate the user
    get_access_token()

    # list all of the groups
    list_ad_groups()


#####################################################################################################
#
# SYNC REGSCALE ADMINS FROM ACTIVE DIRECTORY
#
#####################################################################################################
@ad.command()
def syncAdmins():
    """Syncs members of the RegScale-admins group and assigns roles"""
    # authenticate the user
    get_access_token()

    # set the Microsoft Graph Endpoint
    get_group("RegScale-admin")


#####################################################################################################
#
# SYNC REGSCALE GENERAL USERS FROM ACTIVE DIRECTORY
#
#####################################################################################################
@ad.command()
def syncGeneral():
    """Syncs members of the RegScale-general group and assigns roles"""
    # authenticate the user
    get_access_token()

    # set the Microsoft Graph Endpoint
    get_group("RegScale-general")


#####################################################################################################
#
# SYNC REGSCALE READ ONLY FROM ACTIVE DIRECTORY
#
#####################################################################################################
@ad.command()
def syncReadonly():
    """Syncs members of the RegScale-readonly group and assigns roles"""
    # authenticate the user
    get_access_token()

    # set the Microsoft Graph Endpoint
    get_group("RegScale-readonly")


#############################################################################
#
#   Supporting Functions
#
#############################################################################


def check_config(strKey, strTitle, config):
    def error(str):
        logger.error("ERROR: No Azure AD %s set in the init.yaml file.", str)

    if strKey not in config:
        error(strTitle)
        sys.exit()
    elif config[strKey] is None:
        error(strTitle)
        sys.exit()
    elif config[strKey] == "":
        error(strTitle)
        sys.exit()


def get_access_token():
    appl = Application()

    config = appl.config
    # load the config from YAML
    # with open("init.yaml", "r") as stream:
    #     config = yaml.safe_load(stream)

    # validation for each field
    check_config("adClientId", "Client ID", config)
    check_config("adTenantId", "Tenant ID", config)
    check_config("adSecret", "Secret", config)
    check_config("adGraphUrl", "Graph URL", config)
    check_config("adAuthUrl", "Authentication URL", config)

    # generate the endpoint
    authURL = config["adAuthUrl"] + str(config["adTenantId"])
    graphURL = config["adGraphUrl"]

    # configure the Microsoft MSAL library to authenticate and gain an access token
    app = msal.ConfidentialClientApplication(
        config["adClientId"],
        authority=authURL,
        client_credential=config["adSecret"],
    )

    # use MSAL to get the token (no caching for security)
    try:
        token = app.acquire_token_for_client(scopes=graphURL)
        config["adAccessToken"] = "Bearer " + token["access_token"]

        # write the changes back to file
        appl.save_config(config)
        logger.info("Azure AD Login Successful!")
        logger.info("Init.yaml file updated successfully with the access token.")
    except Exception as ex:
        logger.error("ERROR: Unable to authenticate to Azure AD \n %s", ex)
        sys.exit()

    # return the result
    return token


# lists all RegScale groups in AD
def list_ad_groups():
    appl = Application()
    api = Api(appl)
    # load the config from YAML
    with open("init.yaml", "r") as stream:
        config = yaml.safe_load(stream)

    # validate
    check_config("adAccessToken", "Access Token", config)
    check_config("adGraphUrl", "Graph URL", config)

    # trim the URL
    strGraphUrl = config["adGraphUrl"].replace(".default", "")

    # set the endpoint
    groupsURL = strGraphUrl + "v1.0/groups?$filter=startswith(displayName,'RegScale')"

    # setup the header
    headers = {"Authorization": config["adAccessToken"]}

    # get the AD group info
    logger.info("Fetching relevant AD Groups from Azure for RegScale")
    try:
        groups_response = api.get(url=groupsURL, headers=headers)
        groupsData = groups_response.json()
    except Exception as ex:
        logger.error(
            "ERROR: Unable to retrieve group information from Azure Active Directory.\n%s",
            ex,
        )
        sys.exit()

    # loop through the groups and log the results
    if "value" in groupsData:
        for g in groupsData["value"]:
            logger.info("GROUP: " + g["displayName"])
        logger.info(str(len(groupsData["value"])) + " total groups retrieved.")
    else:
        # error handling (log error)
        if "error" in groupsData:
            try:
                logger.error(
                    groupsData["error"]["code"] + ": " + groupsData["error"]["message"]
                )
            except Exception as ex:
                logger.error("Unknown Error! %s", ex)
                logger.error(groupsData)

    # write out group data to file
    with open(
        f"artifacts{sep}RegScale-AD-groups.json", "w", encoding="utf-8"
    ) as outfile:
        outfile.write(json.dumps(groupsData, indent=4))


# retrieves the RegScale groups from Azure AD
# flake8: noqa: C901
def get_group(str_group):
    """Syncs members of the RegScale-admins group and assigns roles"""
    # variables
    app = Application()
    api = Api(app)
    new_users = []
    remove_users = []

    # see if readonly
    b_read_only = False
    if str_group == "RegScale-readonly":
        b_read_only = True

    # load the config from YAML
    with open("init.yaml", "r") as stream:
        config = yaml.safe_load(stream)

    # validate and trim the Graph URL
    check_config("adAccessToken", "Access Token", config)
    check_config("adGraphUrl", "Graph URL", config)
    str_graph_url = config["adGraphUrl"].replace(".default", "")

    # set the Microsoft Graph Endpoint
    if str_group == "RegScale-admin":
        groups_url = (
            str_graph_url
            + "v1.0/groups?$filter=startswith(displayName,'RegScale-admin')"
        )
    elif str_group == "RegScale-general":
        groups_url = (
            str_graph_url
            + "v1.0/groups?$filter=startswith(displayName,'RegScale-general')"
        )
    elif str_group == "RegScale-readonly":
        groups_url = (
            str_graph_url
            + "v1.0/groups?$filter=startswith(displayName,'RegScale-readonly')"
        )
    else:
        logger.error("ERROR: Unknown RegScale group (%s) requested for sync", str_group)

    # setup the header
    headers = {"Authorization": config["adAccessToken"]}

    # get the AD group info
    logger.info("Fetching relevant AD Groups from Azure for RegScale")
    try:
        groupsResponse = api.get(groups_url, headers=headers)
        groupsData = groupsResponse.json()
    except Exception as ex:
        logger.error(
            "ERROR: Unable to retrieve group information from Azure Active Directory.\n%s",
            ex,
        )
        sys.exit()

    # write out group data to file
    with open(
        f"artifacts{sep}adGroupList-" + str_group + ".json", "w", encoding="utf-8"
    ) as outfile:
        outfile.write(json.dumps(groupsData, indent=4))

    # loop through each group to find admins
    if len(groupsData) == 0:
        logger.error("ERROR: %s group has not been setup yet in Azure AD.", str_group)
        sys.exit()
    else:
        # get group info
        if "value" in groupsData:
            foundGroup = groupsData["value"][0]
            groupId = foundGroup["id"]
        else:
            # error handling (log error)
            if "error" in groupsData:
                try:
                    logger.error(
                        groupsData["error"]["code"]
                        + ": "
                        + groupsData["error"]["message"]
                    )
                    sys.exit()
                except Exception as ex:
                    logger.error("Unknown Error!\n%s", ex)
                    logger.error("data: %s", groupsData)
                    sys.exit()

        # get AD group members
        membersURL = str_graph_url + "v1.0/groups/" + str(groupId) + "/members"

        # get the member list for the AD group
        logger.info("Fetching the list of members for this AD group - " + str(groupId))
        try:
            memberResponse = api.get(membersURL, headers=headers)
            memberData = memberResponse.json()
        except Exception:
            logger.error(
                "ERROR: Unable to retrieve member list for Azure Active Directory group - "
                + str(groupId)
            )
            sys.exit()

        # write out member data to file
        with open(
            f"artifacts{sep}adMemberList-" + str(groupId) + ".json", "w"
        ) as outfile:
            outfile.write(json.dumps(memberData, indent=4))
        logger.info(memberData)
        # retrieve the list of RegScale users
        urlUsers = config["domain"] + "/api/accounts/getList"
        regscale_headers = {"Authorization": config["token"]}
        try:
            userResponse = api.get(urlUsers, headers=regscale_headers)
            userData = userResponse.json()
        except Exception:
            logger.error("ERROR: Unable to retrieve user list from RegScale")
            sys.exit()

        # retrieve the list of RegScale roles
        urlRoles = config["domain"] + "/api/accounts/getRoles"
        try:
            roleResponse = api.get(urlRoles, headers=regscale_headers)
            roleData = roleResponse.json()
        except Exception:
            logger.error("ERROR: Unable to retrieve roles from RegScale")
            sys.exit()

        # loop through the members of the AD group (create new if not in RegScale)
        for m in memberData["value"]:
            # see if it exists
            bMemberFound = False
            for u in userData:
                if "externalId" in u:
                    if m["id"] == u["externalId"]:
                        bMemberFound = True

            # handle new user flow
            if bMemberFound == False:
                # create a new user
                newUser = {
                    "id": "",
                    "userName": m["userPrincipalName"],
                    "email": m["mail"],
                    "password": "",
                    "firstName": m["givenName"],
                    "lastName": m["surname"],
                    "workPhone": m["mobilePhone"],
                    "pictureURL": "",
                    "activated": True,
                    "jobTitle": m["jobTitle"],
                    "orgId": None,
                    "emailNotifications": True,
                    "tenantId": 1,
                    "ldapUser": True,
                    "externalId": m["id"],
                    "dateCreated": None,
                    "lastLogin": None,
                    "readOnly": b_read_only,
                }
                new_users.append(newUser)

        # loop through the users (disable if not in AD group)
        for u in userData:
            if "externalId" in u:
                bDisable = True
                for m in memberData["value"]:
                    if m["id"] == u["externalId"]:
                        bDisable = False
                if bDisable == True:
                    remove_users.append(u)

        # write out new user list to file
        with open(f"artifacts{sep}newUsers.json", "w", encoding="utf-8") as outfile:
            outfile.write(json.dumps(new_users, indent=4))

        # write out disabled user list to file
        with open(f"artifacts{sep}removeUsers.json", "w", encoding="utf-8") as outfile:
            outfile.write(json.dumps(remove_users, indent=4))

        # Logging
        logger.info("%s new users to process.", str(len(new_users)))

        # loop through each user
        regscale_new = []
        for us in new_users:
            # add new users in bulk
            url_new_users = config["domain"] + "/api/accounts/azureAD"
            regscale_headers = {"Authorization": config["token"]}
            try:
                strUser = api.post(url_new_users, headers=regscale_headers, json=us)
                user_new = {"id": strUser.text}
                regscale_new.append(user_new)
                logger.info("User created or updated: %s", us["userName"])
            except Exception as ex:
                logger.error("ERROR: Unable to create new user %s", us["userName"])
                logger.error(ex)
                sys.exit()

        # write out new user list to file
        with open(
            f"artifacts{sep}newRegScaleUsers.json", "w", encoding="utf-8"
        ) as outfile:
            outfile.write(json.dumps(regscale_new, indent=4))

        # set the role
        strRole = ""
        if str_group == "RegScale-admin":
            strRole = "Administrator"
        elif str_group == "RegScale-general":
            strRole = "GeneralUser"
        elif str_group == "RegScale-readonly":
            strRole = "ReadOnly"

        # set the RegScale role based on the AD group
        regScaleRole = None
        for r in roleData:
            if r["name"] == strRole:
                regScaleRole = r
        if r is None:
            logger.error(
                "Error: Unable to locate RegScale role for group: %s", str_group
            )
            sys.exit()

        # loop through the users and assign roles
        int_roles = 0
        for us in regscale_new:
            # check the role
            url_check_role = (
                config["domain"]
                + "/api/accounts/checkRole/"
                + us["id"]
                + "/"
                + regScaleRole["id"]
            )
            try:
                role_check = api.get(url=url_check_role, headers=regscale_headers)
                str_check = role_check.text
            except Exception as ex:
                logger.error(
                    "ERROR: Unable to check role: %s/%s\n, %s",
                    us["id"],
                    regScaleRole["id"],
                    ex,
                )
                sys.exit()

            # add the role
            if str_check == "false":
                # add the role
                url_assign_role = config["domain"] + "/api/accounts/assignRole/"
                # role assignment object
                assign = {"roleId": regScaleRole["id"], "userId": us["id"]}
                try:
                    requests.request(
                        "POST", url_assign_role, headers=regscale_headers, json=assign
                    )
                    int_roles += 1
                except Exception as ex:
                    logger.error(
                        "ERROR: Unable to assign role: %s/%s\n%s",
                        us["id"],
                        regScaleRole["id"],
                        ex,
                    )
                    sys.exit()

        # output results
        if int_roles > 0:
            logger.info("Total Roles Assigned: %s", str(int_roles))

        # loop through and remove users
        int_removals = 0
        for us in remove_users:
            # check the role
            url_check_role = (
                config["domain"]
                + "/api/accounts/checkRole/"
                + us["id"]
                + "/"
                + regScaleRole["id"]
            )
            try:
                role_check = api.get(url=url_check_role, headers=regscale_headers)
                str_check = role_check.text
            except Exception as ex:
                logger.error(
                    "ERROR: Unable to check role: %s/%s\n%s",
                    us["id"],
                    regScaleRole["id"],
                    ex,
                )
                sys.exit()

            # add the role
            if str_check == "true":
                # remove the role
                urlRemoveRole = (
                    config["domain"]
                    + "/api/accounts/deleteRole/"
                    + us["id"]
                    + "/"
                    + regScaleRole["id"]
                )
                try:
                    api.delete(url=urlRemoveRole, headers=regscale_headers)
                    int_removals += 1
                except Exception as ex:
                    logger.error(
                        "ERROR: Unable to remove role: %s/%s\n%s",
                        us["id"],
                        regScaleRole["id"],
                        ex,
                    )
                    sys.exit()

                # deactive the user if they were in this role
                urlDeactivate = (
                    config["domain"]
                    + "/api/accounts/changeUserStatus/"
                    + us["id"]
                    + "/false"
                )
                try:
                    api.get(urlDeactivate, headers=regscale_headers)
                    logger.warning("%s account deactivated.", us["userName"])
                except Exception as ex:
                    logger.error(
                        "ERROR: Unable to check role: %s/%s\n%s",
                        us["id"],
                        regScaleRole["id"],
                        ex,
                    )
                    sys.exit()

        # output results
        logger.info(
            str(int_removals) + " users had roles removed and accounts disabled."
        )
