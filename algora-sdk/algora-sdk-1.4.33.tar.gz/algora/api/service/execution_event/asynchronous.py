from typing import Dict, Any

import pandas as pd

from algora.api.service.execution_event.__util import (
    _get_all_portfolio_states_request_info, _get_all_cash_payments_request_info, _create_execution_event_request_info,
    _get_all_execution_events_request_info
)
from algora.api.service.execution_event.model import ExecutionEventRequest
from algora.common.decorators import async_data_request
from algora.common.enum import Order
from algora.common.function import no_transform
from algora.common.requests import __async_put_request, __async_get_request


@async_data_request
async def async_get_all_execution_events(execution_id: str, order: Order = Order.ASC) -> pd.DataFrame:
    """
    Asynchronously get all execution events.

    Args:
        execution_id (str): Execution ID
        order (Order): SQL Order

    Returns:
        DataFrame: DataFrame of execution events
    """
    request_info = _get_all_execution_events_request_info(execution_id, order)
    return await __async_get_request(**request_info)


@async_data_request(transformers=[lambda data: pd.DataFrame([r['data'] for r in data])])
async def async_get_all_portfolio_states(execution_id: str, order: Order = Order.ASC) -> pd.DataFrame:
    """
    Asynchronously get all portfolio states.

    Args:
        execution_id (str): Execution ID
        order (Order): SQL Order

    Returns:
        DataFrame: DataFrame of portfolio states
    """
    request_info = _get_all_portfolio_states_request_info(execution_id, order)
    return await __async_get_request(**request_info)


@async_data_request(transformers=[lambda data: pd.DataFrame([r['data'] for r in data])])
async def async_get_all_cash_payments(execution_id: str, order: Order = Order.ASC) -> pd.DataFrame:
    """
    Asynchronously get all cash payments.

    Args:
        execution_id (str): Execution ID
        order (Order): SQL Order

    Returns:
        DataFrame: DataFrame of cash payments
    """
    request_info = _get_all_cash_payments_request_info(execution_id, order)
    return await __async_get_request(**request_info)


@async_data_request(transformers=[no_transform])
async def async_create_execution_event(request: ExecutionEventRequest) -> Dict[str, Any]:
    """
    Asynchronously create execution event.

    Args:
        request (ExecutionEventRequest): Execution event request

    Returns:
        Dict[str, Any]: Execution event response
    """
    request_info = _create_execution_event_request_info(request)
    return await __async_put_request(**request_info)
