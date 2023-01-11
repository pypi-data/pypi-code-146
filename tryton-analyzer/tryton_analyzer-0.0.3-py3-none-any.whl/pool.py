from __future__ import annotations

import os
from collections.abc import Generator
from pathlib import Path

from libcst.metadata import CodeRange
from trytond.pool import Pool as TrytonPool
from trytond.pool import PoolBase

from .analyzer import CompletionTargetFound, PythonCompletioner
from .parsing import (
    Module,
    ParsedFile,
    ParsedPythonFile,
    ParsedViewFile,
    ParsedXMLFile,
    ParsingError,
)
from .tools import CompletionItem, Diagnostic, generate_completions_from_model


class TrytonInitException(Exception):
    pass


class PoolManager:
    def __init__(self) -> None:
        super().__init__()
        self._parsed: dict[Path, ParsedFile | None] = {}
        self._pools: dict[tuple[str, ...], Pool] = {}
        self._modules: dict[str, Module] = {}

    def _get_module(self, module_name: str) -> Module:
        if module_name in self._modules:
            return self._modules[module_name]
        module = Module(module_name)
        self._modules[module_name] = module
        return module

    def generate_diagnostics(
        self,
        path: Path,
        ranges: list[CodeRange] | None = None,
        data: str | None = None,
    ) -> list[Diagnostic]:
        parsed = self.get_parsed(path, data=data)
        if parsed:
            return self._get_diagnostics(parsed, ranges=ranges)
        return []

    def generate_completions(
        self, path: Path, line: int, column: int, data: str | None = None
    ) -> list[CompletionItem]:
        parsed = self.get_parsed(path, data=data)
        if parsed and isinstance(parsed, ParsedPythonFile):
            return self._get_completions(parsed, line, column)
        return []

    def get_parsed(
        self, path: Path, data: str | None = None
    ) -> ParsedFile | None:
        Parser: type[ParsedFile] | None = self._parser_from_path(path)
        if Parser is None:
            return None
        can_fallback = data is not None
        if not can_fallback:
            with open(path) as f:
                data = f.read()

        parsed: ParsedFile | None = None
        try:
            parsed = Parser(path, data=data)
        except ParsingError:
            if path in self._parsed:
                parsed = self._parsed[path]
            if parsed is None and can_fallback:
                try:
                    parsed = Parser(path)
                except ParsingError:
                    parsed = None
            else:
                parsed = None

        if parsed is not None and parsed.get_module_name():
            parsed.set_module(self._get_module(parsed.get_module_name()))
        self._parsed[path] = parsed
        return parsed

    def _parser_from_path(self, path: Path) -> type[ParsedFile] | None:
        if path.match("*.py"):
            return ParsedPythonFile
        elif path.match("view/*.xml"):
            return ParsedViewFile
        elif path.match("*.xml"):
            return ParsedXMLFile
        else:
            return None

    def get_pool(self, module_names: list[str]) -> Pool:
        key = tuple(sorted(module_names))
        if key in self._pools:
            return self._pools[key]

        try:
            pool = TrytonPool(module_list=key)
            pool.init()
        except Exception as e:
            TrytonPool._pool.pop(key, None)
            TrytonPool._started = False
            raise TrytonInitException(str(e))
        finally:
            TrytonPool._current = None
        self._pools[key] = Pool(pool)
        return self._pools[key]

    def _get_diagnostics(
        self, parsed: ParsedFile, ranges: list[CodeRange] | None = None
    ) -> list[Diagnostic]:
        return parsed.get_analyzer(self).analyze(ranges=ranges or [])

    def _get_completions(
        self, parsed: ParsedFile, line: int, column: int
    ) -> list[Diagnostic]:
        completioner = PythonCompletioner(parsed, self, line, column)
        try:
            completioner.analyze()
        except CompletionTargetFound:
            return generate_completions_from_model(completioner._target_model)
        else:
            return []

    def generate_module_diagnostics(
        self, module_name: str
    ) -> list[Diagnostic]:
        module = self._get_module(module_name)
        module_path = module.get_directory()
        diagnostics = []

        def to_analyze() -> Generator[Path, None, None]:
            for file_path in os.listdir(module_path):
                yield Path(file_path)
            if os.path.isdir(module_path / "tests"):
                for file_path in os.listdir(module_path / "tests"):
                    yield Path("tests") / file_path
            if os.path.isdir(module_path / "views"):
                for file_path in os.listdir(module_path / "views"):
                    if file_path.endswith(".xml"):
                        yield Path("views") / file_path

        for file_path in to_analyze():
            diagnostics += self.generate_diagnostics(module_path / file_path)

        return diagnostics


class Pool:
    def __init__(self, pool: TrytonPool) -> None:
        super().__init__()
        self._pool: TrytonPool = pool

    def get(self, name: str, kind: str) -> PoolBase:
        return self._pool.get(name, type=kind)
