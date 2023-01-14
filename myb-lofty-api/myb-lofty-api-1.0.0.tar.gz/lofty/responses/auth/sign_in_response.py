from .device_metadata import DeviceMetadata


class SignInResponse:

    def __init__(self, authentication_result: dict):
        # A JWT
        self.access_token: str = authentication_result.get('AccessToken')
        # Example: 3600
        self.expires_in: int = authentication_result.get('ExpiresIn')
        # Typically 'Bearer'
        self.token_type: str = authentication_result.get('TokenType')
        # A JWT
        self.refresh_token: str = authentication_result.get('RefreshToken')
        # A JWT
        self.id_token: str = authentication_result.get('IdToken')
        self.device_metadata: DeviceMetadata = DeviceMetadata(authentication_result.get('NewDeviceMetadata')) \
            if 'NewDeviceMetadata' in authentication_result else None
