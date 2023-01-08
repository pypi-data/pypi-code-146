#!/usr/bin/env python3

from .build import build_etree
from .forms import parse_form
from .html import extract_js_str, make_all_urls_absolute, parse_html_etree
from .text import extract_multiline_text, extract_text, normalize_spaces
from .utils import Element, detach, is_element, tostring
from .xml import parse_xml_etree
