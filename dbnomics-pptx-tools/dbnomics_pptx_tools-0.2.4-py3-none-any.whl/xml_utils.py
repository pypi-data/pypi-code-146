from lxml.etree import _Element


def remove_element(element: _Element) -> None:
    element.getparent().remove(element)
