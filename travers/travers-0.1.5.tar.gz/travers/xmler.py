"""
travers

(C) 2023 Justin Joyce.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from xml.etree import cElementTree as ElementTree  # nosec
from collections import defaultdict


def _strip_namespace(entry):
    if isinstance(entry, dict):
        for k in [k for k in entry.keys() if k.startswith("{")]:
            k2 = k.split("}", 1)[1]
            entry[k2] = entry.pop(k)
        for k in [k for k in entry.keys() if k.startswith("@{")]:
            k2 = k.split("}", 1)[1]
            entry[f"@{k2}"] = entry.pop(k)
        for child in entry:
            if isinstance(entry[child], (list, dict)):
                _strip_namespace(entry[child])
    if isinstance(entry, list):
        for child in entry:
            if isinstance(child, (list, dict)):
                _strip_namespace(child)


def _etree_to_dict(t):
    d = {t.tag: {} if t.attrib else None}
    children = list(t)
    if children:
        dd = defaultdict(list)
        for dc in map(_etree_to_dict, children):
            for k, v in dc.items():
                dd[k].append(v)
        d = {t.tag: {k: v[0] if len(v) == 1 else v for k, v in dd.items()}}
    if t.attrib:
        d[t.tag].update(("@" + k, v) for k, v in t.attrib.items())
    if t.text:
        text = t.text.strip()
        if children or t.attrib:
            if text:
                d[t.tag]["#text"] = text
        else:
            d[t.tag] = text
    return d


def parse(xml_string):
    tree = ElementTree.XML(xml_string)
    dictionary = _etree_to_dict(tree)
    _strip_namespace(dictionary)
    return dictionary
