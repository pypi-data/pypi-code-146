# FlexiRPG -- XML utilities
#
# Copyright (C) 2000-2001 The OpenRPG Project
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

import xml.dom
import traceback
import sys

def toxml(root,pretty=0):
    if pretty:
        return root.toprettyxml(indent='  ')
    else:
        return root.toxml()

def _strip_text_nodes(node):
    child = node.firstChild
    while child:
        next_child = child.nextSibling
        if child.nodeType == xml.dom.Node.TEXT_NODE:
            child.data = child.data.strip()
            if child.data == "":
                node.removeChild(child)
        else:
            _strip_text_nodes(child)
        child = next_child

def _parse_xml(parse_func, parse_param):
    try:
        doc = parse_func(parse_param)
        doc.normalize()
        _strip_text_nodes(doc)
        return doc
    except Exception as e:
        traceback.print_exc(file=sys.stdout)
        return None

def parseXml(s):
    return _parse_xml(xml.dom.minidom.parseString, s.encode('utf-8'))

def parse_file(filename):
    return _parse_xml(xml.dom.minidom.parse, filename)

def safe_get_text_node(xml_dom):
    """ returns the child text node or creates one if doesnt exist """
    t_node = xml_dom.firstChild
    if t_node == None:
        doc = xml_dom
        while doc.nodeType != xml.dom.Node.DOCUMENT_NODE:
            doc = doc.parentNode
        t_node = doc.createTextNode("")
        t_node = xml_dom.appendChild(t_node)
    return t_node

def bool_attrib(xml_dom, attrib_name, default_if_missing):
    """Get an XML attribute as a bool.

    Returns:
       The XML attribute converted to a bool, or 'default_if_missing'
       if the attribute does not exist.
    """
    if xml_dom.hasAttribute(attrib_name):
        attrib = xml_dom.getAttribute(attrib_name)
        return attrib.lower() == "true" or attrib == "1"
    else:
        return default_if_missing


def str_attrib(xml_dom, attrib_name, default_if_missing):
    """Get an XML attribute as a string.

    Returns:
      The XML attribute, or 'default_if_missing' if the attribute does
      not exist.
    """
    if xml_dom.hasAttribute(attrib_name):
        return xml_dom.getAttribute(attrib_name)
    else:
        return default_if_missing

def int_attrib(xml_dom, attrib_name, default_if_missing):
    """Get an XML attribute as an int.

    Returns:
      The XML attribute, or 'default_if_missing' if the attribute does
      not exist.
    """
    if xml_dom.hasAttribute(attrib_name):
        try:
            return int(xml_dom.getAttribute(attrib_name))
        except ValueError:
            pass
    return default_if_missing

def float_attrib(xml_dom, attrib_name, default_if_missing):
    """Get an XML attribute as a float.

    Returns:
      The XML attribute, or 'default_if_missing' if the attribute does
      not exist.
    """
    if xml_dom.hasAttribute(attrib_name):
        try:
            return float(xml_dom.getAttribute(attrib_name))
        except ValueError:
            pass
    return default_if_missing
