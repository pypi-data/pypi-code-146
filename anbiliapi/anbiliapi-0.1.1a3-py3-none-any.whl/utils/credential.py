from pydantic import BaseModel


class Credential(BaseModel):
    SESSDATA: str
    bili_jct: str
    buvid3: str
    DedeUserID: str
