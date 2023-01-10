#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""RegScale Email Reminders"""

# standard python imports
import re
import sys
from datetime import datetime
from typing import Tuple

import click
import pandas as pd
from requests import JSONDecodeError
from rich.console import Console

from app.api import Api
from app.logz import create_logger
from app.threadhandler import create_threads, thread_assignment
from app.utils import (
    check_license,
    create_progess_object,
    get_css,
    send_email,
    str_to_date,
    uncamel_case,
)
from models.pipeline import Pipeline

job_progress = create_progess_object()
logger = create_logger()

# empty global lists to be used for threads
tenant_pipeline = []
final_pipeline = []
emails = []


@click.group()
def reminder():
    """Email users of their upcoming Tasks, Issues, Assessments, Data Calls, and Security Plans."""


@reminder.command()
@click.option(
    "--days",
    default=30,
    show_default=True,
    help="RegScale will look for Assessments, Tasks, Issues, Security Plans, "
    + "and Data Calls using today + # of days entered. Default is 30 days.",
)
def send_reminders(days):
    """Get Assessments, Issues, Tasks, Data Calls and Security Plans
    for the users that have email notifications enabled, email comes
    from support@regscale.com"""
    app = check_license()
    api = Api(app)
    config = {}
    try:
        # load the config from YAML
        config = app.load_config()
    except FileNotFoundError:
        logger.error("ERROR: No init.yaml file or permission error when opening file.")

    # make sure config is set before processing
    if "domain" not in config:
        raise ValueError("ERROR: No domain set in the initialization file.")
    if config["domain"] == "":
        raise ValueError("ERROR: The domain is blank in the initialization file.")
    if ("token" not in config) or (config["token"] == ""):
        raise ValueError(
            "ERROR: The token has not been set in the initialization file."
        )

    # set base url, used for other api paths
    base_url = config["domain"] + "/api/"

    # get the user's tenant id, used to get all active
    # users for that instance of the application
    res = api.get(url=base_url + "accounts/find/" + config["userId"]).json()
    ten_id = res["tenantId"]

    # Use the api to get a list of all active users
    # with emailNotifications set to True for
    # the tenant id of the current user
    response = api.get(url=f"{base_url}accounts/{str(ten_id)}/True")

    # try to convert the response to a json file, exit if it errors
    try:
        users = response.json()
    # if error encountered, exit the application
    except JSONDecodeError as ex:
        logger.error("ERROR: Unable to retrieve active users from RegScale: \n%s", ex)
        sys.exit()

    # get the user's max_threads from init.yaml, make sure it is an int
    if not isinstance(config["max_threads"], int):
        # none specified so use 1000
        config["max_threads"] = 1000

    # start a console progress bar and threads for the given task
    # create the threads with the given function, arguments and thread count
    with job_progress:
        task1 = job_progress.add_task(
            f"[#f8b737]Fetching pipeline for {len(users)} user(s)...", total=len(users)
        )

        create_threads(
            process=get_pipeline,
            args=(api, users, base_url, str(days), config, task1),
            thread_count=len(users),
            max_threads=config["max_threads"],
        )

        # start a console progress bar and threads for the given task
        task2 = job_progress.add_task(
            f"[#ef5d23]Analyzing pipeline for {len(tenant_pipeline)} user(s)...",
            total=len(tenant_pipeline),
        )
        create_threads(
            process=analyze_pipeline,
            args=(config, task2),
            thread_count=len(tenant_pipeline),
            max_threads=config["max_threads"],
        )

        # start a console progress bar and threads for the given task
        task3 = job_progress.add_task(
            f"[#21a5bb]Sending an email to {len(final_pipeline)} user(s)...",
            total=len(final_pipeline),
        )
        create_threads(
            process=format_and_email,
            args=(api, config, task3),
            thread_count=len(final_pipeline),
            max_threads=config["max_threads"],
        )

    # create one data table from all pandas data tables in emails
    email_data = pd.concat(emails)

    # create console variable and print # of emails sent successfully
    console = Console()
    console.print(
        f"[green]Successfully sent an email to {email_data.Emailed.sum()} user(s)..."
    )

    # format email to notify person that called the command of the outcome
    email_payload = {
        "id": 0,
        "from": "Support@RegScale.com",
        "emailSenderId": config["userId"],
        "to": res["email"],
        "cc": "",
        "dateSent": "",
        "subject": f"RegScale Reminders Sent to {email_data.Emailed.sum()} User(s)",
        "body": get_css(".\\models\\email_style.css")
        + email_data.to_html(justify="left", index=False)
        .replace('border="1"', 'border="0"')
        .replace("&amp;", "&")
        .replace("&gt;", ">")
        .replace("&lt;", "<")
        .replace("’", "'"),
    }

    # send the email to the user
    send_email(api=api, domain=config["domain"], payload=email_payload)


def get_pipeline(args: Tuple, thread: int):
    """
    function used by threads to send emails to users with upcoming and/or outstanding
    Tasks, Assessments, Data Calls, Issues, Security Plans
    """
    # set up my args from the args tuple
    api, all_users, base_url, days, config, task = args

    # get the thread assignment for the current thread
    threads = thread_assignment(
        thread=thread, total_items=len(all_users), max_threads=config["max_threads"]
    )

    # check the Assessments, Issues, Tasks, Data Calls and Security Plans
    # for each user in all users dictionary and store them in the list
    for i in range(len(threads)):
        user = all_users[threads[i]]

        # get all the assessments, issues, tasks, data calls and security plans
        # for the user we can email, using the # of days entered by the user
        # if no days were entered, the default is 30 days
        assessments = api.get(
            url=f"{base_url}assessments/userOpenItemsDays/{user['id']}/{days}"
        ).json()
        issues = api.get(
            url=f"{base_url}issues/userOpenItemsDays/{user['id']}/{days}"
        ).json()
        tasks = api.get(
            url=f"{base_url}tasks/userOpenItemsDays/{user['id']}/{days}"
        ).json()
        data_calls = api.get(
            url=f"{base_url}datacalls/userOpenItemsDays/{user['id']}/{days}"
        ).json()
        sec_plans = api.get(
            url=f"{base_url}securityplans/userOpenItemsDays/{user['id']}/{days}"
        ).json()

        # create list that has Tuples of the user's pipeline and categories
        pipelines = {
            "Assessments": {"Pipeline": assessments},
            "Issues": {"Pipeline": issues},
            "Tasks": {"Pipeline": tasks},
            "Data Calls": {"Pipeline": data_calls},
            "Security Plans": {"Pipeline": sec_plans},
        }

        # create variable to see how many total objects are in the user's pipeline
        total_tasks = 0

        # iterate through the user's pipeline tallying their items
        for pipeline in pipelines.values():
            total_tasks += len(pipeline["Pipeline"])

        # check the total # of items in their pipeline
        if total_tasks > 0:
            # map and add the data to a global variable
            tenant_pipeline.append(
                Pipeline(
                    email=user["email"],
                    fullName=f'{user["firstName"]} {user["lastName"]}',
                    pipelines=pipelines,
                    totalTasks=total_tasks,
                )
            )
        job_progress.update(task, advance=1)


def analyze_pipeline(args: Tuple, thread: int):
    """
    function to set up data tables from the user's pipeline
    """
    config, task = args

    # get the assigned threads
    threads = thread_assignment(
        thread=thread,
        total_items=len(tenant_pipeline),
        max_threads=config["max_threads"],
    )
    for i in range(len(threads)):
        # get the pipeline from the global tenant_pipeline
        pipelines = tenant_pipeline[threads[i]].pipelines

        # set up local variable for user pipeline
        user_pipeline = []

        # check if the user has already been analyzed
        if not tenant_pipeline[threads[i]].analyzed:
            # change the user's status to analyzed
            tenant_pipeline[threads[i]].analyzed = True

            # start out in the beginning of the pipelines
            # and iterate through all of their items
            for pipe in pipelines:
                # creating variable to store html table for the user's email
                prelim_pipeline = []

                # iterate through the items in the pipeline category while
                # creating legible table headers
                for item in pipelines[pipe]["Pipeline"]:
                    # create list variable to store the renamed column names
                    headers = []

                    # iterate through all columns for the item and see if the header
                    # has to be changed to Title Case and if the data has to revalued
                    for key in item.keys():
                        # change the camelcase header to a Title Case Header
                        fixed_key = uncamel_case(key)

                        # check the keys to revalue the data accordingly
                        if key == "uuid":
                            # create html url using data for the html table
                            href = f'{config["domain"]}/{pipe.lower().replace(" ", "")}'
                            href += f'/form/{item["id"]}'
                            # have to add an if clause for mso to display the view button correctly
                            url = (
                                '<!--[if mso]><v:roundrect xmlns:v="urn:schemas-microsoft-com:vml"'
                                f'xmlns:w="urn:schemas-microsoft-com:office:word" href="{href}" '
                                'style="height:40px;v-text-anchor:middle;width:60px;" arcsize="5%" '
                                'strokecolor="#22C2DC" fillcolor="#1DC3EB"><w:anchorlock/><center'
                                ' style="color:#ffffff;font-family:Roboto, Arial, sans-serif;font'
                                '-size:14px;">View</center></v:roundrect><![endif]-->'
                            )
                            url += f'<a href="{href}" style="mso-hide:all;">View</a>'

                            # replace the UUID with the HTML url
                            item[key] = url

                            # append the header to the headers list
                            headers.append("Action")
                        # check if the item is a date field and reformat it
                        elif "date" in key.lower() or "finish" in key.lower():
                            # convert string to a date
                            date = str_to_date(item[key])

                            # reformat the date to a legible string
                            item[key] = datetime.strftime(date, "%b %d, %Y")

                            # append the Title Case header to the headers list
                            headers.append(fixed_key)
                        # if it is the id field, make it all caps
                        elif key == "id":
                            # change the key to all uppercase
                            headers.append(key.upper())
                        # see if the data is a string and has any html elements
                        elif isinstance(item[key], str) and "<" in item[key]:
                            # replace </br> with \n
                            text = item[key].replace("</br>", "\n")

                            # strip other html codes from string values
                            item[key] = re.sub("<[^<]+?>", "", text)

                            # append the Title Case header to headers
                            headers.append(fixed_key)
                        # the data doesn't have to be reformatted, append the Title Case Header
                        else:
                            headers.append(fixed_key)
                    # add it to the final pipeline for the user
                    prelim_pipeline.append(item)
                # check to see if there is an item for the bucket before
                # appending it to the final_pipeline for the email
                if len(prelim_pipeline) > 0:
                    # convert the item to a pandas data table
                    data = pd.DataFrame(prelim_pipeline)

                    # replace the columns with our legible data headers
                    data.columns = headers

                    # append the data item and bucket to our local user_pipeline list
                    user_pipeline.append({"bucket": pipe, "items": data})
            # add the user's pipeline data to the global pipeline for the emails
            final_pipeline.append(
                Pipeline(
                    email=tenant_pipeline[threads[i]].email,
                    fullName=tenant_pipeline[threads[i]].fullName,
                    pipelines=user_pipeline,
                    totalTasks=tenant_pipeline[threads[i]].totalTasks,
                    analyzed=True,
                )
            )
        job_progress.update(task, advance=1)


def format_and_email(args: Tuple, thread: int):
    """
    function to email all users with an html formatted email
    """
    # set up my args from the args tuple
    api, config, task = args

    threads = thread_assignment(
        thread=thread,
        total_items=len(final_pipeline),
        max_threads=config["max_threads"],
    )

    # get assigned threads
    for i in range(len(threads)):
        # get the user's pipeline details
        email = final_pipeline[threads[i]].email
        total_tasks = final_pipeline[threads[i]].totalTasks

        # create list to store the html tables
        tables = []

        # see if the user has been emailed already
        if not final_pipeline[threads[i]].emailed:
            # set the emailed flag to true
            final_pipeline[threads[i]].emailed = True

            # iterate through all items in final_pipeline to
            # set up data tables as a html tables using pandas
            for item in final_pipeline[threads[i]].pipelines:
                # add a header for the data table
                tables.append(f'<h1>{item["bucket"]}</h1>')

                # add data table to our tables list, format table to have no border
                # and justify everything to the left
                tables.append(
                    item["items"]
                    .to_html(justify="left", index=False)
                    .replace('border="1"', 'border="0"')
                )
            # join all the items in tables and seperate them all with a </br> tag
            tables = "</br>".join(tables)

            # fix any broken html tags
            tables = (
                tables.replace("&amp;", "&")
                .replace("&gt;", ">")
                .replace("&lt;", "<")
                .replace("’", "'")
            )

            # create email payload
            email_payload = {
                "id": 0,
                "from": "Support@RegScale.com",
                "emailSenderId": config["userId"],
                "to": email,
                "cc": "",
                "dateSent": "",
                "subject": f"RegScale Reminder: {total_tasks} Upcoming Items",
                "body": get_css(".\\models\\email_style.css") + tables,
            }

            # send the email and get the response
            emailed = send_email(
                api=api, domain=config["domain"], payload=email_payload
            )

            # set up dict to use for pandas data
            data = {
                "Email Address": '<!--[if mso]><v:roundrect xmlns:v="urn:schemas-microsoft-com:vml"'
                'xmlns:w="urn:schemas-microsoft-com:office:word" href="mailto:'
                f'{email}"style="height:auto;v-text-anchor:middle;mso-width-'
                'percent:150;" arcsize="5%" strokecolor="#22C2DC" fillcolor='
                '"#1DC3EB"><w:anchorlock/><center style="color:#ffffff;font-'
                f'family:Roboto, Arial, sans-serif;font-size:14px;">{email}'
                '</center></v:roundrect><![endif]--><a href="mailto:'
                f'{email}" style="mso-hide:all;">{email}</a>',
                "User Name": final_pipeline[threads[i]].fullName,
                "Total Tasks": total_tasks,
                "Emailed": emailed,
            }
            table = pd.DataFrame([data])
            emails.append(table)
        job_progress.update(task, advance=1)
