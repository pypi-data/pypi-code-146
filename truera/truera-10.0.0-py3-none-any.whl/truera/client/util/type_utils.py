"""
# Types, typing, type handling utilities

## Dealing with __future__.annotations

Some part of these utilities are for consistently dealing with method
annotations under __future__.annotation and without it. You will find `TypeLike`
to signify something which already is a type or a string which needs to be
evaluated to retrieve the named type.

The benefit of __future__.annotations, however, is that we can type more things
that might not otherwise be typable. Additionally, the same handling we need for
this feature are also useful for referring to types that come from optionally
installed packages without producing errors when they are not installed.

## New types and Replacements of existing types

Some existing types do not operate in a manner we would like to so they are
provided here with alternate definitions. These are:

- Optional(t) - now isinstance(None, Optional(int)) == True
- Union(t1, ..., tn) - now isinstance on Union works
- Intersection(t1, ..., tn) - opposite of Union, isinstance works as expected.
- Unit() - a type that always fails its isinstance check.
- Exemplified(t, module) - wraps the given type with capability to list example
  subtypes found within the provided `module`.
- RegexTypeMatch(pattern) - makes subtyping checks based on type names that
  match the given pattern.

Note that in all of these cases, the type parameters are specified as arguments
to constructors as opposed to generic variables which are the cause of their
undesired functionality. That is, we use `Optional(int)` as opposed to
`Optional[int]`.

## Caveats

No actual static type checking is done using these types. They are purely for
runtime checking, for type-based dispatches like overloading, and documentation.
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod
import importlib
import inspect
import re
import types
from typing import Any, Callable, Iterable, Set, Tuple, Type
from typing import Union as tUnion

from truera.client.util.python_utils import cache_on_first_arg
from truera.client.util.python_utils import caller_frame

Annotation = tUnion[Type, str]
ObjLike = tUnion[object, str]  # str may be object so unsure about this


def render_annotation(annot: Annotation) -> str:
    mod, name = parts_of_annotation(annot)
    if mod is None or mod == "builtins" or mod.startswith("truera."):
        # Don't bother printing "builtins" as those are always available in
        # globals. Also don't print truera module names. Those should be
        # documented in ingestion examples.
        return name
    else:
        return f"{mod}.{name}"


def parts_of_annotation(annot: Annotation) -> Tuple[str, str]:
    """
    Given an annotation which is a type or string that may optionally be wrapped
    in quotes if __future__.annotations is used, produce its module of origin
    and name. If the annotation does not refer to a module, returns None for
    that portion.
    """

    if istype(annot):
        module = None,
        if hasattr(annot, "__module__"):
            if hasattr(annot.__module__, "__name__"):
                module = annot.__module__.__name__
            else:
                module = str(annot.__module__)

        name = None
        if hasattr(annot, "__name__"):
            name = annot.__name__

        return module, name

    if annot[0] in ["'", '"'] and annot[0] == annot[-1]:
        annot = annot[1:-1]
        if "." in annot:
            parts = annot.split(".")
            return parts[0], annot
        else:
            return None, annot
    else:
        return None, annot


class Unit(Type):
    """
    A type that cannot have any instances. Instance check always fail. This is
    used for types/classes which are not installed or cannot be retrieved for
    whatever reason.
    """

    def __init__(self):
        pass

    def __new__(cls):
        return super().__new__(cls, "Unit", (), {})

    def __instancecheck__(cls, _):
        return False

    def __subclasscheck__(cls, _):
        return False


unit = Unit()


class Monoid(ABC):
    """
    Monoid. Abstraction of the concept of set of objects with a plus operation
    that can add two objects to produce a third. Models things like
    accumulators, or map-reduce like operations. Must also define a zero object
    for the starting points for monoid-based operations.
    """

    @staticmethod
    @abstractmethod
    def zero() -> Monoid:
        pass

    @staticmethod
    @abstractmethod
    def plus(a: Monoid, b: Monoid) -> Monoid:
        pass


def eval_object(obj: ObjLike, globals={}) -> object:
    """
    Given an object or a string that names it, produce the object if possible.
    Might return None if the module containing that object cannot be loaded
    (i.e. not installed).
    """
    if isinstance(obj, str):
        return get_object_by_name(obj, globals=globals)
    else:
        return obj


@cache_on_first_arg
def eval_type(typ: Annotation, globals={}) -> Type:
    """
    Given a type or a string that names it, produce the type if possible.
    Might return None if the module containing that type cannot be loaded (i.e.
    not installed).
    """

    if istype(typ):
        return typ
    else:
        return get_type_by_name(typ, globals=globals)


@cache_on_first_arg
def istype(obj) -> bool:
    """
    Determine whether the given object can be used as a type. For some versions
    of python, some things like typing.Callable are not instances of Type hence
    this hack is neccessary.
    """

    if isinstance(obj, Type):
        return True

    # The above does not always work. typing.Sequence is not a type for example.

    if hasattr(obj, "__subclasscheck__"):
        return True

    if obj is Callable:
        return True

    return False


def fullname(obj: Any) -> str:
    """
    Get the full module/package class name of the given object.
    """

    if isinstance(obj, types.ModuleType):
        return obj.__name__
    elif isinstance(obj, type):
        return obj.__module__ + "." + obj.__name__
    elif hasattr(obj, "__class__"):
        return fullname(obj.__class__)
    else:
        raise ValueError(f"Cannot determine full name of {obj}.")


def _find_matches(mod, walked: Set, found: Set, t: Type):
    if mod in walked:
        return

    walked.add(mod)

    for name in dir(mod):
        try:
            submod = getattr(mod, name)
        except:
            continue

        fname = fullname(submod)

        if inspect.ismodule(submod):  #, types.ModuleType):
            if fname.startswith(fullname(mod)):
                for m in _find_matches(submod, walked=walked, found=found, t=t):
                    yield m
        elif fname in found:
            continue

        elif inspect.isclass(submod):
            if issubclass(submod, t):
                found.add(fname)
                yield submod
        else:
            if isinstance(submod, t):
                found.add(fname)
                yield submod


def find_matches(mod: types.ModuleType, t: Type) -> Iterable[Type]:
    """
    Walk the module hierarchy starting with the given module `mod` producing all
    of the contents that match the given type `t`.
    """
    return _find_matches(mod, set(), set(), t=t)


@cache_on_first_arg
def get_type_by_name(typ: Annotation, globals={}) -> Type:
    obj = get_object_by_name(typ, globals)

    if not istype(obj):
        print(f"WARNING: name {typ} does not refer to a type.")

        return unit

    return obj


# @functools.lru_cache(maxsize=128, ) # cannot use this cache with globals
def get_object_by_name(obj: ObjLike, globals={}) -> object:
    """
    When using "from __future__ import annotations", all annotations are
    strings. Those which were specified as strings get further quoted inside the
    string like:

        def func(arr: 'numpy.ndarray): ...

    The annotation for `arr` will be:

        "'numpy.ndarray'"

    That is, a string with an additional ' quotation. On the other hand, for:

        def func(arr: numpy.array): ...

    The annotation will be:

        "numpy.ndarray"
    """

    if not isinstance(obj, str):
        return obj

    if obj[0] in ['"', "'"] and obj[0] == obj[-1]:
        obj = obj[1:-1]

    try:
        # Module might already be loaded and available in globals. For
        # example in "import numpy as np". Then "np" will be numpy in that
        # context. Globals needs to be known for this to work though.

        return eval(obj, globals)

    except Exception as e:
        # Otherwise assume the type is written as "module...attribute" so we
        # first try to import top-level module. This allows us to refer to types
        # without importing them ahead of time.
        # print(f"WARNING: Could not evaluate '{obj}': {e}.")
        pass  # continue

    if "." not in obj:
        print(f"WARNING: could not evaluate object from string '{obj}'.")
        return unit

    else:
        addr = obj.split(".")
        mod_name = addr[0]
        addr = addr[1:]

    try:
        mod = importlib.import_module(mod_name)

    except:
        print(f"WARNING: could not import module {mod_name}")
        # This is expected if module is not installed.
        return unit

    try:
        # Get sub-modules or final attribute.
        for comp in addr:
            mod = getattr(mod, comp)

        return mod

    except Exception as e:
        # This is less expected but could still happen for example due to
        # differing tensorflow versions that all have the same top-level name
        # but different contents.
        print(
            f"WARNING: loaded module for {obj} but could not load type/class because {e}."
        )
        return unit


def annotation_isinstance(obj: Any, annot: Annotation, globals={}) -> bool:
    """
    `isinstance` equivalent that works for more things including types given by
    name as is the case when delayed type evaluation is enabled (annotations in
    __future__).
    """

    annot_type = eval_type(annot, globals=globals)

    return isinstance(obj, annot_type)


def annotation_issubclass(
    annot1: Annotation, annot2: Annotation, globals={}
) -> bool:
    """
    `issubclass` equivalent that works for more things including types given by
    name as is the case when delayed type evaluation is enabled (annotations in
    __future__).
    """

    annot1_type = eval_type(annot1, globals=globals)
    annot2_type = eval_type(annot2, globals=globals)

    return issubclass(annot1_type, annot2_type)


class Exemplified(Type):
    """
    A Type that can list its sub-types.
    """

    def __init__(self, type: Type, base_module: Union[str, types.ModuleType]):
        self.type = type
        self.base_module = eval_object(
            base_module, globals=caller_frame().f_globals
        )

    def __new__(cls, type: Type, base_module: types.ModuleType):
        # Needed for Type subtypes.
        self = super().__new__(
            cls, type.__name__, type.__bases__, dict(type.__dict__)
        )
        return self

    def __str__(self):
        return self.__name__

    def __repr__(self):
        return str(self)

    def __instancecheck__(cls, obj):
        return cls.type.__instancecheck__(obj)

    def __subclasscheck__(cls, cls2):
        return cls.type.__subclasscheck__(cls2)

    def exemplify(self):
        return find_matches(self.base_module, t=self)

    @property
    def __doc__(self):
        msg = f"Installed examples of {self.type}:\n"
        if self.base_module is not None:
            for submod in Exemplified.exemplify(self):  # pylint confusion here
                msg += f"\t{fullname(submod)}\n"
        else:
            pass

        return msg


class RegexTypeMatch(Type):
    """
    A Type whose membership is determined by a regular expression on type/class
    names.
    """

    def __new__(cls, name, pattern, *args, **kwargs):
        # This is needed for Type subtypes.
        return super().__new__(cls, name, (type,), {})

    def __init__(
        self,
        name: str,
        pattern: str,
    ):
        self.name = name
        self.pattern = re.compile(pattern)

    def __instancecheck__(cls, obj):
        fname = fullname(obj)
        return cls.pattern.fullmatch(fname) is not None

    def __subclasscheck__(cls, cls2):
        # Subclass check needs to find a class with a matching name in any of
        # the bases which can be retrieved from the method resolution order
        # list. TODO: maybe there are more clear ways of getting base/parent
        # types?
        return any(
            cls.pattern.fullmatch(fullname(c)) is not None for c in cls2.mro()
        )

    def __str__(self):
        # str quotes pattern in the typical regular expression delimeter .
        return f"/{self.pattern.pattern}/"

    def __repr__(self):
        return str(self)


class Optional(Type):
    """
    An optional type with an instance check that returns true when tested with
    None.
    """

    def __new__(cls, typ: Annotation):
        # Needed for Type subtypes.
        return super().__new__(
            cls, f"{cls.__name__}({render_annotation(typ)})", (), {}
        )

    def __init__(self, typ: Annotation):
        self.typ_as_named = fullname(typ)
        self.typ = eval_type(typ, globals=caller_frame().f_globals)

    def __instancecheck__(cls, obj):
        return obj is None or isinstance(obj, cls.typ)

    def __subclasscheck__(cls, obj):
        # Check the type constructor is subclass of Optional constructor.
        if hasattr(obj, "__class__"):
            cls2 = obj.__class__
            if not issubclass(cls2, cls.__class__):
                return False

        # Also check that type argument is also subclass. Note that this only applies to
        # our custom Optional and subclasses.
        if hasattr(obj, "typ"):
            return issubclass(obj.typ, cls.typ)
        else:
            return False

    def __str__(self):
        return f"Optional[{self.typ}]"


class Intersection(Type):
    """
    Intersection type that can be used for isinstance and issubclass .
    """

    def __new__(cls, *types):
        # Needed for Type subtypes.
        return super().__new__(
            cls, f"Intersection[{', '.join(map(str, types))}]", (), {}
        )

    def __init__(self, *types: Tuple[Annotation]):
        self.types_as_named = tuple(
            t if isinstance(t, str) else fullname(t) for t in types
        )
        self.types = tuple(
            eval_type(typ, globals=caller_frame().f_globals) for typ in types
        )

    def __instancecheck__(cls, obj):
        return all(isinstance(obj, t) for t in cls.types)

    def __subclasscheck__(cls, cls2):
        return all(issubclass(cls2, t) for t in cls.types)

    def __str__(self):
        return f"Intersection[{', '.join(map(str, self.types_as_named))}]"


class Not(Type):
    """
    Not type, instance and subclass checks are negated.
    """

    def __new__(cls, typ):
        # Needed for Type subtypes.
        return super().__new__(cls, f"Not[{typ}]", (), {})

    def __init__(self, typ: Annotation):
        self.type_as_named = typ if isinstance(typ, str) else fullname(typ)
        self.type = eval_type(typ, globals=caller_frame().f_globals)

    def __instancecheck__(cls, obj):
        return not (isinstance(obj, cls.type))

    def __subclasscheck__(cls, cls2):
        return not (issubclass(cls2, cls.type))

    def __str__(self):
        return f"Not[{self.type_as_named}]"


class Union(Type):
    """
    Union type that can be used for isinstance and issubclass .
    """

    def __new__(cls, *types):
        # Needed for Type subtypes.
        return super().__new__(
            cls, f"Union[{', '.join(map(str, types))}]", (), {}
        )

    def __init__(self, *types: Tuple[Annotation]):
        self.types_as_named = tuple(
            t if isinstance(t, str) else fullname(t) for t in types
        )
        self.types = tuple(
            eval_type(typ, globals=caller_frame().f_globals) for typ in types
        )

    def __instancecheck__(cls, obj):
        return any(isinstance(obj, t) for t in cls.types)

    def __subclasscheck__(cls, cls2):
        return any(issubclass(cls2, t) for t in cls.types)

    def __str__(self):
        return f"Union[{', '.join(map(str, self.types))}]"
