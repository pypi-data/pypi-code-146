import argparse
from typing import Any, Dict, List, Optional
from declarative_argparse.options.abc import IDeclarativeOption


class _StoreTruth(IDeclarativeOption):
    ACTION: str
    DEFAULT: bool
    def add_to_argparser(self, argp: argparse.ArgumentParser) -> None:
        args: List[str] = []
        args += self.long_forms
        args += self.short_forms
        kwargs: Dict[str, Any] = {}
        kwargs['action'] = self.ACTION
        kwargs['default'] = self.DEFAULT
        if self.description is not None:
            kwargs['help'] = self.description
        self.action = argp.add_argument(*args, **kwargs)

    def get_value(self) -> Optional[bool]:
        o = super().get_value()
        if o is None:
            return None
        return bool(o)

    def handle_input(self, arg_content: str) -> Any:
        return

class StoreTrueDO(_StoreTruth):
    ACTION: str = 'store_true'
    DEFAULT: bool = False

class StoreFalseDO(_StoreTruth):
    ACTION: str = 'store_false'
    DEFAULT: bool = True
