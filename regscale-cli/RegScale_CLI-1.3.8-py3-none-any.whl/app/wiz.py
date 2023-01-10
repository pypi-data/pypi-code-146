#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# standard python imports

import datetime
import json
import sys
from datetime import date
from os import mkdir, path, sep

import click
import requests
import yaml
from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport

from app.api import Api
from app.logz import create_logger
from app.utils import check_config_for_issues, check_license
from models.wiz import AssetType

logger = create_logger()

# Private and global variables
AUTH0_URLS = [
    "https://auth.wiz.io/oauth/token",
    "https://auth0.gov.wiz.io/oauth/token",
    "https://auth0.test.wiz.io/oauth/token",
    "https://auth0.demo.wiz.io/oauth/token",
]
COGNITO_URLS = [
    "https://auth.app.wiz.io/oauth/token",
    "https://auth.gov.wiz.io/oauth/token",
    "https://auth.test.wiz.io/oauth/token",
    "https://auth.demo.wiz.io/oauth/token",
]

# Create group to handle Wiz.io integration
@click.group()
def wiz():
    """Integrates continuous monitoring data from Wiz.io"""


#####################################################################################################
#
# AUTHENTICATE TO WIZ
#
#####################################################################################################
@wiz.command()
def authenticate():
    """Authenticate to Wiz."""
    app = check_license()
    api = Api(app)
    # Login with service account to retrieve a 24 hour access token that updates YAML file
    logger.info("Authenticating - Loading configuration from init.yaml file")

    # load the config from YAML
    with open("init.yaml", "r") as stream:
        config = yaml.safe_load(stream)

    # get secrets
    if "wizClientId" in config:
        client_id = config["wizClientId"]
    else:
        logger.error("No Wiz Client ID provided in the init.yaml file.")
        sys.exit(1)
    if "wizClientSecret" in config:
        client_secret = config["wizClientSecret"]
    else:
        logger.error("No Wiz Client Secret provided in the init.yaml file.")
        sys.exit(1)
    if "wizAuthUrl" in config:
        wiz_auth_url = config["wizAuthUrl"]
    else:
        logger.error("No Wiz Authentication URL provided in the init.yaml file.")
        sys.exit(1)

    # get access token
    headers = {"content-type": "application/x-www-form-urlencoded"}
    # payload = {f"grant_type=client_credentials&client_id={client_id}&client_secret={client_secret}&audience=beyond-api"}

    # login and get token
    logger.info("Attempting to retrieve OAuth token from Wiz.io")
    token, scope = get_token(
        api=api,
        client_id=client_id,
        client_secret=client_secret,
        token_url=wiz_auth_url,
    )

    # assign values

    config["wizAccessToken"] = token
    config["wizScope"] = scope

    # write our the result to YAML
    # write the changes back to file
    try:
        with open(r"init.yaml", "w") as file:
            yaml.dump(config, file)
        logger.info(
            "Access token written to init.yaml call to support future API calls.  Token is good for 24 hours."
        )
    except Exception:
        logger.error("Error opening init.yaml (permissions) or file does not exist.")


def get_token(api: Api, client_id: str, client_secret: str, token_url: str) -> tuple:
    """Return Wiz.io token

    Args:
        api (Api): api instance
        client_id (str): client id
        client_secret (str): client secret
        token_url (str): token url

    Raises:
        Exception: general exception

    Returns:
        tuple(str,str): tuple of token and scope.
    """
    logger.info("Getting a token")
    response = api.post(
        url=token_url,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data=generate_authentication_params(client_id, client_secret, token_url),
    )
    logger.debug(response.json())
    if response.status_code != requests.codes.ok:
        raise Exception(
            f"Error authenticating to Wiz [{response.status_code}] - {response.text}"
        )
    response_json = response.json()
    token = response_json.get("access_token")
    scope = response_json.get("scope")
    if not token:
        raise Exception(
            f'Could not retrieve token from Wiz: {response_json.get("message")}'
        )
    if not scope:
        raise Exception("Could not retrieve scope from Wiz")
    logger.info("SUCCESS: Wiz.io access token successfully retrieved.")
    return token, scope


def generate_authentication_params(client_id, client_secret, token_url):
    """Create the Correct Parameter format based on URL."""
    if token_url in AUTH0_URLS:
        return {
            "grant_type": "client_credentials",
            "audience": "beyond-api",
            "client_id": client_id,
            "client_secret": client_secret,
        }
    elif token_url in COGNITO_URLS:
        return {
            "grant_type": "client_credentials",
            "audience": "wiz-api",
            "client_id": client_id,
            "client_secret": client_secret,
        }
    else:
        raise Exception("Invalid Token URL")


#####################################################################################################
#
# PROCESS INVENTORY FROM WIZ
#
#####################################################################################################
@wiz.command()
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
# flake8: noqa: C901
def inventory(regscale_id, regscale_module):
    """Process inventory list from Wiz"""
    app = check_license()
    api = Api(app)
    # load the config from YAML
    with open("init.yaml", "r") as stream:
        config = yaml.safe_load(stream)

    # get secrets
    url = config["wizUrl"]
    token = config["wizAccessToken"]
    strUser = config["userId"]
    strExcludes = config["wizExcludes"]

    # set health check URL
    url_assets = (
        config["domain"]
        + "/api/assets/getAllByParent/"
        + str(regscale_id)
        + "/"
        + str(regscale_module)
    )

    # set headers
    headersGet = {"Accept": "application/json", "Authorization": config["token"]}

    # get the full list of assets
    logger.info("Fetching full asset list from RegScale")
    try:
        assetResponse = api.get(url=url_assets, headers=headersGet)
        if assetResponse.status_code != 204:
            assetData = assetResponse.json()
            logger.info(str(len(assetData)) + " total assets retrieved from RegScale.")

        else:
            assetData = None
    except Exception as e:
        logger.error("ERROR: Unable to retrieve asset list from RegScale.")

        logger.error(e)
        sys.exit(1)

    # output the results of the Wiz assets
    with open(f"artifacts{sep}RegScaleAssets.json", "w") as outfile:
        outfile.write(json.dumps(assetData, indent=4))

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

    # The GraphQL query that defines which data you wish to fetch.
    query = gql(
        """
  query GraphSearch(
      $query: GraphEntityQueryInput
      $controlId: ID
      $projectId: String!
      $first: Int
      $after: String
      $fetchTotalCount: Boolean!
      $quick: Boolean
      $fetchPublicExposurePaths: Boolean = false
      $fetchInternalExposurePaths: Boolean = false
      $fetchIssueAnalytics: Boolean = false
    ) {
      graphSearch(
        query: $query
        controlId: $controlId
        projectId: $projectId
        first: $first
        after: $after
        quick: $quick
      ) {
        totalCount @include(if: $fetchTotalCount)
        maxCountReached @include(if: $fetchTotalCount)
        pageInfo {
          endCursor
          hasNextPage
        }
        nodes {
          entities {
            id
            name
            type
            properties
            hasOriginalObject
            userMetadata {
              isInWatchlist
              isIgnored
              note
            }
            technologies {
              id
              icon
            }
            issueAnalytics: issues(filterBy: { status: [IN_PROGRESS, OPEN] })
              @include(if: $fetchIssueAnalytics) {
              lowSeverityCount
              mediumSeverityCount
              highSeverityCount
              criticalSeverityCount
            }
            publicExposures(first: 10) @include(if: $fetchPublicExposurePaths) {
              nodes {
                ...NetworkExposureFragment
              }
            }
            otherSubscriptionExposures(first: 10)
              @include(if: $fetchInternalExposurePaths) {
              nodes {
                ...NetworkExposureFragment
              }
            }
            otherVnetExposures(first: 10)
              @include(if: $fetchInternalExposurePaths) {
              nodes {
                ...NetworkExposureFragment
              }
            }
          }
          aggregateCount
        }
      }
    }

    fragment NetworkExposureFragment on NetworkExposure {
      id
      portRange
      sourceIpRange
      destinationIpRange
      path {
        id
        name
        type
        properties
        issueAnalytics: issues(filterBy: { status: [IN_PROGRESS, OPEN] })
          @include(if: $fetchIssueAnalytics) {
          lowSeverityCount
          mediumSeverityCount
          highSeverityCount
          criticalSeverityCount
        }
      }
    }
"""
    )

    # The variables sent along with the above query
    variables = {
        "fetchPublicExposurePaths": True,
        "fetchInternalExposurePaths": False,
        "fetchIssueAnalytics": False,
        "first": 50,
        "query": {
            "type": ["TECHNOLOGY"],
            "select": True,
            "relationships": [
                {
                    "type": [{"type": "HAS_TECH", "reverse": True}],
                    "with": {"type": ["ANY"], "select": True},
                }
            ],
        },
        "projectId": "*",
        "fetchTotalCount": False,
        "quick": False,
        "after": "100",
    }

    # fetch the list of assets
    transport = AIOHTTPTransport(url=url, headers={"Authorization": "Bearer " + token})
    client = Client(
        transport=transport, fetch_schema_from_transport=True, execute_timeout=55
    )

    # loop through until all records have been fetched
    intFetch = 1
    assets = {}
    while intFetch > 0:
        # Fetch the query!
        try:
            wizAssets = client.execute(query, variable_values=variables)
            logger.info("Wiz Fetch #" + str(intFetch) + " completed")
        except Exception:
            # error - unable to retrieve Wiz assets
            logger.error(
                "Error - unable to fetch Wiz assets.  Ensure access token is valid and correct Wiz API endpoint was provided."
            )

            sys.exit(1)
        if intFetch == 1:
            # initialize the object
            assets = wizAssets
        else:
            # append any new records
            for n in wizAssets["graphSearch"]["nodes"]:
                assets["graphSearch"]["nodes"].append(n)

        # get page info
        pageInfo = wizAssets["graphSearch"]["pageInfo"]

        # Check if there are additional results
        if pageInfo["hasNextPage"]:
            # Update variables to fetch the next batch of items
            variables["after"] = pageInfo["endCursor"]
            # update loop cursor
            intFetch += 1
        else:
            # No additional results. End the loop/
            intFetch = 0

    # output the results of the Wiz assets
    with open(f"artifacts{sep}wizAssets.json", "w") as outfile:
        outfile.write(json.dumps(assets, indent=4))
    logger.info(
        str(len(assets["graphSearch"]["nodes"]))
        + " assets retrieved for processing from Wiz.io."
    )

    # get the Wiz nodes to process
    processing = assets["graphSearch"]["nodes"]

    # loop over the results
    intAssetLoop = 0
    newAssets = []
    updateAssets = []
    for node in processing:
        # ignore built-in service principals
        if node["entities"][0]["name"] not in strExcludes:
            intAssetLoop += 1
            logger.info(
                str(intAssetLoop)
                + ") "
                + node["entities"][1]["type"]
                + ": "
                + node["entities"][1]["name"]
            )

            # get the Wiz ID
            strWizId = node["entities"][1]["id"]

            # see if it already exists
            bFound = False
            updateAsset = None
            if assetData is not None:
                for ast in assetData:
                    if "wizId" in ast:
                        if ast["wizId"] == strWizId:
                            bFound = True
                            updateAsset = ast
                            break

            # get the Wiz metadata
            strMetadata = json.dumps(node["entities"])

            # see if a new record or already exists
            if bFound is True:
                # update the record
                updateAsset["name"] = node["entities"][1]["name"]
                updateAsset["assetType"] = node["entities"][1]["type"]
                updateAsset["lastUpdatedById"] = strUser
                updateAsset["wizInfo"] = strMetadata
                updateAsset["assetCategory"] = map_category(node["entities"][1]["type"])
                updateAssets.append(updateAsset)

            else:
                # create a new asset
                newAsset = {
                    "id": 0,
                    "name": node["entities"][1]["name"],
                    "otherTrackingNumber": "",
                    "serialNumber": "",
                    "ipAddress": "",
                    "macAddress": "",
                    "manufacturer": "",
                    "model": "",
                    "assetOwnerId": strUser,
                    "operatingSystem": "",
                    "osVersion": "",
                    "assetType": node["entities"][1]["type"],
                    "categoryType": "",
                    "cmmcAssetType": "",
                    "cpu": 0,
                    "ram": 0,
                    "diskStorage": 0,
                    "description": "string",
                    "endOfLifeDate": None,
                    "purchaseDate": None,
                    "status": "Active (On Network)",
                    "wizId": strWizId,
                    "wizInfo": strMetadata,
                    "facilityId": None,
                    "orgId": None,
                    "parentId": int(regscale_id),
                    "parentModule": str(regscale_module),
                    "createdById": strUser,
                    "dateCreated": None,
                    "lastUpdatedById": strUser,
                    "dateLastUpdated": None,
                }
                newAsset["assetCategory"] = map_category(node["entities"][1]["type"])
                newAssets.append(newAsset)

    # output the results of the Wiz assets
    with open(f"artifacts{sep}wizNewAssets.json", "w") as outfile:
        outfile.write(json.dumps(newAssets, indent=4))
    logger.info(
        str(len(newAssets)) + " new assets processed and ready for upload into RegScale"
    )

    # output the results of the Wiz assets
    with open(f"artifacts{sep}wizUpdateAssets.json", "w") as outfile:
        try:
            logger.debug(updateAssets)
            outfile.write(json.dumps(updateAssets, indent=4))
        except ValueError as vex:
            logger.warning("Unable to save file \n%s", vex)
    logger.info(
        str(len(updateAssets))
        + " existing assets processed and ready to update in RegScale"
    )

    # update each existing Wiz issue in RegScale
    urlCreateAsset = config["domain"] + "/api/assets/"
    header = {"Authorization": config["token"]}

    # loop over new assets and create new in RegScale
    for n in newAssets:
        try:
            assetUpload = api.post(url=urlCreateAsset, headers=header, json=n)
            assetUploadResponse = assetUpload.json()
            # output the result
            logger.info(
                "Success: New asset created in RegScale # "
                + str(assetUploadResponse["id"])
                + " for Wiz Asset: "
                + assetUploadResponse["name"]
            )
        except Exception:
            logger.error("ERROR: Unable to create asset: " + n["otherTrackingNumber"])

    # loop over existing assets and update in RegScale
    for ast in updateAssets:
        urlUpdateAsset = config["domain"] + "/api/assets/" + str(ast["id"])
        try:
            assetUpload = api.put(urlUpdateAsset, headers=header, json=ast)
            assetUploadResponse = assetUpload.json()
            # output the result
            logger.info(
                "Success: Asset updated in RegScale # "
                + str(assetUploadResponse["id"])
                + " for Wiz Asset: "
                + assetUploadResponse["name"]
            )
        except Exception:
            logger.error("ERROR: Unable to update asset: " + ast["wizId"])
            logger.debug(ast["assetCategory"])


#####################################################################################################
#
# PROCESS ISSUES FROM WIZ
#
#####################################################################################################
@wiz.command()
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
# flake8: noqa: C901
def issues(issue_level, regscale_id, regscale_module):
    """Process issues from Wiz"""
    app = check_license()
    api = Api(app)
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
    url = config["wizUrl"]
    token = config["wizAccessToken"]
    str_user = config["userId"]

    # set headers
    url_issues = (
        config["domain"]
        + "/api/issues/getAllByParent/"
        + str(regscale_id)
        + "/"
        + str(regscale_module).lower()
    )
    headersGet = {"Accept": "application/json", "Authorization": config["token"]}

    # get the existing issues for the parent record that are already in RegScale
    logger.info("Fetching full issue list from RegScale")
    logger.debug(headersGet)
    issueResponse = api.get(url=url_issues, headers=headersGet)
    # check for null/not found response
    if issueResponse.status_code == 204:
        logger.warning("No existing issues for this RegScale record.")
        issuesData = []
    else:
        try:
            issuesData = issueResponse.json()
        except Exception:
            logger.error("ERROR: Unable to fetch issues from RegScale")
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
    if len(issuesData) > 0:
        with open(f"artifacts{sep}existingRecordIssues.json", "w") as outfile:
            outfile.write(json.dumps(issuesData, indent=4))
        logger.info(
            "Writing out RegScale issue list for Record #"
            + str(regscale_id)
            + " to the artifacts folder (see existingRecordIssues.json)"
        )
    logger.info(
        str(len(issuesData))
        + " existing issues retrieved for processing from RegScale."
    )

    # The GraphQL query that defines which data you wish to fetch.
    query = gql(
        """
    query IssuesTable($filterBy: IssueFilters, $first: Int, $after: String, $orderBy: IssueOrder) {
        issues(filterBy: $filterBy, first: $first, after: $after, orderBy: $orderBy) {
        nodes {
            ...IssueDetails
        }
        pageInfo {
            hasNextPage
            endCursor
        }
        totalCount
        informationalSeverityCount
        lowSeverityCount
        mediumSeverityCount
        highSeverityCount
        criticalSeverityCount
        uniqueEntityCount
        }
    }

        fragment IssueDetails on Issue {
        id
        control {
        id
        name
        query
        securitySubCategories {
          id
          externalId
          title
          description
          category {
            id
            externalId
            name
            framework {
              id
              name
            }
          }
        }
        }
        createdAt
        updatedAt
        projects {
        id
        name
        businessUnit
        riskProfile {
            businessImpact
        }
        }
        status
        severity
        entity {
        id
        name
        type
        }
        entitySnapshot {
        id
        type
        name
        }
        note
        serviceTicket {
        externalId
        name
        url
        }
    }
    """
    )

    # The variables sent along with the above query
    variables = {
        "first": 25,
        "filterBy": {"status": ["OPEN", "IN_PROGRESS"]},
        "orderBy": {"field": "SEVERITY", "direction": "DESC"},
    }

    # fetch the list of issues
    transport = AIOHTTPTransport(url=url, headers={"Authorization": "Bearer " + token})
    client = Client(
        transport=transport, fetch_schema_from_transport=True, execute_timeout=55
    )

    # loop through until all records have been fetched
    intFetch = 1
    issues = {}
    while intFetch > 0:
        # Fetch the query!
        try:
            wizIssues = client.execute(query, variable_values=variables)
        except Exception:
            # error - unable to retrieve Wiz issues
            logger.info(
                "Error - unable to fetch Wiz issues.  Ensure access token is valid and correct Wiz API endpoint was provided."
            )
            sys.exit(1)
        if intFetch == 1:
            # initialize the object
            issues = wizIssues
        else:
            # append any new records
            for n in wizIssues["issues"]["nodes"]:
                issues["issues"]["nodes"].append(n)

        # get page info
        pageInfo = wizIssues["issues"]["pageInfo"]

        # Check if there are additional results
        if pageInfo["hasNextPage"]:
            # Update variables to fetch the next batch of items
            variables["after"] = pageInfo["endCursor"]
            # update loop cursor
            intFetch += 1
        else:
            # No additional results. End the loop/
            intFetch = 0

    # output the results of the Wiz issues
    with open(f"artifacts{sep}wizIssues.json", "w") as outfile:
        outfile.write(json.dumps(issues, indent=4))
    logger.info(
        str(len(issues["issues"]["nodes"]))
        + " issues retrieved for processing from Wiz.io."
    )

    # create arrays for processing
    regScaleClose = []
    regScaleUpdate = []
    regScaleNew = []

    # loop through the Wiz issues
    for iss in issues["issues"]["nodes"]:
        # default to Not Found
        bFound = False

        # see if this issue already exists in RegScale
        for exists in issuesData:
            if "wizId" in exists:
                if exists["wizId"] == iss["id"]:
                    bFound = True
                    # capture the existing record
                    issFound = exists

        # pre-process metadata
        strTitle = iss["entity"]["name"] + " - " + iss["control"]["name"]
        strDescription = "<strong>Wiz Control ID: </strong>" + iss["control"]["id"]
        strDescription += "<br/><strong>Asset Type: </strong>" + iss["entity"]["type"]
        strDescription += "<br/><strong>Severity: </strong>" + iss["severity"]
        strDescription += "<br/><strong>Date First Seen: </strong>" + str(
            iss["createdAt"]
        )
        strDescription += "<br/><strong>Date Last Seen: </strong>" + str(
            iss["updatedAt"]
        )

        # process subcategories for security frameworks
        categories = iss["control"]["securitySubCategories"]
        strTable = "<table><tr><td>Control ID</td><td>Category/Family</td><td>Framework</td><td>Description</td></tr>"
        for cat in categories:
            strTable += "<tr>"
            strTable += "<td>" + str(cat["externalId"]) + "</td>"
            strTable += "<td>" + str(cat["category"]["name"]) + "</td>"
            strTable += "<td>" + str(cat["category"]["framework"]["name"]) + "</td>"
            strTable += "<td>" + str(cat["description"]) + "</td>"
            strTable += "</tr>"
        strTable += "</table>"

        # get today's date as a baseline
        todayDate = date.today().strftime("%m/%d/%y")

        # handle status and due date
        if iss["severity"] == "LOW":
            days = check_config_for_issues(config=config, issue="wiz", key="low")
            strSeverity = "III - Low - Other Weakness"
            dueDate = datetime.datetime.strptime(
                todayDate, "%m/%d/%y"
            ) + datetime.timedelta(days=days)
        elif iss["severity"] == "MEDIUM":
            days = check_config_for_issues(config=config, issue="wiz", key="medium")
            strSeverity = "II - Moderate - Reportable Condition"
            dueDate = datetime.datetime.strptime(
                todayDate, "%m/%d/%y"
            ) + datetime.timedelta(days=days)
        elif iss["severity"] == "HIGH":
            days = check_config_for_issues(config=config, issue="wiz", key="high")
            strSeverity = "II - Moderate - Reportable Condition"
            dueDate = datetime.datetime.strptime(
                todayDate, "%m/%d/%y"
            ) + datetime.timedelta(days=days)
        elif iss["severity"] == "CRITICAL":
            days = check_config_for_issues(config=config, issue="wiz", key="critical")
            strSeverity = "I - High - Significant Deficiency"
            dueDate = datetime.datetime.strptime(
                todayDate, "%m/%d/%y"
            ) + datetime.timedelta(days=days)
        else:
            logger.error("Unknown Wiz severity level: " + iss["severity"])

        # handle parent assignments for deep linking
        if regscale_module == "securityplans":
            intSecurityPlanId = regscale_id
        else:
            intSecurityPlanId = 0
        if regscale_module == "projects":
            intProjectId = regscale_id
        else:
            intProjectId = 0
        if regscale_module == "supplychain":
            intSupplyChainId = regscale_id
        else:
            intSupplyChainId = 0
        if regscale_module == "components":
            intComponentId = regscale_id
        else:
            intComponentId = 0

        # process based on whether found or not
        if bFound is True:
            # update existing record
            logger.info(
                "RegScale Issue #"
                + str(issFound["id"])
                + " already exists for "
                + str(issFound["wizId"])
                + ".  Queuing for update."
            )
            # update the description
            issFound["description"] = strDescription + "<br/><br/>" + strTable
            # add to the update array
            regScaleUpdate.append(issFound)
        else:
            # process new record
            issNew = {
                "id": 0,
                "uuid": iss["entity"]["id"],
                "title": strTitle,
                "dateCreated": iss["createdAt"],
                "description": strDescription + "<br/><br/>" + strTable,
                "severityLevel": strSeverity,
                "issueOwnerId": str_user,
                "costEstimate": 0,
                "levelOfEffort": 0,
                "dueDate": str(dueDate),
                "identification": "Security Control Assessment",
                "status": check_config_for_issues(
                    config=config, issue="wiz", key="status"
                ),
                "dateCompleted": None,
                "facilityId": None,
                "orgId": None,
                "controlId": 0,
                "assessmentId": 0,
                "requirementId": 0,
                "securityPlanId": intSecurityPlanId,
                "projectId": intProjectId,
                "supplyChainId": intSupplyChainId,
                "policyId": 0,
                "componentId": intComponentId,
                "incidentId": 0,
                "jiraId": "",
                "serviceNowId": "",
                "wizId": iss["id"],
                "prismaId": "",
                "parentId": regscale_id,
                "parentModule": regscale_module,
                "createdById": str_user,
                "lastUpdatedById": str_user,
                "dateLastUpdated": iss["updatedAt"],
            }
            # add the issue to the processing array
            regScaleNew.append(issNew)

    # see if any issues are open in RegScale that have been closed in Wiz (in RegScale but not in Wiz)
    for iss in issuesData:
        # only process open issues
        if iss["status"] == "Open":
            # default to close unless found
            bClose = True
            # loop through each Wiz issue and look for a match
            for wizIss in issues["issues"]["nodes"]:
                if iss["wizId"] == wizIss["id"]:
                    # still open in Wiz
                    bClose = False
            # if not found, close it
            if bClose is True:
                # set closed status
                iss["Status"] = "Closed"
                iss["DateCompleted"] = datetime.date.today().strftime("%m/%d/%Y")
                # queue to close
                regScaleClose.append(iss)

    # output the result to logs
    with open(f"artifacts{sep}regScaleUpdateIssues.json", "w") as outfile:
        outfile.write(json.dumps(regScaleUpdate, indent=4))
    logger.warning(
        str(len(regScaleUpdate))
        + " Wiz issues were previously seen and have been updated."
    )

    # output the result to logs
    with open(f"artifacts{sep}regScaleNewIssues.json", "w") as outfile:
        outfile.write(json.dumps(regScaleNew, indent=4))
    logger.error(
        str(len(regScaleNew))
        + " new Wiz issues have been processed and are ready for upload."
    )

    # output the result to logs
    with open(f"artifacts{sep}regScaleCloseIssues.json", "w") as outfile:
        outfile.write(json.dumps(regScaleClose, indent=4))
    logger.info(
        str(len(regScaleClose))
        + " Wiz issues have been closed and are ready for closure in RegScale."
    )

    # Warn that processing is beginning
    logger.warning("PRE-PROCESSING COMPLETE: Batch updates beginning.....")

    # update each existing Wiz issue in RegScale
    url_update_issue = config["domain"] + "/api/issues/"
    postHeader = {"Authorization": config["token"]}
    for proc in regScaleUpdate:
        try:
            issueUpload = api.put(
                url=(url_update_issue + str(proc["id"])), headers=postHeader, json=proc
            )
            issueUploadResponse = issueUpload.json()
            # output the result
            logger.info(
                "Success: Issue update for RegScale # "
                + str(issueUploadResponse["id"])
                + " loaded for Wiz ID #."
                + str(issueUploadResponse["wizId"])
            )
        except Exception:
            logger.error("ERROR: Unable to update " + str(proc["id"]))

    # load each new Wiz issue into RegScale
    url_create_issue = config["domain"] + "/api/issues"
    for proc in regScaleNew:
        try:
            issueUpload = api.post(url=url_create_issue, headers=postHeader, json=proc)
            issueUploadResponse = issueUpload.json()
            # output the result
            logger.info(
                "Success: New RegScale Issue # "
                + str(issueUploadResponse["id"])
                + " loaded for Wiz ID #."
                + str(issueUploadResponse["wizId"])
            )
        except Exception:
            logger.error("ERROR: Unable to create " + str(proc))

    # close issues that have been remediated in RegScale
    url_close_issue = config["domain"] + "/api/issues/"
    for proc in regScaleClose:
        try:
            issueUpload = api.put(
                url=(url_close_issue + str(proc["id"])),
                headers=postHeader,
                json=proc,
            )
            issueUploadResponse = issueUpload.json()
            # output the result
            logger.info(
                "Success: Closed RegScale Issue # "
                + str(issueUploadResponse["id"])
                + "; Wiz ID #."
                + str(issueUploadResponse["wizId"])
            )
        except Exception:
            logger.error("ERROR: Unable to close Issue # " + str(proc["id"]))


#####################################################################################################
#
# PROCESS THREATS FROM WIZ
#
#####################################################################################################
@wiz.command()
def threats():
    """Process threats from Wiz"""
    check_license()
    logger.info("Threats - COMING SOON")


#####################################################################################################
#
# PROCESS VULNERABILITIES FROM WIZ
#
#####################################################################################################
@wiz.command()
def vulnerabilities():
    """Process vulnerabilities from Wiz"""
    check_license()
    logger.info("Vulnerabilities - COMING SOON")


def map_category(asset_string: str) -> str:
    """category mapper

    Args:
        wiz_dict (dict): _description_
        asset_string (str): _description_

    Returns:
        str: category
    """
    try:
        return getattr(AssetType, asset_string).value
    except Exception as ex:
        logger.warning("Unable to find %s in AssetType enum \n", ex)
    # Default to Software, if there is an exception
    return "Software"
