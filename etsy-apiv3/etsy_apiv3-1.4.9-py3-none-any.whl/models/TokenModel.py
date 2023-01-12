import pydantic


class Token(pydantic.BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    expires_in: int
    expires_at: float