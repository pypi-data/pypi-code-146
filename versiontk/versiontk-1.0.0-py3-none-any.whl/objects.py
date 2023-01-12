from dataclasses import dataclass


@dataclass(frozen=False, order=True)
class Version:
    major: int
    minor: int
    patch: int
