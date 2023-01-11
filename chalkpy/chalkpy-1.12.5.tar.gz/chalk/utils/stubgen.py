import argparse
import os
import pathlib
import typing
import warnings
from typing import Dict, List, NamedTuple, Optional, Tuple, Type, Union

from typing_extensions import Annotated, get_args, get_origin

from chalk.features import Feature, Features, FeatureSetBase
from chalk.importer import get_directory_root, import_all_python_files_from_dir
from chalk.streams import Windowed
from chalk.utils.collection_type import GenericAlias

try:
    from types import UnionType
except ImportError:
    UnionType = None


class ParsedAnnotation(NamedTuple):
    annotation: str
    include_in_protocol_cls: bool


class ParsedFeaturesClass(NamedTuple):
    module: str
    annotations: Dict[str, ParsedAnnotation]


class StubGenerator:
    def __init__(self) -> None:
        self._parsed_feature_classes: Dict[str, ParsedFeaturesClass] = {}
        self._module_to_stubs: List[Type[Features]] = []
        self._imports: Dict[Tuple[str, ...], str] = {}  # Mapping of full module name to the name it is imported as

    def _add_import(
        self, item: Union[str, type, typing._SpecialForm, Windowed], import_as: Optional[str] = None
    ) -> str:
        """Add an import for item.

        If ``item`` is already imported, then it will not be imported again.
        Its existing import name will be returned

        Args:
            item: The thing to import. Should be the full path to the item (e.g. ``typing.Optional``)

        Returns:
            str: The name that ``item`` will be imported as.
        """
        if isinstance(item, typing._SpecialForm):
            item = str(item)
        if isinstance(item, Windowed):
            item = type(item)
        if isinstance(item, type):
            item = f"{item.__module__}.{item.__name__}"
        if not isinstance(item, str):
            raise TypeError(f"Invalid type for {item}: {type(item)}")
        item_split = tuple(item.split("."))
        if item_split[0] == "builtins":
            assert len(item_split) == 2
            return item_split[1]
        if item_split in self._imports:
            imported_name = self._imports[item_split]
            if import_as is not None and import_as != imported_name:
                raise ValueError(
                    f"Item {'.'.join(item_split)} already imported as {imported_name}; cannot be imported again as {import_as}"
                )
            return imported_name
        if import_as is None:
            import_as = self._get_import_name(item_split)
        self._imports[item_split] = import_as
        return self._imports[item_split]

    def _get_import_name(self, item_split: Tuple[str, ...]):
        if item_split[0] in ("typing", "typing_extensions"):
            assert len(item_split) == 2
            return item_split[1]
        item_split = tuple(x.replace("_", "__") for x in item_split)
        item = f"__stubgen_{'_'.join(item_split)}"
        return item

    def _register_imports_for_annotation(self, annotation: Union[type, Windowed, GenericAlias]) -> str:

        if annotation == type(None):
            return "None"
        origin, args = get_origin(annotation), get_args(annotation)
        if origin is None:
            assert args == ()
            # Likely a "simple" annotation, like an enum class
            if isinstance(annotation, Windowed):
                origin_name = self._add_import(annotation, import_as="Windowed")
                arg_name = self._register_imports_for_annotation(annotation._kind)
                return f"{origin_name}[{arg_name}]"
            elif annotation.__module__ == "builtins":
                assert isinstance(annotation, type)
                return annotation.__name__
            else:
                return self._add_import(annotation)
        # Some sort of generic class, like a collection, or optional
        if origin == UnionType:
            # Convert new-style type unions to old-style typing.Unions
            origin = typing.Union
        if origin == Annotated:
            # If annotated, only pay attention to the first arg -- the actual type
            return self._register_imports_for_annotation(args[0])
        origin_name = self._add_import(origin)
        arg_names = [self._register_imports_for_annotation(arg) for arg in args]
        return f"{origin_name}[" + ", ".join(arg_names) + "]"

    def register_features_class(self, features_cls: Type[Features]):
        annotations: Dict[str, ParsedAnnotation] = {}
        for f in features_cls.features:
            assert isinstance(f, Feature)
            assert f.typ is not None
            if f.typ.is_dataframe:
                self._add_import("chalk.features.DataFrame", "DataFrame")
                annotations[f.attribute_name] = ParsedAnnotation(
                    "DataFrame",
                    include_in_protocol_cls=True,
                )
            else:
                # Make a best-effort to figure out imports.
                annotations[f.attribute_name] = ParsedAnnotation(
                    self._register_imports_for_annotation(f.typ.parsed_annotation),
                    include_in_protocol_cls=not f.is_windowed_pseudofeature and not f.is_autogenerated,
                )
        if features_cls.__name__ in self._parsed_feature_classes:
            raise ValueError(
                f"Unable to generate stubs due to multiple features sets called {features_cls.__name__}. Feature set names must be unique. Please rename one of these feature sets."
            )
        self._parsed_feature_classes[features_cls.__name__] = ParsedFeaturesClass(
            module=features_cls.__module__,
            annotations=annotations,
        )

    def generate_features_decorator_stub_file(self):
        self._add_import("typing.Optional", "Optional")
        self._add_import("typing.Protocol", "Protocol")
        self._add_import("typing.Type", "Type")
        self._add_import("typing.overload", "overload")
        self._add_import("chalk.features.feature_set.FeaturesMeta", "FeaturesMeta")
        self._add_import("chalk.features.Features", "Features")
        self._add_import("chalk.utils.duration.Duration", "Duration")
        self._add_import("chalk.features.Tags", "Tags")
        lines = [
            "# AUTO-GENERATED FILE. Do not edit. Run chalkpy stubgen to generate.",
            "# fmt: off",
            "# isort: skip_file",
            "from __future__ import annotations",
            "",
        ]
        # sort the imports for consistency
        imports = sorted(self._imports.items())
        for imp, import_as in imports:
            module = imp[:-1]
            name = imp[-1]
            lines.append(f"from {'.'.join(module)} import {name} as {import_as}")
        lines.append("")

        # The overall strategy is to create 3 stub classes for each features class.
        #
        # In no particular order:
        #
        # Class 1: The metaclasss. The metaclass includes @property descriptors for each class variable.
        # These descriptors are used to annotation class attributes as Type[feature]
        # Pyright requires that all annotations are types, not instances.
        #
        # Class 2: The class. The class includes an __init__ signature that includes all features, with the
        # correct type annotation. All features have a default value of `...`, since Chalk does not require feature
        # sets to be complete. Inside the __init__ body, all instance attributes are annotated. Placing the annotation
        # here, as opposed to the class body, does not conflict with the metaclass annotations
        #
        # Class 3: The protocol class. Since the @features decorator is passed the end user's class definition, and returns the
        # Chalk-ified version of it, we cannot "import" the user's class definition. So, we define a protocol class that contains the
        # same instance attributes. The type checker can match the user's class against the protocol.
        #
        # An @overload is used to match each protocol class (class #3) to the typestub version of the class (class #2)
        # Since the first matching protocol will be used, the feature sets with the _most_ features should appear first
        # Also including the class name as part of the sort key for stability
        parsed_feature_classes = sorted(
            self._parsed_feature_classes.items(), key=lambda x: (len(x[1].annotations), x[0]), reverse=True
        )
        for feature_cls_name, features_cls in parsed_feature_classes:
            # First generate the metaclass definition
            lines.append(
                f"""\
class {feature_cls_name}Metaclass(FeaturesMeta):"""
            )
            for attribute, annotation in features_cls.annotations.items():
                lines.append(
                    f"""\
    @property
    def {attribute}(self) -> Type[{annotation.annotation}]: ...
"""
                )
            if len(features_cls.annotations) == 0:
                lines.append(
                    f"""\
    ...
"""
                )
            # Next, generate the class definition
            lines.append(
                f"""\
class {feature_cls_name}(Features, metaclass={feature_cls_name}Metaclass):"""
            )
            lines.append(
                f"""\
    def __init__(
        self,"""
            )
            for attribute, annotation in features_cls.annotations.items():
                lines.append(
                    f"""\
        {attribute}: {annotation.annotation} = ...,"""
                )
            lines.append(
                """\
    ):"""
            )
            for attribute, annotation in features_cls.annotations.items():
                lines.append(
                    f"""\
        self.{attribute}: {annotation.annotation}"""
                )
            if len(features_cls.annotations) == 0:
                lines.append(
                    f"""\
        ..."""
                )
            lines.append("")
            # Finally, generate the protocol class representing the features class that is being transformed
            lines.append(
                f"""\
class {feature_cls_name}Protocol(Protocol):"""
            )
            has_proto_annotation = False
            for attribute, annotation in features_cls.annotations.items():
                if not annotation.include_in_protocol_cls:
                    continue
                has_proto_annotation = True
                lines.append(
                    f"""\
    {attribute}: {annotation.annotation}"""
                )
            if not has_proto_annotation:
                lines.append(
                    f"""\
    ..."""
                )
            lines.append("")

        # Add overloads to the @features decorator to hint that it returns
        # instances of the classes defined above, not the classes defined in the user's module
        # This allows us to put all type stubs in one file, under the chalk/features/feature namespace,
        # rather than having to create a type stub for each user's feature class.
        for features_cls_name, features_cls in parsed_feature_classes:
            # For each features class, adding two overloads. The first overload transforms the definition
            # from the user's code into our stub. However, since we are technically importing the version that
            # has already been transformed with @features, we need to annotate how to handle a class that
            # has already been processed -- hence the second definition which is effectively a no-op.
            lines.append(
                f"""\
@overload
def features(item: Type[{features_cls_name}Protocol]) -> Type[{features_cls_name}]: ...
"""
            )

        # We also need to handle when the user annotates the features class with args, such as an owner or tags, e.g.
        # @features(owner=...)
        # class MyFeaturesClass:
        #     ...
        # To do this, we add one additional overload for features that returns a protocol class.
        # This protocol class implements __call__ with overloads, similar to the above
        lines.append(
            """\
@overload
def features(
    *,
    owner: Optional[str] = ...,
    tags: Optional[Tags] = ...,
    max_staleness: Optional[Duration] = ...,
    etl_offline_to_online: Optional[bool] = ...,
) -> __stubgen__features_proto: ...

class __stubgen__features_proto(Protocol):"""
        )
        for features_cls_name, features_cls in parsed_feature_classes:
            overload = (
                "@overload" if len(parsed_feature_classes) > 1 else ""
            )  # It is incorrect to use @overload if there is just one definition
            lines.append(
                f"""\
    {overload}
    def __call__(self, item: Type[{features_cls_name}Protocol]) -> Type[{features_cls_name}]: ...
"""
            )
        if len(parsed_feature_classes) == 0:
            lines.append(
                """\
    ...
"""
            )
        return lines


def configure_stubgen_argparse(parser: argparse.ArgumentParser):
    parser.add_argument(
        "--root",
        type=str,
        default=None,
        help="Project root to scan for features definitions. By default, will find the directory root.",
    )
    parser.add_argument(
        "--stub_path",
        "-s",
        type=str,
        default=None,
        help="Folder containing custom type stubs. By default, will use the `typings` folder, relative to the project root",
    )


def run_stubgen(args: argparse.Namespace):
    root = args.root
    if root is None:
        root = get_directory_root() or pathlib.Path(os.getcwd())
    else:
        assert isinstance(root, str)
        root = os.path.abspath(root)
        root = pathlib.Path(root)
    stub_path = args.stub_path
    if stub_path is None:
        stub_path = str(root / "typings")
    assert isinstance(stub_path, str)
    failed_imports = import_all_python_files_from_dir(root)
    if len(failed_imports) > 0:
        warnings.warn(
            f"Stubs may be incomplete due to errors in loading the following files: {', '.join([x.filename for x in failed_imports])}"
        )
    stubgen = StubGenerator()
    for features_cls in FeatureSetBase.registry.values():
        stubgen.register_features_class(features_cls)
    lines = stubgen.generate_features_decorator_stub_file()
    folder = os.path.join(stub_path, "chalk", "features")
    os.makedirs(folder, exist_ok=True)
    output_file = os.path.join(folder, "feature_set_decorator.pyi")
    with open(output_file, "w+") as f:
        f.write("\n".join(lines))
    print(f"Successfully wrote type stubs to {output_file}")
