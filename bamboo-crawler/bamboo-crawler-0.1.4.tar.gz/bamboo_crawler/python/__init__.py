import re
from dataclasses import dataclass
from datetime import date, datetime, time
from typing import Any, Dict, Iterable, Optional, Union
from urllib.parse import parse_qs, urlparse

from ..interfaces.context import Context
from ..interfaces.processor import Processor


@dataclass
class PythonProcessor(Processor):
    mappers: Dict[str, str]

    def __safe_eval(
        self, code: str, data: Any, metadata: Dict[str, Any]
    ) -> Any:
        def extract_digit(data: str) -> str:
            return "".join(x for x in data if x.isdigit())

        allowed_functions = {
            "int": int,
            "float": float,
            "str": str,
            "extract_digit": extract_digit,
            "urlparse": urlparse,
            "parse_qs": parse_qs,
            "date": date,
            "time": time,
            "datetime": datetime,
            "max": max,
            "all": all,
            "any": any,
            "divmod": divmod,
            "sorted": sorted,
            "ord": ord,
            "chr": chr,
            "bin": bin,
            "sum": sum,
            "pow": pow,
            "len": len,
            "range": range,
            "map": map,
            "re": re,
        }
        globals_ = {"__builtins__": allowed_functions}
        locals_ = {"_": data, "meta": metadata}
        try:
            return eval(code, globals_, locals_)
        except Exception:
            return None

    def process(
        self, data: Union[str, bytes], *, context: Optional[Context] = None
    ) -> Iterable[Dict[str, Any]]:
        yield {
            key: self.__safe_eval(
                code, data, metadata=context.metadata if context else {}
            )
            for key, code in self.mappers.items()
        }
