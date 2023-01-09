from pydantic import BaseModel


class Editor(BaseModel):
    slug: str
    name: str
    api_url: str
    status: bool
    _test_mode: bool
