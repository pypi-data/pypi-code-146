#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""RegScale File Comparison"""

# standard python imports
import sys
from datetime import datetime, timedelta
from os.path import exists
from pathlib import Path

import click
import pandas as pd
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeElapsedColumn,
)

from app.api import Api
from app.logz import create_logger
from app.utils import (
    check_license,
    create_regscale_assessment,
    get_current_datetime,
    get_file_name,
    get_file_type,
    get_recent_files,
    upload_file_to_regscale,
)
from models.assessment import Assessment
from models.click import NotRequiredIf
from typing import Tuple

job_progress = Progress(
    "{task.description}",
    SpinnerColumn(),
    BarColumn(),
    TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
    TimeElapsedColumn(),
)
logger = create_logger()


@click.group()
def compare():
    """Create RegScale Assessment of differences after comparing two files"""


@compare.command(name="compare_files")
@click.option(
    "--most_recent_in_file_path",
    type=click.Path(exists=True, dir_okay=True, path_type=Path),
    help="Grab two most recent files in the provided directory for comparison",
    default=None,
    cls=NotRequiredIf,
    not_required_if=["old_file", "new_file"],
)
@click.option(
    "--most_recent_file_type",
    type=click.Choice([".csv", ".xlsx"], case_sensitive=False),
    help="Filter the directory for .csv or .xlsx file types",
    default=None,
    cls=NotRequiredIf,
    not_required_if=["old_file", "new_file"],
)
@click.option(
    "--old_file",
    type=click.Path(),
    help=(
        "Enter file path of the original file to compare: must be used with --new_file, "
        + "not required if --most_recent_in_file_path & --most_recent_file_type is used"
    ),
    cls=NotRequiredIf,
    not_required_if=["most_recent_in_file_path", "most_recent_file_type"],
)
@click.option(
    "--new_file",
    type=click.Path(),
    help=(
        "Enter file path of new file to compare: must be used with --old_file, "
        + "not required if --most_recent_in_file_path & --most_recent_file_type is used"
    ),
    cls=NotRequiredIf,
    not_required_if=["most_recent_in_file_path", "most_recent_file_type"],
)
@click.option(
    "--key",
    type=click.STRING,
    help="Enter unique key to compare the files",
    required=True,
)
@click.option(
    "--regscale_module_name",
    type=click.STRING,
    help="Enter RegScale parent module",
    required=True,
)
@click.option(
    "--regscale_parent_id",
    type=click.INT,
    help="Enter RegScale ID for the provided regscale_module_name",
    required=True,
)
def compare_files(
    old_file: str,
    new_file: str,
    most_recent_in_file_path: Path,
    most_recent_file_type: str,
    key: str,
    regscale_parent_id: int,
    regscale_module_name: str,
):
    """Compare the two given files while using the provided key for any differences.
    Supports csv, xls and xlsx files."""
    app = check_license()
    api = Api(app)

    # see if most_recent_in argument was used, get the old and new file
    if most_recent_in_file_path:
        # get the two most_recent_file_type in the provided most_recent_in_file_path
        recent_files = get_recent_files(
            file_path=most_recent_in_file_path,
            file_count=2,
            file_type=most_recent_file_type,
        )
        # verify we have two files to compare
        if len(recent_files) == 2:
            # set the old_file and new_file accordingly
            old_file = recent_files[1]
            new_file = recent_files[0]
        else:
            # notify user we don't have two files to compare and exit application
            logger.error(
                "Required 2 files to compare, but only 1 %s file found in %s!",
                most_recent_file_type,
                str(most_recent_in_file_path),
            )
            sys.exit(1)
    # make sure both file paths exist
    if exists(old_file) and exists(new_file):
        with job_progress:
            # check the file extensions and compare them
            old_file_type, new_file_type = get_file_type(old_file), get_file_type(
                new_file
            )
            if old_file_type == ".csv" and new_file_type == ".csv":
                file_type = ".csv"
            elif old_file_type == ".xlsx" and new_file_type == ".xlsx":
                file_type = ".xlsx"
            elif old_file_type == ".xls" and new_file_type == ".xls":
                file_type = ".xls"
            else:
                logger.error(
                    "%s files are not a supported file type provided for comparison.",
                    old_file_type,
                )
                sys.exit(1)
            # get the file names of from the provided file paths
            old_file_name, new_file_name = get_file_name(old_file), get_file_name(
                new_file
            )

            # create task for progress bar
            comparing = job_progress.add_task(
                f"[#f8b737]Comparing {file_type} files for differences...", total=1
            )
            output, old_row_count, new_row_count = comparison(
                old_file, new_file, key, file_type
            )

            # mark the comparing task as complete
            job_progress.update(comparing, advance=1)

            # create task for formatting data
            formatting = job_progress.add_task(
                "[#ef5d23]Formatting data of comparison outcome...",
                total=1,
            )

            # drop any rows that has no value for the provided key
            output = output.dropna(subset=[key])

            # check if there were any changes, if no changes the assessment
            # will be created with complete as the status
            if output.empty:
                status = "Complete"
                actual_finish = get_current_datetime()
                report = (
                    f"<h3>No differences between {old_file_name} & {new_file_name}</h3>"
                )
            else:
                status = "Scheduled"
                actual_finish = False
                # format report string for assessment
                report = (
                    f"<h3>{old_file_name} Deleted Rows</h3>"
                    f"{create_filtered_html_table(output, 'flag', 'deleted')}"
                    f"<h3>{new_file_name} Added Rows</h3>"
                    f"{create_filtered_html_table(output, 'flag', 'added')}"
                )

            # get data overview
            overview = create_overview(
                data=output,
                old_row_count=old_row_count,
                new_row_count=new_row_count,
                old_file=old_file_name,
                new_file=new_file_name,
            )

            # set up descript for assessment
            desc = (
                f"Comparing two {file_type} files using {key} as a key.<br>"
                f"<b>{old_file_name}</b> contains <b>{old_row_count}</b> row(s) and<br>"
                f"<b>{new_file_name}</b> contains <b>{new_row_count}</b> row(s)<br>{overview}"
            )

            # set up title for the new Assessment
            title = f"{file_type} Comparison for {regscale_module_name.title()}-{regscale_parent_id}"

            # set up plannedFinish date with days from config file
            finish_date = (
                datetime.now() + timedelta(days=app.config["assessmentDays"])
            ).strftime("%Y-%m-%dT%H:%M:%S")

            # map to assessment dataclass
            new_assessment = Assessment(
                leadAssessorId=app.config["userId"],
                title=title,
                assessmentType="Control Testing",
                plannedStart=get_current_datetime(),
                plannedFinish=finish_date,
                assessmentReport=report,
                assessmentPlan=desc,
                createdById=app.config["userId"],
                dateCreated=get_current_datetime(),
                lastUpdatedById=app.config["userId"],
                dateLastUpdated=get_current_datetime(),
                parentModule=regscale_module_name,
                parentId=regscale_parent_id,
                status=status,
            )
            # update the appropriate fields to complete the assessment
            if actual_finish:
                new_assessment.actualFinish = actual_finish
                new_assessment.assessmentResult = "Pass"

            # mark the formatting task as complete
            job_progress.update(formatting, advance=1)

            # create new task for creating assessment in RegScale
            create_assessment = job_progress.add_task(
                "[#21a5bb]Creating assessment in RegScale...",
                total=1,
            )

            # create a new assessment in RegScale
            new_assessment_id = create_regscale_assessment(
                url=f"{app.config['domain']}/api/assessments",
                new_assessment=new_assessment.dict(),
                api=api,
            )

            # verify creating the assessment was successful
            if new_assessment_id:
                # mark the create_assessment task as complete
                job_progress.update(create_assessment, advance=1)

                # create new task for file uploads
                upload_files = job_progress.add_task(
                    "[#0866b4]Uploading files to the new RegScale Assessment...",
                    total=2,
                )

                # upload the old file to the new RegScale assessment
                old_file_upload = upload_file_to_regscale(
                    file_name=old_file,
                    parent_id=new_assessment_id,
                    parent_module="assessments",
                    api=api,
                )
                # verify upload file was successful before updating the task
                if old_file_upload:
                    job_progress.update(upload_files, advance=1)

                # upload the new file to the new RegScale Assessment
                new_file_upload = upload_file_to_regscale(
                    file_name=new_file,
                    parent_id=new_assessment_id,
                    parent_module="assessments",
                    api=api,
                )
                # verify upload file was successful before updating the task
                if new_file_upload:
                    job_progress.update(upload_files, advance=1)

                # notify user if uploads were successful
                if old_file_upload and new_file_upload:
                    logger.info(
                        "Files uploaded to the new assessment in RegScale successfully"
                    )
                else:
                    logger.error(
                        "Unable to upload both files to the assessment in RegScale."
                    )

                # check if domain ends with /
                if app.config["domain"].endswith("/"):
                    # remove the trailing /
                    domain = app.config["domain"][:-1]
                else:
                    # no trailing /
                    domain = app.config["domain"]

                # notify user assessment was created and output a link to it
                logger.info(
                    "New assessment has been created and marked as %s: %s/assessments/form/%s",
                    status,
                    domain,
                    new_assessment_id,
                )
            else:
                # notify the user we were unable to create the assessment int RegScale
                logger.error("Unable to create new RegScale Assessment!")
                sys.exit(1)
    else:
        # notify user the file paths need to be checked
        logger.error("Please check the file paths of the provided files and try again.")
        sys.exit(1)


def comparison(
    file_one: str, file_two: str, key: str, file_type: str
) -> Tuple[pd.DataFrame, int, int]:
    """
    function that will compare two files using the provided key, uses
    a comparison method depending on the provided file_type and will
    return the differences between the two files in a pandas dataframe
    """
    if file_type.lower() == ".csv":
        # open the files
        df1 = pd.read_csv(file_one)
        df2 = pd.read_csv(file_two)
    elif file_type.lower() in [".xlsx", ".xls"]:
        # open the files
        df1 = pd.read_excel(file_one)
        df2 = pd.read_excel(file_two)
    else:
        logger.error("Unsupported file type provided for comparison.")
        sys.exit(1)
    # get the row count of the provided files
    old_row_count = len(df1)
    new_row_count = len(df2)

    # add flags to each dataset
    df1["flag"] = "deleted"
    df2["flag"] = "added"

    # combine the two datasets
    df = pd.concat([df1, df2])

    # get the differences between the two datasets
    output = df.drop_duplicates(df.columns.difference(["flag", key]), keep=False)

    # return the differences and the row counts for each file
    return output, old_row_count, new_row_count


def create_overview(
    data: pd.DataFrame,
    old_row_count: int,
    new_row_count: int,
    old_file: str,
    new_file: str,
) -> str:
    """
    function to create html formatted description from comparing
    data from provided pandas dataframe and row counts
    """
    # convert data frame to a series style dictionary
    data = data.to_dict("series")

    # create dictionary to store all the changes
    changes = {"deletes": 0, "additions": 0}

    # combine the flags and update the changes dictionary
    for change in data["flag"].items():
        if change[1] == "deleted":
            changes["deletes"] += 1
        elif change[1] == "added":
            changes["additions"] += 1

    # calculate % of rows deleted from old_file
    percent_deleted = round(
        ((old_row_count - changes["deletes"]) / old_row_count) * -100 + 100, 2
    )

    # calculate % of rows added to new_file
    percent_added = round(
        ((new_row_count - changes["additions"]) / new_row_count) * -100 + 100, 2
    )

    # format the html string with the changes and percentages
    overview = f"<br>{changes['deletes']} row(s) deleted from {old_file}: ({percent_deleted}%)<br>"
    overview += (
        f"<br>{changes['additions']} row(s) added to {new_file}: ({percent_added}%)<br>"
    )

    # return the html formatted string
    return overview


def create_filtered_html_table(
    data: pd.DataFrame, column: str, value, pop_flag: bool = True
) -> dict:
    """
    function to return a html formatted table of data from the provided
    pandas dataframe where the provided column == provided value
    """
    # filter the provided pandas dataframe on the column and value provided
    filtered_data = data.loc[data[column] == value]

    # remove the field if requested, default is True
    if pop_flag:
        # remove the column from the dataset
        filtered_data.pop(column)

    # return HTML formatted data table
    return (
        filtered_data.to_html(justify="left", index=False)
        if not filtered_data.empty
        else None
    )
