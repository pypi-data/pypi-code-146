from typing import Dict, Any


class BaseError(Exception):
    def __init__(self, message: str, data: Dict[Any, Any] = None):
        self.message = message
        self.data = data
