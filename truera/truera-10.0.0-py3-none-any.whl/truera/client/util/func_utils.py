"""
Utilities for manipulating, extending, documenting, importing python methods or
modules.
"""

from __future__ import annotations

from abc import ABCMeta
from copy import copy
import functools
from inspect import BoundArguments
from inspect import Parameter
from inspect import Signature
from inspect import signature
import sys
import traceback
from types import MethodType
from typing import (
    Any, Callable, Dict, Iterable, List, Mapping, OrderedDict, Sequence, Tuple,
    TypeVar
)
import warnings

from truera.client.util.python_utils import caller_frame
from truera.client.util.type_utils import annotation_isinstance
from truera.client.util.type_utils import eval_type
from truera.client.util.type_utils import Monoid
from truera.client.util.type_utils import Optional
from truera.client.util.type_utils import parts_of_annotation
from truera.client.util.type_utils import render_annotation

T = TypeVar("T")
C = TypeVar("C")
U = TypeVar("U")
V = TypeVar("V")

# positional args
PArgs = Tuple[Any]
# keyword args
KWArgs = Mapping[str, Any]
# both
Args = Tuple[PArgs, KWArgs]

BindingsMap = Callable[[BoundArguments], BoundArguments]
ArgsMap = Callable[[PArgs, KWArgs], Args]


def retab(s, tab: str = "  ", tab_first: bool = True):
    """
    Changes the tab/margin of the given string `s` to the given `tab`. If
    `tab_first` is provided, also adds the marging to the first line of `s`.
    """

    if tab_first:
        return "\n".join([tab + s for s in s.split("\n")])
    else:
        return ("\n" + tab).join(s.split("\n"))


def compose(fs: Sequence[Callable]) -> Callable:
    """
    Compose the sequence of single arg methods, applied in same order as sequence.
    """

    def composed(arg):
        for f in fs:
            arg = f(arg)
        return arg

    return composed


def doc_untab(obj: Any) -> Tuple[str, str]:
    """
    Get the margin and a de-marginalized docstring of the given object.
    """

    if not hasattr(obj, "__doc__"):
        return ("", "")

    doc = obj.__doc__

    if doc is None:
        return ("", "")

    while doc[0] == "\n":
        doc = doc[1:]

    tab = ""

    while doc[0] in [" ", "\t"]:
        tab += doc[0]
        doc = doc[1:]

    lines = []
    for line in doc.split("\n"):
        if line.startswith(tab):
            line = line[len(tab):]

        lines.append(line)

    return (tab, "\n".join(lines))


def doc_render(obj) -> str:
    """
    Draws the given object's docstring removing its margin.
    """

    _, doc = doc_untab(obj)

    if doc[-1] == "\n":
        doc = doc[0:-1]

    return doc


def doc_prepend(obj: Any, text: str) -> None:
    """
    Prepend the given text to the docstring for the given object. Prepends
    using the same margins that exist already.
    """

    if not obj.__doc__:
        doc = ""
    else:
        doc = obj.__doc__

    tabwidth = 0

    # Check if there is a margin made of spaces in the existing docstring.
    if len(doc) > 2:

        if doc[0] == "\n":
            # Check for docstrings delimited with """ that start on the next
            # line after delimeter. The first line in such docstrings does not
            # have a margin, so we throw away the first line.

            lines = doc.split("\n")
            l1 = lines[1]
        else:
            l1 = doc

        for i, c in enumerate(l1):
            if c != " ":
                break

        tabwidth = i

    textlines = text.split("\n")
    tabedtext = "\n".join(
        [(" " * tabwidth) + textline for textline in textlines]
    )

    doc = tabedtext + "\n" + doc

    obj.__doc__ = doc


class Deprecate:

    @staticmethod
    def module(name, message, dep_version, remove_version):
        """
        Immediately issue a warning that the module with the given `name` is
        deprecated.
        """

        warnings.warn(
            message=
            f"Module {name} is deprecated since version {dep_version} and will be removed in {remove_version}. {message}",
            category=DeprecationWarning
        )

    @staticmethod
    def method(message, dep_version, remove_version):
        """
        Mark the given method as being deprecated since `dep_version` and that it
        will be removed in version `remove_version`.
        """

        def wrapper(thing):
            if isinstance(thing, classmethod):
                func = thing.__func__
                extra_decorator = classmethod
            elif isinstance(thing, Callable):
                func = thing
                extra_decorator = lambda x: x
            else:
                raise RuntimeError(
                    f"Do not know how to wrap object of type {type(thing)}."
                )

            dep_message = f"Method {func.__name__} is deprecated since version {dep_version} and will be removed in {remove_version}. {message}"

            @functools.wraps(func)
            @extra_decorator
            def f(*args, **kwargs):
                warnings.warn(message=dep_message, category=DeprecationWarning)
                return func(*args, **kwargs)

            # Also add depreciation message to the doc string.
            doc_prepend(f, f"DEPRECATED: {dep_message}")
            return f

        return wrapper


class WrapperMeta(ABCMeta):
    """
    ABC to help enforce some rules regarding wrappers. 
    
    - Attribute protection: classes that mark attributes with "__protected__"
      cannot have those attributes overridden by child classes.
    
    - Initialization requirements: methods marked with "__require__" need to be
      executed during an objects initialization. Mark parent initializers to
      require children to call the parent initializer.

    - Abstract method deprecation. Allows for wrappers to accept old methods in
      place of new renamed ones while issuing deprecation warnings.
    """

    @staticmethod
    def deprecates(oldfunc_name: str, dep_version: str, remove_version: str):
        """
        Mark an abstract method as deprecating the given method (name). During
        class construction, the marked field will be filled in using the oldfunc
        method if it exists, issuing a deprecation warning.
        """

        def wrapper(absfunc):
            # TODO: figure out a working way to detect whether absfunc is an
            # abstractmethod.

            #  assert isinstance(absfunc, abstractmethod), "This deprecation wrapper is meant for abstract methods only."

            absfunc.__deprecates__ = (oldfunc_name, dep_version, remove_version)

            return absfunc

        return wrapper

    # TODO: try to reuse typing.final
    @staticmethod
    def protect(obj) -> Any:
        """Decorator to mark the given object as protected."""

        if isinstance(obj, Callable) or isinstance(obj, classmethod):
            obj.__protected__ = True

        elif isinstance(obj, property):
            if obj.fset is not None:
                obj.fset.__protected__ = True
            if obj.fget is not None:
                obj.fget.__protected__ = True
            if obj.fdel is not None:
                obj.fdel.__protected__ = True

        else:
            raise ValueError(f"Unhandled object type to protect: {type(obj)}")

        return obj

    def __check_protect(obj, attr, base_name, class_name):
        """
        Check if the given object is marked protected and if so, throw an error
        with the other args as debugging info.
        """

        if hasattr(obj, "__protected__") and getattr(obj, "__protected__"):
            raise AttributeError(
                f"Attribute {attr} of {base_name} should not be overriden in child class {class_name}."
            )

    def __check_deprecates(base_val, attr, attrs):
        """
        Check if an abstractmethod in `base_val` named `attr` is defined in
        `attrs` by its old name.
        """

        if hasattr(base_val.__func__, "__deprecates__"):

            oldmethod_name, dep_version, remove_version = getattr(
                base_val.__func__, "__deprecates__"
            )

            if oldmethod_name in attrs:
                # Issue warning.
                warnings.warn(
                    f"Method {oldmethod_name} is deprecated since {dep_version} and will be removed in {remove_version}. "
                    f"The method was renamed to {base_val.__func__.__name__}.",
                    DeprecationWarning
                )

                # Replace the abstract method with concrete implementation from `oldmethod_name`.
                attrs[attr] = attrs[oldmethod_name]
            else:
                # Leave abstract, will cause abstractmethod undefined in parent __new__ .
                pass
        else:
            # This should cause abstracmethod needs to be defined in the parent __new__ .
            pass

    @staticmethod
    def require(func) -> Any:
        """
        Decorator to mark the given method as required during initialization and
        must be overriden.
        """

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            wrapper.__require__ = False
            return func(*args, **kwargs)

        wrapper.__require__ = True

        return wrapper

    @staticmethod
    def require_if_extended(func) -> Any:
        """
        Decorator to mark the given method as required during initialization but
        does not need to be overriden.
        """

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            wrapper.__require__ = False
            return func(*args, **kwargs)

        wrapper.__require__ = True
        wrapper.__extend_optional__ = True

        return wrapper

    def __init__(cls, name, bases, attrs):
        """
        When instantiating an object, do some checks and wraps some methods
        depending on what the object is.
        """

        if len(bases) == 0:
            # If instantiating metaclass itself, do nothing.
            super().__init__(name, bases, attrs)
            return

        # Otherwise the instantiated object has some parent class base.
        # TODO: What if they have more than one?

        if not "__init__" in attrs:
            # If the child class has no initializer of its own, check if we wanted it to.

            if hasattr(bases[0], "__init__") and hasattr(
                bases[0], "__require__"
            ) and not hasattr(bases[0].__init__, "__extend_optional__"):
                # If your parent has an init with is required, you need to have an init (and call the parent).
                raise AttributeError(
                    f"Wrapper class {name} needs to define __init__."
                )
            else:
                # If we did not want child class to have __init__ of its own, nothing else to do.

                super().__init__(name, bases, attrs)
                return

        init = attrs['__init__']

        if hasattr(init, "__require__"):
            # If the child we are looking at is one annotated with require, we
            # are in one of the base wrapper classes. No more enforcements for
            # those.

            super().__init__(name, bases, attrs)
            return

        # Otherwise we have a child class that has an init and extended one of the wrapper classes.
        # We wraper the init method as follows:

        @functools.wraps(init)
        def wrapper(self, *args, **kwargs):
            nonlocal init

            # Set the __require__ mark for all base classes that have the mark to True.
            for base in bases:
                if hasattr(base, "__init__"):
                    baseinit = getattr(base, "__init__")
                    if hasattr(baseinit, "__require__"):
                        baseinit.__require__ = True

            # Call the child initializer.
            init(self, *args, **kwargs)

            # Check that __required__ marks have now been changed to False. Note that this is done
            # by the wrapper in the @require decorator.
            for base in bases:
                if hasattr(base, "__init__"):
                    baseinit = getattr(base, "__init__")
                    if hasattr(baseinit, "__require__"):
                        if baseinit.__require__:
                            raise RuntimeError(
                                f"Class {base.__name__} initializer must be called by child class {name}."
                            )

        # Update the created class' initializer with the wrapper.
        cls.__init__ = wrapper
        attrs['__init__'] = wrapper  # not sure if this is needed too

        super().__init__(name, bases, attrs)

    def __new__(meta, name, bases, attrs):
        """
        When creating a new instance, check if any attributes are defined in the
        parent class and are labeled as protected. If so, throw an error. Also
        check for deprecated abstractmethods to point them to new names while
        issuing warnings.
        """

        for base in bases:
            # Check all the bases.

            for attr, base_val in base.__dict__.items():
                if hasattr(base_val, "__func__"):
                    # if abstract, check if for deprecated methods that can be renamed

                    meta.__check_deprecates(base_val, attr, attrs)

            for attr in attrs:
                # For each attribute in the created class.

                if hasattr(base, attr):
                    # Check if the base class also has that attribute.

                    base_val = getattr(base, attr)

                    # Checks need to be done differently for some objects than others.
                    # property in particular does not like creating new attributes to mark
                    # protection, hence this condition here.

                    if isinstance(base_val, Callable
                                 ) or isinstance(base_val, classmethod):

                        # And if so, whether it is marked as protected.
                        meta.__check_protect(
                            base_val, attr, base.__name__, name
                        )

                    elif isinstance(base_val, property):
                        # If attribute in base class was a property, check whether any of its
                        # constituent methods were marked protected.
                        if base_val.fget is not None:
                            meta.__check_protect(
                                base_val.fget, attr, base.__name__, name
                            )
                        if base_val.fset is not None:
                            meta.__check_protect(
                                base_val.fset, attr, base.__name__, name
                            )
                        if base_val.fdel is not None:
                            meta.__check_protect(
                                base_val.fdel, attr, base.__name__, name
                            )
                    else:
                        pass

        return super().__new__(meta, name, bases, attrs)


# method decorator
def derive(**derivations: Dict[str, 'decorator']):
    """
    A decorator that creates multiple methods based on the given `func`, each as
    named and wrapped by the given set of `derivations`. Each derivation must be
    a method decorator. Methods derived in this way will need pylint exceptions
    for E1101 at call sites. For example, using:

    # pylint: disable=E1101
    """

    # TODO: modify docstring

    frame = caller_frame()

    try:
        # get the caller's locals so we can give them the derived methods
        locals = frame.f_locals

        def wrapper(func):
            for name, decorator in derivations.items():
                locals[name] = decorator()(func)

            # Returned function is added to caller's locals as per decorator
            # semantics assuming `derive` is used as a decorator.
            return func

        return wrapper
    finally:
        del frame


# method decorator
def singlefun_of_manyfun():
    """
    Convert a method that accepts and returns a list of items to instead
    accept and return a single item. Any args other than the first are preserved.
    """

    def wrapper(func: Callable[[List[U]], List[V]]) -> Callable[[U], V]:

        @functools.wraps(func)
        def ret_fun(item: U, *args, **kwargs) -> V:
            results: List[V] = func([item], *args, **kwargs)
            return results[0]

        return ret_fun

    return wrapper


# method decorator
def self_singlefun_of_self_manyfun():
    """
    Convert a member method that accepts and returns a list of items to instead
    accept and return a single item. Self and args other than the first non-self
    arg are preserved.
    """

    def wrapper(func: Callable[[C, List[U]], List[V]]) -> Callable[[C, U], V]:

        @functools.wraps(func)
        def ret_fun(self: C, item: U, *args, **kwargs) -> V:
            results: List[V] = func(self, [item], *args, **kwargs)
            return results[0]

        return ret_fun

    return wrapper


def render_args_kwargs(args, kwargs):
    """
    Create a representation of args/kwargs lists but shorten large values so
    your screen does not get swamped.
    """

    message = f"args={str(args)[0:128]}\n"
    message += f"kwargs=\n"
    for k, v in kwargs.items():
        message += retab(f"{k}: {str(v)[0:32]}", "\t") + "\n"
    return message


def render_exception(exc: Exception):
    """
    Create a representation of an exception that includes minimal frame
    information for exception raise site. This differs in the output of
    str(Exception) especially for assertion exceptions that do not print out the
    raise site.
    """

    tb_info = traceback.extract_tb(exc.__traceback__)
    filename, line_number, function_name, text = tb_info[-1]
    message = f"{str(type(exc).__name__)} {filename}:{line_number}:{function_name}:{text}"
    text = str(exc)
    if text:
        message += "\n" + retab(text, "\t")

    return message


def render_sig(func, withdoc: bool = False, override_name: str = None):
    """
    Given a function, produce a string describing its signature in a manner that
    is independent of whether __future__.annotations have been imported or not.

    - `withdoc` - also include the docstring
    - `override_name` - use the given string as the function's name, useful for
      overloaded functions.
    """

    func_name = func.__name__
    if override_name is not None:
        func_name = override_name

    sig = signature(func)

    ret = f"{func_name}("

    mods = []

    arg_parts = []

    for name, param in sig.parameters.items():
        arg_ret = ""

        if param.kind is Parameter.VAR_KEYWORD:
            arg_ret += "**"
        elif param.kind is Parameter.VAR_POSITIONAL:
            arg_ret += "*"

        arg_ret += f"{name}"
        if param.annotation is not Parameter.empty:
            _mod, annot = parts_of_annotation(param.annotation)
            if _mod is not None:
                mods.append(_mod)
            arg_ret += f": {render_annotation(param.annotation)}"
        if param.default is not Parameter.empty:
            arg_ret += f"={param.default}"

        arg_parts.append(arg_ret)

    ret += ", ".join(arg_parts)

    _mod, annot = parts_of_annotation(sig.return_annotation)
    if _mod is not None:
        mods.append(_mod)
    ret += f") -> {render_annotation(sig.return_annotation)}"

    if withdoc:
        if func.__doc__ is not None:
            ret += "\n" + retab(doc_render(func), "\t")

        if len(mods) > 0:
            # Add a list of required modules to the doc string. Disabled for now because it includes
            # pre-installed ones as well. Need to filter them out.
            # ret += f"({', '.join(mods)} required)\n"
            pass
        else:
            pass
            # ret += "\n"

    return ret


def typechecks(obj, typ, globals):
    """
    Check whether a inspect.Parameter annotation is matched by the given object.
    A such an annotation can be empty in which case we return affirmative.
    """

    if typ is Parameter.empty:
        return True
    return annotation_isinstance(obj, typ, globals=globals)


def bind_relevant(m: Callable, kwargs) -> BoundArguments:
    """
    Create a binding for the given method `m` from the subset of args that are
    parameters to m. This means that other elements of kwargs that do not match
    the signature are ignored.
    """
    sig = signature(m)
    return sig.bind_partial(
        **{k: v for k, v in kwargs.items() if k in sig.parameters.keys()}
    )


def bind_relevant_and_call(m: Callable[..., T], kwargs) -> T:
    """
    Binding relevant arguments of `m` from `kwargs` and call it with them.
    Return whatever `m` returns.
    """

    bindings = bind_relevant(m, kwargs)

    return m(*bindings.args, **bindings.kwargs)


def sig_bind(
    sig: Signature,
    args: tuple,
    kwargs: dict,
    post_bind_handlers: Iterable[BindingsMap] = None,
    globals: dict = {}
) -> Optional(BoundArguments):
    """
    Given a signature `sig`, check whether it matches the given arguments in
    `args` and `kwargs` as if the user called a method with that signature with
    those args.

    `globals` is required to retrieve types from their names in case that
    __future__.annotations is enabled.

    If `post_bind_handlers` are provided, those functions can transform bindings
    AFTER signature is matched. 

    Returns the bound arguments object if successful or None otherwise.
    """

    post_bind_handlers = post_bind_handlers or []

    _typechecks = functools.partial(typechecks, globals=globals)

    sig = sig.replace()  # copy

    # Accumulate required positional args here.
    positional = []
    # Accumulate keyword bindings here.
    keyword = dict()

    # Will be emptying these out so make a copy first.
    args = list(args)  # list for popping
    kwargs = copy(kwargs)  # will be popping, don't want to affect the given one

    # Track whether signature has *args or **kwargs. This will determine whether
    # it is ok to have args or kwargs left over.
    had_varargs = False
    had_varkwargs = False

    for i, (name, param) in enumerate(sig.parameters.items()):
        typ = param.annotation

        default = param.default
        kind = param.kind

        if name in kwargs:
            # TODO: Should we check that parameter can be keyword?

            if _typechecks(kwargs[name], typ):
                keyword[name] = kwargs[name]
                del kwargs[name]

            # This is needed if we don't use our own Optional type:
            # elif default is not Parameter.empty and kwargs[name] is None:
            # Ok to provide None for an optional parameter, in which case
            # the dispatcher will just delete that argument before
            # dispatching.

            else:
                # A keyword argument's type did not match. This means signature
                # does not match so we return None to indicate that.
                # print(f"Could not match {name}:{typ} by {kwargs[name]}")
                return None

        elif (
            kind is Parameter.POSITIONAL_ONLY or
            kind is Parameter.POSITIONAL_OR_KEYWORD
        ) and len(args) > 0 and _typechecks(args[0], typ):
            # If no type is given or type matches, put it onto list of required positional args
            positional.append(args.pop(0))

            # Otherwise the type of a required positional arge does not
            # match but might match some keyword parameter's type. This will
            # be handled in the further case below.

        elif kind is Parameter.VAR_POSITIONAL:
            had_varargs = True

        elif kind is Parameter.VAR_KEYWORD:
            had_varkwargs = True

        else:
            # In this case a parameter's name was not in kwargs but there might
            # be a value of the right type in the remining positional values. So
            # we try to find it.

            vals_of_type = [
                (i, v)
                for i, v in enumerate(args)
                if annotation_isinstance(v, typ, globals=globals)
            ]

            if len(vals_of_type) == 1:
                i, v = vals_of_type[0]
                args.pop(i)

                if kind is Parameter.POSITIONAL_ONLY:
                    positional.append(v)

                elif kind is Parameter.KEYWORD_ONLY or kind is Parameter.POSITIONAL_OR_KEYWORD:
                    keyword[name] = v

                else:
                    raise RuntimeError(f"Unhandled annotation kind {kind}.")

            elif len(vals_of_type) > 1:
                raise ValueError(
                    f"Found more than 1 matching positional argument for {name}: {typ}"
                )

            elif default is not Parameter.empty:
                keyword[name] = default

            else:
                # did not match this parameter
                return None

    # Return failure if there were positional args left over but signature did not have a *args.
    if len(args) > 0 and not had_varargs:
        return None

    if len(kwargs) > 0:
        # Similarly for keyword args.
        if not had_varkwargs:
            return None

    bindings = sig.bind(*positional, *args, **keyword, **kwargs)
    bindings.apply_defaults()

    for handler in post_bind_handlers:
        bindings = handler(sig, bindings)

    return bindings


class Undispatch(Exception):
    """
    Throw this in an overloaded method to pretend like that method
    should not have been called, and continue looking for other matching methods.
    """
    pass


def sig_fill_defaults(sig: Signature, globals) -> Signature:
    """
    Replaces parameters that have annotation marked Optional but have no default
    value, to instead have a default None.
    """

    new_params = OrderedDict(sig.replace().parameters)

    for name, param in sig.parameters.items():
        annot = param.annotation

        default = param.default

        if default is not Parameter.empty:
            continue

        if annot is not Parameter.empty:
            annot_type = eval_type(annot, globals)
            if annotation_isinstance(annot_type, Optional, globals):
                new_param = param.replace(default=None)
                new_params[name] = new_param

    return sig.replace(parameters=new_params.values())


def overload(
    accumulate: Optional(Monoid) = None,
    pre_bind_handlers: Sequence[ArgsMap] = None,
    post_bind_handlers: Sequence[BindingsMap] = None,
    fill_defaults: bool = True
):
    """
    Decorator to specify a method to overload. Attaches several things to the
    returned method which are then used to define additional implementations, as
    well as replacing the method with a dispatching mechanism which selects from
    among the overloaded methods based on their signatures as compared to given
    arguments when called.

    If optional `accumulate` monoid is provided, all matching methods are called
    and their result is combined using the given monoid. Without the monoid,
    only the first matching method is called unless that call throws
    `Undispatch` in which case the next matching method is called.

    Functions specified in `post_bind_handlers` are called on the bound
    variables of matching overloaded functions before they are called and can
    change those bindings if needed (i.e. replace default values).

    Functions specified in `pre_bind_handlers` are called on args, kwargs before
    any matching is attempted.

    If `fill_defaults` is true, annotations subclassing `type_utils.Optional`
    will get their defaults set to `None` if not already set.

    Overloaded methods may call each other but you have to be careful to not go
    into an infinite call loop.

    Returns method with additional attributes:

    - register: the method used to add additional method definitions to
      overload.
    - options: the collection of methods overloaded.
    - render_options: method to render the collection of methods overloaded.
    """

    # Need to get caller's globals in case they provide type annotations via
    # module aliases like np for numpy. This only applies to delayed annotations
    # enabled with __future__.annotations .
    globals = caller_frame().f_globals

    class Dispatch(Callable):

        def __init__(self, firstf: Callable):
            assert isinstance(
                firstf, Callable
            ), f"Callable expected, got {type(firstf)} instead."

            # The list of overloaded signatures/methods including the first one.
            self.options = []

            # Keep track of the first method. Will be adjusting subsequence overloads with
            # this one's name and adding to this method's docstring.
            self.firstf = firstf

            # First method's name which will be replicated into all other registered
            # methods.
            self.firstname = firstf.__name__

            self.__name__ = self.firstname
            # Make all of the options show up under the same name, does not impact
            # being able to call them by their original name if needed

            # Adjust the dispatch's doc string to include, presently, just the first
            # method.

            self.is_method = False
            self.callable_type = "function"

            self.pre_bind_handlers = pre_bind_handlers or []
            self.post_bind_handlers = post_bind_handlers or []
            self.fill_defaults = fill_defaults

            if isinstance(firstf, MethodType):
                # Methods have a pre-bound first argument refering to instance
                # or class. TODO(piotrm): This does not work: whether this is a
                # method or function is not known at the time the containing
                # class is defined. Our own wrapper gets wrapped as a method
                # with bound self by the getattribute method of the class in
                # which we use overload.
                self.is_method = True
                self.callable_type = "method"

            # We must return from the decorator a function, not a method. At the
            # same time, we need to refer to self in said function. So we create
            # a function here that captures self from its scope instead of an
            # argument.

            def dispatch(*args, **kwargs):
                return self(*args, **kwargs)  # __call__

            dispatch.register = self.register
            dispatch.get_options_for = self.get_options_for
            dispatch.__name__ = self.firstname

            self.dispatch = dispatch

            self.register(firstf)

            self.__redoc()

        def __call__(self, *args, **kwargs):
            # The main functionality, the dispatch method replacing the firstf
            # decorated method determines which of the registered options to use
            # given the provided arguments.

            for handler in self.pre_bind_handlers:
                args, kwargs = handler(args=args, kwargs=kwargs)

            # Keep track of matching calls to print out an error message if they all fail.
            failed_calls = []

            # If monoid given, start with a zero.
            if accumulate is not None:
                ret = accumulate.zero()

            # Keep track if any signature matched the given args.
            matched = False

            # For each signature/method in order they were reigstered.
            for option_sig, option_func in self.options:

                try:
                    # Check if it matches the given args.
                    bindings = sig_bind(
                        option_sig,
                        post_bind_handlers=self.post_bind_handlers,
                        globals=globals,
                        args=args,
                        kwargs=kwargs
                    )
                except Exception as e:
                    failed_calls.append((option_func, e))
                    continue

                # Not None means it matched.
                if bindings is not None:
                    # print(f"matched {option_sig}")

                    # TODO: need some infinite recursion check here. The below doesn't quite work.
                    # Make sure we are not going in circles.
                    # st = inspect.stack()
                    # if st[2].function == "dispatch":
                    #    if st[1].frame == st[3].frame:
                    #        raise RuntimeError(
                    #            "Dispatched methods are calling themselves in circles."
                    #        )
                    #for f in inspect.stack():
                    #    print(f.function)
                    #    print(f.frame)

                    # Call the matched method, catching Undispatch
                    try:
                        next_ret = option_func(
                            *bindings.args, **bindings.kwargs
                        )
                    except Undispatch as e:
                        # If caught Undispatch, continue loop until another
                        # method matches.
                        failed_calls.append((
                            option_func,
                            e,
                        ))
                        continue
                    except Exception as e:
                        failed_calls.append((option_func, e))
                        continue
                    else:
                        # Otherwise after a successful call,

                        if accumulate is not None:
                            # Accumulate its result if monoid was provided.
                            ret = accumulate.plus(ret, next_ret)
                        else:
                            # Or return it if no monoid was provided.
                            return next_ret

                    # Only happens in accumulator mode, make note that some
                    # method matched.
                    matched = True

                else:
                    # Signature did not match.
                    pass

            # Return the accumulated results in accumulation mode.
            if matched:
                return ret

            # Otherwise construct an error message that includes all of the
            # registered options.
            message = f"No remaining matching definitions for {self.firstname} found. Given arguments:\n\n"

            message += retab(render_args_kwargs(args, kwargs), tab="\t") + "\n"

            if len(failed_calls) > 0:
                message += "Failed calls:\n\n"
                for func, exc in failed_calls:
                    message += retab(
                        render_sig(
                            func, withdoc=True, override_name=self.firstname
                        ), "\t"
                    ) + "\n\n"
                    message += retab(
                        "FAILURE: " +
                        retab(render_exception(exc), "\t", tab_first=False),
                        "\t"
                    ) + "\n\n"

                message += "\n\n"

            message += "Options are:\n\n"
            message += retab(self.render_options(), "\t")

            raise TypeError(message)

        def get_options_for(self, *args, **kwargs):
            for option_sig, option_func in self.options:

                # Check if it matches the given args.
                try:
                    bindings = sig_bind(
                        option_sig,
                        globals=globals,
                        args=(self,) + args,
                        kwargs=kwargs
                    )

                    if bindings is not None:
                        yield option_func

                except:
                    pass

        def render_options(self) -> str:
            """
            Create a string listing all the registered signatures.
            """

            message = ""
            for _, func in self.options:
                # Override the name of the method in the signature so that all
                # listed methods appear to have the same name as the first
                # overloaded method.
                message += render_sig(func, override_name=self.firstname)
                message += "\n\n"

            return message

        def register(self, f: Callable) -> Callable:
            """
            Decorator to add a new method to the list of overloaded options for
            the originally decorated method. Returns the registered method as
            is. You can use this to name overloaded methods different things and
            call them explicitly outside of the dispatch mechanism, while still
            using the mechanism for calls to the first registered method.
            """

            sig = signature(f)

            if self.fill_defaults:
                sig = sig_fill_defaults(sig, globals)

            self.options.append((sig, f))
            self.__redoc()

            # Note that we are not returning the dispatch here but instead the
            # function being registered in the dispatch. This lets us to refer
            # to it specifically by whatever name it was defined with when
            # decorated without going through the dispatch if we need to.

            return f

        def __redoc(self):
            # Update the docstring of the wrapper of the first function
            # decorated with overload (the one the user gets a handle on).
            self.dispatch.__doc__ = (
                f"Overloaded {self.callable_type}, options are:\n\n" +
                retab(self.render_options(), tab="\t")
            )

    def wrapper(firstf):
        d = Dispatch(firstf)

        # We return a function, not a method, not an instance. The function comes with
        # various "sub-functions" like register to add more options to the overload.
        return d.dispatch

    return wrapper

    # End of def overload(...)
