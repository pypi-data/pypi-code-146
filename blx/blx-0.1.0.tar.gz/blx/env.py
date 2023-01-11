from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

__all__ = ["Env", "env"]


@dataclass
class Env:
    BUCKET: str
    HOST: str
    ACCESS_KEY: str
    SECRET_KEY: str


load_dotenv()

env = Env(
    os.getenv("BUCKET", "bucket-name"),
    os.getenv("HOST", "s3.address.io"),
    os.getenv("ACCESS_KEY", "access-key"),
    os.getenv("SECRET_KEY", "secret-key"),
)
