#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" standard python imports """

import collections
import dataclasses
import json
import os
import re
import warnings
from dataclasses import asdict
from datetime import datetime, timedelta
from pathlib import Path

import click
import matplotlib.pyplot as plt
import pandas as pd
import requests
from requests.exceptions import RequestException
from rich.console import Console
from rich.panel import Panel
from rich.pretty import Pretty, pprint
from rich.progress import track
from tenable.sc import TenableSC

from app._version import __version__
from app.api import Api
from app.application import Application
from app.logz import create_logger
from app.utils import (
    check_config_for_issues,
    epoch_to_datetime,
    get_current_datetime,
    validate_mac_address,
)
from models.asset import Asset
from models.issue import Issue
from models.tenable import TenableAsset

console = Console()

logger = create_logger()
app = Application()
api = Api(app)


# Create group to handle OSCAL processing
@click.group()
def tenable():
    """Performs actions on the Tenable.sc API"""


@tenable.command(name="export_scans")
@click.argument(
    "file_name",
    type=click.Path(),
    # help="Save list of usable scans to file in json format.",
)
def export_scans(file_name: Path, export=True):
    """Export scans from Tenable Host"""
    results = get_usable_scan_list()
    if export:
        with open(file_name, "w", encoding="utf-8") as file:
            json.dump(results, file)


def get_usable_scan_list() -> list:
    """Usable Scans from Tenable Host

    Returns:
        list: _description_
    """
    results = []
    try:
        tsc = gen_tsc()
        results = tsc.scans.list()["usable"]
    except Exception as ex:
        logger.error(ex)
    return results


def get_detailed_scans(scan_list: list = None) -> list:
    """Generate list of detailed scans

    Args:
        scan_list (_type_, optional): return detailed information of a list of scans.
        Defaults to usable_scan_list.
    Warning:
        this action could take 20 minutes or more to complete.
    """
    tsc = gen_tsc()
    detailed_scans = []
    for scan in track(scan_list, description="Fetching detailed scans.."):
        try:
            det = tsc.scans.details(id=scan["id"])
            detailed_scans.append(det)
        except RequestException as ex:  # This is the correct syntax
            raise SystemExit(ex) from ex

    return detailed_scans


@tenable.command(name="save_queries")
@click.option("--file_path", type=click.Path(), help="Enter file path", required=True)
def save_queries(file_path: Path):
    """Get a list of query definitions."""
    query_list = get_queries()
    save_as_file(file_path=Path(file_path), data=query_list)


def get_queries():
    """list of query definitions"""
    tsc = gen_tsc()
    return tsc.queries.list()


@tenable.command(name="query_vuln")
@click.option(
    "--query_id", type=click.INT, required=True, help="Enter Tenable query id"
)
@click.option(
    "--regscale_ssp_id", type=click.INT, required=True, help="Enter RegScale SSP id"
)
@click.option(
    "--create_issue",
    type=click.BOOL,
    required=False,
    help="Create Issue in RegScale from Vulnerability in RegScale.",
)
# Add Prompt for Regscale SSP name
def query_vuln(query_id: int, regscale_ssp_id: int, create_issue: bool = False):
    """Query Tenable vulnerabilities and sync assets to RegScale."""
    q_vuln(query_id=query_id, ssp_id=regscale_ssp_id, create_issue=create_issue)


@tenable.command(name="trend_vuln")
@click.option(
    "-p",
    "--plugins",
    multiple=True,
    help="Enter one or more pluginID's to see a trendline. (by report date)",
)
@click.option(
    "-d", "--dnsname", multiple=False, help="Enter DNS name of asset to trend."
)
def trend_vuln(plugins: list, dnsname: str):
    """Trend vulnerabilities from vulnerability scans.

    Args:
        plugins (_type_): _description_
    """
    plugins = list(plugins)
    logger.info(plugins)
    trend_vulnerabilities(filter=plugins, dns=dnsname)


def q_vuln(query_id: int, ssp_id: int, create_issue: bool) -> list:
    """Query Tenable vulnerabilities"""
    # At SSP level, provide a list of vulnerabilities and the counts of each
    # Normalize the data based on mac address
    reg_assets = lookup_reg_assets_by_parent(ssp_id)

    tenable_data = fetch_vulns(
        query_id=query_id, regscale_ssp_id=ssp_id, create_issue=create_issue
    )
    tenable_vulns = tenable_data[0]
    tenable_df = tenable_data[1]

    assets_to_be_inserted = list(
        set(
            [
                dat
                for dat in tenable_vulns
                if dat.macAddress
                not in set(
                    asset.macAddress for asset in inner_join(reg_assets, tenable_vulns)
                )
            ]
        )
    )
    counts = collections.Counter(s.pluginName for s in tenable_vulns)
    update_assets = []
    insert_assets = []
    for vuln in set(tenable_vulns):  # you can list as many input dicts as you want here
        vuln.counts = dict(counts)[vuln.pluginName]
        lookup_assets = lookup_asset(reg_assets, vuln.macAddress, vuln.dnsName)
        # Update parent id to SSP on insert
        if len(lookup_assets) > 0:
            for asset in set(lookup_assets):
                # Do update
                # asset = reg_asset[0]
                asset.parentId = ssp_id
                asset.parentModule = "securityplans"
                asset.macAddress = vuln.macAddress.upper()
                asset.osVersion = vuln.operatingSystem
                asset.purchaseDate = "01-01-1970"
                asset.endOfLifeDate = "01-01-1970"
                if asset.ipAddress is None:
                    asset.ipAddress = vuln.ipAddress
                asset.operatingSystem = determine_os(asset.operatingSystem)
                try:
                    assert asset.id
                    # avoid duplication
                    if asset.macAddress.upper() not in set(
                        v["macAddress"].upper() for v in update_assets
                    ):
                        update_assets.append(asdict(asset))
                except AssertionError as aex:
                    logger.error(
                        "Asset does not have an id, unable to update!\n%s", aex
                    )

    for t_asset in assets_to_be_inserted:
        if len(assets_to_be_inserted) > 0:
            # Do Insert
            r_asset = Asset(
                name=t_asset.dnsName,
                otherTrackingNumber=t_asset.pluginID,
                parentId=ssp_id,
                parentModule="securityplans",
                ipAddress=t_asset.ip,
                macAddress=t_asset.macAddress,
                assetOwnerId=app.config["userId"],
                status=get_status(t_asset),
                assetType="Other",
                operatingSystem=determine_os(t_asset.operatingSystem),
            )
            # avoid duplication
            if r_asset.macAddress.upper() not in set(
                v["macAddress"].upper() for v in insert_assets
            ):
                insert_assets.append(asdict(r_asset))
    try:
        api.update_server(
            method="post",
            url=app.config["domain"] + "/api/assets",
            json_list=insert_assets,
            message=f"Inserting {len(insert_assets)} assets from this Tenable query to RegScale.",
        )

        logger.info("Regscale Assets successfully inserted: %i", len(insert_assets))
    except requests.exceptions.RequestException as rex:
        logger.error("Unable to Insert Tenable Assets to RegScale\n%s", rex)
    try:
        api.update_server(
            method="put",
            url=app.config["domain"] + "/api/assets",
            json_list=update_assets,
            message=f"Updating {len(update_assets)} assets from this Tenable query to RegScale.",
        )
        logger.info("Regscale Assets successfully updated: %i", len(update_assets))
    except requests.RequestException as rex:
        logger.error("Unable to Update Tenable Assets to RegScale\n%s", rex)
    if create_issue:
        today = get_current_datetime(format="%Y-%m-%d")
        create_regscale_issue_from_vuln(
            regscale_ssp_id=ssp_id, df=tenable_df[tenable_df["report_date"] == today]
        )
    return update_assets

    # save_as_file(file_path=Path(file_path), data=vulns)


def determine_os(os_string: str) -> str:
    """determine RegScale friendly OS name

    Args:
        s (str): _description_

    Returns:
        _type_: _description_
    """
    linux_words = ["linux", "ubuntu", "hat", "centos", "rocky", "alma", "alpine"]
    if re.compile("|".join(linux_words), re.IGNORECASE).search(os_string):
        os_string = "Linux"
    elif (os_string.lower()).startswith("windows"):
        if "server" in os_string:
            os_string = "Windows Server"
        else:
            os_string = "Windows Desktop"
    else:
        os_string = "Other"
    return os_string


def get_status(asset: TenableAsset) -> str:
    """Convert Tenable asset status to RegScale asset status.

    Args:
        asset (TenableAsset): Tenable Asset

    Returns:
        str: RegScale status
    """
    if asset.family.type == "active":
        return "Active (On Network)"
    return "Off-Network"  # Probably not correct


def format_vulns():
    """_summary_"""


def lookup_asset(asset_list: list, mac_address: str, dns_name: str = None):
    """Return single asset"""
    results = []
    if validate_mac_address(mac_address):
        if dns_name:
            results = [
                Asset.from_dict(asset)
                for asset in asset_list
                if asset["macAddress"] == mac_address and asset["name"] == dns_name
            ]
        else:
            results = [
                Asset.from_dict(asset)
                for asset in asset_list
                if asset["macAddress"] == mac_address
            ]
    # Return unique list
    return list(set(results))


def trend_vulnerabilities(
    filter: list,
    dns: str,
    filter_type="pluginID",
    filename="vulnerabilities.pkl",
):
    """Trend vulnerabilities data to the console"""
    if len(filter) > 0:
        df = pd.read_pickle(filename)
        unique_cols = ["pluginID", "dnsName", "severity", "report_date"]
        df = df[df[filter_type].isin(filter)]
        df = df[df["dnsName"] == dns]
        df = df[unique_cols]
        df = df.drop_duplicates(subset=unique_cols)

        df.loc[df["severity"] == "Info", "severity_code"] = 0
        df.loc[df["severity"] == "Low", "severity_code"] = 1
        df.loc[df["severity"] == "Medium", "severity_code"] = 2
        df.loc[df["severity"] == "High", "severity_code"] = 3
        df.loc[df["severity"] == "Critical", "severity_code"] = 4
        # Deal with linux wayland sessions
        if (
            "XDG_SESSION_TYPE" in os.environ
            and os.getenv("XDG_SESSION_TYPE") == "wayland"
        ):
            os.environ["QT_QPA_PLATFORM"] = "wayland"
        # plotting graph
        for d in filter:
            plt.plot(df["report_date"], df["severity_code"], label=d)
        logger.info("Plotting %s rows of data\n", len(df))
        logger.info(df.head())
        plt.legend()
        plt.show(block=True)


def map_tenable_severity_to_regscale(code):
    """Map Severity Codes to RegScale."""
    if code == "Info":
        return "IV - Not Assigned"
    elif code == "Low":
        return "III - Low - Other Weakness"
    elif code == "Medium":
        return "II - Moderate - Reportable Condition"
    elif code in ["High", "Critical"]:
        return "I - High - Significant Deficiency"


def create_regscale_issue_from_vuln(regscale_ssp_id: int, df: pd.DataFrame) -> None:
    """Sync Tenable Vulnerabilities to RegScale issues.

    Args:
        df (pd.DataFrame): pandas dataframe
    """
    default_status = check_config_for_issues(
        config=app.config, issue="tenable", key="status"
    )
    regscale_new_issues = []
    regscale_existing_issues = []
    existing_issues_req = api.get(
        app.config["domain"]
        + f"/api/issues/getAllByParent/{regscale_ssp_id}/securityplans"
    )
    if existing_issues_req.status_code == 200:
        regscale_existing_issues = existing_issues_req.json()
    columns = list(df.columns)
    for index, row in df.iterrows():
        if df["severity"][index] != "Info":
            if df["severity"][index] == "Critical":
                default_due_delta = check_config_for_issues(
                    config=app.config, issue="tenable", key="critical"
                )
            elif df["severity"][index] == "High":
                default_due_delta = check_config_for_issues(
                    config=app.config, issue="tenable", key="high"
                )
            else:
                default_due_delta = check_config_for_issues(
                    config=app.config, issue="tenable", key="moderate"
                )
            logger.debug("Processing row: %i", index + 1)
            fmt = "%Y-%m-%d %H:%M:%S"
            plugin_id = row[columns.index("pluginID")]
            port = row[columns.index("port")]
            protocol = row[columns.index("protocol")]
            due_date = datetime.strptime(
                row[columns.index("last_scan")], fmt
            ) + timedelta(days=default_due_delta)
            if row[columns.index("synopsis")]:
                title = row[columns.index("synopsis")]
            issue = Issue(
                title=title if title else row[columns.index("pluginName")],
                description=row[columns.index("description")]
                if row[columns.index("description")]
                else row[columns.index("pluginName")]
                + f"<br>Port: {port}<br>Protocol: {protocol}",
                issueOwnerId=app.config["userId"],
                status=default_status,
                severityLevel=map_tenable_severity_to_regscale(
                    row[columns.index("severity")]
                ),
                dueDate=due_date.strftime(fmt),
                identification="Vulnerability Assessment",
                parentId=row[columns.index("regscale_ssp_id")],
                parentModule="securityplans",
                pluginId=plugin_id,
                vendorActions=row[columns.index("solution")],
                assetIdentifier=f'DNS: {row[columns.index("dnsName")]} - IP: {row[columns.index("ip")]}',
            )
            if issue.title in set([iss["title"] for iss in regscale_new_issues]):
                # Update
                update_issue = [
                    iss for iss in regscale_new_issues if iss["title"] == issue.title
                ][0]
                if update_issue["assetIdentifier"] != issue.assetIdentifier:
                    assets = set(update_issue["assetIdentifier"].split("<br>"))
                    if issue.assetIdentifier not in assets:
                        update_issue["assetIdentifier"] = (
                            update_issue["assetIdentifier"]
                            + "<br>"
                            + issue.assetIdentifier
                        )
            else:
                if issue.title not in set(
                    [iss["title"] for iss in regscale_existing_issues]
                ):
                    # Add
                    regscale_new_issues.append(dataclasses.asdict(issue))
        else:
            logger.debug("Row %i not processed: %s", index, row["description"])
    logger.info(
        f"Posting {len(regscale_new_issues)} new issues to RegScale condensed from {len(df)} Tenable vulnerabilities."
    )
    if len(regscale_new_issues) > 0:
        api.update_server(
            url=app.config["domain"] + "/api/issues",
            message=f"Posting {len(regscale_new_issues)} issues..",
            json_list=regscale_new_issues,
        )


def log_vulnerabilities(
    data: list, query_id: int, regscale_ssp_id: int, create_issue: bool
) -> pd.DataFrame:
    """Logs Vulnerabilities to a file

    Args:
        data (list[dict]), optional: _description_
    Returns:
        Pandas Dataframe
    """
    warnings.filterwarnings("ignore", category=FutureWarning)
    try:
        df = pd.DataFrame(data)
        df["query_id"] = query_id
        df["regscale_ssp_id"] = regscale_ssp_id
        df["first_scan"] = df["firstSeen"].apply(epoch_to_datetime)
        df["last_scan"] = df["lastSeen"].apply(epoch_to_datetime)
        df["severity"] = [d.get("name") for d in df["severity"]]
        df["family"] = [d.get("name") for d in df["family"]]
        df["repository"] = [d.get("name") for d in df["repository"]]
        df["report_date"] = get_current_datetime(format="%Y-%m-%d")
        filename = "vulnerabilities.pkl"

        df.drop_duplicates()
        if not Path(filename).exists():
            logger.info("Saving vulnerability data to %s", filename)
            df.to_pickle(filename)
        else:
            logger.info(
                "Updating vulnerabilities.pkl with the latest data from Tenable"
            )
            old_df = pd.read_pickle(filename)
            old_df = old_df[
                old_df["report_date"] != get_current_datetime(format="%Y-%m-%d")
            ]
            try:
                df = pd.concat([old_df, df]).drop_duplicates()
            except ValueError as vex:
                logger.error("Pandas ValueError:\n%s", vex)
            df.to_pickle(filename)
        severity_arr = df.groupby(["severity", "repository"]).size().to_frame()
        console.rule("[bold red]Vulnerability Overview")
        console.print(severity_arr)
        return df

    except pd.errors.DataError as dex:
        logger.error(dex)


def fetch_vulns(query_id: int, regscale_ssp_id: int, create_issue: bool) -> tuple:
    """Fetch vulnerablilities by query id

    Args:
        id (int), optional: _description_
    Returns:
        data (list) list of vulnerabilities.
    """
    tsc = gen_tsc()
    data = []
    if query_id:
        description = f"Fetching Vulnerabilities for Tenable query id: {query_id}"
        vulns = tsc.analysis.vulns(query_id=query_id)
        for vuln in track(vulns, description=description, show_speed=False):
            data.append(TenableAsset.from_dict(vuln))
        logger.info("Found %i vulnerabilities", len(data))
    df = log_vulnerabilities(
        data,
        query_id=query_id,
        regscale_ssp_id=regscale_ssp_id,
        create_issue=create_issue,
    )
    return data, df


@tenable.command(name="list_tags")
def list_tags():
    """Query a list of tags on the server and print to console."""
    tag_list = get_tags()
    pprint(tag_list)


def get_tags():
    """list of query definitions"""
    tsc = gen_tsc()
    return tsc.queries.tags()


def gen_tsc() -> TenableSC:
    """Generate Tenable Object"""
    config = Application().config
    tsc = TenableSC(
        url=config["tenable_url"],
        access_key=config["tenable_access_key"],
        secret_key=config["tenable_secret_key"],
        vendor="RegScale, Inc.",
        product="RegScale CLI",
        build=__version__,
    )
    return tsc


def pretty_print(data: list, title: str = None):
    """Pretty print and render data for visual

    Args:
        data (list): list of dicts (probably)
        title (str, optional): simple title. Defaults to None.
    """
    pretty = Pretty(data)
    panel = Panel(pretty)
    if title:
        panel.title = title
    print(panel)


def save_as_file(file_path: Path, data: list):
    """Save as file

    Args:
        file_path (Path): _description_
        data (dict): _description_
    """
    with open(file_path, "w", encoding="utf-8") as file:
        try:
            logger.info("Saving %s", file_path.absolute())
            json.dump(data, fp=file)
        except TypeError as ex:
            logger.error("TypeError: Cannot save queries: %s\n%s", file_path, ex)


def gen_config():
    """Return config

    Returns:
        dict: configuration
    """
    return api.config


def inner_join(reg_list: list, tenable_list: list) -> list:
    """_summary_

    Args:
        reg_list (list): _description_
        tenable_list (list): _description_

    Returns:
        list: _description_
    """
    set1 = set(lst["macAddress"].lower() for lst in reg_list)
    data = []
    try:
        data = [
            list_ten for list_ten in tenable_list if list_ten.macAddress.lower() in set1
        ]
    except KeyError as ex:
        logger.error(ex)
    return data


def lookup_reg_assets_by_parent(regscale_ssp_id: int) -> list:
    """Return a list of Regscale Assets"""
    config = api.config
    regscale_assets_url = (
        config["domain"] + f"/api/assets/getAllByParent/{regscale_ssp_id}/securityplans"
    )
    results = []

    response = api.get(url=regscale_assets_url)
    try:
        if response.status_code == 200 and len(response.json()) > 0:
            results = response.json()
    except requests.JSONDecodeError as ex:
        logger.error("Unable to fetch assets from RegScale:\n%s", ex)
    return results


def reg_ssp(ssp_id) -> list:
    """return ssp information

    Args:
        id (int): ssp_id

    Returns:
        list: ssp
    """
    data = []
    try:
        response = api.get(app.config["domain"] + f"/api/securityplans/{ssp_id}")
        data = response.json()
    except requests.RequestException as rex:
        logger.error(rex)
    return data


def reg_vulns() -> list:
    """Return a list of Regscale Vulnerablilites"""
    config = api.config
    regscale_vulnerablilites_url = config["domain"] + "/api/vulnerability/getAll"
    results = []
    vulns = api.get(url=regscale_vulnerablilites_url)
    try:
        if len(vulns.json()) > 0:
            return vulns.json()
    except requests.JSONDecodeError as ex:
        logger.error("Unable to fetch vulnerabilities from Regscale:\n%s", ex)
    return results
