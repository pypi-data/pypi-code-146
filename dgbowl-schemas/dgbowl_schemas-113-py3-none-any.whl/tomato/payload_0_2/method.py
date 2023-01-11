from pydantic import BaseModel, Extra


class Method(BaseModel, extra=Extra.allow):
    """
    The :class:`Method` schema is completely *device*- and ``technique``- dependent,
    with extra arguments required by each ``technique`` defined by each device driver.
    """

    device: str
    """tag of the *device* within a tomato *pipeline*"""

    technique: str
    """name of the technique, must be listed in the capabilities of the *device*"""
