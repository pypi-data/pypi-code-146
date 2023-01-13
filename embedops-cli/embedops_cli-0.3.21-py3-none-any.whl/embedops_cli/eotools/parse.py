#!/usr/bin/env python
"""
`parse.py`
=======================================================================
A script to parse information from build logs
* Author(s): Bryan Siepert
"""
import re
import json
from sys import exit as sys_exit
from os.path import exists as file_exists
from pprint import pformat
import logging

from embedops_cli.config import settings
from embedops_cli.utilities import post_dict, get_compiler
from embedops_cli.eotools.log_parser.iar import SIZE_PATTERN as IAR_SIZE_PATTERN
from embedops_cli.eotools.log_parser.gnu_size_berkeley import (
    SIZE_PATTERN as SIZE_SIZE_PATTERN,
)

_logger = logging.getLogger(__name__)
EXPECTED_RETURN_CODE = 200


def parse_storage_sizes(log_filename, compiler):
    """Check each line in a log file for compiler RAM, flash data, and flash code sizes"""

    build_data = None
    storage_sizes = None
    storage_collection = []

    if compiler == "IAR":
        size_regex = IAR_SIZE_PATTERN
        _logger.info("IAR size pattern loaded")
    elif compiler in ("TI", "GCC"):
        size_regex = SIZE_SIZE_PATTERN
        _logger.info("GNU size pattern loaded for TI and GCC")
    else:
        _logger.warning(f"EMBEDOPS_COMPILER {compiler} not supported")
        sys_exit(1)

    if file_exists(log_filename):
        with open(log_filename, "r", encoding="ascii") as build_log:
            build_data = build_log.read()
    else:
        _logger.critical(f"log file {log_filename} not found")
        sys_exit(1)

    build_results = re.finditer(size_regex, build_data)
    for result in build_results:
        storage_sizes = {
            "flash_code_size": None,
            "flash_data_size": None,
            "ram_size": None,
        }
        storage_sizes["ram_size"] = int(result["ram_size"].replace("'", ""))
        storage_sizes["flash_code_size"] = int(
            result["flash_code_size"].replace("'", "")
        )
        storage_sizes["flash_data_size"] = int(
            result["flash_data_size"].replace("'", "")
        )
        storage_sizes["dimensions"] = {
            "build_target_name": result["target_name"],
        }
        if "target_group" in result.groupdict():
            storage_sizes["dimensions"]["build_target_group"] = result["target_group"]
        # TODO: deprecate this dimension re:eo-548
        if storage_sizes["dimensions"].get("build_target_group"):
            storage_sizes["dimensions"]["build_target"] = " - ".join(
                [
                    storage_sizes["dimensions"]["build_target_name"],
                    storage_sizes["dimensions"]["build_target_group"],
                ]
            )
        else:
            storage_sizes["dimensions"]["build_target"] = storage_sizes["dimensions"][
                "build_target_name"
            ]
        storage_collection.append(storage_sizes)
    _logger.debug(f"parsed metrics: {json.dumps(storage_collection, indent=2)}")
    return storage_collection


def _report_metrics(metrics_collections, run_id, embedops_repo_key):

    headers = {"X-API-Key": embedops_repo_key, "Content-Type": "application/json"}
    if run_id == "LOCAL":
        _logger.info("\nResults:")

    for build_metrics in metrics_collections:
        for key in build_metrics:
            if key == "dimensions":
                continue
            stats_data = {
                "ciRunId": run_id,
                "name": key,
                "value": build_metrics[key],
                "dimensions": build_metrics["dimensions"],
            }

            if run_id == "LOCAL":
                _logger.info(f"\t{key} : {pformat(build_metrics[key])}")
            else:
                response = post_dict(
                    settings.metrics_endpoint,
                    json_dict=stats_data,
                    headers=headers,
                )
                # TODO: Refactor this to remove the duplication with similar
                # code in `create_run.py`, perhaps in a shared API library :O
                if response.status_code != EXPECTED_RETURN_CODE:
                    _logger.error(
                        f"FAILING: Expected response type {EXPECTED_RETURN_CODE}(Created)"
                        f"from metrics creation endpoint, got {response.status_code}"
                    )
                    response_string = pformat(response.json(), indent=4)
                    _logger.error(response_string)

                    sys_exit(1)
                response_string = pformat(response.json(), indent=4)
                _logger.info("Created metric:")
                _logger.info(response_string)


def parse_reports(input_filename, compiler, run_id, embedops_repo_key):
    """Parse the given file for compile sized totals"""
    if not file_exists(input_filename):
        raise FileNotFoundError(
            f"The given input file {input_filename} cannot be found"
        )
    storage_sizes = parse_storage_sizes(input_filename, compiler)
    _logger.info(f"Got storage sizes: {json.dumps(storage_sizes, indent=2)}")
    if not storage_sizes:
        _logger.error("no build target sizes found")
        sys_exit(1)
    _report_metrics(storage_sizes, run_id, embedops_repo_key)


def main():
    """The main entrypoint for the module, to allow for binary-izing"""

    compiler = get_compiler()
    if compiler not in ("IAR", "TI", "GCC"):
        _logger.warning("EMBEDOPS_COMPILER not set")
        sys_exit(1)
    input_file = settings.input_file
    run_id = settings.run_id

    try:
        api_repo_key = settings.api_repo_key
    except AttributeError:
        api_repo_key = None

    _logger.info(f"EMBEDOPS_INPUT_FILE {input_file}")
    _logger.info(f"EMBEDOPS_RUN_ID {run_id}")

    if run_id is None:
        _logger.warning(
            "EMBEDOPS_RUN_ID not set. Assuming local build, will not push metrics"
        )
        run_id = "LOCAL"
    elif run_id == "LOCAL":
        _logger.info("Local build requested. Will not push metrics")
    elif api_repo_key is None:
        _logger.warning(
            "EMBEDOPS_API_REPO_KEY not set. Assuming local build, will not push metrics."
        )
        run_id = "LOCAL"

    _logger.info("EMBEDOPS_API_REPO_KEY set (not echoing)")

    # this should read directly from settings
    parse_reports(input_file, compiler, run_id, api_repo_key)


if __name__ == "__main__":
    main()
