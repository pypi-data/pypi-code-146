#!/usr/bin/env python
# -*- coding: utf-8 -*-

#----------------------------------------------------------------------------------------------------------------------------------
# includes

# 2+3 compat
from __future__ import absolute_import, division, print_function, unicode_literals

# standards
import re
import xml.etree.ElementTree

# klon
from klon.compatibility import text_type

#----------------------------------------------------------------------------------------------------------------------------------

class Klon:

    @classmethod
    def build_etree(cls, tag, *args):
        if not isinstance(tag, text_type):
            raise ValueError('Tag must be a %s, got %r' % (text_type.__name__, tag))
        attrib, args = cls._compile_attrib(*args)
        tag, attrib = cls._parse_css_style_tags(tag, attrib)
        element = cls._create_element(tag, attrib)
        cls._append_children(element, args)
        return element

    @classmethod
    def _compile_attrib(cls, *args):
        attrib = {}
        if len(args) > 0 and isinstance(args[0], dict):
            attrib.update(args[0])
            args = args[1:]
        return attrib, args

    @classmethod
    def _parse_css_style_tags(cls, tag, attrib):
        match = re.search(r'^(.+?)(\#|\.)(.+)', tag)
        if match:
            tag, key, value = match.groups()
            key = {'#': 'id', '.': 'class'}[key]
            attrib[key] = value
        return tag, attrib

    @classmethod
    def _append_children(cls, element, args):
        text_anchor = None
        for child in args:
            if child in (None, (), []):
                pass
            elif isinstance(child, text_type):
                if text_anchor is None:
                    element.text = (element.text or '') + child
                else:
                    text_anchor.tail = (text_anchor.tail or '') + child
            else:
                if not cls._is_element(child):
                    child = cls.build_etree(*child)
                element.append(child)
                text_anchor = child

    # The rest are overriden in LxmlKlon to use lxml.etree instead of xml.etree.ElementTree

    @classmethod
    def _create_element(cls, tag, attrib):
        return xml.etree.ElementTree.Element(tag, attrib)

    @classmethod
    def _is_element(cls, obj):
        return isinstance(obj, xml.etree.ElementTree.Element)

    @classmethod
    def tostring(cls, etree, **kwargs):
        return xml.etree.ElementTree.tostring(etree, **kwargs)

#----------------------------------------------------------------------------------------------------------------------------------
