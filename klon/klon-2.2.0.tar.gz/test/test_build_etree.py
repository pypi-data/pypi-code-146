#!/usr/bin/env python3

# it's the pytest way, pylint: disable=redefined-outer-name


# 2+3 compat
from __future__ import absolute_import, division, print_function, unicode_literals

# standards
import re

# 3rd parties
import pytest

# klon
from klon import build_etree, tostring


def check(element, tag, attrib=None, children=None, text=None, tail=None):
    assert element.tag == tag
    assert element.attrib == (attrib or {})
    assert element.text == text
    assert len(element) == len(children or [])
    for child, child_definition in zip(element, children or []):
        check(child, **child_definition)
    assert element.tail == tail


def check_str(element, expected_str):
    generated_bytes = tostring(element, encoding='UTF-8')
    generated_str = generated_bytes.decode('UTF-8')
    assert _normalize_str(generated_str) == _normalize_str(expected_str)


def _normalize_str(text):
    # Smoothe over the slight cosmetic differences btw the output of xml.etree.ElementTree.tostring and lxml.etree.tostring
    text = re.sub(r'^<\?xml[^>]*>\s*', '', text)
    text = re.sub(r' (?=/>)', '', text)
    return text


def test_build_empty_node():
    element = build_etree('mynode')
    check(element, 'mynode')
    check_str(element, '<mynode />')


def test_build_attrib_from_dict():
    element = build_etree('mynode', {'a': '1'})
    check(element, 'mynode', {'a': '1'})
    check_str(element, '<mynode a="1" />')


def test_css_style_id():
    element = build_etree('mynode#test')
    check(element, 'mynode', {'id': 'test'})
    check_str(element, '<mynode id="test" />')


def test_css_style_class():
    element = build_etree('mynode.test')
    check(element, 'mynode', {'class': 'test'})
    check_str(element, '<mynode class="test" />')


def test_build_node_with_text():
    element = build_etree('mynode', 'Text')
    check(element, 'mynode', text='Text')
    check_str(element, '<mynode>Text</mynode>')


def test_build_node_with_multiple_text():
    element = build_etree('mynode', 'Te', 'xt')
    check(element, 'mynode', text='Text')
    check_str(element, '<mynode>Text</mynode>')


def test_build_node_with_text_and_attrib():
    element = build_etree('mynode', {'a': '1'}, 'Te', 'xt')
    check(element, 'mynode', attrib={'a': '1'}, text='Text')
    check_str(element, '<mynode a="1">Text</mynode>')


def test_node_with_children():
    element = build_etree('mynode', ['mychild'])
    check(element, 'mynode', children=[{'tag': 'mychild'}])
    check_str(element, '<mynode><mychild /></mynode>')


def test_node_with_children_attribs():
    element = build_etree('mynode', ['mychild', {'a': '1'}])
    check(element, 'mynode', children=[{'tag': 'mychild', 'attrib': {'a': '1'}}])
    check_str(element, '<mynode><mychild a="1" /></mynode>')


def test_node_with_children_text():
    element = build_etree('mynode', ['mychild', {'a': '1'}, 'Text'])
    check(element, 'mynode', children=[{'tag': 'mychild', 'attrib': {'a': '1'}, 'text': 'Text'}])
    check_str(element, '<mynode><mychild a="1">Text</mychild></mynode>')


def test_node_with_children_tail():
    element = build_etree('mynode', ['mychild'], 'Tail')
    check(element, 'mynode', children=[{'tag': 'mychild', 'tail': 'Tail'}])
    check_str(element, '<mynode><mychild />Tail</mynode>')


def test_node_with_prebuilt_child():
    child = build_etree('mychild')
    element = build_etree('mynode', child)
    check(element, 'mynode', children=[{'tag': 'mychild'}])
    check_str(element, '<mynode><mychild /></mynode>')


def test_non_str_tag():
    with pytest.raises(ValueError):
        build_etree(object(), {'a': '1'})


def test_byte_tag():
    with pytest.raises(ValueError):
        build_etree(b'mytag', {'a': '1'})


def test_empty_children_array_are_noop():
    element = build_etree('mynode', ['mychild', 'a', [], 'b'], [], 'c')
    check(element, 'mynode', children=[{'tag': 'mychild', 'text': 'ab', 'tail': 'c'}])
    check_str(element, '<mynode><mychild>ab</mychild>c</mynode>')


def test_none_values_are_noop():
    element = build_etree('mynode', ['mychild', 'a', None, 'b'], None, 'c')
    check(element, 'mynode', children=[{'tag': 'mychild', 'text': 'ab', 'tail': 'c'}])
    check_str(element, '<mynode><mychild>ab</mychild>c</mynode>')
