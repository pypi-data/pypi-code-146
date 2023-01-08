#!/usr/bin/env python3

# standards
from pathlib import Path
import re

# 3rd parties
import pytest

# klon
from klon import parse_form, parse_html_etree


def _load_fixture(method):
    html_file = Path(__file__).parent / 'test_forms.html'
    doc = parse_html_etree(html_file.read_text('UTF-8'))
    form = doc.xpath('//form')[0]
    if method is None:
        form.attrib.pop('method', '')
    else:
        form.attrib['method'] = method
    expected_query_string = doc.xpath('//a/@href')[0].lstrip('?')
    return form, expected_query_string


@pytest.mark.parametrize('method', [None, 'GET', 'POST'])
def test_form_parser(method):
    form, expected_query_string = _load_fixture(method)
    obtained_preq = parse_form(form).prepare()
    obtained_qs = re.sub(r'.+\?', '', obtained_preq.url) if method in (None, 'GET') else obtained_preq.body
    assert obtained_qs == expected_query_string


@pytest.mark.parametrize('method', [None, 'GET', 'POST'])
def test_form_parser_method(method):
    form, _qs_unused = _load_fixture(method)
    assert parse_form(form).method == method or 'GET'
