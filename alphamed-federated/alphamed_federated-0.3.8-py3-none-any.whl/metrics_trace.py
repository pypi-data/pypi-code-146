"""A wrapper for metrics trace data."""


import csv
from typing import AnyStr, Dict, Iterable, Iterator, List, overload


class MetricsTrace:
    """A group of metrics trace log."""

    @overload
    def __init__(self, headers: Iterable[str]):
        ...

    @overload
    def __init__(self, headers: Iterable[str], values: Dict[str, AnyStr]):
        ...

    @overload
    def __init__(self, headers: Iterable[str], values: List[Dict[str, AnyStr]]):
        ...

    def __init__(self, headers: Iterable[str], values=None) -> None:
        if (
            not headers
            or not isinstance(headers, Iterable)
            or not all(isinstance(_header, str) for _header in headers)
        ):
            raise TypeError('headers must be a list of header names')
        self.headers = headers

        if values and not isinstance(values, (dict, list)):
            raise TypeError('values must be a dict or a list of dict')

        self._data = []
        if values and isinstance(values, dict):
            self.append_metrics_item(item=values)
        elif values and isinstance(values, list):
            self.append_metrics_list(metrics_list=values)

    def _validate_value_item(self, _value: Dict[str, AnyStr]):
        if not _value or not isinstance(_value, dict):
            raise TypeError(f'invalid value item: {_value}')
        for _header in _value.keys():
            if not _header or not isinstance(_header, str) or _header not in self.headers:
                raise TypeError(f'invalid item: {_header}')
        if len(self.headers) != len(_value):
            raise TypeError(f'item list not match, expect {self.headers}, received {_value.keys()}')

    def append_metrics_item(self, item: Dict[str, AnyStr]):
        self._validate_value_item(item)
        self._data.append(tuple(item[_key] for _key in self.headers))

    def append_metrics_list(self, metrics_list: List[Dict[str, AnyStr]]):
        if not metrics_list or not isinstance(metrics_list, list):
            raise TypeError(f'invalid value type: {type(metrics_list)}')
        for _item in metrics_list:
            self.append_metrics_item(_item)

    def to_csv(self, file: str):
        """Export metrics data into a csv file."""
        with open(file, 'w') as metrics_file:
            writer = csv.DictWriter(metrics_file, fieldnames=self.headers)
            writer.writeheader()
            for _item in self._data:
                writer.writerow(dict((_key, str(_val))
                                for (_key, _val) in zip(self.headers, _item)))

    def trace(self) -> Iterator[dict]:
        for _item in self._data:
            yield dict((_key, str(_val))
                       for (_key, _val) in zip(self.headers, _item))
