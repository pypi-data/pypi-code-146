#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os.path as osp
import xml.etree.ElementInclude as EI
import xml.etree.ElementTree as ET

from poppy.core.logger import logger
from roc.idb.parsers.idb_parser import IDBParser

__all__ = ['BasePALISADEParser', 'PALISADEException']


class PALISADEException(Exception):
    """
    Exception for PALISADE.
    """


class BasePALISADEParser(IDBParser):
    """
    Base class used for the parsing of the XML of the PALISADE IDB
    """

    def __init__(self, idb, mapping_file_path):
        """
        Store the file names of the XML files containing the IDB and the
        mapping to the SRDB.
        """
        super().__init__(mapping_file_path)
        self._source = 'PALISADE'
        self.idb = osp.join(idb, 'xml', 'RPW_IDB.xml')
        self.enumerations = None

        # create the tree of the IDB
        self.store_tree()

        # store the palisade metadata as a map indexed by SRDB IDs
        self.palisade_metadata_map = {}

    def store_tree(self):
        """
        Create the tree from the file given in argument.
        """
        # check that the file exist
        if self.idb is None or not osp.isfile(self.idb):
            message = "IDB {0} doesn't exist".format(self.idb)
            logger.error(message)
            raise FileNotFoundError(message)

        # get the tree and namespace
        self.tree, self.namespace = self.parse_and_get_ns(self.idb)

        # get the root element
        self.root = self.tree.getroot()

        # get the directory path
        self._path = self.get_path()

        # include other files from root : First level
        EI.include(self.root, loader=self._loader)
        # include other files from child of root (second level)
        # FIXME : Implement the general case with several level of "include"
        EI.include(self.root, loader=self._loader)

        # compute the parent map after includes
        self.parent_map = {
            child: parent for parent in self.tree.iter() for child in parent
        }

    def get_path(self):
        """
        Return the directory path of the IDB to be used as root for the
        included files in the XML.
        """
        # get the absolute path of the directory
        return osp.abspath(osp.dirname(self.idb))

    def _loader(self, href, parse, encoding=None):
        """
        The loader of included files in XML. In our case, the parse attribute
        is always XML so do not do anything else.
        """
        # open the included file and parse it to be returned
        with open(osp.join(self._path, href), 'rb') as f:
            return ET.parse(f).getroot()

    def _find(self, node, path, *args):
        """
        To find a node with the namespace passed as argument.
        """
        return node.find(
            path.format(*[self._ns[x] if x in self._ns else x for x in args])
        )

    def _findall(self, node, path, *args):
        """
        To findall a node with the namespace passed as argument.
        """
        return node.findall(
            path.format(*[self._ns[x] if x in self._ns else x for x in args])
        )

    def get_structures(self):
        """
        Get a dictionary of all structures defined in the XML IDB.
        """
        # get all structures
        structures = self._findall(self.root, './/{0}StructDefinition', '',)
        # keep a dictionary of the structure name and the corresponding node
        self.structures = {
            struct.attrib['ID']: struct for struct in structures
        }

    def generate_srdb_ids_from_palisade_id(self, palisade_id):
        """
        Given a PALISADE ID, generate the corresponding SRDB ID(s)
        """
        for packet_type in ['TM', 'TC']:
            if palisade_id in self.palisade_to_srdb_id[packet_type]:
                if isinstance(
                    self.palisade_to_srdb_id[packet_type][palisade_id], list
                ):
                    for srdb_id in self.palisade_to_srdb_id[packet_type][
                        palisade_id
                    ]:
                        yield srdb_id
                else:
                    yield self.palisade_to_srdb_id[packet_type][palisade_id]

    def get_palisade_category(self, node):
        """
        Get the palisade category of a given node using the parent map of the xml tree

        :param node: the node we want the category
        :return: the palisade category
        """

        current_node = node

        node_tag_list = []

        while 'parent is a node of the xml tree':
            # get the parent node
            parent = self.parent_map.get(current_node, None)

            if parent is None:
                break

            if parent.tag.endswith('Category'):
                # prepend the category to the list
                node_tag_list.insert(0, parent.attrib['Name'])

            current_node = parent

        return '/' + '/'.join(node_tag_list)

    def is_enumeration(self, parameter):
        """
        Return True if a parameter is an enumeration.
        """
        return parameter.is_enumeration()

    @property
    def namespace(self):
        return self._ns

    @namespace.setter
    def namespace(self, namespace):
        self._ns = namespace

        # store some information from the namespace
        self.struct_tag = '{0}Struct'.format(self._ns[''])
        self.param_tag = '{0}Parameter'.format(self._ns[''])
        self.spare_tag = '{0}Spare'.format(self._ns[''])
        self.loop_tag = '{0}Loop'.format(self._ns[''])

    def version(self):
        """
        Return the version of the IDB defined in the XML file.
        """
        if 'Version' not in self.root.attrib:
            message = 'No version for the IDB from the specified XML file.'
            logger.error(message)
            raise PALISADEException(message)
        return self.root.attrib['Version'].replace(' ', '_').upper()
