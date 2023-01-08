from contextlib import contextmanager
from io import StringIO
from typing import List
from xml.sax.xmlreader import AttributesNSImpl

from . import constants
from .expressions import Bind, Condition, ForLoop, Expression
from .render import RenderedElement


class BaseElement:
    def __init__(self, xml_tag: str, xml_attrs: AttributesNSImpl):
        self.xml_tag = xml_tag

        self.xml_attrs = self._parse_xml_attrs(xml_attrs)
        self.parent = None
        self.children = []  # type: List[BaseElement]

    def _parse_xml_attrs(self, xml_attrs: AttributesNSImpl):
        attrs = {}
        for (namespace, attr_name), attr_value in xml_attrs.items():
            if namespace is None:
                attrs[attr_name] = attr_value
            else:
                key = ''.join(f'{{{n}}}' for n in namespace) + attr_name
                if constants.XML_NAMESPACE_DATA_BINDING in namespace:
                    value = Bind(expr=attr_value)
                elif namespace == (constants.XML_NAMESPACE_POJO,):
                    value = Bind(expr=attr_value)
                elif namespace == (constants.XML_NAMESPACE_FLOW_CONTROL,):
                    if attr_name == 'if':
                        value = Condition(expr=attr_value)
                    elif attr_name == 'for':
                        value = ForLoop(expr=attr_value)
                    else:
                        raise ValueError  # TODO: raise custom error
                else:
                    value = attr_value

                attrs[key] = value

        return attrs

    def add_child(self, element: 'BaseElement'):
        element.parent = self
        self.children.append(element)

    def build_rendering_tree(self, indent=1):
        yield self, indent
        for child in self.children:
            child.build_rendering_tree(indent=indent + 1)

    @property
    def attrs_as_xml(self) -> str:
        retval = ''
        for k, v in self.xml_attrs.items():
            if isinstance(v, Expression):
                v = v.expr

            k = k.replace(f'{{{constants.XML_NAMESPACE_DATA_BINDING}}}', 'b:')
            k = k.replace(f'{{{constants.XML_NAMESPACE_FLOW_CONTROL}}}', 'c:')
            retval += f' {k}="{v}"'

        return retval

    def render(self, context):
        klass = getattr(self, 'RENDERED_ELEMENT_CLASS', RenderedElement)
        return klass(self, context)


class AnonymusElement:
    def __init__(self, text):
        self.text = text
        self.xml_tag = None
        self.children = []
