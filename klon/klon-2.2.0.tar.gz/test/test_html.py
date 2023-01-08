#!/usr/bin/env python3

# 3rd parties
import pytest

# klon
from klon import Element, build_etree, make_all_urls_absolute, parse_html_etree, tostring


@pytest.mark.parametrize(
    'base_url, etree, expected',
    [
        (
            # relative URLs are made absolute
            'http://example.com/',
            build_etree('div', ['a', {'href': 'relative/link'}]),
            build_etree('div', ['a', {'href': 'http://example.com/relative/link'}]),
        ),
        (
            # absolute URLs are untouched
            'http://example.com/',
            build_etree('div', ['a', {'href': 'http://absolute/link'}]),
            build_etree('div', ['a', {'href': 'http://absolute/link'}]),
        ),
        (
            # an https:// URL doesn't override an http:// URL
            'https://example.com/',
            build_etree('div', ['a', {'href': 'http://absolute/link'}]),
            build_etree('div', ['a', {'href': 'http://absolute/link'}]),
        ),
        (
            # an #anchor link gets merged too
            'http://example.com/',
            build_etree('div', ['a', {'href': '#anchor'}]),
            build_etree('div', ['a', {'href': 'http://example.com/#anchor'}]),
        ),
        (
            # not just ahrefs are updated -- see full list in klon/html.py
            'http://example.com/',
            build_etree('div', ['img', {'src': 'image.jpg'}]),
            build_etree('div', ['img', {'src': 'http://example.com/image.jpg'}]),
        ),
        (
            # the root element is updated too
            'http://example.com/',
            build_etree('a', {'href': 'relative/link'}),
            build_etree('a', {'href': 'http://example.com/relative/link'}),
        ),
        (
            # if the URL attribute is missing we don't complain
            'http://example.com/',
            build_etree('div', ['a', {'name': 'rover'}]),
            build_etree('div', ['a', {'name': 'rover'}]),
        ),
        (
            # empty links are replaced by the full base URL, as a browser does
            'http://example.com/',
            build_etree('div', ['a', {'href': ''}]),
            build_etree('div', ['a', {'href': 'http://example.com/'}]),
        ),
    ]
)
def test_make_all_urls_absolute(base_url, etree, expected):
    make_all_urls_absolute(base_url, etree)
    assert tostring(etree) == tostring(expected)


@pytest.mark.parametrize(
    'input_str, expected_tree',
    [
        # We're not going to test the intricacies of lxml's HTML-parsing abilities here (e.g. how it handles mismatched angle
        # brackets), but rather just test the behaviour of our function.
        (
            '<html><body><h1>Hello</h1></body></html>',
            ['html', ['body', ['h1', 'Hello']]],
        ),
        (
            # <html><body> is auto-inserted (this is done by lxml)
            '<h1>Hello</h1>',
            ['html', ['body', ['h1', 'Hello']]],
        ),
        (
            # a plain string is converted to a <p> (this is done by lxml)
            'Hello',
            ['html', ['body', ['p', 'Hello']]],
        ),
        (
            # a None input triggers a TypeError
            None,
            TypeError,
        ),
        (
            # an empty string triggers a ValueError
            '',
            ValueError,
        ),
        (
            # a string consisting of whitespace only also triggers a ValueError
            ' ',
            ValueError,
        ),
        (
            # a string consisting of an xml declaration only counts as an empty string
            '<?xml version="1.0" encoding="UTF-8" ?>',
            ValueError,
        ),
    ]
)
def test_html_parser(input_str, expected_tree):

    def compare(obtained: Element, expected: Element) -> None:
        assert obtained.tag == expected.tag
        for key, value in expected.attrib.items():
            assert obtained.get(key) == value
        assert len(obtained) == len(expected)
        for ochild, echild in zip(obtained, expected):
            compare(ochild, echild)

    if isinstance(expected_tree, type) and issubclass(expected_tree, Exception):
        with pytest.raises(expected_tree):
            parse_html_etree(input_str)
    else:
        obtained = parse_html_etree(input_str)
        expected = build_etree(*expected_tree)
        compare(obtained, expected)
