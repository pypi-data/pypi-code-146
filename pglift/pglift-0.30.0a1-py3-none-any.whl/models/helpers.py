import enum
import functools
import inspect
import logging
import typing
from abc import ABC, abstractmethod
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime
from typing import (
    Any,
    Callable,
    ClassVar,
    Dict,
    Iterator,
    List,
    Literal,
    Mapping,
    Sequence,
    Tuple,
    Type,
    TypeVar,
    Union,
)

import click
import pydantic
from pydantic.utils import deep_update, lenient_issubclass

from ..types import AnsibleArgSpec, Port, StrEnum

Callback = Callable[..., Any]
ClickDecorator = Callable[[Callback], Callback]
ModelType = Type[pydantic.BaseModel]
T = TypeVar("T", bound=pydantic.BaseModel)
Operation = Literal["create", "update"]

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class ParamSpec(ABC):
    """Intermediate representation for a future click.Parameter."""

    param_decls: Sequence[str]
    attrs: Dict[str, Any]
    loc: Tuple[str, ...]

    objtype: ClassVar = click.Parameter

    @property
    @abstractmethod
    def decorator(self) -> ClickDecorator:
        """The click decorator for this parameter."""

    def match_loc(self, loc: Tuple[Union[str, int], ...]) -> bool:
        """Return True if this parameter spec matches a 'loc' tuple (from
        pydantic.ValidationError).
        """
        return self.loc == loc

    def badparameter_exception(self, message: str) -> click.BadParameter:
        return click.BadParameter(
            message, None, param=self.objtype(self.param_decls, **self.attrs)
        )


class ArgumentSpec(ParamSpec):
    """Intermediate representation for a future click.Argument."""

    objtype: ClassVar = click.Argument

    def __post_init__(self) -> None:
        assert (
            len(self.param_decls) == 1
        ), f"expecting exactly one parameter declaration: {self.param_decls}"

    @property
    def decorator(self) -> ClickDecorator:
        return click.argument(*self.param_decls, **self.attrs)


class OptionSpec(ParamSpec):
    """Intermediate representation for a future click.Option."""

    objtype: ClassVar = click.Option

    @property
    def decorator(self) -> ClickDecorator:
        return click.option(*self.param_decls, **self.attrs)


def unnest(model_type: Type[T], params: Dict[str, Any]) -> Dict[str, Any]:
    obj: Dict[str, Any] = {}
    known_fields = {(f.alias or f.name): f for f in model_type.__fields__.values()}
    for k, v in params.items():
        if v is None:
            continue
        if k in known_fields:
            obj[k] = v
        elif "_" in k:
            p, subk = k.split("_", 1)
            try:
                field = known_fields[p]
            except KeyError:
                raise ValueError(k)
            nested = unnest(field.type_, {subk: v})
            obj[p] = deep_update(obj.get(p, {}), nested)
        else:
            raise ValueError(k)
    return obj


def parse_params_as(model_type: Type[T], params: Dict[str, Any]) -> T:
    obj = unnest(model_type, params)
    return model_type.parse_obj(obj)


DEFAULT = object()


def choices_from_enum(e: Type[enum.Enum]) -> List[Any]:
    if lenient_issubclass(e, StrEnum):
        return list(e)
    else:
        return [v.value for v in e]


@dataclass(frozen=True)
class _Parent:
    argname: str
    required: bool


def _paramspecs_from_model(
    model_type: ModelType,
    operation: Operation,
    *,
    _parents: Tuple[_Parent, ...] = (),
) -> Iterator[Tuple[Tuple[str, str], ParamSpec]]:
    """Yield parameter declarations for click corresponding to fields of a
    pydantic model type.
    """

    def default(ctx: click.Context, param: click.Argument, value: Any) -> Any:
        if (param.multiple and value == ()) or (value == param.default):
            return DEFAULT
        return value

    model_cli_config = getattr(model_type, "_cli_config", {})

    for field in model_type.__fields__.values():
        if field.field_info.const:
            continue
        cli_config = model_cli_config.get(field.name, {})
        if cli_config.get("hide", False):
            continue
        argname = cli_config.get("name", field.alias)
        if operation == "update" and field.field_info.extra.get("readOnly"):
            continue
        modelname = field.alias
        ftype = field.outer_type_
        nested = lenient_issubclass(ftype, pydantic.BaseModel)
        assert isinstance(
            field.required, bool  # ModelField.required defaults to Undefined.
        ), f"expecting a boolean for {field}.required"
        required = field.required
        if not nested and not _parents and required:
            yield (modelname, argname), ArgumentSpec(
                (argname.replace("_", "-"),), {"type": ftype}, loc=(modelname,)
            )
        else:
            metavar = argname.upper()
            argparts = tuple(p.argname for p in _parents) + tuple(argname.split("_"))
            fname = f"--{'-'.join(argparts)}"
            description = None
            if field.field_info.description:
                description = field.field_info.description
                description = description[0].upper() + description[1:]
            attrs: Dict[str, Any] = {}
            origin_type = typing.get_origin(field.outer_type_)
            if lenient_issubclass(ftype, enum.Enum):
                try:
                    choices = cli_config["choices"]
                except KeyError:
                    choices = choices_from_enum(ftype)
                attrs["type"] = click.Choice(choices)
            elif nested:
                yield from _paramspecs_from_model(
                    ftype, operation, _parents=_parents + (_Parent(argname, required),)
                )
                continue
            elif origin_type is not None and lenient_issubclass(origin_type, list):
                if operation != "create":
                    continue
                attrs["multiple"] = True
                try:
                    (itemtype,) = ftype.__args__
                except ValueError:
                    pass
                else:
                    if lenient_issubclass(itemtype, enum.Enum):
                        attrs["type"] = click.Choice(choices_from_enum(itemtype))
                    else:
                        attrs["metavar"] = metavar
            elif lenient_issubclass(ftype, pydantic.SecretStr):
                attrs["prompt"] = (
                    description.rstrip(".") if description is not None else True
                )
                attrs["prompt_required"] = False
                attrs["confirmation_prompt"] = True
                attrs["hide_input"] = True
            elif lenient_issubclass(ftype, bool):
                fname = f"{fname}/--no-{fname[2:]}"
                # Use None to distinguish unspecified option from the default value.
                attrs["default"] = None
            else:
                attrs["metavar"] = metavar
            if description is not None:
                if description[-1] not in ".?":
                    description += "."
                attrs["help"] = description
            if field.required and all(p.required for p in _parents):
                attrs["required"] = True
            argname = "_".join(argparts)
            loc = tuple(p.argname for p in _parents) + (modelname,)
            modelname = "_".join(loc)
            yield (modelname, argname), OptionSpec(
                (fname,), {"callback": default, **attrs}, loc=loc
            )


def parameters_from_model(
    model_type: ModelType, operation: Operation, *, parse_model: bool = True
) -> ClickDecorator:
    """Attach click parameters (arguments or options) built from a pydantic
    model to the command.

    >>> class Obj(pydantic.BaseModel):
    ...     message: str
    ...     ignored: int = pydantic.Field(default=0, readOnly=True)

    >>> import click

    >>> @click.command("echo")
    ... @parameters_from_model(Obj, "update")
    ... @click.option("--caps", is_flag=True, default=False)
    ... @click.pass_context
    ... def cmd(ctx, obj, caps):
    ...     output = obj.message
    ...     if caps:
    ...         output = output.upper()
    ...     click.echo(output)

    The argument in callback function must match the base name (lower-case) of
    the pydantic model class. In the example above, this is named "obj".
    Otherwise, a TypeError is raised.

    >>> from click.testing import CliRunner
    >>> runner = CliRunner()
    >>> r = runner.invoke(cmd, ["hello, world"])
    >>> print(r.stdout.strip())
    hello, world
    >>> r = runner.invoke(cmd, ["hello, world", "--caps"])
    >>> print(r.stdout.strip())
    HELLO, WORLD
    """

    def decorator(f: Callback) -> Callback:

        modelnames_and_argnames, paramspecs = zip(
            *reversed(list(_paramspecs_from_model(model_type, operation)))
        )

        def params_to_modelargs(kwargs: Dict[str, Any]) -> Dict[str, Any]:
            args = {}
            for modelname, argname in modelnames_and_argnames:
                value = kwargs.pop(argname)
                if value is DEFAULT:
                    continue
                args[modelname] = value
            return args

        if parse_model:
            s = inspect.signature(f)
            model_argname = model_type.__name__.lower()
            try:
                model_param = s.parameters[model_argname]
            except KeyError:
                raise TypeError(
                    f"expecting a '{model_argname}: {model_type.__name__}' parameter in '{f.__name__}{s}'"
                )
            if model_param.annotation not in (
                model_type,
                inspect.Signature.empty,
            ) and not issubclass(model_type, model_param.annotation):
                raise TypeError(
                    f"expecting a '{model_argname}: {model_type.__name__}' parameter in '{f.__name__}{s}'; got {model_param.annotation}"
                )

            @functools.wraps(f)
            def callback(**kwargs: Any) -> Any:
                args = params_to_modelargs(kwargs)
                with catch_validationerror(*paramspecs):
                    model = parse_params_as(model_type, args)
                kwargs[model_argname] = model
                return f(**kwargs)

        else:

            @functools.wraps(f)
            def callback(**kwargs: Any) -> Any:
                args = params_to_modelargs(kwargs)
                values = unnest(model_type, args)
                kwargs.update(values)
                with catch_validationerror(*paramspecs):
                    return f(**kwargs)

        cb = callback
        for p in paramspecs:
            cb = p.decorator(cb)
        return cb

    return decorator


@contextmanager
def catch_validationerror(*paramspec: ParamSpec) -> Iterator[None]:
    try:
        yield None
    except pydantic.ValidationError as e:
        errors = e.errors()
        for pspec in paramspec:
            for err in errors:
                if pspec.match_loc(err["loc"]):
                    raise pspec.badparameter_exception(err["msg"]) from None
        logger.debug("a validation error occurred", exc_info=True)
        raise click.ClickException(str(e))


PYDANTIC2ANSIBLE: Mapping[Union[Type[Any], str], AnsibleArgSpec] = {
    bool: {"type": "bool"},
    float: {"type": "float"},
    Port: {"type": "int"},
    int: {"type": "int"},
    str: {"type": "str"},
    pydantic.SecretStr: {"type": "str", "no_log": True},
    datetime: {"type": "str"},
}


def argspec_from_model(model_type: ModelType) -> Dict[str, AnsibleArgSpec]:
    """Return the Ansible module argument spec object corresponding to a
    pydantic model class.
    """
    spec = {}
    model_config = getattr(model_type, "_ansible_config", {})

    def description_list(value: str) -> List[str]:
        return list(filter(None, (s.strip() for s in value.split("."))))

    for field in model_type.__fields__.values():
        ftype = field.outer_type_

        ansible_config = model_config.get(field.name, {})
        if ansible_config.get("hide", False):
            continue
        origin_type = typing.get_origin(ftype)
        is_model = lenient_issubclass(ftype, pydantic.BaseModel)
        is_enum = lenient_issubclass(ftype, enum.Enum)
        is_list = is_dict = False
        if origin_type is not None:
            is_list = lenient_issubclass(origin_type, list)
            is_dict = lenient_issubclass(origin_type, dict)
        try:
            arg_spec: AnsibleArgSpec = ansible_config["spec"]
        except KeyError:
            arg_spec = AnsibleArgSpec()
            try:
                arg_spec.update(PYDANTIC2ANSIBLE[ftype])
            except KeyError:
                if is_model:
                    arg_spec = {
                        "type": "dict",
                        "options": argspec_from_model(ftype),
                        "description": description_list(
                            field.field_info.description or field.name
                        ),
                    }
                elif is_enum:
                    arg_spec["choices"] = ansible_config.get(
                        "choices", [f.value for f in ftype]
                    )
                elif is_list:
                    arg_spec["type"] = "list"
                    sub_type = typing.get_args(ftype)[0]
                    if issubclass(sub_type, pydantic.BaseModel):
                        arg_spec["elements"] = "dict"
                        arg_spec["options"] = argspec_from_model(sub_type)
                    elif issubclass(sub_type, StrEnum):
                        arg_spec["elements"] = "str"
                    else:
                        arg_spec["elements"] = sub_type.__name__
                elif is_dict:
                    arg_spec["type"] = "dict"
                elif lenient_issubclass(ftype, str):
                    arg_spec["type"] = "str"

        if field.required:
            arg_spec.setdefault("required", True)

        if field.default is not None:
            default = field.default
            if is_model:
                default = default.dict(by_alias=True)
            elif is_enum:
                default = default.value
            elif lenient_issubclass(ftype, Port):
                default = int(default)
            arg_spec.setdefault("default", default)

        if field.field_info.description:
            arg_spec.setdefault(
                "description", description_list(field.field_info.description)
            )
        spec[field.alias] = arg_spec

    return spec
