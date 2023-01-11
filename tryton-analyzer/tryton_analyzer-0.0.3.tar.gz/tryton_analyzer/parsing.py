from __future__ import annotations

import ast
import importlib
from io import BytesIO
from pathlib import Path
from typing import TYPE_CHECKING, Any, TypeVar

import libcst as cst
from libcst import CSTNode, ParserSyntaxError
from lxml import etree
from trytond.modules import get_module_info

if TYPE_CHECKING:
    from .analyzer import Analyzer
    from .pool import PoolManager

T = TypeVar("T")


class ParsingError(Exception):
    def __init__(self, path: Path):
        super().__init__()
        self.path = path


class ParsingSyntaxError(ParsingError):
    def __repr__(self) -> str:
        return f"Syntax Error parsing contents of {self.path}"


class ModuleNotFound(ParsingError):
    def __repr__(self) -> str:
        return f"Could not identify module from path {self.path}"


class ParsedFile:
    def __init__(self, path: Path, data: str | None = None):
        super().__init__()
        self._path: Path = path

        self._module_path: Path | None = self._find_module_path()
        self._module_name: str = (
            self._module_path.stem if self._module_path else ""
        )
        self._module: Module | None = None
        if not data:
            with open(path) as f:
                data = f.read()
        self._raw_data: str = data
        self._raw_lines: list[str] = data.splitlines()
        self._parse(data)

    def _find_module_path(self) -> Path | None:
        names = [self._path.stem]
        for path in self._path.parents:
            names.append(path.stem)
            if (path / "tryton.cfg").is_file():
                return path
        return None

    def _parse(self, data: str) -> None:
        raise ParsingSyntaxError(self._path)

    def get_module_name(self) -> str:
        return self._module_name

    def get_module_path(self) -> Path:
        if self._module_path:
            return self._module_path
        raise ModuleNotFound(self._path)

    def get_filename(self) -> str:
        return self._path.stem

    def get_path(self) -> Path:
        return self._path

    def set_module(self, module: Module | None) -> None:
        self._module = module

    def get_module(self) -> Module | None:
        return self._module

    def get_analyzer(self, pool_manager: PoolManager) -> Analyzer:
        raise NotImplementedError

    def get_parsed(self) -> Any:
        raise NotImplementedError

    def get_raw_lines(self) -> list[str]:
        return self._raw_lines


class ParsedXMLFile(ParsedFile):
    _parsed: etree.iterparse

    def __init__(self, path: Path, data: str | None = None):
        super().__init__(path, data)

    def _parse(self, data: str) -> None:
        # We want a lazy iteration, so we rely on "get_parsed" to get an
        # iterator rather than parsing all at once
        pass

    def get_parsed(self) -> etree.iterparse:
        return etree.iterparse(
            BytesIO(self._raw_data.encode("UTF-8")),
            events=["start", "comment", "end"],
        )

    def get_analyzer(self, pool_manager: PoolManager) -> Analyzer:
        from .analyzer import XMLAnalyzer

        return XMLAnalyzer(self, pool_manager)


class ParsedViewFile(ParsedFile):
    _parsed: etree.iterparse

    def __init__(self, path: Path, data: str | None = None):
        super().__init__(path, data)

    def _parse(self, data: str) -> None:
        # We want a lazy iteration, so we rely on "get_parsed" to get an
        # iterator rather than parsing all at once
        pass

    def get_parsed(self) -> etree.iterparse:
        return etree.iterparse(
            BytesIO(self._raw_data.encode("UTF-8")),
            events=["start", "comment", "end"],
        )

    def get_analyzer(self, pool_manager: PoolManager) -> Analyzer:
        from .analyzer import ViewAnalyzer

        return ViewAnalyzer(self, pool_manager)


class ParsedPythonFile(ParsedFile):
    _parsed: CSTNode

    def __init__(self, path: Path, data: str | None = None):
        super().__init__(path, data)
        self._import_path: str | None = self._find_import_path()

    def _find_import_path(self) -> str | None:
        names = [self._path.stem]
        for path in self._path.parents:
            names.append(path.stem)
            if (path / "tryton.cfg").is_file():
                return "trytond.modules." + ".".join(reversed(names))
        return None

    def get_import_path(self) -> str:
        if self._import_path:
            return self._import_path
        raise ModuleNotFound(self._path)

    def _parse(self, data: str) -> None:
        try:
            self._parsed = cst.parse_module(data)
        except ParserSyntaxError:
            raise ParsingSyntaxError(self._path)

    def get_parsed(self) -> CSTNode:
        return self._parsed

    def get_analyzer(self, pool_manager: PoolManager) -> Analyzer:
        from .analyzer import PythonAnalyzer

        return PythonAnalyzer(self, pool_manager)


class Module:
    def __init__(self, module_name: str) -> None:
        super().__init__()
        self._name: str = module_name
        self._path: Path = self._get_path()
        # keys: filename / classname
        # values: type(model, wizard,...) / module_list
        self._modules_per_class: dict[
            tuple[str, str], tuple[str, tuple[str, ...]]
        ] = self._get_modules_per_class()
        self._module_info = get_module_info(module_name)
        self._model_data: dict[str, tuple[list[str], etree.Element]] = {}
        self._load_fs_ids()

    def _get_path(self) -> Path:
        try:
            if self._name in ('ir', 'res'):
                import_name = f"trytond.{self._name}"
            else:
                import_name = f"trytond.modules.{self._name}"
            imported = importlib.import_module(import_name)
            if imported.__file__ is None:
                raise ImportError(
                    f"Could not locate tryton module {self._name}"
                )
        except ImportError:
            raise ImportError(
                f"Module {self._name} not found as a tryton module"
            )
        return Path(imported.__file__).parent

    def get_directory(self) -> Path:
        return self._path

    def get_module_list_for_import(
        self, filename: str, classname: str
    ) -> tuple[str, tuple[str, ...]] | None:
        return self._modules_per_class.get((filename, classname))

    def get_name(self) -> str:
        return self._name

    def get_model_data(self, fs_id: str) -> Any:
        if self._model_data:
            return self._model_data.get(fs_id, None)
        return self._model_data.get(fs_id, None)

    def _load_fs_ids(self) -> None:
        for xml_file in self._module_info["xml"]:
            self._model_data.update(self._extract_fs_ids_infos(xml_file))

    def _extract_fs_ids_infos(
        self, filename: str
    ) -> dict[str, tuple[list[str], etree.Element]]:
        try:
            with open(self._path / filename) as f:
                parsed = etree.parse(BytesIO(f.read().encode("UTF-8")))
        except etree.XMLSyntaxError:
            return {}
        per_fs_ids = {}
        for data_node in parsed.xpath("/tryton/data"):
            modules = sorted(
                [self._name]
                + [
                    x.strip()
                    for x in data_node.attrib.get("depends", "").split(",")
                    if x.strip()
                ]
            )
            for record in data_node.xpath("record"):
                if "id" not in record.attrib:
                    continue
                per_fs_ids[record.attrib["id"]] = (list(modules), record)
        return per_fs_ids

    def get_view_info(
        self, filename: str
    ) -> tuple[list[str], str, str] | None:
        for module_list, record in self._model_data.values():
            if record.attrib.get("model", "") != "ir.ui.view":
                continue
            view_file_name = record.xpath("field[@name='name']")
            if not view_file_name:
                continue
            if view_file_name[0].text != filename:
                continue
            model_name = record.xpath("field[@name='model']")
            view_type = record.xpath("field[@name='type']")
            if not model_name or not view_type:
                return None
            return (module_list, view_type[0].text, model_name[0].text)
        return None

    def _get_modules_per_class(
        self,
    ) -> dict[tuple[str, str], tuple[str, tuple[str, ...]]]:
        result: dict[tuple[str, str], tuple[str, tuple[str, ...]]] = {}
        with open(self._path / "__init__.py") as f:
            parsed_init = ast.parse(f.read())

        for register_call in ast.walk(parsed_init):
            if (
                isinstance(register_call, ast.FunctionDef)
                and register_call.name == "register"
            ):
                type_ = ""
                for node in register_call.body:
                    if (
                        not isinstance(node, ast.Expr)
                        or not isinstance(node.value, ast.Call)
                        or not isinstance(node.value.func, ast.Attribute)
                        or node.value.func.attr != "register"
                        or not isinstance(node.value.func.value, ast.Name)
                        or node.value.func.value.id != "Pool"
                    ):
                        continue
                    modules = [self._name]
                    cur_imports: list[tuple[str, str]] = []
                    for arg in node.value.args:
                        if not isinstance(arg, ast.Attribute):
                            continue
                        if not isinstance(arg.value, ast.Name):
                            continue
                        cur_imports.append((arg.value.id, arg.attr))
                    for keyword in node.value.keywords:
                        if keyword.arg == "depends" and (
                            isinstance(keyword.value, ast.List)
                        ):
                            modules += [
                                x.value
                                for x in keyword.value.elts
                                if isinstance(x, ast.Constant)
                            ]
                        elif keyword.arg == "type_" and (
                            isinstance(keyword.value, ast.Constant)
                        ):
                            type_ = keyword.value.value
                    result.update(
                        {
                            (file_name, class_name): (
                                type_,
                                tuple(sorted(modules)),
                            )
                            for file_name, class_name in cur_imports
                        }
                    )
        return result
