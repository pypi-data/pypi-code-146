from enum import Enum

import dash_bootstrap_components as dbc


class FilterError(Exception):
    pass


class TruEraError(Enum):
    NO_ERROR = ""
    MEMORY_ERROR = "Cannot perform computations with this much data. Please reduce the selected number of records."
    FILTER_ERROR = "No available data with current filters. Please change filter specifications or increase the selected number of records."


class VizResponse:

    def __init__(self, result, error_code=TruEraError.NO_ERROR):
        self.result = result
        self.error_code = error_code

    def is_error(self):
        return self.error_code != TruEraError.NO_ERROR

    def get_error_text(self):
        return self.error_code.value


def create_component_alert_bar(id):
    return dbc.Alert(
        "",
        id=id,
        is_open=False,
        color="danger",
        dismissable=True,
        style={
            "display": "block",
            "margin-left": "auto",
            "margin-right": "auto"
        }
    )


def viz_callback(f):

    def wrapper(*args, **kwargs):
        result = None
        error = TruEraError.NO_ERROR
        try:
            result = f(*args, **kwargs)
        except MemoryError:
            error = TruEraError.MEMORY_ERROR
        except FilterError:
            error = TruEraError.FILTER_ERROR
        return VizResponse(result, error)

    return wrapper


class FeatureFlag(Enum):
    ALPHA = 'alpha'
    BETA = 'beta'
    GA = 'general_audience'
