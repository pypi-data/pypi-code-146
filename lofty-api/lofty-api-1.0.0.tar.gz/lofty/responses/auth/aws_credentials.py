from datetime import datetime


class AwsCredentials:

    def __init__(self, credentials_result: dict):
        self.access_key_id: str = credentials_result.get('AccessKeyId')
        self.secret_key: str = credentials_result.get('SecretKey')
        self.session_token: str = credentials_result.get('SessionToken')
        self.expiration: datetime = credentials_result.get('Expiration')
