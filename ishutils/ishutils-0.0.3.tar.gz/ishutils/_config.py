import dataclasses


@dataclasses.dataclass(kw_only=True)
class Config:
    confirm: bool = True
