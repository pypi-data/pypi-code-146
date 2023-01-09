# SPDX-FileCopyrightText: 2022 Georg-August-Universität Göttingen
#
# SPDX-License-Identifier: LGPL-3.0-or-later

"""Helper functions to work with TextGrid metadata XML"""
import io
import os
import re
import logging
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Optional

import defusedxml.ElementTree as dT
from jinja2 import Environment, FileSystemLoader
from xsdata.formats.dataclass.context import XmlContext
from xsdata.formats.dataclass.parsers import XmlParser

from tgclients.databinding.tgsearch import Response, ResultType
from tgclients.databinding.textgrid_metadata_2010 import MetadataContainerType

try:
    import icu
except ImportError:
    icu = None

logger = logging.getLogger(__name__)

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

class TextgridMetadata:
    """Helper functions to work with TextGrid metadata XML"""

    def __init__(self):
        context = XmlContext()
        self._parser = XmlParser(context=context)
        self._file_extension_map = self._build_extension_map()
        if icu is not None:
            self._transliterator = self._create_transliterator()

    @staticmethod
    def create(title: str, mimetype: str) -> str:
        """Create XML metadata for an TextGrid Object

        Args:
            title (str): title of the object
            mimetype (str): format / MIME type of the object

        Returns:
            str: XML metadata as string
        """
        path = Path(__file__).parent / 'templates'
        env = Environment(
            loader=FileSystemLoader(Path(path)), autoescape=True)
        template = env.get_template('metadata.xml.jinja2')
        metadata = template.render(title=title, format=mimetype)
        return metadata

    def build(self, title: str, mimetype: str) -> MetadataContainerType:
        """Build metadata for an TextGrid Object

        Args:
            title (str): title of the object
            mimetype (str): format / MIME type of the object

        Returns:
            MetadataContainerType: metadata
        """
        metadata = TextgridMetadata().create(title, mimetype)
        return self._parser.from_string(metadata, MetadataContainerType)

    @staticmethod
    def get_xpath(xml: str, xpath: str) -> str:
        namespaces = TextgridMetadata._register_namespaces(xml)
        xml_stream = io.StringIO(xml)
        element_tree = dT.parse(xml_stream)
        result = element_tree.find(xpath, namespaces).text
        return result

    @staticmethod
    @DeprecationWarning
    # This is not used. TODO: remove
    def get_xpath2(xml: str, xpath: str) -> str:
        namespaces = TextgridMetadata._register_namespaces(xml)
        xml_stream = io.StringIO(xml)
        element_tree = dT.parse(xml_stream)
        result = element_tree.findall(xpath, namespaces)
        return result

    @staticmethod
    def _register_namespaces(xml: str) -> dict:
        """Register namespaces to the global ElementTree and return a
        dictionary of them.

        Args:
            xml (str): XML Document

        Returns:
            dict: Namespaces dictionary
        """
        xml_stream = io.StringIO(xml)
        # Uses a list comprehension and element tree's iterparse function to
        # create a dictionary containing the namespace prefix and its uri. The
        # underscore is utilized to remove the "start-ns" output. `iterparse`
        # returns an iterator providing (event, elem) pairs.
        # see https://medium.datadriveninvestor.com/getting-started-using-pythons-elementtree-to-navigate-xml-files-dc9bc720eaa6
        namespaces = {node[0]: node[1]
                      for _, node in dT.iterparse(xml_stream, events=['start-ns'])}

        # Iterates through the newly created namespace dictionary registering the prefixes
        for prefix, uri in namespaces.items():
            ET.register_namespace(prefix + '_', uri)

        return namespaces

    def searchresponse2object(self, xml: str) -> Response:
        return self._parser.from_string(xml, Response)

    def filename_from_metadata(self, metadata: ResultType) -> str:
        """Generate a filename for a textgrid search metadata result
        containg title, textfgrid-uri and extension

        Args:
            metadata (ResultType): tgsearch metadata result

        Returns:
            str: the filename
        """
        title = metadata.object_value.generic.provided.title[0]
        mimetype = metadata.object_value.generic.provided.format
        uri = metadata.object_value.generic.generated.textgrid_uri.value
        return self.filename(title, uri, mimetype)

    def filename(self, title: str, tguri: str, mimetype: str) -> str:
        """Generate a filename for the triple of
        title, textfgrid-uri and extension

        Args:
            title (str): the title
            tguri (str): the textgrid uri
            mimetype (str): the mime type (e.g. 'text/xml')

        Returns:
            str: the filename
        """
        title = self.transliterate(title)
        tg_id = self.remove_tg_prefix(tguri)
        ext = self.extension_for_format(mimetype)
        if ext is not None:
            return f'{title}.{tg_id}.{ext}'
        else:
            return f'{title}.{tg_id}'

    def _build_extension_map(self) -> dict:
        # converted to python from info.textgrid.utils.export.filenames.FileExtensionMap
        # of link-rewriter (https://gitlab.gwdg.de/dariah-de/textgridrep/link-rewriter)
        extension_map = {}
        map_line_pattern = re.compile(
            '^[ \t]*([^# \t]+)[ \t]*([^#]+)[ \t]*(#.*)?$')
        space_pattern = re.compile('[ \t]+')

        with open(os.path.join(__location__, 'mime.types'), encoding='utf8') as mimefile:
            for line in mimefile.readlines():
                line_match = map_line_pattern.match(line.rstrip('\n'))
                if line_match is not None:
                    entry = space_pattern.split(line_match.group(2))
                    # extend the list in the dict, so extensions definded first are first in list
                    if line_match.group(1) not in extension_map:
                        extension_map[line_match.group(1)] = entry
                    else:
                        extension_map[line_match.group(1)].extend(entry)

        return extension_map

    def extension_for_format(self, mimetype: str) -> Optional[str]:
        """Find a matching extension for a textgrid mime type.
        The first matching extension for a mime type is returned, so
        extensions defined first in mime.types will be used.

        Args:
            mimetype (str): the mime type, as found in textgrid
                            metadata format field (e.g. text/xml)

        Returns:
            str: a filename extension
        """
        if mimetype in self._file_extension_map:
            return self._file_extension_map[mimetype][0]
        else:
            return None

    @staticmethod
    def remove_tg_prefix(tguri: str) -> str:
        return tguri[9:]

    @staticmethod
    def id_from_filename(filename: str) -> str:
        """extract the id from a filename which is named according to link rewriters
        textgrid metadata to filename mapping

        Args:
            filename (str): the filename

        Returns:
            str: the id
        """
        last_dot = filename.rfind('.')
        next_to_last_dot = filename.rfind('.', 0, last_dot)
        # a textgrid uri has a revision number in the end.
        # if the chars after the last dot are not numeric, we have a filename extension
        if not filename[last_dot+1:].isnumeric():
            # extension is there? we need the '.' before the dot separating the uri
            # from the revision component
            next_to_last_dot = filename.rfind('.', 0, next_to_last_dot)
        else:
            # there is no extension to cut of, we want the end of the string
            last_dot = None

        return filename[next_to_last_dot+1:last_dot]

    def transliterate(self, title: str) -> str:
        """replace all chars which may be problematic in filenames from title string

        Args:
            title (str): a title from textgrid metadata

        Returns:
            str: the title string with problematic chars replaced
        """
        name: str = ''
        if icu is None:
            logger.warning('Transliterating without PyICU, you may need that for correct results')
            name = title.replace(' ', '_').replace(']', '_').replace('[', '_').replace(':', '_')
        else:
            name = self._transliterator.transliterate(title)
        return name

    # return type needs to be hidden, because it is not available if PyICU is not installed
    def _create_transliterator(self):
        with open(os.path.join(__location__, 'tgfilenames.rules'), encoding='utf8') as rulesfile:
            rules = rulesfile.read()
            return icu.Transliterator.createFromRules(
                'TgFilenames', rules, icu.UTransDirection.FORWARD)
