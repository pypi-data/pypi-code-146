"""Utils for stripping html tags from text."""
import io
import re
from typing import Callable, Dict, List, Optional

from lxml import etree

ENCODING = 'utf-8'


def strip_href(value: str) -> str:
    """Check link attribute href."""
    if not value or value[:1] == '/':
        return value
    if re.match("(https?://|mailto:)", value):
        return value
    return ""


def strip_src(value: str) -> str:
    """Check link attribute href."""
    if not value or value[:1] == '/':
        return value
    if re.match("https?://", value):
        return value
    return ""


ATTRIBUTE_CALLBACKS = {
    'a_href': strip_href,
    'img_src': strip_src,
    'blockquote_cite': strip_href,
}

ALLOWED_TAGS: Dict[str, List[str]] = {
    'a': ['href', 'target', 'class'],
    'address': ['class'],
    'b': [],
    'br': [],
    'bdi': [],
    'bdo': [],
    'blockquote': ['class', 'cite'],
    'caption': [],
    'cite': ['class'],
    'code': ['class'],
    'div': ['class'],
    'em': ['class'],
    'h1': ['class'],
    'h2': ['class'],
    'h3': ['class'],
    'h4': ['class'],
    'h5': ['class'],
    'h6': ['class'],
    'hr': [],
    'i': ['class'],
    'img': ['src', 'width', 'height', 'alt', 'title', 'class'],
    'li': [],
    'ol': [],
    'p': ['class'],
    'pre': ['class'],
    'small': ['class'],
    'span': ['class'],
    'strong': ['class'],
    'sub': [],
    'sup': [],
    'table': ['class', 'width'],
    'tbody': [],
    'td': [],
    'th': [],
    'tr': [],
    'u': ['class'],
    'ul': ['class'],
}


def keep_only_tags(
    body: Optional[str],
    allowed_tags: Dict[str, List[str]] = ALLOWED_TAGS,
    attribute_callbacks: Dict[str, Callable] = ATTRIBUTE_CALLBACKS,
    encoding: str = ENCODING
) -> Optional[str]:
    """Keep only defined tags and attributes in the HTML content."""
    if body is None or "<" not in body:
        return body
    allowed: Dict[str, List[str]] = {'body': []}
    allowed.update(allowed_tags)
    doc = etree.Element("body")
    # It can't be HTMLParser because it creates tags on text that doesn't have them.
    reader = etree.XMLParser(recover=True, remove_blank_text=True, encoding=encoding)
    root = etree.parse(io.StringIO(f'<body>{body}</body>'), reader)
    for node in root.xpath("//*"):
        if node.tag not in allowed:
            continue
        attributes = {}
        for key, value in node.attrib.items():
            if key not in allowed[node.tag]:
                continue
            value = attribute_callbacks.get(f'{node.tag}_{key}', lambda value: value)(value)
            if value:
                attributes[key] = value
        element = etree.Element(node.tag, **attributes)
        element.text = node.text
        element.tail = node.tail
        doc.append(element)

    content = etree.tostring(doc, method="html", encoding=encoding).decode(encoding)
    return re.sub('</?body>', '', content)
