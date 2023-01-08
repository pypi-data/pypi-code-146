# coding: utf-8
from copy import copy

from .elements import BaseElement, AnonymusElement
from .exceptions import ElementNameConflict


class ElementRegistry:
    def __init__(self):
        self.xml_to_object_mapper = {}
        self.anonymus_element_klass = AnonymusElement

    def element(self, name=None, element_class=None, namespace=None):
        if namespace:
            fqdn = '{' + namespace + '}' + name
        else:
            fqdn = name

        if name is not None and fqdn in self.xml_to_object_mapper.keys():
            raise ElementNameConflict(element_class.__name__)

        if name is None and element_class is None:
            # @registry.tag()
            return self.element_function
        elif name is not None and element_class is None:
            if callable(name):
                # @registry.tag
                return self.element_function(name)
            else:
                # @registry.tag('somename') or @registry.tag(name='somename')
                def dec(func):
                    return self.element(fqdn, func, namespace=None)
                return dec
        elif name is not None and element_class is not None:
            self.xml_to_object_mapper[fqdn] = element_class
            return element_class

    def element_function(self, element_class):
        self.xml_to_object_mapper[element_class.__name__] = element_class
        return element_class

    def get_class_by_name(self, element_name: str) -> type:
        if element_name not in self.xml_to_object_mapper.keys():
            return BaseElement

        return self.xml_to_object_mapper[element_name]

    def __copy__(self):
        other = ElementRegistry()
        other.xml_to_object_mapper = copy(self.xml_to_object_mapper)

        return other


registry = ElementRegistry()
