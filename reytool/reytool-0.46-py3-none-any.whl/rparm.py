# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    : 2022-12-05 14:10:42
@Author  : Rey
@Contact : reyxbo@163.com
@Explain : Rey's parameters directory type
"""


from typing import Any, Tuple, Dict, Iterable, Iterator, Literal, Optional, Union
from .rbasic import is_iterable


class RParm(object):
    """
    Rey's parameters directory type.

    Methods
    -------
    attribute : parms, default
    syntax : [index | slice], for, in/ not in
    enter parameter : len
    symbol : +(l/ r), -(l/ r), &(l/ r), +=, -=, &=
    function : items, keys, values, get, pop
    """
    
    def __init__(self, *parms: Dict, default: Union[Any, Literal["error"]] = "error") -> None:
        """
        Set parameters directory attribute.

        Parameters
        ----------
        *parms : Parameters

        default : Default method when index fails.
            - Any : Return this value.
            - Literal['error'] : Throw error.
        """

        parms = {}
        for parm in parms:
            parms.update(parm)
        self.parms = parms
        self.default = default
    
    def __call__(self, *keys: Any) -> Any:
        """
        Indexes key value pair.
        """

        if keys == ():
            ret = self.parms
        else:
            ret = {key: self.parms[key] for key in keys}
        return ret

    def __getattr__(self, key: Any) -> Any:
        """
        Index value.
        """

        value = self.parms[key]
        return value

    def __getitem__(self, indexes: Union[Any, Tuple]) -> Any:
        """
        Batch indexing directory values.
        """

        if type(indexes) == tuple:
            if self.default == "error":
                vals = [self.parms[key] for key in indexes]
            else:
                vals = [self.parms.get(key, self.default) for key in indexes]
        else:
            if self.default == "error":
                vals = self.parms[indexes]
            else:
                vals = self.parms.get(indexes, self.default)
        return vals

    def __setitem__(self, key: Any, value: Any) -> None:
        """
        Create or modify key value pair.
        """

        self.parms[key] = value
    
    def __iter__(self) -> Iterator:
        """
        Return iterable directory keys.
        """

        return self.keys

    def __contains__(self, key: Any) -> bool:
        """
        Judge contain.
        """

        judge = key in self.parms
        return judge

    def __len__(self) -> int:
        """
        Return parameters directory length.
        """
        return self.len

    def __add__(self, parms: Dict) -> Dict:
        """
        Union directory.
        """

        if is_iterable(parms, [str, bytes, dict]):
            parms = {key: val for parm in parms for key, val in parm.items()}
        parms = {**self.parms, **parms}
        return parms
    
    def __radd__(self, parms: Dict) -> Dict:
        """
        Union directory right.
        """

        if is_iterable(parms, [str, bytes, dict]):
            parms = {key: val for parm in parms for key, val in parm.items()}
        parms = {**parms, **self.parms}
        return parms

    def __iadd__(self, parms: Dict) -> Any:
        """
        Union directory and definition.
        """

        if is_iterable(parms, [str, bytes, dict]):
            parms = {key: val for parm in parms for key, val in parm.items()}
        parms = {**self.parms, **parms}
        self.parms = parms
        return self

    def __sub__(self, parms: Iterable) -> Dict:
        """
        Difference directory.
        """
        
        main_set = set(self.parms)
        sub_set = set(parms)
        diff_set = main_set - sub_set
        parms = {key: self.parms[key] for key in diff_set}
        return parms

    def __rsub__(self, parms: Dict) -> Dict:
        """
        Difference directory right.
        """

        main_set = set(parms)
        sub_set = set(self.parms)
        diff_set = main_set - sub_set
        parms = {key: parms[key] for key in diff_set}
        return parms

    def __isub__(self, parms: Dict) -> Any:
        """
        Difference directory and definition.
        """

        main_set = set(self.parms)
        sub_set = set(parms)
        diff_set = main_set - sub_set
        parms = {key: self.parms[key] for key in diff_set}
        self.parms = parms
        return self

    def __and__(self, parms: Dict) -> Dict:
        """
        Intersection directory.
        """

        if is_iterable(parms, [str, bytes, dict]):
            parms = {key: val for parm in parms for key, val in parm.items()}
        main_set = set(self.parms)
        sub_set = set(parms)
        inte_set = main_set & sub_set
        parms = {key: self.parms[key] for key in inte_set}
        return parms

    def __rand__(self, parms: Dict) -> Dict:
        """
        Intersection directory right.
        """

        if is_iterable(parms, [str, bytes, dict]):
            parms = {key: val for parm in parms for key, val in parm.items()}
        main_set = set(parms)
        sub_set = set(self.parms)
        inte_set = main_set & sub_set
        parms = {key: parms[key] for key in inte_set}
        return parms

    def __iand__(self, parms: Dict) -> Dict:
        """
        Intersection directory and definition.
        """

        if is_iterable(parms, [str, bytes, dict]):
            parms = {key: val for parm in parms for key, val in parm.items()}
        main_set = set(self.parms)
        sub_set = set(parms)
        inte_set = main_set & sub_set
        parms = {key: self.parms[key] for key in inte_set}
        self.parms = parms
        return self

    def items(self) -> Iterator:
        """
        Get directory all keys and values.
        """

        items = self.parms.items()
        return items

    def keys(self) -> Iterator:
        """
        Get directory all keys.
        """

        keys = self.parms.keys()
        return keys

    def values(self) -> Iterator:
        """
        Get directory all values.
        """

        values = self.parms.values()
        return values

    def get(self, keys: Union[Any, Iterable], default: Optional[Any] = None) -> Dict:
        """
        Batch get directory values.
        """

        if default == None and self.default != "error":
            default = self.default
        if is_iterable(keys):
            vals = [self.parms.get(key, default) for key in keys]
        else:
            vals = self.parms.get(keys, default)
        return vals

    def pop(self, keys: Union[Any, Iterable], default: Optional[Any] = None) -> Dict:
        """
        Batch pop directory values.
        """

        if default == None and self.default != "error":
            default = self.default
        if is_iterable(keys):
            vals = [self.parms.pop(key, default) for key in keys]
        else:
            vals = self.parms.pop(keys, default)
        return vals