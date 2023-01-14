import re
from typing import Dict, Generator, Union

import xmltodict
from lxml import etree
from lxml.etree import tostring

from reljicd_utils.utils import read_file


def dict_from_xml_file(file: str) -> Dict[str, Union[Dict, str]]:
    if file.startswith('s3'):
        return xmltodict.parse(read_file(file))
    else:
        with open(file, 'r') as f:
            return xmltodict.parse(f.read())


def xml_dict_generator(file: str, tag: str) -> Generator[Dict, None, None]:
    context = etree.iterparse(file, tag=tag)
    for _, elem in context:
        yield xmltodict.parse(tostring(elem))[tag]
        elem.clear()


def count_tags(file: str, tag: str) -> int:
    context = etree.iterparse(file, tag=tag)
    counter = 0
    for _, elem in context:
        counter += 1
        elem.clear()
    return counter


TAG_RE = re.compile(r'<[^>]+>')


def remove_tags(text: str) -> str:
    return TAG_RE.sub('', text)
