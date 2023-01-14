# -*- coding: utf-8; -*-
"""Singleton objects marking the place of an ID wherever necessary.

For example one can reprensent a docker command, that would require a
container ID like this::

    ['docker', 'exec', '-ti', ContainerID, '--', 'bash', '-c', 'script.sh']

The following placeholders are defined:

- ContainerID
- ImageID


Note: you should not need to create new placeholders. You must use the
one provided.
"""
from typing import Dict


__all__ = ['ContainerID', 'ImageID']


class _Placeholder:
    """Class to create placeholders

    Many commands are parameterized by some ID (image ID, container
    ID, ...)  We use this class create singleton objects that mark the
    place of such ID;

    """
    __slots__ = ('__name',
                 )
    __EXISTING_PLACEHOLDERS: Dict[str, '_Placeholder'] = {}

    def __init__(self, name: str) -> None:
        """
        """
        self.__name = name

    def __new__(cls, name: str) -> '_Placeholder':
        if name in cls.__EXISTING_PLACEHOLDERS:
            return cls.__EXISTING_PLACEHOLDERS[name]
        placeholder = super().__new__(type(name + 'Type', (_Placeholder, ), {'__name': name}))
        cls.__EXISTING_PLACEHOLDERS[name] = placeholder
        return placeholder

    def __repr__(self):
        return '{}.{}'.format(__name__, self.__name)

    def __str__(self):
        return self.__name


ContainerID = _Placeholder('ContainerID')  # pylint: disable=invalid-name
ContainerIDType = type(ContainerID)
ImageID = _Placeholder('ImageID')  # pylint: disable=invalid-name
ImageIDType = type(ImageID)


# vim: et:sw=4:syntax=python:ts=4:
