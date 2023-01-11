import hashlib
import hmac
import requests

class Auth:
    @classmethod
    def get_auth(cls, organization_id, api_key):
        response = requests.get('https://app.moderntreasury.com/api/ping',
                         auth=(organization_id, api_key))
        return response


    def is_valid_webhook_request(request, webhook_auth_key):
        """
        Validates a webhook request, ensuring a valid signature.
        :param request: request
        :return: True if valid, False otherwise
        """
        secret = webhook_auth_key
        hash_bytes = hmac.new(secret, msg=request.body, digestmod=hashlib.sha256).hexdigest()

        if not hash_bytes == request.headers.get("x-signature", "").split("=")[0]:
            return False
        return True