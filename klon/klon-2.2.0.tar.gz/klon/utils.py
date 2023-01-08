#!/usr/bin/env python3

# standards
from typing import Any, Type, Union, no_type_check, overload

# 3rd parties
import lxml.etree as ET


Element = Union[ET._Element]  # this is exported, and can be used for type annotations


@no_type_check  # until lxml-stubs improves
def detach(node: Element, *, reattach_tail: bool = True) -> Element:
    parent = node.getparent()
    if parent is None:
        raise Exception('Node has no parent')
    if reattach_tail and node.tail:
        prev = node.getprevious()
        if prev is not None:
            prev.tail = (prev.tail + node.tail) if prev.tail else node.tail
        else:
            parent.text = (parent.text + node.tail) if parent.text else node.tail
    parent.remove(node)
    return node


def is_element(obj: Any) -> bool:
    return isinstance(obj, ET._Element)


@overload
def tostring(etree: Union[Element, ET._ElementUnicodeResult], encoding: Type[str] = str, **kwargs) -> str:
    ...
@overload
def tostring(etree: Union[Element, ET._ElementUnicodeResult], encoding: str, **kwargs) -> bytes:
    ...
def tostring(etree, encoding=str, **kwargs):
    if isinstance(etree, ET._ElementUnicodeResult):
        text = str(etree)
        if encoding is not str:
            return text.encode(encoding)
        return text
    return ET.tostring(etree, encoding=encoding, **kwargs).strip()
