from dataclasses import dataclass


@dataclass
class JsonStatus:
    success: bool
    message: str


@dataclass
class JsonRequestError:
    success: bool
    formError: dict
