from __future__ import annotations

from dataclasses import dataclass

from semantha_sdk.model import SemanthaModelEntity


@dataclass(frozen=True)
class Domain:
    id: str
    name: str
    base_url: str


@dataclass(frozen=True)
class Domains(SemanthaModelEntity):

    def __post_init__(self):
        assert type(self.data) is list

    @property
    def domains(self) -> list[Domain]:
        return [Domain(domain["id"], domain["name"], base_url=domain["baseUrl"]) for domain in self.data]
