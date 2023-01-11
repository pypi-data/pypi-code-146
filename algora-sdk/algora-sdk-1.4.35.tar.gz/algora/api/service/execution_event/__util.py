from algora.api.service.execution_event.model import ExecutionEventRequest
from algora.common.enum import Order


def _get_all_execution_events_request_info(execution_id: str, order: Order = Order.ASC) -> dict:
    config = {
        "endpoint": f"config/execution/event/{execution_id}?order={order}"
    }

    return config


def _get_all_portfolio_states_request_info(execution_id: str, order: Order = Order.ASC) -> dict:
    config = {
        "endpoint": f"config/execution/event/{execution_id}?type=PORTFOLIO&order={order}"
    }

    return config


def _get_all_cash_payments_request_info(execution_id: str, order: Order = Order.ASC) -> dict:
    config = {
        "endpoint": f"config/execution/event/{execution_id}?type=CASH_PAYMENT&order={order}"
    }

    return config


def _create_execution_event_request_info(request: ExecutionEventRequest) -> dict:
    return {
        "endpoint": "config/execution/event",
        "json": request.request_dict()
    }
