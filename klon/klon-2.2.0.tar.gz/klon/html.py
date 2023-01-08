#!/usr/bin/env python3

# standards
import re
from typing import no_type_check
from urllib.parse import urljoin

# 3rd parties
import lxml.etree as ET


TAGS_WITH_URL_ATTRIBUTES = {
    'a': ['href'],
    'area': ['href'],
    'audio': ['src'],
    'base': ['href'],
    'blockquote': ['cite'],
    'del': ['cite'],
    'embed': ['src'],
    'form': ['action'],
    'frame': ['src'],
    'iframe': ['src'],
    'img': ['src', 'srcset'],
    'input': ['src'],
    'ins': ['cite'],
    'link': ['href'],
    'object': ['data'],
    'script': ['src'],
    'source': ['src', 'srcset'],
    'track': ['src'],
    'video': ['poster', 'src'],
}


XPATH_TAGS_WITH_URL_ATTRIBUTES = '//*[%s]' % ' or '.join(
    f'self::{tag}' for tag in sorted(TAGS_WITH_URL_ATTRIBUTES)
)


def parse_html_etree(html_str: str, remove_comments: bool = False) -> ET._Element:
    if not isinstance(html_str, str):
        raise TypeError('Expected str, not %s; %s' % (type(html_str).__name__, repr(html_str)[:100]))

    # It's rare for HTML docs to contain an XML declaration, but when they do, lxml throws an exception, so remove them
    html_str = re.sub(r'^<\?xml[^>]+\?>', '', html_str)

    html_str = html_str.strip()
    if html_str == '':
        raise ValueError("Can't parse HTML etree from an empty string")

    parser = ET.HTMLParser(remove_comments=remove_comments)
    return ET.HTML(html_str, parser)


@no_type_check  # until lxml-stubs improves
def make_all_urls_absolute(base_url: str, etree: ET._Element) -> None:
    """
    Modify all links in the given HTML etree to be absolute URLs, using the given `base_url` to resolve relative URLs.
    """
    for node in etree.xpath(XPATH_TAGS_WITH_URL_ATTRIBUTES):  # type: ignore[union-attr]
        for attr in TAGS_WITH_URL_ATTRIBUTES[node.tag]:
            value = node.get(attr)
            if value is not None:
                if attr == 'srcset':
                    new_value = re.sub(
                        r'((?:^|,)\s*)(\S+)',
                        lambda m: m[1] + urljoin(base_url, m[2]),
                        value,
                    )
                else:
                    new_value = urljoin(base_url, value)
                if new_value != value:
                    node.set(attr, new_value)


@no_type_check
def extract_js_str(element: ET._Element) -> str:
    return '\n\n'.join(
        re.sub(r'^\s*<!--', '', re.sub(r'-->\s*$', '', script_str))
        for script_str in element.xpath('.//script/text()')
    )
