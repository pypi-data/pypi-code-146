import sys
from typing import Optional, Union

from ..interfaces.context import Context
from ..interfaces.inputter import Inputter
from ..interfaces.outputter import Outputter


class StdinInputter(Inputter[str]):
    def read(self) -> Context[str]:
        return Context(sys.stdin.read())


class StdoutOutputter(Outputter[Union[str, bytes]]):
    def write(
        self,
        value: Union[str, bytes],
        *,
        context: Optional[Context[Union[str, bytes]]] = None
    ) -> None:
        if isinstance(value, bytes):
            value = value.decode()
        sys.stdout.write(value)
