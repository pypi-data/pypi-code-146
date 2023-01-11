from typing import Union

from ..extensions import UnknownType
from ..models.canvas_initialize_webhook import CanvasInitializeWebhook
from ..models.canvas_interaction_webhook import CanvasInteractionWebhook

WebhookMessage = Union[CanvasInteractionWebhook, CanvasInitializeWebhook, UnknownType]
