#!/usr/bin/env python3

# standards
from typing import Union

# 3rd parties
import lxml.etree as ET


def parse_xml_etree(xml_str: Union[bytes, str], remove_comments: bool = False) -> ET._Element:
    parser = ET.XMLParser(remove_comments=remove_comments)
    return ET.XML(xml_str, parser)
