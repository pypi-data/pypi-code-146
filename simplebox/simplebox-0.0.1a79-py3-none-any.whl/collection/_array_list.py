#!/usr/bin/env python
# -*- coding:utf-8 -*-
from ._abstractlist import _AbstractList, _T, Iterable


class ArrayList(_AbstractList[_T]):
    """
    A superset of list, which mainly adds streaming operations
    """
    def __init__(self, *args: _T, iterable: Iterable[_T] = None):
        super().__init__(*args, iterable=iterable)


__all__ = [ArrayList]
