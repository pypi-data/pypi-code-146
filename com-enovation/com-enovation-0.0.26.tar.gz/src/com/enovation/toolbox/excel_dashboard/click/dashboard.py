import logging
from inspect import stack
from pathlib import Path

import click
from click import BadParameter

from com.enovation.helper.click.python_literal_argument_and_option import PythonLiteralOption
from com.enovation.toolbox.excel_dashboard import ExcelDashboarder


_logger: logging.Logger = logging.getLogger(__name__)


@click.command('dashboard')
@click.pass_context
@click.argument('alias-config', type=str)
@click.argument('file', type=click.Path(exists=False))
@click.option(
    '--parameters', cls=PythonLiteralOption, type=dict, default=None,
    help='The parameters, provided as a dictionary, that are required in the dashboard configuration.'
)
@click.option(
    '--alias-parameters', cls=PythonLiteralOption, type=dict, default=None,
    help='The parameters, loaded as an alias in context, that are required in the dashboard configuration.'
)
def dashboard(ctx_context, alias_config, file, parameters, alias_parameters):
    """
    TODO

    The following business rules are checked:
    - BR_001, ALIAS_CONFIG should exist in context
    - BR_002, ALIAS_CONFIG should be a dictionary
    - BR_003, PARAMETERS, if provided, should be a dictionary
    - BR_004, ALIAS_PARAMETERS, if provided, should be a dictionary
    - BR_005, ALIAS_PARAMETERS, if provided, should only contain string values
    - BR_006, ALIAS_PARAMETERS, if provided, should list parameters that all exist in context
    - BR_007, there should not be duplicates across PARAMETERS and ALIAS_PARAMETERS

    """
    _logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called")
    _dict_the_config: dict
    _dict_the_parameters: dict = {}

    # BR_001, ALIAS_CONFIG should exist in context
    if alias_config not in ctx_context.obj:
        raise BadParameter(
            message=f"BR_001, no object labelled '{alias_config}' could be found in context, which is not expected.",
            param_hint=f"BR_001, ensure you effectively have an object labelled '{alias_config}' in context.",
            ctx=ctx_context
        )

    # BR_002, ALIAS_CONFIG should be a dictionary
    if not isinstance(ctx_context.obj[alias_config], dict):
        raise BadParameter(
            message=f"BR_002, object labelled '{alias_config}' is of type '{type(ctx_context.obj[alias_config])}', "
                    f"which is not expected.",
            param_hint=f"BR_002, ensure you provide a 'dict' instance.",
            ctx=ctx_context
        )

    _dict_the_config = ctx_context.obj[alias_config]

    if parameters is not None:

        # BR_003, PARAMETERS, if provided, should be a dictionary
        if not isinstance(parameters, dict):
            raise BadParameter(
                message=f"BR_003, parameter 'parameters' is of type '{type(parameters)}', "
                        f"which is not expected.",
                param_hint=f"BR_003, ensure you provide a parameter 'parameters' of type 'dict'.",
                ctx=ctx_context
            )

        _dict_the_parameters = parameters

    if alias_parameters is not None:

        # BR_004, ALIAS_PARAMETERS, if provided, should be a dictionary
        if not isinstance(alias_parameters, dict):
            raise BadParameter(
                message=f"BR_004, parameter 'parameters' is of type '{type(alias_parameters)}', "
                        f"which is not expected.",
                param_hint=f"BR_004, ensure you provide a parameter 'alias_parameters' of type 'dict'.",
                ctx=ctx_context
            )

        for k, v in alias_parameters.items():

            # BR_005, ALIAS_PARAMETERS, if provided, should only contain string values
            if not isinstance(v, str):
                raise BadParameter(
                    message=f"BR_005, alias_parameter with key '{k}' points to an alias label of type "
                            f"'{type(v)}', which is not expected.",
                    param_hint=f"BR_005, ensure you provide 'alias_parameters' of type 'dict[str,str]'.",
                    ctx=ctx_context
                )

            # BR_006, ALIAS_PARAMETERS, if provided, should list parameters that all exist in context
            if v not in ctx_context.obj:
                raise BadParameter(
                    message=f"BR_006, no object labelled '{v}' could be found in context, which is not expected.",
                    param_hint=f"BR_006, ensure you effectively have an object labelled '{v}' in context.",
                    ctx=ctx_context
                )

            # BR_007, there should not be duplicates across PARAMETERS and ALIAS_PARAMETERS
            if k in _dict_the_parameters:
                raise Exception(f"BR_007, parameter '{k}' is provided both into 'parameters' and 'alias_parameter'. "
                                f"This is not expected, as we can't know which one to keep, and which one to discard.")

            _dict_the_parameters[k] = ctx_context.obj[v]

    # We can now call the ExcelDashboarder
    _the_excel_dashboard: ExcelDashboarder = ExcelDashboarder()

    try:
        _the_excel_dashboard.excelize(
            p_output_file_path=Path(file),
            dict_config=_dict_the_config,
            **_dict_the_parameters
        )
    except Exception as an_exception:
        click.secho('An exception was thrown!!!', blink=True, fg='red')
        click.secho(f"{an_exception}", fg='blue')
        raise Exception(f"") from an_exception

    _logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning")
