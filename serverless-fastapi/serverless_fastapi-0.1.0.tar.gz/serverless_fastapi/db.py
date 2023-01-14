from hashlib import sha256
from jose import jwt
from pydantic import Field, BaseModel
from typing import Optional
from serverless_fastapi.config import Settings

class DBCredentials(BaseModel):
    database_url: Optional[str]
    token: Optional[str] = Field(default=None)
    
    def hash(self):
        return sha256(self.dict()['database_url'].encode()).hexdigest()
    
    def encode(self):
        return jwt.encode(self.database_url, self.hash())
    
    def decode(self):
        return jwt.decode(self.database_url, self.hash())
    
    
    def __init__(self, **data):
        super().__init__(**data)
        if self.database_url is None:
            self.database_url = Settings().DATABASE_URL
        self.token = jwt.encode(
            {"database_url": self.database_url},
            self.hash())