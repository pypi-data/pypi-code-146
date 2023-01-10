from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.assay_result_create import AssayResultCreate
from ..types import UNSET, Unset

T = TypeVar("T", bound="ResultsBulkCreateRequest")


@attr.s(auto_attribs=True, repr=False)
class ResultsBulkCreateRequest:
    """  """

    _results: List[AssayResultCreate]
    _table_id: Union[Unset, None, str] = UNSET

    def __repr__(self):
        fields = []
        fields.append("results={}".format(repr(self._results)))
        fields.append("table_id={}".format(repr(self._table_id)))
        return "ResultsBulkCreateRequest({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        results = []
        for results_item_data in self._results:
            results_item = results_item_data.to_dict()

            results.append(results_item)

        table_id = self._table_id

        field_dict: Dict[str, Any] = {}
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if results is not UNSET:
            field_dict["results"] = results
        if table_id is not UNSET:
            field_dict["tableId"] = table_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_results() -> List[AssayResultCreate]:
            results = []
            _results = d.pop("results")
            for results_item_data in _results:
                results_item = AssayResultCreate.from_dict(results_item_data, strict=False)

                results.append(results_item)

            return results

        try:
            results = get_results()
        except KeyError:
            if strict:
                raise
            results = cast(List[AssayResultCreate], UNSET)

        def get_table_id() -> Union[Unset, None, str]:
            table_id = d.pop("tableId")
            return table_id

        try:
            table_id = get_table_id()
        except KeyError:
            if strict:
                raise
            table_id = cast(Union[Unset, None, str], UNSET)

        results_bulk_create_request = cls(
            results=results,
            table_id=table_id,
        )

        return results_bulk_create_request

    @property
    def results(self) -> List[AssayResultCreate]:
        if isinstance(self._results, Unset):
            raise NotPresentError(self, "results")
        return self._results

    @results.setter
    def results(self, value: List[AssayResultCreate]) -> None:
        self._results = value

    @property
    def table_id(self) -> Optional[str]:
        if isinstance(self._table_id, Unset):
            raise NotPresentError(self, "table_id")
        return self._table_id

    @table_id.setter
    def table_id(self, value: Optional[str]) -> None:
        self._table_id = value

    @table_id.deleter
    def table_id(self) -> None:
        self._table_id = UNSET
