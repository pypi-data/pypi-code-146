import base64
from pathlib import Path
from urllib.parse import urlparse


class Common:

    @staticmethod
    def get_project_root() -> Path:
        return Path(__file__).parents[5]

    @staticmethod
    def transform_dict_with_mapping(dict_, mapping, default_value=None):
        transformed_dict = {k: dict_.get(v, default_value) for k, v in mapping.items()}
        return transformed_dict

    @staticmethod
    def validate_schema(data, schema):
        error = {}
        try:
            schema().load(data)
        except Exception as e:
            error = e
        return data, error

    @staticmethod
    def is_url(url: str) -> bool:
        """
        Check input string is URL or not

        Input:
            - url (str): String need to validate

        Output: result after checked (True/False)
        """
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except ValueError:
            return False

    @staticmethod
    def hash_message(message_value: str) -> str:
        """
        Hash message into Base64.
        Input:
        - message_value (str): Message need to hash

        Output:
        - base64_message (str): Messsage after hashed

        """
        message_bytes = message_value.encode('utf-8')
        base64_bytes = base64.b64encode(message_bytes)
        base64_message = base64_bytes.decode('utf-8')
        return base64_message
