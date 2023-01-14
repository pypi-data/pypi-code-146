"""Authentication and database connection."""
from typing import Optional
from hashlib import sha256
from jose import jwt
from pydantic import BaseModel


class DBCredentials(BaseModel):
    """Database credentials"""
    database_url: str
    token: Optional[str] = None
    
    def hash(self):
        """Hashes the database url"""
        return sha256(self.database_url.encode()).hexdigest()
    
    def encode(self):
        """Encodes the database url"""
        return jwt.encode(self.database_url, self.hash())
    
    def decode(self):
        """Decodes the database url"""
        return jwt.decode(self.database_url, self.hash())
    
    
    def __init__(self, **data):
        super().__init__(**data)
        self.token = jwt.encode(
            {"database_url": self.database_url},
            self.hash()
        )