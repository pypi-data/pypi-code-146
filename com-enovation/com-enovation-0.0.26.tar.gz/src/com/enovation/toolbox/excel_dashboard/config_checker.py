from os.path import join, dirname
from inspect import stack
from logging import Logger, getLogger
import json
from pathlib import Path
from typing import Union

from jsonschema import RefResolver, Validator
from jsonschema.validators import validator_for


class ConfigChecker:
    """
    The ConfigChecker
    """
    _logger: Logger = getLogger(__name__)

    # The main excel_dashboard json schema
    _path_excel_dashboard_json_schema: Path = Path(join(dirname(__file__), 'config_checkers/excel_dashboard.json'))

    # Basic json schemas, used across widgets, are subscribed below.
    _lst_paths_to_basic_json_schemas: list = [
        Path(join(dirname(__file__), 'config_checkers/xlsxwriter_workbook__add_format.json')),
        Path(join(dirname(__file__), 'config_checkers/xlsxwriter_colors.json')),
        Path(join(dirname(__file__), 'config_checkers/xlsxwriter_vba.json')),
        Path(join(dirname(__file__), 'config_checkers/xlsxwriter_address_range.json')),
        Path(join(dirname(__file__), 'config_checkers/xlsxwriter_worksheet__add_table.json')),
        Path(join(dirname(__file__), 'config_checkers/xlsxwriter_worksheet__conditional_format__options.json')),
        Path(join(dirname(__file__), 'config_checkers/xlsxwriter_worksheet__conditional_format.json')),
        Path(join(dirname(__file__), 'config_checkers/xlsxwriter_workbook__set_properties.json')),
        Path(join(dirname(__file__), 'config_checkers/xlsxwriter_worksheet__freeze_panes.json')),
        Path(join(dirname(__file__), 'config_checkers/xlsxwriter_worksheet__set_column.json')),
    ]

    # The Validator instance which is used to later validate json configurations
    _obj_validator: Validator = None

    def __init__(
            self,
            lst_widgets_json_schemas: list[dict],
            str_base_json_schema_id: str = "https://enovation.com/excel_dashboard",
    ):
        """
        Initialize the config checker. The json schemas are loaded, and a RefResolver is instantiated.

        By default, the config checker will validate an excel dashboard, but we can set another json schema, mostly
        used to validate json schemas unitarily.
        """
        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called.")

        _dict_the_store_of_json_schema: dict = {}

        # We register the widgets' schemas: their schemas are loaded, and registered in the dictionary
        for i_json_schema_path in lst_widgets_json_schemas:
            self._register_json_schema(
                dict_store_of_json_schema=_dict_the_store_of_json_schema,
                json_schema=i_json_schema_path
            )

        # We register the the main excel dashboard schema, after having enriched it with the eligible widgets
        _dict_the_enriched_excel_dashboard_json_schema: dict = self._enrich_master_json_schema(
            dict_store_of_json_schema=_dict_the_store_of_json_schema,
            path_json_schema=self._path_excel_dashboard_json_schema
        )

        self._register_json_schema(
            dict_store_of_json_schema=_dict_the_store_of_json_schema,
            json_schema=_dict_the_enriched_excel_dashboard_json_schema
        )

        # We register the basic json schemas
        for i_json_schema_path in self._lst_paths_to_basic_json_schemas:
            self._register_json_schema(
                dict_store_of_json_schema=_dict_the_store_of_json_schema,
                json_schema=i_json_schema_path
            )

        # We eventually instantiate the reference resolver, and the Validator
        if str_base_json_schema_id not in _dict_the_store_of_json_schema:
            raise Exception(f"We could not find the base json schema '{str_base_json_schema_id}'.")

        _the_resolver: RefResolver = RefResolver.from_schema(
            schema=_dict_the_store_of_json_schema[str_base_json_schema_id],
            store=_dict_the_store_of_json_schema
        )

        self._obj_validator = validator_for(
            _dict_the_store_of_json_schema[str_base_json_schema_id]
        )(
            _dict_the_store_of_json_schema[str_base_json_schema_id],
            resolver=_the_resolver
        )

        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning.")

    def _register_json_schema(
            self,
            dict_store_of_json_schema: dict,
            json_schema: Union[Path, dict],
    ):
        """
        Function that:
         - Loads a json schema from a path
         - checks there is an $id
         - checks this $id was not previously registered, and
         - eventually load this schema into the dictionary.
        :param dict_store_of_json_schema: the store of json schemas
        :param json_schema: the json schema which is processed, either a path to a json file or a dictionary
        """
        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called.")

        _dict_json_schema: dict
        _error_msg: str

        if isinstance(json_schema, Path):
            with open(json_schema, "r") as _the_file:
                _dict_json_schema: dict = json.loads(_the_file.read())
            _error_msg = f"When loading json schema from file '{json_schema}'"
        else:
            _dict_json_schema = json_schema
            _error_msg = f"When loading json schema '{json_schema}'"

        if "$id" not in _dict_json_schema:
            self._logger.error(f"{_error_msg}', it did not have an $id, so it could not be loaded in the json schemas "
                               f"store.")
        elif _dict_json_schema["$id"] in dict_store_of_json_schema:
            self._logger.error(f"{_error_msg}, its $id '{_dict_json_schema['$id']}' was already registered. This new "
                               f"version will be therefore ignored, and only the first version will be kept.")
        else:
            dict_store_of_json_schema[_dict_json_schema["$id"]] = _dict_json_schema

        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning.")

    def _enrich_master_json_schema(
            self,
            dict_store_of_json_schema: dict,
            path_json_schema: Path
    ) -> dict:
        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called.")

        with open(path_json_schema, "r") as _the_file:
            _dict_the_return: dict = json.loads(_the_file.read())

        _lst_widgets_schemas: list[dict] = [
            {
                "properties": {
                    "widget_id": {
                        "const": i_schema_id
                    },
                    "config": {
                        "$ref": i_schema_id[len("https://enovation.com"):]
                    }
                },
                "required": [
                    "config"
                ]
            }
            for i_schema_id in dict_store_of_json_schema
        ]

        _dict_the_return["properties"]["sheets"]["patternProperties"][""]["properties"]["widgets"][
            "patternProperties"][""]["oneOf"] = _lst_widgets_schemas

        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning.")

        return _dict_the_return

    def validate(self, dict_to_validate: dict):
        """
        Validate the parameter "dict_to_validate" against a given json schema. If the dict to validate is correct, the
        function returns. Otherwise, an exception ValidationError is thrown.

        In case we need to make the ValidationError more explicit, we can override this function, catch the exception,
        and adjust it to make it more meaningful before re-raising it.

        :param dict_to_validate: the dictionary to validate
        """
        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called.")

        self._obj_validator.validate(
            instance=dict_to_validate
        )

        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning.")
