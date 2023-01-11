# pylint: disable=too-few-public-methods
"""Flywheel CLI global models"""

from pydantic import BaseModel  # pylint: disable=no-name-in-module


class FWAuth(BaseModel):
    """Flywheel site and user info model"""

    api_key: str
    host: str
    user_id: str
    is_admin: bool
    is_device: bool
