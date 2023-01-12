from pydantic import BaseModel


class Auth(BaseModel):
    client_key: str
    client_secret: str
    token: dict
    