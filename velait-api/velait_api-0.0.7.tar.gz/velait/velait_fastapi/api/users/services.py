from velait.velait_fastapi.api.users.exceptions import NotAuthorizedError
from velait.velait_fastapi.api.users.schemas import UserSchema
from velait.velait_fastapi.connections.exceptions import RequestError
from velait.velait_fastapi.connections.http import HTTPClient


class SSOService:
    def __init__(self, sso_client: HTTPClient):
        self.sso_client = sso_client

    def _create_authorization_headers(self, token: str):
        return {"Authorization": token}

    async def get_user_info(self, token: str):
        try:
            if not token:
                raise NotAuthorizedError()

            user_info = await self.sso_client.request(
                "/o/userinfo/", "GET", headers=self._create_authorization_headers(token))
        except RequestError:
            raise NotAuthorizedError()

        return UserSchema(
            id=user_info['uuid'],
            username=user_info['preferred_username'],
            email=user_info['email'],
            permissions=user_info['groups'],
        )


__all__ = ['SSOService']
