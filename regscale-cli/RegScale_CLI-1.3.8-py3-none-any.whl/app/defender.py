#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" RegScale Microsoft Defender recommendations integration"""

# standard python imports
import sys
from datetime import datetime, timedelta
from json import JSONDecodeError
from typing import Tuple

import click
from rich.console import Console

from app.ad import check_config
from app.api import Api
from app.login import is_valid
from app.logz import create_logger
from app.threadhandler import create_threads, thread_assignment
from app.utils import (
    check_config_for_issues,
    check_license,
    create_progess_object,
    get_current_datetime,
    uncamel_case,
)
from models.recommendations import Recommendations

job_progress = create_progess_object()
logger = create_logger()
regscale_issues = []
defender_recs = []
unique_recs = []
closed = []
updated = []


@click.group()
def defender():
    """Create RegScale issues for each Microsoft Defender Recommendation"""


@defender.command()
def get_recommendations():
    """
    Get Microsoft Defender recommendations and create RegScale
    issues with the information from Microsoft Defender
    """
    # Get Status of Client Application
    app = check_license()
    api = Api(app)
    try:
        # load the config from YAML
        config = app.load_config()
    except FileNotFoundError:
        logger.error("ERROR: No init.yaml file or permission error when opening file.")
        sys.exit()

    # make sure azure tokens are set before continuing
    check_config("azureClientId", "Azure Client ID", config)
    check_config("azureTenantId", "Azure Tenant ID", config)
    check_config("azureSecretId", "Azure Secret", config)

    # check if RegScale token is valid:
    if is_valid(app=app):
        # check the azure token, get a new one if needed
        jwt = check_token(config=config, api=api, app=app)

        # set headers for the data
        headers = {"Content-Type": "application/json", "Authorization": jwt}

        # get Microsoft Defender recommendations
        get_recs(api=api, headers=headers, resource="recommendations")
        logger.info(
            "Found %s Microsoft Defender recommendation(s).", len(defender_recs)
        )

        # get all issues from RegScale where the defenderId field is populated
        get_issues(api=api, config=config, field="defenderId")

        # get the user's max_threads from init.yaml, make sure it is an int
        if not isinstance(config["max_threads"], int):
            # none specified so use 1000
            config["max_threads"] = 1000

        # create progress bars for each threaded task
        with job_progress:
            # see if there are any issues with defender id populated
            if len(regscale_issues) > 0:
                # create progress bar and analyze the RegScale issues
                task1 = job_progress.add_task(
                    f"[#f8b737]Analyzing {len(regscale_issues)} RegScale issue(s)...",
                    total=len(regscale_issues),
                )
                # evaluate open issues in RegScale:
                create_threads(
                    process=evaluate_open_issues,
                    args=(api, config, regscale_issues, defender_recs, task1),
                    thread_count=len(regscale_issues),
                    max_threads=config["max_threads"],
                )

            # compare defender recommendations and RegScale issues
            # while removing duplicates and updating existing RegScale Issues,
            # and adding new unique recommendations to unique_recs global variable
            if len(defender_recs) > 0 and len(regscale_issues) >= 0:
                task2 = job_progress.add_task(
                    f"[#ef5d23]Comparing {len(defender_recs)} recommendation(s) and "
                    + f"{len(regscale_issues)} issue(s)...",
                    total=len(defender_recs),
                )
                create_threads(
                    process=compare_recs_and_issues,
                    args=(api, config, regscale_issues, defender_recs, task2),
                    thread_count=len(defender_recs),
                    max_threads=config["max_threads"],
                )
            # start threads and progress bar for # of issues that need to be created
            if len(unique_recs) > 0:
                task3 = job_progress.add_task(
                    f"[#21a5bb]Creating {len(unique_recs)} issue(s) in RegScale...",
                    total=len(unique_recs),
                )
                create_threads(
                    process=create_issue,
                    args=(api, unique_recs, config, task3),
                    thread_count=len(unique_recs),
                    max_threads=config["max_threads"],
                )
        # start a rich console object
        console = Console()
        # check if issues needed to be created, updated or closed and print the appropriate message
        if (len(unique_recs) + len(updated) + len(closed)) == 0:
            console.print("[green]No changes required for existing RegScale issue(s)!")
        else:
            console.print(
                f"[red] {len(unique_recs)} issue(s) created, {len(updated)} issue(s)"
                + f" updated and {len(closed)} issue(s) were closed in RegScale."
            )
    # Notify user the RegScale token needs to be updated
    else:
        logger.error(
            "Login Error: Invalid RegScale Credentials, please login for a new token."
        )
        sys.exit()


def check_token(config, api, app) -> str:
    """
    check if current Azure token is valid, if not replace it
    """
    # get the token from init.yaml
    current_token = config["azureAccessToken"]
    # check the token if it isn't blank
    if current_token is not None:
        # set the headers
        header = {"Content-Type": "application/json", "Authorization": current_token}
        # test current token by getting recommendations
        token_pass = api.get(
            url="https://api.securitycenter.microsoft.com/api/recommendations",
            headers=header,
        ).status_code
        # check the status code
        if token_pass == 200:
            # token still valid, return it
            token = config["azureAccessToken"]
        elif token_pass == 403:
            # token doesn't have permissions, notify user and exit
            logger.error(
                """ERROR: Incorrect permissions set for application.
                            Cannot retrieve recommendations."""
            )
            sys.exit()
        else:
            # token is no longer valid, get a new one
            token = get_token(api=api, config=config, app=app)
    # token is empty, get a new token
    else:
        token = get_token(api=api, config=config, app=app)
    return token


def get_token(api, config, app):
    """
    function to get a new token
    """
    # set the url and body for request
    url = f'https://login.windows.net/{config["azureTenantId"]}/oauth2/token'
    data = {
        "resource": "https://api.securitycenter.windows.com",
        "client_id": config["azureClientId"],
        "client_secret": config["azureSecretId"],
        "grant_type": "client_credentials",
    }

    # get the data
    response = api.post(
        url=url,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data=data,
    )
    try:
        # try to read the response and parse the token
        res = response.json()
        token = res["access_token"]

        # add the token to init.yaml
        config["azureAccessToken"] = "Bearer " + token

        # write the changes back to file
        app.save_config(config)

        # notify the user we were successful
        logger.info(
            "Azure Login Successful! Init.yaml file was updated with the new access token."
        )

        # return the token string
        return config["azureAccessToken"]
    except JSONDecodeError as ex:
        # notify user we weren't able to get a token and exit
        logger.error("ERROR: Unable to authenticate to Azure Access \n %s", ex)
        sys.exit()


def get_recs(api, headers: dict, resource: str):
    """
    function to get recommendations from Microsoft Defender
    """
    # set the url with the provided resource provided
    url = f"https://api.securitycenter.microsoft.com/api/{resource}?$top=10000"

    # get the data via api call
    response = api.get(url=url, headers=headers)
    try:
        # try to get the values from the api response
        recommendations = response.json()["value"]

        # add the records into the global recommendations for the threads to use
        for rec in recommendations:
            defender_recs.append(Recommendations(id=rec["id"], data=rec))
    except JSONDecodeError:
        # notify user if there was a json decode error from API response and exit
        logger.error("JSON Decode error")
        sys.exit()
    except KeyError:
        # notify user there was no data from API response and exit
        logger.error("No data found.")
        sys.exit()


def assign_severity(score) -> str:
    """
    function to return RegScale severity string, used for payload
    to create new issue via RegScale API
    """
    # check severity score and assign it to the appropriate RegScale severity
    if score >= 7:
        level = "I - High - Significant Deficiency"
    elif 4 <= score < 7:
        level = "II - Moderate - Reportable Condition"
    elif score < 4:
        level = "III - Low - Other Weakness"
    else:
        # if null or not an integer use Not Assigned
        level = "IV - Not Assigned"
    # return severity level
    return level


def get_due_date(score, config) -> str:
    """
    function to return due date based on the severity score of
    the Microsoft Defender recommendation; the values are in the init.yaml
    and if not, use the industry standards
    """
    # check severity score and assign it to the appropriate due date
    # using the init.yaml specified days
    today = datetime.now().strftime("%m/%d/%y")
    if score >= 7:
        days = check_config_for_issues(config=config, issue="defender", key="high")
        due_date = datetime.strptime(today, "%m/%d/%y") + timedelta(days=days)
    elif 4 <= score < 7:
        days = check_config_for_issues(config=config, issue="defender", key="moderate")
        due_date = datetime.strptime(today, "%m/%d/%y") + timedelta(days=days)
    elif score < 4:
        days = check_config_for_issues(config=config, issue="defender", key="low")
        due_date = datetime.strptime(today, "%m/%d/%y") + timedelta(days=days)
    else:
        # if null or not an integer use 45 days
        due_date = datetime.strptime(today, "%m/%d/%y") + timedelta(days=45)
    return due_date.strftime("%Y-%m-%dT%H:%M:%S")


def get_issues(api, config, field: str):
    """
    function to get the RegScale issues for the provided
    integration field that has data populated
    """
    # set the url with the field provided
    url = f'{config["domain"]}/api/issues/getAllByIntegrationField/{field}'
    # get the data via API
    response = api.get(url=url)
    try:
        # try to convert the data to a json
        issues = response.json()
        # iterate through the RegScale issues and append
        # it to the global variable regscale_issues
        for issue in issues:
            regscale_issues.append(Recommendations(id=issue["id"], data=issue))
    except JSONDecodeError as ex:
        # unable to conver the data to a json, display error and exit
        logger.error("ERROR: Unable to retrieve issues from RegScale: \n%s", ex)
        sys.exit()


def format_description(rec: dict, tenant_id: str) -> str:
    """
    function to format the provided dictionary into a html table
    """
    # create empty dictionary to store formatted recommendation headers
    payload = {}

    # create url to Microsoft 365 Defender recommendations, will be added to description
    url = f"https://security.microsoft.com/security-recommendations?tid={tenant_id}"
    url += f'<a href="{url}>{url}</a>"'

    # iterate through recommendation headers and uncamelcase them
    for key in rec.keys():
        # skip the associated threats key, this has a list of guids
        if key.lower() != "associatedthreats":
            # uncamelcase the key
            new_key = uncamel_case(key)

            # store it into our payload dictionary
            payload[new_key] = rec[key]
    # store the html data into description as an unordered html list
    description = '<table style="border: 1px solid;">'

    # iterate through payload to create a html table for description
    for key in payload.keys():
        # check if the value is blank
        if payload[key] is not None and payload[key] != "":
            # add the item as a html data table
            description += (
                f'<tr><td style="border: 1px solid;"><b>{key}</b></td>'
                f'<td style="border: 1px solid;">{payload[key]}</td></tr>'
            )
    # add url to recommendations
    description += (
        '<tr><td style="border: 1px solid;"><b>View Recommendations</b></td>'
        f'<td style="border: 1px solid;">{url}</td></tr>'
    )
    # end the html table
    description += "</table>"

    # return the html table as a string
    return description


def compare_recs_and_issues(args, thread: int):
    """
    function to check for duplicates between issues in RegScale and
    recommendations from Microsoft Defender
    """
    # set local variables with the args that were passed
    api, config, issues, recommendations, task = args

    # find which records should be executed by the current thread
    threads = thread_assignment(
        thread=thread,
        total_items=len(recommendations),
        max_threads=config["max_threads"],
    )

    # iterate through the thread assignment items and process them
    for i in range(len(threads)):
        # set the recommendation for the thread for later use in the function
        rec = recommendations[threads[i]]

        # see if recommendation has been analyzed already
        if not rec.analyzed:
            # change analyzed flag
            rec.analyzed = True

            # set duplication flag to false
            dupe_check = False

            # iterate through the RegScale issues with defenderId populated
            for issue in issues:
                # check if the RegScale defenderId == Windows Defender ID
                if issue.data["defenderId"] == rec.data["id"]:
                    # change the duplication flag to True
                    dupe_check = True
                    # check if the RegScale issue is closed or cancelled
                    if issue.data["status"].lower() in ["closed", "cancelled"]:
                        # reopen RegScale issue because Microsoft Defender has
                        # recommended it again
                        change_issue_status(
                            api=api,
                            config=config,
                            status=check_config_for_issues(
                                config=config, issue="defender", key="status"
                            ),
                            issue=issue.data,
                            rec=rec.data,
                        )
            # check if the recommendation is a duplicate
            if dupe_check is False:
                # append unique recommendation to global unique_reqs
                unique_recs.append(rec)
        job_progress.update(task, advance=1)


def evaluate_open_issues(args, thread: int):
    """
    function to check for Open RegScale issues against Windows
    Defender recommendations and will close the issues that are
    no longer recommended by Microsoft Defender
    """

    # set up local variables from the passed args
    api, config, issues, recs, task = args

    # find which records should be executed by the current thread
    threads = thread_assignment(
        thread=thread, total_items=len(issues), max_threads=config["max_threads"]
    )
    # iterate through the thread assignment items and process them
    for i in range(len(threads)):
        # set the issue for the thread for later use in the function
        issue = issues[threads[i]]

        # check if the issue has already been analyzed
        if not issue.analyzed:
            # set analyzed to true
            issue.analyzed = True

            # convert recommendations list to a dictionary
            recs_dct = {recs[i]["id"]: recs[i] for i in range(len(recs))}

            # get all the ids of the Defender Recommendations and make it a list
            vals = list(recs_dct.keys())

            # check if the RegScale defenderId was recommended by Microsoft Defender
            if issue.data["defenderId"] not in vals and issue.data["status"] not in [
                "Closed",
                "Cancelled",
            ]:
                # the RegScale issue is no longer being recommended and the issue
                # status is not closed or cancelled, we need to close the issue
                change_issue_status(
                    api=api, config=config, status="Closed", issue=issue.data
                )
        job_progress.update(task, advance=1)


def change_issue_status(api, config, status: str, issue: dict, rec: dict = None):
    """
    function to change a RegScale issue to the provided status
    """

    # update issue last updated time, set user to current user and change status
    # to the status that was passed
    issue["lastUpdatedById"] = config["userId"]
    issue["dateLastUpdated"] = get_current_datetime("%Y-%m-%dT%H:%M:%S")
    issue["status"] = status

    # check if rec dictionary was passed, if not create it
    if rec is not None:
        issue["title"] = rec["recommendationName"]
        issue["description"] = format_description(
            rec=rec, tenant_id=config["azureTenantId"]
        )
        issue["severityLevel"] = assign_severity(rec["severityScore"])
        issue["issueOwnerId"] = config["userId"]
        issue["dueDate"] = get_due_date(score=rec["severityScore"], config=config)

    # if we are closing the issue, update the date completed
    if status.lower() == "closed":
        issue["dateCompleted"] = get_current_datetime("%Y-%m-%dT%H:%M:%S")
        issue[
            "description"
        ] += "<p>No longer recommended via Microsoft 365 Defender as of {}</p>".format(
            get_current_datetime("%b %d,%Y")
        )
        closed.append(issue)
        print(issue["id"])
    else:
        issue["dateCompleted"] = ""
        updated.append(issue)

    # use the api to change the status of the given issue
    api.put(url=f'{config["domain"]}/api/issues/{issue["id"]}', json=issue)


def create_issue(args: Tuple, thread: int):
    """
    function to utilize threading and create an issues in RegScale for the assigned thread
    """
    # set up local variables from args passed
    api, recommendations, config, task = args

    # find which records should be executed by the current thread
    threads = thread_assignment(
        thread=thread,
        total_items=len(recommendations),
        max_threads=config["max_threads"],
    )
    # iterate through the thread assignment items and process them
    for i in range(len(threads)):
        # set the recommendation for the thread for later use in the function
        rec = recommendations[threads[i]]

        # check if the recommendation was already created as a RegScale issue
        if not rec.created:
            # set created flag to true
            rec.created = True

            # format the description as a html table
            description = format_description(
                rec=rec.data, tenant_id=config["azureTenantId"]
            )

            # set up the data payload for RegScale API
            data = {
                "title": f'{rec.data["recommendationName"]}',
                "dateCreated": get_current_datetime("%Y-%m-%dT%H:%M:%S"),
                "description": description,
                "severityLevel": assign_severity(rec.data["severityScore"]),
                "issueOwnerId": config["userId"],
                "dueDate": get_due_date(score=rec.data["severityScore"], config=config),
                "identification": "Vulnerability Assessment",
                "status": check_config_for_issues(
                    config=config, issue="defender", key="status"
                ),
                "defenderId": rec.data["id"],
                "vendorName": rec.data["vendor"],
                "parentId": 0,
                "createdById": config["userId"],
                "lastUpdatedById": config["userId"],
                "dateLastUpdated": get_current_datetime("%Y-%m-%dT%H:%M:%S"),
                "isPublic": True,
            }
            # create issue in RegScale via api
            api.post(url=f'{config["domain"]}/api/issues', json=data)
        job_progress.update(task, advance=1)
