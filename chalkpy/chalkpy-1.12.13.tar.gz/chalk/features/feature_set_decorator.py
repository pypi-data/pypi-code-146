import ast
import functools
import inspect
import re
import sys
import textwrap
import threading
import types
from datetime import datetime, timedelta
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Mapping,
    MutableMapping,
    Optional,
    Tuple,
    Type,
    TypeVar,
    Union,
    cast,
    overload,
)

from chalk.features.feature_field import Feature, feature_time
from chalk.features.feature_set import Features, FeatureSetBase
from chalk.features.feature_wrapper import FeatureWrapper
from chalk.features.tag import Tags
from chalk.serialization.parsed_annotation import ParsedAnnotation
from chalk.streams import Windowed
from chalk.utils.collections import ensure_tuple
from chalk.utils.duration import Duration, timedelta_to_duration
from chalk.utils.metaprogramming import MISSING, create_fn, field_assign, set_new_attribute
from chalk.utils.string import removeprefix, to_snake_case

T = TypeVar("T")

__all__ = ["features"]


@overload
def features(
    *,
    owner: Optional[str] = None,
    tags: Optional[Tags] = None,
    etl_offline_to_online: bool = ...,
    max_staleness: Optional[Duration] = ...,
    name: Optional[str] = None,
) -> Callable[[Type[T]], Type[T]]:
    ...


@overload
def features(cls: Type[T]) -> Type[T]:
    ...


def features(
    cls: Optional[Type[T]] = None,
    *,
    owner: Optional[str] = None,
    tags: Optional[Tags] = None,
    etl_offline_to_online: Optional[bool] = None,
    max_staleness: Optional[Duration] = ...,
    name: Optional[str] = None,
) -> Union[Callable[[Type[T]], Type[T]], Type[T]]:
    """Returns the same class as was passed in, with dunder methods
    added based on the fields defined in the class.

    Examines PEP 526 __annotations__ to determine fields.
    """

    def wrap(c: Type[T]) -> Type[T]:
        namespace = name or to_snake_case(c.__name__)
        if name is not None and re.sub(r"[^a-z_0-9]", "", namespace) != namespace:
            raise ValueError(
                (
                    f"Namespace must be composed of lower-case alpha-numeric characters and '_'. Provided namespace "
                    f"'{namespace}' for class '{c.__name__}' contains invalid characters."
                )
            )
        if name is not None and len(namespace) == 0:
            raise ValueError(f"Namespace cannot be an empty string, but is for the class '{c.__name__}'.")
        updated_class = _process_class(
            cls=c,
            owner=owner,
            tags=ensure_tuple(tags),
            etl_offline_to_online=etl_offline_to_online,
            max_staleness=timedelta_to_duration(max_staleness)
            if isinstance(max_staleness, timedelta)
            else max_staleness,
            namespace=namespace,
        )
        set_new_attribute(
            cls=updated_class,
            name="namespace",
            value=namespace,
        )
        assert issubclass(updated_class, Features)
        FeatureSetBase.registry[updated_class.__chalk_namespace__] = updated_class

        primary_feature = _discover_feature(
            updated_class,
            "primary",
            lambda f: f.primary,
            lambda f: f.name == "id" and not f.has_resolved_join and not f.is_feature_time,
        )
        if primary_feature is not None:
            primary_feature.primary = True

        timestamp_feature = _discover_feature(
            updated_class,
            "feature time",
            lambda f: f.is_feature_time,
        )
        set_new_attribute(cls=updated_class, name="__chalk_primary__", value=primary_feature)
        set_new_attribute(cls=updated_class, name="__chalk_ts__", value=timestamp_feature)
        if FeatureSetBase.hook is not None:
            FeatureSetBase.hook(cast(Features, updated_class))

        return cast(Type[T], updated_class)

    # See if we're being called as @features or @features().
    if cls is None:
        # We're called with parens.
        return wrap

    # We're called as @features without parens.
    return wrap(cls)


def _discover_feature(cls: Type[Features], name: str, *conditions: Callable[[Feature], bool]):
    for cond in conditions:
        features = [c for c in cls.features if cond(c)]
        if len(features) == 1:
            return features[0]
        if len(features) > 1:
            raise ValueError(
                f"Multiple {name} features are not supported in {cls.__name__}: "
                + ", ".join(f"{cls.__name__}.{x.name}" for x in features)
            )
    return None


def _init_param(f: Feature):
    # Return the __init__ parameter string for this field.  For
    # example, the equivalent of 'x:int=3' (except instead of 'int',
    # reference a variable set to int, and instead of '3', reference a
    # variable set to 3).
    return f"{f.attribute_name}:_type_{f.attribute_name}=MISSING"


def _getattribute_fn(_globals: Dict[str, Any]):
    # If calling getattr() on an instance for a feature name, do NOT return a class-level FeatureWrapper
    # Instead, raise an attribute error
    return create_fn(
        name="__getattribute__",
        args=["self", "attribute_name"],
        body=[
            "o = object.__getattribute__(self, attribute_name)",
            "if isinstance(o, FeatureWrapper):",
            "    raise AttributeError(f'Feature {attribute_name} is not defined on this instance of class {type(self).__name__}')",
            "return o",
        ],
        _globals=_globals,
        _locals={
            "FeatureWrapper": FeatureWrapper,
        },
        return_type=Any,
    )


def _init_fn(fields: List[Feature], self_name: str, _globals: Dict[str, Any]):
    # fields contains both real fields and InitVar pseudo-fields.

    # Make sure we don't have fields without defaults following fields
    # with defaults.  This actually would be caught when exec-ing the
    # function source code, but catching it here gives a better error
    # message, and future-proofs us in case we build up the function
    # using ast.

    _locals: MutableMapping[str, Any] = {f"_type_{f.attribute_name}": f.typ and f.typ.annotation for f in fields}
    _locals.update(
        {
            "MISSING": MISSING,
            # '_HAS_DEFAULT_FACTORY': _HAS_DEFAULT_FACTORY,
        }
    )

    body_lines = []
    for f in fields:
        assert f.attribute_name is not None
        line = field_assign(f.attribute_name, f.attribute_name, self_name)
        # line is None means that this field doesn't require
        # initialization (it's a pseudo-field).  Just skip it.
        if line:
            body_lines.append(line)

    # If no body lines, use 'pass'.
    if not body_lines:
        body_lines = ["pass"]

    # Add the keyword-only args.  Because the * can only be added if
    # there's at least one keyword-only arg, there needs to be a test here
    # (instead of just concatenting the lists together).
    _init_params = [_init_param(f) for f in fields]
    return create_fn(
        name="__init__",
        args=[self_name] + _init_params,
        body=body_lines,
        _locals=_locals,
        _globals=_globals,
        return_type=None,
    )


def _parse_tags(ts: str) -> List[str]:
    ts = re.sub(",", " ", ts)
    ts = re.sub(" +", " ", ts.strip())
    return [xx.strip() for xx in ts.split(" ")]


def _get_field(
    cls: Type,
    annotation_name: str,
    comments: Mapping[str, str],
    class_owner: Optional[str],
    class_tags: Optional[Tuple[str, ...]],
    class_etl_offline_to_online: Optional[bool],
    class_max_staleness: Optional[Duration],
    namespace: str,
):
    # Return a Field object for this field name and type.  ClassVars and
    # InitVars are also returned, but marked as such (see f._field_type).
    # default_kw_only is the value of kw_only to use if there isn't a field()
    # that defines it.

    # If the default value isn't derived from Field, then it's only a
    # normal default value.  Convert it to a Field().
    default = getattr(cls, annotation_name, ...)

    if isinstance(default, Feature):
        # The feature was set like x: int = Feature(...)
        f = default
    elif isinstance(default, Windowed):
        # The feature was set like x: Windowed[int] = windowed()
        # Convert it to a Feature
        f = default.to_feature(bucket=None)
    else:
        # The feature was net set explicitly
        if isinstance(default, types.MemberDescriptorType):
            # This is a field in __slots__, so it has no default value.
            default = ...
        f = Feature(name=annotation_name, namespace=namespace, default=default)

    # Only at this point do we know the name and the type.  Set them.
    f.namespace = namespace
    typ = ParsedAnnotation(cls, annotation_name)
    f.typ = typ
    if typ.is_feature_time is True:
        f.is_feature_time = True
    if typ.is_primary is True:
        f.primary = True

    f.features_cls = cls
    f.attribute_name = annotation_name
    _process_field(f, comments, class_owner, class_tags, class_etl_offline_to_online, class_max_staleness)
    return f


def _process_field(
    f: Feature,
    comments: Mapping[str, str],
    class_owner: Optional[str],
    class_tags: Optional[Tuple[str, ...]],
    class_etl_offline_to_online: Optional[bool],
    class_max_staleness: Optional[Duration],
):
    comment_for_feature = comments.get(f.attribute_name)
    comment_based_description = None
    comment_based_owner = None
    comment_based_tags = None

    if comment_for_feature is not None:
        comment_lines = []
        for line in comment_for_feature.splitlines():
            stripped_line = line.strip()
            if stripped_line.startswith(":owner:"):
                comment_based_owner = removeprefix(stripped_line, ":owner:").strip()
            elif stripped_line.startswith(":tags:"):
                parsed = _parse_tags(removeprefix(stripped_line, ":tags:"))
                if len(parsed) > 0:
                    if comment_based_tags is None:
                        comment_based_tags = parsed
                    else:
                        comment_based_tags.extend(parsed)
            else:
                comment_lines.append(line)

        comment_based_description = "\n".join(comment_lines)

    if f.description is None and comment_based_description is not None:
        f.description = comment_based_description

    if comment_based_tags is not None:
        if f.tags is None:
            f.tags = comment_based_tags
        else:
            f.tags.extend(comment_based_tags)

    if class_tags is not None:
        if f.tags is None:
            f.tags = list(class_tags)
        else:
            f.tags.extend(class_tags)

    if f.owner is not None and comment_based_owner is not None:
        raise ValueError(
            (
                f"Owner for {f.namespace}.{f.name} specified both on the feature and in the comment. "
                f"Please use only one of these two."
            )
        )
    elif f.owner is None:
        f.owner = comment_based_owner or class_owner

    if f.max_staleness is Ellipsis:
        f.max_staleness = class_max_staleness if class_max_staleness is not Ellipsis else None

    if f.etl_offline_to_online is None:
        f.etl_offline_to_online = False if class_etl_offline_to_online is None else class_etl_offline_to_online
    return f


def _recursive_repr(user_function: Callable[[T], str]) -> Callable[[T], str]:
    # Decorator to make a repr function return "..." for a recursive
    # call.
    repr_running = set()

    @functools.wraps(user_function)
    def wrapper(self: T):
        key = id(self), threading.get_ident()
        if key in repr_running:
            return "..."
        repr_running.add(key)
        try:
            result = user_function(self)
        finally:
            repr_running.discard(key)
        return result

    return wrapper


def _repr_fn(fields: List[Feature], _globals: Dict[str, Any]):
    tuples = ",".join(f"('{f.attribute_name}', getattr(self, '{f.attribute_name}', MISSING))" for f in fields)
    fn = create_fn(
        name="__repr__",
        args=["self"],
        body=[
            'return f"{self.__class__.__qualname__}(" + '
            + f"', '.join(f'{{x[0]}}={{x[1]}}' for x in [{tuples}] if x[1] != MISSING)"
            + '+ ")"'
        ],
        _globals=_globals,
        _locals={"MISSING": MISSING},
    )
    return _recursive_repr(fn)


def _eq_fn(fields: List[Feature], _globals: Dict[str, Any]):
    cmp_str = " and ".join(
        f"(getattr(self, '{f.attribute_name}', MISSING) == getattr(other, '{f.attribute_name}', MISSING))"
        for f in fields
    )
    if not cmp_str:
        # if there are no features in this class
        cmp_str = "True"
    return create_fn(
        name="__eq__",
        args=["self", "other"],
        body=["if not isinstance(other, type(self)):", "    return NotImplemented", f"return {cmp_str}"],
        _globals=_globals,
        _locals={
            "MISSING": MISSING,
        },
    )


def _len_fn(_globals: Dict[str, Any]):
    return create_fn(
        name="__len__",
        args=["self"],
        body=[
            "count = 0",
            f"for f in self.features:",
            "    if hasattr(self, f.attribute_name):",
            "        count += 1",
            "return count",
        ],
        _globals=_globals,
        _locals={},
    )


def _iter_fn(fields: List[Feature], _globals: Mapping[str, Any]):
    return create_fn(
        "__iter__",
        args=["self"],
        body=[
            f"for __chalk_f__ in self.features:",
            f"    if hasattr(self, __chalk_f__.attribute_name) and type(__chalk_f__).__name__ == 'Feature' and not __chalk_f__.is_has_one and not __chalk_f__.is_has_many:",
            f"        yield __chalk_f__.fqn, getattr(self, __chalk_f__.attribute_name)",
        ],
    )


def _parse_annotation_comments(cls: Type) -> Mapping[str, str]:
    source = textwrap.dedent(inspect.getsource(cls))

    source_lines = source.splitlines()
    tree = ast.parse(source)
    if len(tree.body) != 1:
        return {}

    comments_for_annotations: Dict[str, str] = {}
    class_def = tree.body[0]
    if isinstance(class_def, ast.ClassDef):
        for stmt in class_def.body:
            if isinstance(stmt, ast.AnnAssign) and isinstance(stmt.target, ast.Name):
                line = stmt.lineno - 2
                comments: List[str] = []
                while line >= 0 and source_lines[line].strip().startswith("#"):
                    comment = source_lines[line].strip().strip("#").strip()
                    comments.insert(0, comment)
                    line -= 1

                if len(comments) > 0:
                    comments_for_annotations[stmt.target.id] = textwrap.dedent("\n".join(comments))

    return comments_for_annotations


def _process_class(
    cls: Type[T],
    owner: Optional[str],
    tags: Tuple[str, ...],
    etl_offline_to_online: Optional[bool],
    max_staleness: Optional[Duration],
    namespace: str,
) -> Type[T]:
    raw_cls_annotations = cls.__dict__.get("__annotations__", {})

    cls_annotations = {}
    for name, annotation in raw_cls_annotations.items():
        if isinstance(annotation, Windowed):
            # NOTE: For Windowed resolvers, both the Annotation and the value are instances of Windowed, unlike normal features
            # whose annotation is the underlying type, and the value is an instance of FeatureWrapper
            # So both `annotation` and `wind` should be instances of Windowed
            # In the future, we should use a subclass of Windowed, rather than an instance, for the type annotation, similar to
            # what we do for Features
            wind = getattr(cls, name, None)
            if wind is None or not isinstance(wind, Windowed):
                raise TypeError(
                    (
                        f"Windowed feature '{namespace}.{name}' is missing windows. "
                        f"To create a windowed feature, use "
                        f"'{name}: Windowed[{annotation._kind.__name__}] = windowed('10m', '30m')."
                    )
                )
            wind.set_kind(kind=annotation.get_kind())
            wind._name = name
            annotation._buckets = wind._buckets
            for bucket in wind._buckets:
                # Make pseudofeatures for each bucket of the window
                feat = wind.to_feature(bucket=bucket)
                setattr(cls, feat.name, feat)
                # For the psuedofeatures, which track an individual bucket, the correct annotation is the
                # underlying annotation, not Windowed[underlying], since it's only one value
                cls_annotations[feat.name] = wind.get_kind()

        cls_annotations[name] = annotation

    cls.__annotations__ = cls_annotations
    if cls.__module__ in sys.modules:
        _globals = sys.modules[cls.__module__].__dict__
    else:
        _globals = {}

    # Find feature times that weren't annotated.
    for (name, member) in inspect.getmembers(cls):
        if name not in cls_annotations and isinstance(member, Windowed):
            raise TypeError(f"Windowed feature '{namespace}.{name}' is missing an annotation, like 'Windowed[str]'")
        if name not in cls_annotations and isinstance(member, Feature):
            # All feature types need annotations, except for datetimes, which we can automatically infer
            if member.typ is not None and member.typ.is_parsed and issubclass(member.typ.underlying, datetime):
                cls_annotations[name] = datetime
            else:
                raise TypeError(f"Feature '{namespace}.{name}' is missing an annotation")

    # If we pass this function something that isn't a class, it could raise
    try:
        comments = _parse_annotation_comments(cls)
    except:
        comments = {}

    cls_fields = [
        _get_field(
            cls=cls,
            annotation_name=name,
            comments=comments,
            class_owner=owner,
            class_tags=tags,
            class_etl_offline_to_online=etl_offline_to_online,
            class_max_staleness=max_staleness,
            namespace=namespace,
        )
        for name in cls_annotations
    ]

    # If there is no timestamp feature, synthesize one
    ts_feature: Optional[Feature] = next((x for x in cls_fields if x.is_feature_time), None)
    if ts_feature is None:
        # Alternatively check if there is a feature called `ts` that is a datetime
        ts_feature = next((x for x in cls_fields if x.name == "ts" and not x.has_resolved_join), None)
        if ts_feature is not None:
            ts_feature.is_feature_time = True
    if ts_feature is None:
        # If the timestamp feature is still none, then synthesize one
        ts_feature = feature_time()
        assert ts_feature is not None
        ts_feature.name = "__chalk_observed_at__"
        ts_feature.attribute_name = "__chalk_observed_at__"
        ts_feature.namespace = namespace
        ts_feature.typ = ParsedAnnotation(underlying=datetime)
        ts_feature.features_cls = cls  # type: ignore
        ts_feature.is_autogenerated = True
        _process_field(
            ts_feature,
            comments=comments,
            class_owner=owner,
            class_tags=tags,
            class_etl_offline_to_online=etl_offline_to_online,
            class_max_staleness=max_staleness,
        )
        cls_fields.append(ts_feature)

    set_new_attribute(
        cls=cls,
        name="__init__",
        value=_init_fn(
            fields=cls_fields,
            # The name to use for the "self"
            # param in __init__.  Use "self"
            # if possible.
            self_name="self",
            _globals=_globals,
        ),
    )

    set_new_attribute(cls=cls, name="__repr__", value=_repr_fn(fields=cls_fields, _globals=_globals))
    set_new_attribute(cls=cls, name="__eq__", value=_eq_fn(fields=cls_fields, _globals=_globals))
    set_new_attribute(cls=cls, name="__hash__", value=None)
    set_new_attribute(cls=cls, name="__iter__", value=_iter_fn(fields=cls_fields, _globals=_globals))

    set_new_attribute(cls=cls, name="__chalk_namespace__", value=namespace)
    set_new_attribute(cls=cls, name="__chalk_owner__", value=owner)
    set_new_attribute(cls=cls, name="__chalk_tags__", value=list(tags))
    set_new_attribute(
        cls=cls, name="__chalk_max_staleness__", value=max_staleness if max_staleness is not Ellipsis else None
    )
    set_new_attribute(
        cls=cls,
        name="__chalk_etl_offline_to_online__",
        value=etl_offline_to_online if etl_offline_to_online is not Ellipsis else False,
    )
    set_new_attribute(cls=cls, name="features", value=cls_fields)
    set_new_attribute(cls=cls, name="__is_features__", value=True)
    set_new_attribute(cls=cls, name="__len__", value=_len_fn(_globals=_globals))
    set_new_attribute(cls=cls, name="__getattribute__", value=_getattribute_fn(_globals=_globals))

    for f in cls_fields:
        assert f.attribute_name is not None
        # Wrap all class features with FeatureWrapper
        setattr(cls, f.attribute_name, FeatureWrapper(f))

    return cls
