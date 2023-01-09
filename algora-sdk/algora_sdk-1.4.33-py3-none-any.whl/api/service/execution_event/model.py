from datetime import date
from typing import Optional, Dict, Any

from algora.api.service.execution_event.enum import EventType
from algora.common.base import Base


class BaseExecutionEvent(Base):
    execution_id: str
    event_type: EventType


class ExecutionEventRequest(BaseExecutionEvent):
    execution_id: str
    event_type: EventType
    data: dict


class ExecutionEventResponse(BaseExecutionEvent):
    id: str
    execution_id: str
    event_type: EventType
    data: Any
    created_at: int


class CashPaymentEvent(Base):
    payment_date: date
    type: str
    amount: float
    position_id: Optional[str]
    currency: Optional[str]


class PortfolioStateEvent(Base):
    date: date
    valuation: float
    pnl: float
    portfolio: Dict[str, Any]
