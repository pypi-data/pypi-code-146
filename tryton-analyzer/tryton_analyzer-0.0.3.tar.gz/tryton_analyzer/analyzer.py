from pathlib import Path
from typing import TYPE_CHECKING, Any, Optional, Union

import libcst as cst
import libcst.matchers as m
from libcst.metadata import CodePosition, CodeRange, PositionProvider
from lxml import etree

from .parsing import (
    ParsedFile,
    ParsedPythonFile,
    ParsedViewFile,
    ParsedXMLFile,
)
from .tools import (
    ConflictingName,
    DebugDiagnostic,
    Diagnostic,
    DuplicateName,
    MissingRegisterInInit,
    MissingSuperCall,
    RecordDuplicateId,
    RecordMissingAttribute,
    RecordUnknownField,
    RecordUnknownModel,
    SuperInvocationMismatchedName,
    SuperInvocationWithParams,
    SuperWithoutParent,
    TrytonTagNotFound,
    TrytonXmlFileUnregistered,
    UnexpectedXMLTag,
    UnknownAttribute,
    UnknownModel,
    UnknownPoolKey,
    analyze_attr,
    ignore_error_code,
)

if TYPE_CHECKING:
    from .pool import Pool, PoolManager


class CompletionTargetFound(Exception):
    pass


class Analyzer:
    _parsed: Any

    def __init__(
        self, parsed: ParsedFile, pool_manager: "PoolManager"
    ) -> None:
        super().__init__()
        self._parsed = parsed.get_parsed()
        self._filename = parsed.get_filename()
        self._filepath = parsed.get_path()
        self._module = parsed.get_module()
        self._raw_lines = parsed.get_raw_lines()
        self._module_path = parsed.get_module_path()
        self._pool_manager = pool_manager
        self._diagnostics: list[Diagnostic] = []

    def add_diagnostic(self, diagnostic: Optional[Diagnostic]) -> None:
        if diagnostic and not self.ignored(
            diagnostic.err_code, diagnostic._position.start.line
        ):
            self._diagnostics.append(diagnostic)

    def get_filepath(self) -> Path:
        return self._filepath

    def get_module_name(self) -> str:
        if not self._module:
            return ""
        return self._module.get_name()

    def analyze(
        self, ranges: Optional[list[CodeRange]] = None
    ) -> list[Diagnostic]:
        raise NotImplementedError

    def ignored(self, err_code: str, line_number: int) -> bool:
        return (
            f"IGNORE-TRYTON-LS-{err_code}" in self._raw_lines[line_number - 1]
        )


class TrytonMetadata:
    def __init__(
        self,
        pool: "Pool",
        model: Any = None,
        model_name: str = "",
        kind: Optional[str] = None,
        class_name: str = "",
    ) -> None:
        super().__init__()
        self._model = model
        self._model_name = model_name
        self._kind = kind
        self._pool = pool
        self._class_name = class_name

    def __repr__(self) -> str:
        return (
            f"{self._model_name} ({self._kind}): {self._model} ({self._pool})"
        )


class PythonAnalyzer(Analyzer, cst.CSTVisitor):
    METADATA_DEPENDENCIES = (PositionProvider,)
    _parsed: cst.CSTNode

    def __init__(
        self, parsed: ParsedPythonFile, pool_manager: "PoolManager"
    ) -> None:
        super().__init__(parsed, pool_manager)
        self._import_path = parsed.get_import_path()
        self._metadata: dict[cst.ClassDef, Optional[TrytonMetadata]] = {}
        self._positions: dict[CodeRange, cst.CSTNode] = {}
        self._cur_class: Optional[cst.ClassDef] = None
        self._cur_function: Optional[cst.FunctionDef] = None
        self._class_for_function: dict[
            cst.FunctionDef, Optional[cst.ClassDef]
        ] = {}
        self._class_metadata: Optional[TrytonMetadata] = None

        self._function_pool_vars: set[str] = set()
        self._node_mappings: dict[Union[cst.CSTNode, str], Any] = {}
        self._node_list_mappings: dict[Union[cst.CSTNode, str], list[Any]] = {}
        self._pool_mappings: set[cst.CSTNode] = set()

        self._ranges: list[CodeRange] = []

    def _track_position(self, node: cst.CSTNode) -> None:
        self._positions[self.get_metadata(PositionProvider, node)] = node

    def _must_analyze(self, node: cst.CSTNode) -> bool:
        if not self._ranges:
            return True
        metadata = self.get_metadata(PositionProvider, node)

        def check_range(range: CodeRange) -> bool:
            if range.end.line < metadata.start.line:
                return False
            if (
                range.end.line == metadata.start.line
                and range.end.column < metadata.start.column
            ):
                return False
            if range.start.line > metadata.end.line:
                return False
            if (
                range.start.line == metadata.end.line
                and range.start.column > metadata.end.column
            ):
                return False
            return True

        return any(check_range(x) for x in self._ranges)

    def visit_ClassDef(self, node: cst.ClassDef) -> bool:
        if not self._must_analyze(node):
            return False
        self._track_position(node)
        self._cur_class = node
        model_node = self._model_name(node)
        if model_node and self._module:
            model_name = model_node.value[1:-1]
            class_name = node.name.value
            import_info = self._module.get_module_list_for_import(
                self._filename, class_name
            )
            if not import_info:
                self._class_metadata = TrytonMetadata(
                    self._pool_manager.get_pool([self._module.get_name()]),
                    model=None,
                    model_name=model_name,
                    class_name=class_name,
                )
                self.add_diagnostic(
                    MissingRegisterInInit.init_from_analyzer(self, model_node)
                )
            else:
                kind, module_list = import_info
                pool = self._pool_manager.get_pool(list(module_list))
                try:
                    model = pool.get(model_name, kind)
                except KeyError:
                    model = None
                self._class_metadata = TrytonMetadata(
                    pool,
                    model=model,
                    model_name=model_name,
                    class_name=class_name,
                    kind=kind,
                )
                if model is None:
                    self.add_diagnostic(
                        UnknownModel.init_from_analyzer(
                            self, model_node, unknown_name=model_name
                        )
                    )
        elif self._module:
            self._class_metadata = TrytonMetadata(
                self._pool_manager.get_pool([self._module.get_name()])
            )
        else:
            self._class_metadata = None
        self._metadata[node] = self._class_metadata
        return True

    def leave_ClassDef(self, node: cst.ClassDef) -> bool:
        self._cur_class = None
        self._class_metadata = None
        return True

    def visit_FunctionDef(self, node: cst.FunctionDef) -> bool:
        if not self._must_analyze(node):
            return False
        self._track_position(node)
        self._cur_function = node
        self._class_for_function[node] = self._cur_class
        self._node_list_mappings = {}
        self._node_mappings = (
            {
                "self": self._class_metadata._model,
                "cls": self._class_metadata._model,
            }
            if self._class_metadata
            else {}
        )
        self._function_pool_vars.clear()
        self.analyze_function(node)
        return True

    def get_import_path(self) -> str:
        if not self._class_metadata:
            return self._import_path
        return f"'{self._import_path}.{self.get_current_class_name()}'"

    def get_function_name(self) -> str:
        if not self._cur_function:
            return ""
        return self._cur_function.name.value

    def get_current_metadata(self) -> Optional[TrytonMetadata]:
        return self._class_metadata

    def get_current_class_node(self) -> Optional[cst.ClassDef]:
        return self._cur_class

    def get_current_function_node(self) -> Optional[cst.FunctionDef]:
        return self._cur_function

    def get_pool(self) -> Optional["Pool"]:
        if not self._class_metadata:
            if self._module:
                return self._pool_manager.get_pool([self._module.get_name()])
            return None
        return self._class_metadata._pool

    def analyze_function(self, node: cst.FunctionDef) -> None:
        self._check_super_call(node)
        self._check_depends(node)

    def _check_depends(self, node: cst.FunctionDef) -> None:
        if not self._class_metadata:
            return
        Model = self._class_metadata._model
        if not Model:
            return
        pool = self._class_metadata._pool
        from trytond.model.fields import Many2One

        for decorator in node.decorators:
            if not m.matches(decorator, m.Decorator(
                        decorator=m.Call(func=m.Attribute(value=m.Name(value='fields'),
                                attr=m.Name(value='depends'))))):
                continue
            for arg in decorator.decorator.args:
                if m.matches(arg, m.Arg(value=m.SimpleString(), keyword=None)):
                    cur_model = Model
                    field_names = arg.value.value[1:-1].split('.')
                    for field_name in field_names[:-1]:
                        if not field_name.startswith('_parent_'):
                            # TODO: dedicated diagnostic
                            self.add_diagnostic(
                                UnknownAttribute.init_from_analyzer(
                                    self,
                                    arg.value,
                                    model_name=cur_model.__name__,
                                    attr_name=field_name,
                                    )
                                )
                            break
                        field_name = field_name[8:]
                        if field_name not in cur_model._fields:
                            # TODO: dedicated diagnostic
                            self.add_diagnostic(
                                UnknownAttribute.init_from_analyzer(
                                    self,
                                    arg.value,
                                    model_name=cur_model.__name__,
                                    attr_name=field_name,
                                    )
                                )
                            break
                        field = cur_model._fields[field_name]
                        if not isinstance(field, Many2One):
                            # TODO: dedicated diagnostic
                            self.add_diagnostic(
                                UnknownAttribute.init_from_analyzer(
                                    self,
                                    arg.value,
                                    model_name=cur_model.__name__,
                                    attr_name=field_name,
                                    )
                                )
                            break
                        try:
                            cur_model = pool.get(field.model_name, 'model')
                        except KeyError:
                            self.add_diagnostic(
                                UnknownModel.init_from_analyzer(
                                    self,
                                    arg.value,
                                    unknown_name=field.model_name,
                                )
                            )
                            break
                    else:
                        field_name = field_names[-1]
                        if field_name not in cur_model._fields:
                            self.add_diagnostic(
                                UnknownAttribute.init_from_analyzer(
                                    self,
                                    arg.value,
                                    model_name=cur_model.__name__,
                                    attr_name=field_name,
                                    )
                                )
                elif m.matches(arg, m.Arg(value=m.List(),
                            keyword=m.Name())):
                    if arg.keyword.value != 'methods':
                        # TODO: dedicated diagnostic
                        self.add_diagnostic(
                            UnknownAttribute.init_from_analyzer(
                                self,
                                arg.value,
                                model_name=cur_model.__name__,
                                attr_name=field_name,
                                )
                            )
                        continue
                    for method in arg.value.elements:
                        if not m.matches(method,
                                m.Element(value=m.SimpleString())):
                            continue
                        method_name = method.value.value[1:-1]
                        if method_name not in dir(Model):
                            self.add_diagnostic(
                                UnknownAttribute.init_from_analyzer(
                                    self,
                                    arg.value,
                                    model_name=Model.__name__,
                                    attr_name=method_name,
                                    )
                                )

    def _check_super_call(self, node: cst.FunctionDef) -> None:
        super_call = m.extractall(
            node,
            m.Call(
                func=m.Attribute(
                    value=m.SaveMatchedNode(
                        m.Call(func=m.Name(value="super")), "super_invocation"
                    ),
                    attr=m.SaveMatchedNode(m.Name(), "super_name"),
                )
            ),
        )
        for cur_call in super_call:
            if cur_call["super_invocation"].args:
                self.add_diagnostic(
                    SuperInvocationWithParams.init_from_analyzer(
                        self, cur_call["super_invocation"]
                    )
                )
            if cur_call["super_name"].value != node.name.value:
                self.add_diagnostic(
                    SuperInvocationMismatchedName.init_from_analyzer(
                        self,
                        cur_call["super_name"],
                        expected_name=node.name.value,
                    )
                )

        if not self._class_metadata:
            return
        Model = self._class_metadata._model
        if not Model:
            return

        has_super = bool(super_call)
        found_base, found_super = False, False
        function_name = self.get_current_function_name()
        for model in Model.mro():
            if self.get_import_path() in str(model):
                found_base = True
            elif found_base and not has_super and function_name in dir(model):
                # model.<name>.__code__ co_filename / co_firstlineno
                parent_func = getattr(model, function_name)
                if not hasattr(parent_func, "__code__"):
                    # TODO: properties do not have code ?
                    break
                parent_file_name = parent_func.__code__.co_filename
                parent_parsed = self._pool_manager.get_parsed(
                    Path(parent_file_name)
                )
                if parent_parsed is None:
                    # TODO: Error
                    break
                wrapper = cst.MetadataWrapper(parent_parsed.get_parsed())
                finder = FunctionFinder(
                    lineno=parent_func.__code__.co_firstlineno
                )
                wrapper.visit(finder)
                if finder._match and not ignore_error_code(
                    finder._match, MissingSuperCall.err_code
                ):
                    self.add_diagnostic(
                        MissingSuperCall.init_from_analyzer(self, node.name)
                    )
                break
            elif (
                found_base
                and has_super
                and not found_super
                and function_name in dir(model)
            ):
                found_super = True
        if has_super and not found_super:
            self.add_diagnostic(
                SuperWithoutParent.init_from_analyzer(self, node.name)
            )

    def leave_FunctionDef(self, node: cst.FunctionDef) -> bool:
        self._cur_function = None
        self._last_class = node
        self._node_mappings = {}
        self._node_list_mappings = {}
        self._function_pool_vars.clear()
        return True

    def _model_name(self, node: cst.ClassDef) -> Optional[cst.SimpleString]:
        extract_data = m.extractall(
            node,
            m.Assign(
                targets=[m.AssignTarget(target=m.Name(value="__name__"))],
                value=m.SaveMatchedNode(m.SimpleString(), "__name__"),
            ),
        )
        if not extract_data:
            return None
        match, *extra_matches = extract_data
        if "__name__" in match:
            name_definition = match["__name__"]
            for extra_match in extra_matches:
                if "__name__" in extra_match:
                    if name_definition.value == extra_match["__name__"].value:
                        self.add_diagnostic(
                            DuplicateName(
                                self.get_node_position(
                                    extra_match["__name__"]
                                ),
                                self._filepath,
                                self.get_module_name(),
                                name_definition.value[1:-1],
                                node.name.value,
                            )
                        )
                    else:
                        self.add_diagnostic(
                            ConflictingName(
                                self.get_node_position(
                                    extra_match["__name__"]
                                ),
                                self._filepath,
                                self.get_module_name(),
                                name_definition.value[1:-1],
                                node.name.value,
                            )
                        )

            return name_definition
        return None

    def leave_Attribute(self, node: cst.Attribute) -> None:
        value_type = self._get_type(node.value)
        if value_type is None:
            return
        attr = node.attr.value
        if attr not in dir(value_type):
            self.add_diagnostic(
                UnknownAttribute.init_from_analyzer(
                    self,
                    node.attr,
                    model_name=value_type.__name__,
                    attr_name=attr,
                )
            )
        analyze_attr(self, node, value_type, attr)

    def visit_Call(self, node: cst.Call) -> None:
        value_type = self._get_type(node.func)
        if value_type is not None:
            # instantiation
            self._node_mappings[node] = value_type
            return
        extracted = m.extract(
            node,
            m.Call(
                func=m.Attribute(
                    value=m.SaveMatchedNode(
                        m.MatchIfTrue(lambda x: x in self._node_mappings),
                        "match",
                    )
                    | m.Name(
                        value=m.SaveMatchedNode(
                            m.MatchIfTrue(lambda x: x in self._node_mappings),
                            "match",
                        )
                    ),
                    attr=m.Name(),
                )
            ),
        )
        if extracted:
            value_type = extracted["match"]
            func_name = node.func.attr.value
            if func_name in ("search", "browse"):
                self._node_list_mappings[node] = self._node_mappings[
                    value_type
                ]

    def visit_For(self, node: cst.For) -> None:
        node.iter.visit(self)
        base_type = self._get_list_type(node.iter)
        if base_type is None:
            return
        self._node_mappings[node.target.value] = base_type

    def visit_ListComp(self, node: cst.ListComp) -> None:
        node.for_in.visit(self)

    def leave_ListComp(self, node: cst.ListComp) -> None:
        self._analyze_comp(node)

    def visit_SetComp(self, node: cst.SetComp) -> None:
        self._analyze_comp(node)

    def leave_CompFor(self, node: cst.CompFor) -> None:
        if not m.matches(node.target, m.Name()):
            return
        base_type = self._get_list_type(node.iter)
        if base_type is None:
            return
        self._node_mappings[node.target.value] = base_type

    def _analyze_comp(self, node: cst.CSTNode) -> None:
        base_type = self._get_type(node.elt)
        if base_type is None:
            return
        self._node_list_mappings[node] = base_type

    def leave_Assign(self, node: cst.Assign) -> None:
        if self._check_is_pool(node):
            return

        mono, multi = None, []
        if m.matches(
            node.targets[0],
            m.AssignTarget(
                target=m.Tuple(
                    elements=[
                        m.AtLeastN(n=1, matcher=m.Element(value=m.Name()))
                    ]
                )
            ),
        ):
            multi = [
                name.value.value
                for name in node.targets[0].target.elements
                if m.matches(name, m.Element(value=m.Name()))
            ]
        elif m.matches(node.targets[0].target, m.Name()):
            mono = node.targets[0].target.value
        else:
            return

        value_type = self._get_type(node.value)
        if value_type is not None:
            if mono:
                self._node_mappings[mono] = value_type
            for name in multi:
                self._node_mappings.pop(name, None)
                self._node_list_mappings.pop(name, None)
            return
        value_type = self._get_list_type(node.value)
        if value_type is not None:
            if mono:
                self._node_list_mappings[mono] = value_type
            elif multi:
                for name in multi:
                    self._node_mappings[name] = value_type
            else:
                for name in multi + ([mono] if mono else []):
                    self._node_mappings.pop(name, None)
                    self._node_list_mappings.pop(name, None)
            return
        for name in multi + ([mono] if mono else []):
            self._node_mappings.pop(name, None)
            self._node_list_mappings.pop(name, None)

    def leave_Subscript(self, node: cst.Subscript) -> None:
        if m.matches(
            node, m.Subscript(slice=[m.SubscriptElement(slice=m.Index())])
        ):
            value_type = self._get_list_type(node.value)
            if value_type is not None:
                self._node_mappings[node] = value_type
                return
        elif m.matches(
            node, m.Subscript(slice=[m.SubscriptElement(slice=m.Slice())])
        ):
            value_type = self._get_list_type(node.value)
            if value_type is not None:
                self._node_list_mappings[node] = value_type
                return

    def visit_Lambda(self, node: cst.Lambda) -> bool:
        # Avoid errors inside lambda calls where the parameters shadow another
        # variable
        return False

    def _get_type(self, node: cst.CSTNode) -> Any:
        if isinstance(node, cst.Name) and node.value in self._node_mappings:
            return self._node_mappings[node.value]
        if node in self._node_mappings:
            return self._node_mappings[node]
        model = self._handle_pool_get(node)
        if model is not None:
            return model

    def _get_list_type(self, node: cst.CSTNode) -> Any:
        if (
            isinstance(node, cst.Name)
            and node.value in self._node_list_mappings
        ):
            return self._node_list_mappings[node.value]
        if node in self._node_list_mappings:
            return self._node_list_mappings[node]

    def _handle_pool_get(self, node: cst.CSTNode) -> Any:
        extracted = m.extract(
            node,
            m.Call(
                func=m.Attribute(
                    value=m.OneOf(
                        m.Call(func=m.Name(value="Pool")),
                        m.Name(
                            value=m.MatchIfTrue(
                                lambda value: value in self._function_pool_vars
                            )
                        ),
                    ),
                    attr=m.Name(value="get"),
                ),
                args=[
                    m.Arg(
                        value=m.SaveMatchedNode(m.SimpleString(), "model_name")
                    ),
                    m.AtMostN(
                        n=1,
                        matcher=m.Arg(
                            value=m.SaveMatchedNode(m.SimpleString(), "kind")
                        ),
                    ),
                ],
            ),
        )
        if extracted is not None and "model_name" in extracted:
            kind = (
                extracted["kind"].value[1:-1]
                if "kind" in extracted
                else "model"
            )
            pool = self.get_pool()
            if not pool:
                return None
            if kind not in pool._pool.classes:
                self.add_diagnostic(
                    UnknownPoolKey.init_from_analyzer(
                        self,
                        extracted["kind"],
                        possible_values=", ".join(pool._pool.classes.keys()),
                    )
                )
            try:
                self._node_mappings[node] = pool.get(
                    extracted["model_name"].value[1:-1], kind
                )
                return self._node_mappings[node]
            except KeyError:
                self.add_diagnostic(
                    UnknownModel.init_from_analyzer(
                        self,
                        extracted["model_name"],
                        unknown_name=extracted["model_name"].value[1:-1],
                    )
                )

    def _check_is_pool(self, node: cst.Assign) -> bool:
        is_pool = m.extract(
            node,
            m.Assign(
                targets=[
                    m.AssignTarget(
                        target=m.SaveMatchedNode(m.Name(), "var_name")
                    )
                ],
                value=m.Call(func=m.Name(value="Pool")),
            ),
        )
        if is_pool is not None and "var_name" in is_pool:
            self._function_pool_vars.add(is_pool["var_name"].value)
            return True
        return False

    def add_debug_diagnostic(self, node: cst.CSTNode, message: str) -> None:
        self._diagnostics.append(
            DebugDiagnostic.init_from_analyzer(self, node, message)
        )

    def get_current_model_name(self) -> str:
        return self._class_metadata._model_name if self._class_metadata else ""

    def get_current_class_name(self) -> str:
        return self._class_metadata._class_name if self._class_metadata else ""

    def get_node_position(self, node: cst.CSTNode) -> CodeRange:
        return self.get_metadata(PositionProvider, node)

    def get_current_function_name(self) -> str:
        return self._cur_function.name.value if self._cur_function else ""

    def analyze(
        self, ranges: Optional[list[CodeRange]] = None
    ) -> list[Diagnostic]:
        self._diagnostics = []
        self._ranges = ranges or []
        wrapper = cst.MetadataWrapper(self._parsed)
        wrapper.visit(self)
        return self._diagnostics

    def ignored(self, err_code: str, line_number: int) -> bool:
        return super().ignored(err_code, line_number) or (
            line_number > 1
            and self._raw_lines[line_number - 2].lstrip().startswith("#")
            and f"IGNORE-TRYTON-LS-{err_code}"
            in self._raw_lines[line_number - 2]
        )


class PythonCompletioner(PythonAnalyzer):
    def __init__(
        self,
        parsed: ParsedPythonFile,
        pool_manager: "PoolManager",
        line: int,
        column: int,
    ) -> None:
        super().__init__(parsed, pool_manager)
        self._line = line
        self._column = column
        self._target_model = None
        self._target_node = None

    def _must_analyze(self, node: cst.CSTNode) -> bool:
        metadata = self.get_metadata(PositionProvider, node)
        result = metadata.start.line <= self._line <= metadata.end.line
        return result

    def visit_Attribute(self, node: cst.Attribute) -> None:
        metadata = self.get_metadata(PositionProvider, node)
        if metadata.start.line == self._line == metadata.end.line and (
            metadata.start.column <= self._column <= metadata.end.column
        ):
            self._target_node = node
        return super().visit_Attribute(node)

    def leave_Attribute(self, node: cst.Attribute) -> None:
        super().leave_Attribute(node)
        if self._target_node != node:
            return
        self._target_model = self._get_type(node.value)
        raise CompletionTargetFound


class FunctionFinder(cst.CSTVisitor):
    METADATA_DEPENDENCIES = (PositionProvider,)

    def __init__(self, lineno: int) -> None:
        super().__init__()
        self._lineno = lineno
        self._match: Optional[cst.FunctionDef] = None

    def visit_ClassDef(self, node: cst.ClassDef) -> bool:
        position = self.get_metadata(PositionProvider, node)
        return position.start.line <= self._lineno <= position.end.line

    def visit_FunctionDef(self, node: cst.FunctionDef) -> bool:
        position = self.get_metadata(PositionProvider, node)
        if position.start.line <= self._lineno <= position.end.line:
            self._match = node
        return False


class XMLAnalyzer(Analyzer):
    def __init__(
        self, parsed: ParsedXMLFile, pool_manager: "PoolManager"
    ) -> None:
        super().__init__(parsed, pool_manager)
        self._ranges: list[CodeRange] = []
        self._fs_ids: dict[str, int] = {}
        self._found_tryton_tag = False
        self._tag_stack: list[etree.Element] = []
        self._current_pool: Optional["Pool"] = None
        self._current_model: Any = None
        self._cur_prefix: int = 0

    def analyze(
        self, ranges: Optional[list[CodeRange]] = None
    ) -> list[Diagnostic]:
        self._diagnostics = []
        self._ranges = ranges or []

        is_tryton_xml = self.check_is_tryton_xml_file()

        try:
            for action, element in self._parsed:
                if action == "start":
                    self.analyze_node_start(element)
                elif action == "end":
                    self.analyze_node_end(element)
        except etree.XMLSyntaxError:
            pass

        if is_tryton_xml and not self._found_tryton_tag:
            self._diagnostics.append(TrytonTagNotFound(self._filepath))
        if not is_tryton_xml and self._found_tryton_tag:
            self._diagnostics.append(TrytonXmlFileUnregistered(self._filepath))
        return self._diagnostics

    def analyze_node_start(self, element: etree.Element) -> None:
        self._tag_stack.append(element)
        if element.text and element.text.startswith("\n"):
            self._cur_prefix = len(element.text) - 1
        analyze_func = getattr(self, f"_analyze_{element.tag}_start", None)
        if analyze_func is None:
            return
        analyze_func(element)

    def analyze_node_end(self, element: etree.Element) -> None:
        analyze_func = getattr(self, f"_analyze_{element.tag}_end", None)
        if analyze_func:
            analyze_func(element)
        self._tag_stack.pop(-1)

    def _analyze_tryton_start(self, node: etree.Element) -> None:
        self._found_tryton_tag = True

    def _analyze_data_start(self, node: etree.Element) -> None:
        if len(self._tag_stack) != 2:
            self.add_diagnostic(
                UnexpectedXMLTag.init_from_analyzer(
                    self, node, tag_name=node.tag
                )
            )
        if not self._module:
            return
        modules = [self._module.get_name()]
        if "depends" in node.attrib:
            modules += [x.strip() for x in node.attrib["depends"].split(",")]
        self._current_pool = self._pool_manager.get_pool(modules)

    def _analyze_record_start(self, node: etree.Element) -> None:
        if len(self._tag_stack) != 3:
            self.add_diagnostic(
                UnexpectedXMLTag.init_from_analyzer(
                    self, node, tag_name=node.tag
                )
            )
        if "model" not in node.attrib:
            self.add_diagnostic(
                RecordMissingAttribute.init_from_analyzer(
                    self, node, attr_name="model"
                )
            )
        if "id" not in node.attrib:
            self.add_diagnostic(
                RecordMissingAttribute.init_from_analyzer(
                    self, node, attr_name="id"
                )
            )
        else:
            if node.attrib["id"] in self._fs_ids:
                self.add_diagnostic(
                    RecordDuplicateId.init_from_analyzer(
                        self,
                        node,
                        fs_id=node.attrib["id"],
                        other_line=str(self._fs_ids[node.attrib["id"]]),
                    )
                )
            else:
                self._fs_ids[node.attrib["id"]] = node.sourceline
        if not self._current_pool or not node.attrib.get("model", None):
            return
        try:
            self._current_model = self._current_pool.get(
                node.attrib["model"], "model"
            )
        except KeyError:
            self.add_diagnostic(
                RecordUnknownModel.init_from_analyzer(
                    self, node, model_name=node.attrib["model"]
                )
            )

    def _analyze_field_start(self, node: etree.Element) -> None:
        if len(self._tag_stack) != 4:
            self.add_diagnostic(
                UnexpectedXMLTag.init_from_analyzer(
                    self, node, tag_name=node.tag
                )
            )
        if "name" not in node.attrib:
            self.add_diagnostic(
                RecordMissingAttribute.init_from_analyzer(
                    self, node, attr_name="name"
                )
            )
        if not self._current_model or "name" not in node.attrib:
            return
        if node.attrib["name"] not in self._current_model._fields:
            self.add_diagnostic(
                RecordUnknownField.init_from_analyzer(
                    self,
                    node,
                    model_name=self._current_model.__name__,
                    field_name=node.attrib["name"],
                )
            )
            return
        if not self._current_pool:
            return
        field = self._current_model._fields[node.attrib["name"]]
        if (
            self._current_model.__name__ == "ir.ui.view"
            and node.attrib["name"] == "model"
        ):
            # Special case because it is a usual case
            try:
                self._current_pool.get(node.text, "model")
            except KeyError:
                self.add_diagnostic(
                    RecordUnknownModel.init_from_analyzer(
                        self, node, model_name=node.text
                    )
                )

    def _analyze_record_end(self, node: etree.Element) -> None:
        self._current_model = None

    def _analyze_data_end(self, node: etree.Element) -> None:
        self._current_pool = None

    def check_is_tryton_xml_file(self) -> bool:
        with open(self._module_path / "tryton.cfg") as f:
            for line in f.readlines():
                if f"{self._filename}.xml" == line.strip():
                    return True
        return False

    def get_node_position(self, node: etree.Element) -> CodeRange:
        return CodeRange(
            start=CodePosition(line=node.sourceline, column=self._cur_prefix),
            end=CodePosition(line=node.sourceline, column=99),
        )

    def ignored(self, err_code: str, line_number: int) -> bool:
        return super().ignored(err_code, line_number) or (
            line_number > 1
            and self._raw_lines[line_number - 2].lstrip().startswith("<!--")
            and f"IGNORE-TRYTON-LS-{err_code}"
            in self._raw_lines[line_number - 2]
        )


class ViewAnalyzer(Analyzer):
    def __init__(
        self, parsed: ParsedViewFile, pool_manager: "PoolManager"
    ) -> None:
        super().__init__(parsed, pool_manager)
        self._ranges: list[CodeRange] = []
        self._module = parsed.get_module()
        assert self._module
        view_info = self._module.get_view_info(parsed.get_filename())
        assert view_info
        modules, view_type, view_model = view_info
        self._current_model = pool_manager.get_pool(modules).get(
            view_model, "model"
        )
        self._view_type = view_type

    def analyze(
        self, ranges: Optional[list[CodeRange]] = None
    ) -> list[Diagnostic]:
        self._diagnostics = []
        self._ranges = ranges or []
        try:
            for action, element in self._parsed:
                if action == "start":
                    self.analyze_node_start(element)
                elif action == "end":
                    self.analyze_node_end(element)
        except etree.XMLSyntaxError:
            pass
        return self._diagnostics

    def analyze_node_start(self, element: etree.Element) -> None:
        if element.text and element.text.startswith("\n"):
            self._cur_prefix = len(element.text) - 1
        analyze_func = getattr(self, f"_analyze_{element.tag}_start", None)
        if analyze_func is None:
            return
        analyze_func(element)

    def analyze_node_end(self, element: etree.Element) -> None:
        analyze_func = getattr(self, f"_analyze_{element.tag}_end", None)
        if analyze_func:
            analyze_func(element)

    def _analyze_form_start(self, node: etree.Element) -> None:
        if self._view_type not in ("list-form", "form"):
            self.add_diagnostic(
                UnexpectedXMLTag.init_from_analyzer(
                    self, node, tag_name=node.tag
                )
            )

    def _analyze_tree_start(self, node: etree.Element) -> None:
        if self._view_type != "tree":
            self.add_diagnostic(
                UnexpectedXMLTag.init_from_analyzer(
                    self, node, tag_name=node.tag
                )
            )

    def _analyze_data_start(self, node: etree.Element) -> None:
        if self._view_type != "inherit":
            self.add_diagnostic(
                UnexpectedXMLTag.init_from_analyzer(
                    self, node, tag_name=node.tag
                )
            )

    def _analyze_label_start(self, node: etree.Element) -> None:
        self._check_name(node)

    def _analyze_field_start(self, node: etree.Element) -> None:
        self._check_name(node, required=True)

    def _analyze_separator_start(self, node: etree.Element) -> None:
        self._check_name(node)

    def _analyze_group_start(self, node: etree.Element) -> None:
        self._check_name(node)

    def _check_name(self, node: etree.Element, required: bool = False) -> None:
        if "name" not in node.attrib:
            if required:
                self.add_diagnostic(
                    RecordMissingAttribute.init_from_analyzer(
                        self, node, attr_name="name"
                    )
                )
            return
        if not self._current_model:
            return
        if node.attrib["name"] not in self._current_model._fields:
            self.add_diagnostic(
                RecordUnknownField.init_from_analyzer(
                    self,
                    node,
                    model_name=self._current_model.__name__,
                    field_name=node.attrib["name"],
                )
            )

    def get_node_position(self, node: etree.Element) -> CodeRange:
        return CodeRange(
            start=CodePosition(line=node.sourceline, column=self._cur_prefix),
            end=CodePosition(line=node.sourceline, column=99),
        )
