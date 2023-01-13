# Copyright (c) 2022-2023 Mario S. Könz; License: MIT
import typing as tp

__all__ = ["public_name"]


def public_name(cls: tp.Type[tp.Any], without_cls: bool = False) -> str:
    parts = []
    for part in cls.__module__.split("."):
        if part.startswith("_"):
            continue
        parts.append(part)

    public_module = "main"
    if parts:
        public_module = ".".join(parts)

    if without_cls:
        return f"{public_module}"
    return f"{public_module}.{cls.__name__}"
