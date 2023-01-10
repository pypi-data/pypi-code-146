#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" standard python imports """
import json
import sys
from copy import deepcopy
from os import mkdir, path, sep

import click
import requests
from rich.progress import track

from app.api import Api
from app.application import Application
from app.logz import create_logger
from app.utils import check_license

logger = create_logger()


# Create group to handle ServiceNow integration
@click.group()
def servicenow():
    """Auto-assigns incidents in ServiceNow for remediation"""
    check_license()


#####################################################################################################
#
# PROCESS ISSUES TO ServiceNow
# ServiceNow REST API Docs: https://docs.servicenow.com/bundle/paris-application-development/page/build/applications/concept/api-rest.html
# Use the REST API Explorer in ServiceNow to select table, get URL, and select which fields to populate
#
#####################################################################################################
@servicenow.command()
@click.option(
    "--issue_level",
    prompt="Enter the Level of Issues to Process",
    help="RegScale will process all issues this level or higher.  Options include: LOW, MEDIUM, HIGH, CRITICAL.",
)
@click.option(
    "--regscale_id",
    prompt="Enter the RegScale Record ID",
    help="RegScale will create and update issues as children of this record.",
)
@click.option(
    "--regscale_module",
    prompt="Enter the RegScale Module name",
    help="Enter the RegScale module.  Options include: projects, policies, supplychain, securityplans, components.",
)
@click.option(
    "--snow_assignment_group",
    prompt="Enter the name of the project in Jira",
    help="RegScale will sync the issues for the record to this ServiceNow assignment group.",
)
@click.option(
    "--snow_incident_type",
    prompt="Enter the ServiceNow incident type",
    help="Enter the ServiceNow incident type to use when creating new issues from RegScale",
)
def issues(
    issue_level, regscale_id, regscale_module, snow_assignment_group, snow_incident_type
):
    """Process issues to ServiceNow"""

    app = Application()

    reg_api = Api(app)
    logger = create_logger()
    # check issue level parameter
    if (
        str(issue_level).upper() != "LOW"
        and str(issue_level).upper() != "MEDIUM"
        and str(issue_level).upper() != "HIGH"
        and str(issue_level).upper() != "CRITICAL"
    ):
        logger.error(
            "You must select one of the following issue levels: LOW, MEDIUM, HIGH, CRITICAL"
        )
        sys.exit(1)

    # load the config from YAML
    config = app.config

    # get secrets
    snow_url = app.config["snowUrl"]
    snow_user = app.config["snowUserName"]
    snow_pwd = app.config["snowPassword"]

    # set headers
    url_issues = (
        config["domain"]
        + "/api/issues/getAllByParent/"
        + str(regscale_id)
        + "/"
        + str(regscale_module).lower()
    )
    regscale_headers = {"Accept": "application/json", "Authorization": config["token"]}
    update_headers = {"Authorization": config["token"]}

    # get the existing issues for the parent record that are already in RegScale
    logger.info("Fetching full issue list from RegScale")
    issue_response = reg_api.get(url_issues, headers=regscale_headers)
    # check for null/not found response
    if issue_response.status_code == 204:
        logger.warning("No existing issues for this RegScale record.")
        issues_data = []
    else:
        try:
            issues_data = issue_response.json()
        except requests.RequestException as rex:
            logger.error("ERROR: Unable to fetch issues from RegScale\n%s", rex)
            sys.exit(1)

    # make directory if it doesn't exist
    if path.exists("artifacts") is False:
        mkdir("artifacts")
        logger.warning(
            "Artifacts directory does not exist.  Creating new directory for artifact processing."
        )
    else:
        logger.info(
            "Artifacts directory exists.  This directly will store output files from all processing."
        )

    # write out issues data to file
    if len(issues_data) > 0:
        with open(
            f"artifacts{sep}existingRecordIssues.json", "w", encoding="utf-8"
        ) as outfile:
            outfile.write(json.dumps(issues_data, indent=4))
        logger.info(
            "Writing out RegScale issue list for Record # %s to the artifacts folder (see existingRecordIssues.json)",
            str(regscale_id),
        )
    logger.info(
        "%s existing issues retrieved for processing from RegScale.",
        str(len(issues_data)),
    )

    # loop over the issues and write them out
    int_new = 0
    regscale_issue_url = config["domain"] + "/api/issues/"
    snow_api = deepcopy(
        reg_api
    )  # no need to instantiate a new config, just copy object
    snow_api.auth = (snow_user, snow_pwd)
    for iss in issues_data:
        try:
            # build the issue URL for cross linking
            str_issue_url = config["domain"] + "/issues/form/" + str(iss["id"])
            if "serviceNowId" not in iss:
                iss["serviceNowId"] = ""
            # see if the ServiceNow ticket already exists
            if iss["serviceNowId"] == "":
                # create a new ServiceNow incident
                snow_incident = {
                    "description": iss["description"],
                    "short_description": iss["title"],
                    "assignment_group": snow_assignment_group,
                    "due_date": iss["dueDate"],
                    "comments": "RegScale Issue #"
                    + str(iss["id"])
                    + " - "
                    + str_issue_url,
                    "state": "New",
                    "urgency": snow_incident_type,
                }

                # create a SNOW incident
                incident_url = snow_url + "api/now/table/incident"
                snow_header = {
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                }
                try:
                    # intNew += 1
                    response = snow_api.post(
                        url=incident_url,
                        headers=snow_header,
                        json=snow_incident,
                    )
                    if not response.raise_for_status():
                        int_new += 1
                    snow_response = response.json()
                    logger.debug(snow_response)
                    # log the result
                    logger.info(
                        "SNOW Incident ID %s created", snow_response["result"]["sys_id"]
                    )
                    # get the SNOW ID
                    iss["serviceNowId"] = snow_response["result"]["sys_id"]
                    # update the issue in RegScale
                    str_update_url = regscale_issue_url + str(iss["id"])
                    try:
                        update_response = reg_api.put(
                            url=str_update_url, headers=update_headers, json=iss
                        )
                        if not update_response.raise_for_status():
                            logger.info(
                                "%i) RegScale Issue # %s was updated with the ServiceNow link.",
                                int_new,
                                str(iss["id"]),
                            )
                        else:
                            logger.error(
                                "Unable to update Regscale Issue #%i", iss["id"]
                            )
                    except requests.exceptions.RequestException as ex:
                        # problem updating RegScale
                        logger.error("Unable to update RegScale: %s", ex)
                        break
                except requests.exceptions.RequestException as ex:
                    # problem creating in ServiceNow
                    logger.error(
                        "Unable to create incident %s in ServiceNow...\n%s",
                        snow_incident,
                        ex,
                    )
        except KeyError as kex:
            logger.error("Unable to find key: %s", kex)

    # output the final result
    logger.info("%i new issue incidents opened in ServiceNow.", int_new)


@servicenow.command()
def sync_work_notes():
    """Sync work notes from ServiceNow to existing issues"""
    sync_notes_to_regscale()


def sync_notes_to_regscale():
    """Sync work notes from ServiceNow to existing issues"""
    app = Application()
    reg_api = Api(app)
    data = []
    # get secrets
    snow_url = app.config["snowUrl"]
    snow_user = app.config["snowUserName"]
    snow_pwd = app.config["snowPassword"]
    incident_url = snow_url + "api/now/table/incident"
    snow_api = deepcopy(
        reg_api
    )  # no need to instantiate a new config, just copy object
    snow_api.auth = (snow_user, snow_pwd)
    offset = 0
    limit = 500
    query = "&sysparm_query=GOTO123TEXTQUERY321=regscale"
    result, offset = query_incidents(
        api=snow_api, incident_url=incident_url, offset=offset, limit=limit, query=query
    )
    data = data + result
    while len(result) > 0:
        result, offset = query_incidents(
            api=snow_api,
            incident_url=incident_url,
            offset=offset,
            limit=limit,
            query=query,
        )
        data = data + result
    process_work_notes(config=app.config, api=reg_api, data=data)


def process_work_notes(config: dict, api: Api, data: list):
    "Process and Sync the worknotes to RegScale."
    for dat in track(
        data,
        description=f"Processing {len(data):,} ServiceNow incidents",
    ):
        sys_id = str(dat["sys_id"])
        update_issues = []
        try:
            regscale_response = api.get(
                url=config["domain"] + f"/api/issues/findByServiceNowId/{sys_id}"
            )
            if regscale_response.raise_for_status():
                logger.warning("Cannot find RegScale issue with a incident %s", sys_id)
            else:
                logger.debug("Processing ServiceNow Issue # %s", sys_id)
                work_item = dat["work_notes"]
                if work_item:
                    issue = regscale_response.json()[0]
                    if work_item not in issue["description"]:
                        logger.info(
                            "Updating work item for RegScale issue # %s and ServiceNow incident # %s",
                            issue["id"],
                            sys_id,
                        )
                        issue["description"] = (
                            f"<strong>ServiceNow Work Notes: </strong>{work_item}<br/>"
                            + issue["description"]
                        )
                        update_issues.append(issue)
        except requests.HTTPError:
            logger.warning(
                "HTTP Error:  Unable to find RegScale issue with ServiceNow incident ID of %s",
                sys_id,
            )
    if len(update_issues) > 0:
        logger.info(update_issues)
        api.update_server(
            url=config["domain"] + "/api/issues",
            message=f"Updating {len(update_issues)} issues..",
            json_list=update_issues,
        )
    else:
        logger.warning(
            "No ServiceNow work items found, No RegScale issues were updated."
        )
        sys.exit(0)


def query_incidents(api: Api, incident_url: str, offset: int, limit: int, query: str):
    """Paginate through query results"""
    offset_param = f"&sysparm_offset={str(offset)}"
    url = incident_url + f"?sysparm_limit={limit}{offset_param}{query}"
    logger.debug(url)
    result = api.get(url=url).json()["result"]
    offset += limit
    logger.debug(len(result))
    return result, offset
