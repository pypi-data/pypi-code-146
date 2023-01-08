from .abc import ABCResponseValidator
from .telegram_api_error_validator import TelegramAPIErrorResponseValidator

DEFAULT_RESPONSE_VALIDATORS = [TelegramAPIErrorResponseValidator()]
