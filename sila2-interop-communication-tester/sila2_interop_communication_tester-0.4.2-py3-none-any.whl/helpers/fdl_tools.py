from pathlib import Path
from typing import NamedTuple

from lxml import etree
from lxml.etree import Element

import sila2_interop_communication_tester


def __path_to_feature_id(path: Path) -> str:
    return path.name.split(".")[0].split("-")[0]


def xpath_sila(element: Element, expression: str):
    return element.xpath(expression, namespaces=dict(sila="http://www.sila-standard.org"))


fdl_dir = Path(sila2_interop_communication_tester.__file__).parent / "resources" / "fdl"
fdl_files: dict[str, Path] = {__path_to_feature_id(f): f.absolute() for f in fdl_dir.glob("*.sila.xml")}
fdl_xmls: dict[str, Element] = {__path_to_feature_id(f): etree.parse(str(f)) for f in fdl_files.values()}


class FullyQualifiedFeatureIdentifier(NamedTuple):
    originator: str
    category: str
    full_version: str
    major_version: str
    identifier: str
    fully_qualified_identifier: str


def get_fully_qualified_identifier(feature_id: str) -> FullyQualifiedFeatureIdentifier:
    root = fdl_xmls[feature_id]
    version = xpath_sila(root, "/sila:Feature/@FeatureVersion")[0]
    originator = xpath_sila(root, "/sila:Feature/@Originator")[0]
    category = xpath_sila(root, "/sila:Feature/@Category")[0]
    identifier = xpath_sila(root, "/sila:Feature/sila:Identifier/text()")[0]
    major_version = version.split(".")[0]
    return FullyQualifiedFeatureIdentifier(
        originator=originator,
        category=category,
        full_version=version,
        major_version=major_version,
        identifier=identifier,
        fully_qualified_identifier="/".join((originator, category, identifier, f"v{major_version}")),
    )
