from __future__ import annotations

from pydantic import BaseModel, Field


class Response(BaseModel):
    success: bool


class ResError(Response):
    message: str


class ResOK(Response):
    site_id: int = Field(..., alias='siteId')
    number_of_webhooks: int = Field(..., alias='numberOfWebhooks')
    request_received_at: str = Field(..., alias='requestReceivedAt')
    request_fullfilled_at: str = Field(..., alias='requestFullfilledAt')
    request_duration: float = Field(..., alias='requestDuration')
