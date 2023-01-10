from typing import Optional, Union
from xmltodict import parse as xml_parse, unparse as xml_unparse
from xml.dom.minidom import parse, parseString
from xml.dom import minidom


def read_xml_dict(path: str, encoding: Optional[str] = None) -> dict:
    return xml_parse(open(path, 'r', encoding=encoding).read())


def read_xml_node(path: str):
    return parse(path)


def create_xml_document() -> minidom.Document:
    return minidom.Document()


def create_xml_node(xml_dom, parent, name: Optional[str] = None, value: Optional[str] = None, properties: dict = {}):
    child_node = xml_dom.createElement(name)
    if value is not None:
        value_node = xml_dom.createTextNode(str(value))
        child_node.appendChild(value_node)
    for k, v in properties.items():
        child_node.setAttribute(k, str(v))
    if parent is None:
        xml_dom.appendChild(child_node)
    else:
        parent.appendChild(child_node)
    return child_node


def del_xml_node(parent, name):
    elements = parent.getElementsByTagName(name)
    for element in elements:
        parent.removeChild(element)


def get_xml_root_node(xml_dom):
    return xml_dom.documentElement


def get_xml_child_nodes(parent):
    return parent.childNodes


def get_xml_nodes(parent, name):
    return parent.getElementsByTagName(name)


def set_xml_node_attribute(node, name: Optional[str] = None, value: Optional[str] = None):
    node.setAttribute(name, value)


def has_xml_node_attribute(node, name: str):
    return node.hasAttribute(name)


def get_xml_node_attribute(node, name: str):
    if has_xml_node_attribute(node, name):
        return node.getAttribute(name)
    return None


def get_xml_node_attributes(node) -> dict:
    attributes = {}
    names = list(node.attributes.keys())
    for name in names:
        attributes[name] = get_xml_node_attribute(node, name)
    return attributes


def remove_xml_node_attribute(node, name: str):
    if has_xml_node_attribute(node, name):
        return node.removeAttribute(name)


def save_xml_node(path: str, xml_dom, encoding: Optional[str] = None, newl: Optional[str] = '', indent: Optional[str] = '', addindent: Optional[str] = ''):
    with open(path, 'w', encoding=encoding) as f:
        xml_dom.writexml(f, encoding=encoding, newl=newl, indent=indent, addindent=addindent)


def xml_node_to_str(node, encoding: Optional[str] = None) -> str:
    return node.toxml() if encoding is None else node.toxml(encoding=encoding).decode()


def xml_str_to_dict(value: str) -> dict:
    return xml_parse(value)


def xml_node_to_dict(node, encoding: Optional[str] = None):
    return xml_str_to_dict(xml_node_to_str(node, encoding=encoding))


def value_to_xml(value: Union[str, bytes, dict]):
    if isinstance(value, bytes):
        value = value.decode()
    elif isinstance(value, dict):
        value = xml_unparse(value, pretty=True)
    return parseString(value)


def value_to_xml_str(value: Union[str, bytes, dict], encoding: Optional[str] = None) -> str:
    return xml_node_to_str(value_to_xml(value), encoding)
