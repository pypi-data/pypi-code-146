import typing
from abc import ABC
from typing import Iterable

from rdflib import Literal

from iolanta.facet import Facet

RowType = typing.TypeVar('RowType')


class LanguageAware(Facet, ABC):
    """Language aware facet."""

    @property
    def language(self) -> str:
        return 'en'

    def _is_row_fitting_language(self, row) -> bool:
        """All literals in the row either have no language or match the site."""
        for field_name, field_value in row.items():
            if (
                isinstance(field_value, Literal)
                and field_value.language
                and field_value.language != self.language
            ):
                return False

        return True

    def filter_by_language(self, rows: Iterable[RowType]) -> Iterable[RowType]:
        return filter(
            self._is_row_fitting_language,
            rows,
        )

    def query(self, query_text: str, **kwargs):
        """Language aware query."""
        return self.filter_by_language(
            super().query(query_text, **kwargs),
        )
