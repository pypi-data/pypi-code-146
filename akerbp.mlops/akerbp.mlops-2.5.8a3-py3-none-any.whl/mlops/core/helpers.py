# helpers.py
import os
from pathlib import Path
from typing import Union, Optional, Dict, List
import logging
from logging import config as logging_config
from akerbp.mlops.core import mappings
from akerbp.mlops.core.logger_config import LOGGING_CONFIG

logging_config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)
logging.captureWarnings(True)


def get_top_folder(path: Union[Path, str]) -> Union[Path, str]:
    """
    Get the top folder of a path.

    Args:
        path (Union[Path, str]): Path to get the top folder from.

    Returns:
        (Union[Path, str]): top parent folder in path
    """
    if isinstance(path, str):
        return path.split(os.sep)[0]
    elif isinstance(path, Path):
        return path.parents[len(path.parents) - 2]


def as_import_path(file_path: Optional[str]) -> Optional[str]:
    """Return path as an import path for python modules


    Args:
        file_path (str, optional): path to file

    Returns:
        (Union[str, None]): path to .py-file with .py extension removed(for importing modules)
    """
    if file_path:
        if not isinstance(file_path, str):
            file_path = str(file_path)
        return file_path.replace(os.sep, ".").replace(".py", "")
    else:
        logger.debug("Empty file path -> empty import path returned")
        return None


def confirm_prompt(question: str) -> bool:
    """Helper function to ask user for confirmation

    Args:
        question (str): question to ask user

    Returns:
        (bool): True if user confirms, False otherwise
    """
    reply = None
    while reply not in ("y", "n"):
        reply = input(f"{question} (y/n): ").lower()
    return reply == "y"


def input_data_validation(required_input: List[str], input: Dict) -> bool:
    """Check if the input data contains all the required input curves.
    Note that the input potentially consists of multiple wells according to the payload structures.

    If input logs are provided in the payload, they need to be provided in the field 'input_logs',
    otherwise the validation fails.
    If no input logs are provided, the validation passes if either the field 'well' or
    'well' and 'keyword_arguments' are specified

    Args:
        required_input (List[str]): list of required input curves
        input (Dict): dictionary containing the input data

    Returns:
        bool: whether the input data contains all the required input curves or not
    """
    if required_input is None:
        print("No required input here")
        return True
    curve_mapping = mappings.curve_mappings
    validated = []
    input_wells = input["input"]
    for well_data in input_wells:

        try:
            curves_in_well_data = list(well_data["input_logs"].keys())
            curves_in_well_data_standardized = [
                curve_mapping[curve]
                if curve != "WELL" and curve in curve_mapping.keys()
                else curve
                for curve in curves_in_well_data
            ]
            input_contains_all_required = sum(
                [
                    True if curve in curves_in_well_data_standardized else False
                    for curve in required_input
                ]
            ) == len(required_input)

            if input_contains_all_required:
                validated.append(True)
            else:
                logger.warning(
                    f"The required input curves are not provided: {required_input}"
                )
                validated.append(False)
        except KeyError:
            wrong_input_log_specification = False
            for key in well_data.keys():
                if isinstance(well_data[key], dict) and len(well_data[key].keys()) > 0:
                    wrong_input_log_specification = True
                    break
            if wrong_input_log_specification:
                logger.warning(
                    f"Data is required to be specified as 'input_logs' in the payload, not '{key}'"
                )
                validated.append(False)
            elif "well" in well_data.keys() and "keyword_arguments" in well_data.keys():
                validated.append(True)
            elif "well" in well_data.keys():
                validated.append(True)
            else:
                logger.warning(
                    "Payload not properly specified. Need to specify field 'well', and optionally 'keyword_arguments' if no input logs are provided"
                )
    if sum(validated) < len(input_wells):
        return False
    else:
        return True
