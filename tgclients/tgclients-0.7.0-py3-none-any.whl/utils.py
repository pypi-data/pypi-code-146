# SPDX-FileCopyrightText: 2022 Georg-August-Universität Göttingen
#
# SPDX-License-Identifier: LGPL-3.0-or-later

"""Utility functions for working with the TextGrid repository"""
from pathlib import Path
from typing import List

import defusedxml.ElementTree as ET
from jinja2 import Environment, FileSystemLoader

from tgclients.databinding.tgsearch import Response as SearchResponse


class Utils:
    """Utility functions for working with the TextGrid repository"""

    @staticmethod
    def list_to_aggregation(textgrid_uri: str, members: List[str]) -> str:
        """Create XML for a TextGrid aggregation from list

        Args:
            textgrid_uri (str): textgrid URI of the aggregation to create
            members (list[str]): list of textgrid URIs inside aggregation

        Returns:
            str: XML for TextGrid Aggregation
        """
        path = Path(__file__).parent / 'templates'
        env = Environment(
            loader=FileSystemLoader(Path(path)), autoescape=True)
        template = env.get_template('aggregation.xml.jinja2')
        aggregation = template.render(id=textgrid_uri, members=members)
        return aggregation

    @staticmethod
    def aggregation_to_list(xml: str) -> List[str]:
        """Extract URIs from TextGrid aggregation into a list

        Args:
            xml (str): TextGrid aggregation XML

        Returns:
            list[str]: TextGrid URIs from aggregation
        """
        res = []
        root = ET.fromstring(xml)
        tag_name = '{http://www.openarchives.org/ore/terms/}aggregates'
        attr_name = '{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource'
        for descendant in root.iter(tag_name):
            res.append(descendant.attrib[attr_name])
        return res
