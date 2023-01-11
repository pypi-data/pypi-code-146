#
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.
#
# request_helper.py: flat functions for working with requests data

from .console import console
from .report_builder import ReportBuilder   

from xtlib import qfe
from xtlib import utils
from xtlib import errors
from xtlib import file_utils
from xtlib import job_helper
from xtlib import run_helper
from xtlib import store_utils

std_cols_desc = {
    # the key here is the USER friendly name (not the physical name)
    "ws_name": "the workspace that the associated job is defined within",
    "request_id": "the id of this request",
    "status": "the status of this request; one of: requested, approved, cancelled",
    "target": "the compute target that this request will run on",
    "nodes": "the number of nodes specified for this request",
    "runs": "the total number of runs specified for this request",
    "cmd": "the job submission (xt run) command for this request",
    "requested_by": "the username of the person that submitted this request",
    "action_by": "the username of the person approved or cancelled this request",
    "create_time": "the timestamp for when this request was created",
    "action_time": "the timestamp for when this request was approved or cancelled",
    "job_id": "if this request was approved, this is the name of the job that was submitted",
    "description": "the question or goal, motivating this job",
    "takeaway": "a summary of what was learned from this job",
}

request_info_props = {key: 1 for key in std_cols_desc}
user_to_actual = {key: key for key in std_cols_desc}


def build_request_filter_dict(store, ws_name, request_names, user_to_actual, builder, workspace, args):
    fd = {}
    option_filters = ["target", "status"]  

    # filter by workspace
    if workspace:
        fd["ws_name"] = workspace

    # filter by names
    if request_names:
        fd["request_id"] = {"$in": request_names}

    # filter by specified options
    for name in option_filters:
        store_name = user_to_actual[name]
        job_helper.build_filter_part(fd, args, name, store_name)

    # filter by filter_list
    filter_exp_list = args["filter"]
    if filter_exp_list:
        builder.process_filter_list(fd, filter_exp_list, user_to_actual)

    # filter by tag
    if "tag" in args:
        tag_name = args["tag"]
        if tag_name:
                fd["tags." + tag_name] = {"$exists": True}

    # filter by tags_all
    tags_all = args["tags_all"]
    if tags_all:
        for tag in tags_all:
            fd["tags." + tag] = {"$exists": True}

    # filter by tags_any
    tags_any = args["tags_any"]
    if tags_any:
        fany_list = []
        
        for tag in tags_any:
            f = {"tags." + tag: {"$exists": True}}
            fany_list.append(f)

        # or all of fany conditions together
        fd["$or"] = fany_list

    return fd


def get_list_requests_records(store, config, user_columns, args):

    names = args["names"] 
    #pool = args["target"]

    workspace = args["workspace"]
    if workspace:
        store.ensure_workspace_exists(workspace, flag_as_error=True)

    # get info about request properties
    actual_to_user = {value: key for key, value in user_to_actual.items()}

    builder = ReportBuilder(config, store)

    # get list of specified jobs
    db = store.get_database()

    request_names = args["names"]

    # build a filter dict for all specified filters
    filter_dict = build_request_filter_dict(store, workspace, request_names, user_to_actual, builder, workspace, args)

    hide_empty_cols = config.get("request-reports", "hide-empty-cols")

    # get the db records for the matching REQUESTS
    #console.print("gathering job data...", flush=True)
    records, limiter, limiter_value = builder.get_db_records(db, filter_dict, workspace, "requests", actual_to_user, 
        user_columns=user_columns, hide_empty_cols=hide_empty_cols, args=args)
        
    return records, limiter, limiter_value, user_to_actual, builder

def list_requests(store, config, args, compare=False):
    available = args["available"]
    report_type = "request-reports"
    user_columns = utils.get_user_columns(args["columns"], report_type, config)

    # we are reusing some of job_helper, so adjust args as needed
    args["list_requests"] = True
    args["jobs_list"] = args["names"]

    records, using_default_last, last, user_to_actual, builder \
        = get_list_requests_records(store, config, user_columns, args)

    if available:
        std_cols = list(user_to_actual.keys())
        tag_cols = job_helper.extract_tag_cols(records)
        lines = builder.available_cols_report("report", std_cols, std_cols_desc, tags_list=tag_cols)

        for line in lines:
            console.print(line)
    else:    
        if compare:
            # filter cols to those that are different
            diff_cols = run_helper.get_different_cols(records)
            args["columns"] = diff_cols 

        avail_list = list(user_to_actual.keys())
        lines, row_count, was_exported = builder.build_report(records, user_columns=user_columns, report_type=report_type, args=args)

        store_name = config.get("store")
        workspace = args["workspace"]
        console.print("requests from {}/{}:".format(store_name, workspace))

        if was_exported:
            console.print("")

            for line in lines:
                console.print(line)
        else:
            # console.print the report
            if row_count > 0:
                console.print("")

                for line in lines:
                    console.print(line)

                if row_count > 1:
                    if using_default_last:
                        console.print("total requests listed: {} (limited by --last={})".format(row_count, last))
                    else:
                        console.print("total requests listed: {}".format(row_count))
            else:
                console.print("no matching requests found")

