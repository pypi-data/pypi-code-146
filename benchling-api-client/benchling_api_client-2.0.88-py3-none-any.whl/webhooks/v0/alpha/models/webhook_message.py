from typing import Union

from ..extensions import UnknownType
from ..models.lifecycle_activate_webhook import LifecycleActivateWebhook
from ..models.lifecycle_deactivate_webhook import LifecycleDeactivateWebhook

WebhookMessage = Union[LifecycleActivateWebhook, LifecycleDeactivateWebhook, UnknownType]
