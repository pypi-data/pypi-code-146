import base64
from typing import Optional, Type
from aiolago.types.base import BaseRoute, BaseModel, lazyproperty

__all__ = [
    'WebhookRoute',
]

class WebhookRoute(BaseRoute):

    @lazyproperty
    def public_key(self):
        api_response = self.client.get(
            url = 'webhooks/public_key',
            headers = self.headers
        )
        coded_response = self.handle_response(api_response).text
        return base64.b64decode(coded_response)
