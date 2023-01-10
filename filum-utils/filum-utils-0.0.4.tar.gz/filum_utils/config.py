import os


class Config:
    APPSTORE_BASE_URL = "https://appstore.filum.gq"
    APPSTORE_USERNAME = "appstore@filum.ai"
    APPSTORE_PASSWORD = ""

    NOTIFICATION_BASE_URL = "https://notification.filum.gq"
    NOTIFICATION_USERNAME = "notification@filum.ai"
    NOTIFICATION_PASSWORD = ""

    SUBSCRIPTION_BASE_URL = "https://subscription.filum.gq"
    SUBSCRIPTION_USERNAME = "subscription@filum"
    SUBSCRIPTION_PASSWORD = ""

    FILUM_BASE_URL = "https://api.filum.gq"
    FILUM_USERNAME = "filum_dev"
    FILUM_PASSWORD = ""

    EVENT_API_BASE_URL = "https://event.filum.gq"

    SEGMENT_RECORD_LIMIT = 3000

    def __init__(self):
        for attr in dir(self):
            if not attr.isupper():
                continue
            default_value = getattr(self, attr)
            value_type = type(default_value)

            value = os.getenv(attr) or default_value

            if value and isinstance(default_value, list) and isinstance(value, str):
                value = value.split(",")
            elif value_type is bool and isinstance(value, str):
                value = value.lower() in ["true", "yes", "t", "i", "1"]
            else:
                value = value_type(value)

            setattr(self, attr, value)


config = Config()
