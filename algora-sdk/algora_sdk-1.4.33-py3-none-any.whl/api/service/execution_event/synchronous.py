from typing import Dict, Any

import pandas as pd

from algora.api.service.execution_event.__util import (
    _get_all_portfolio_states_request_info, _get_all_cash_payments_request_info, _create_execution_event_request_info,
    _get_all_execution_events_request_info
)
from algora.api.service.execution_event.model import ExecutionEventRequest
from algora.common.decorators import data_request
from algora.common.enum import Order
from algora.common.function import no_transform
from algora.common.requests import __put_request, __get_request


@data_request
def get_all_execution_events(execution_id: str, order: Order = Order.ASC) -> pd.DataFrame:
    """
    Get all execution events.

    Args:
        execution_id (str): Execution ID
        order (Order): SQL Order

    Returns:
        DataFrame: DataFrame of execution events
    """
    request_info = _get_all_execution_events_request_info(execution_id, order)
    return __get_request(**request_info)


@data_request(transformers=[lambda data: pd.DataFrame([r['data'] for r in data])])
def get_all_portfolio_states(execution_id: str, order: Order = Order.ASC) -> pd.DataFrame:
    """
    Get all portfolio states.

    Args:
        execution_id (str): Execution ID
        order (Order): SQL Order

    Returns:
        DataFrame: DataFrame of portfolio states
    """
    request_info = _get_all_portfolio_states_request_info(execution_id, order)
    return __get_request(**request_info)


@data_request(transformers=[lambda data: pd.DataFrame([r['data'] for r in data])])
def get_all_cash_payments(execution_id: str, order: Order = Order.ASC) -> pd.DataFrame:
    """
    Get all cash payments.

    Args:
        execution_id (str): Execution ID
        order (Order): SQL Order

    Returns:
        DataFrame: DataFrame of cash payments
    """
    request_info = _get_all_cash_payments_request_info(execution_id, order)
    return __get_request(**request_info)


@data_request(transformers=[no_transform])
def create_execution_event(request: ExecutionEventRequest) -> Dict[str, Any]:
    """
    Create execution event.

    Args:
        request (ExecutionEventRequest): Execution event request

    Returns:
        Dict[str, Any]: Execution event response
    """
    request_info = _create_execution_event_request_info(request)
    return __put_request(**request_info)
