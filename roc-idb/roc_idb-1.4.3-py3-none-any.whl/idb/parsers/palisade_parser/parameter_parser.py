#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from roc.idb.parsers.idb_elements import (
    ParameterDefinition,
    Parameter,
    Time,
    SimpleType,
    Enumeration,
)

__all__ = ['ParameterParser']


class ParameterParser:
    """
    Mixin class used to parse parameters
    """

    def populate_parameters(self):
        """
        Get information on parameters from the IDB, and store them to be
        easily accessible later.
        """
        # look for the nodes in the IDB
        nodes = self._findall(self.root, './/{0}ParameterDefinition', '')

        # loop over nodes
        for node in nodes:
            # name of the parameter
            palisade_id = node.attrib['ID']

            # store the palisade id of the associated tf/enum if any
            tf_palisade_id = None

            # initialize the dict containing the parameter definition info
            definition_dict = {
                'palisade_id': palisade_id,
                'maximum': None,
                'minimum': None,
                'description': None,
                'default': None,
                'unit': None,
                'transfer_function': None,
                'is_editable': None,
            }

            # give the description
            definition_dict['description'] = self._find(
                node, '{0}Description', ''
            ).text

            # store also the node of the definition
            definition_dict['node'] = node

            # if the paramater has a max, min, unit or default value, store it
            if 'Max' in node.attrib:
                definition_dict['maximum'] = node.attrib['Max']
            if 'Min' in node.attrib:
                definition_dict['minimum'] = node.attrib['Min']
            if 'Unit' in node.attrib:
                definition_dict['unit'] = node.attrib['Unit']
            if 'Default' in node.attrib:
                definition_dict['default'] = str(node.attrib['Default'])

            if 'TFIDRef' in node.attrib:
                tf_palisade_id = node.attrib['TFIDRef']

            # look for fixed parameters
            if (definition_dict['minimum'] is None) or (
                definition_dict['maximum'] is None
            ):
                definition_dict['is_editable'] = None
            else:
                definition_dict['is_editable'] = not (
                    definition_dict['minimum'] == definition_dict['maximum']
                )

            # get the parameter type from one of the following nodes

            enum = self._find(node, '{0}Enum', '')
            simple_type = self._find(node, '{0}SimpleType', '')
            time = self._find(node, '{0}Time', '')

            is_enum = False

            # if a simple type
            if simple_type is not None:
                definition_dict['data_type'] = SimpleType(
                    simple_type.attrib['Type']
                )

            # check if enum
            elif enum is not None:
                is_enum = True

                # get the reference of the enum as the transfer function id
                tf_palisade_id = enum.attrib['IDRef']

            # check if time
            elif time is not None:
                definition_dict['data_type'] = Time(
                    time.attrib['Coding'],
                    self._find(time, '{0}Coarse', '').attrib['Len'],
                    self._find(time, '{0}Fine', '').attrib['Len'],
                )

            # get the corresponding srdb_id(s)
            if self.parameters_mapping is None:
                raise Exception(
                    'The mapping table is required to load the parameter definitions'
                )
            else:
                srdb_id_maps = {
                    packet_type: self.parameters_mapping[packet_type].get(
                        palisade_id, None
                    )
                    for packet_type in ['TM', 'TC']
                }
                srdb_id_list = [
                    (
                        packet_type,
                        Parameter.nameFromSRDBID(
                            srdb_id_map['SRDBID'],
                            packet_type,
                            srdb_id_map['kind'],
                        ),
                    )
                    for packet_type, srdb_id_map in srdb_id_maps.items()
                    if srdb_id_map is not None
                ]

            for packet_type, srdb_id in srdb_id_list:
                # create the parameter from the srdb_id and the info dict

                # check for enum
                if is_enum:
                    # create the enumeration and assign it as data_type
                    enum_srdb_id = self.palisade_to_srdb_id[packet_type][
                        tf_palisade_id
                    ]
                    definition_dict['data_type'] = Enumeration.manager[
                        enum_srdb_id
                    ]
                    definition_dict['transfer_function'] = enum_srdb_id
                elif tf_palisade_id is not None:
                    # get the srdb_id of the tf
                    tf_srdb_id = self.palisade_to_srdb_id[packet_type].get(
                        tf_palisade_id, None
                    )
                    definition_dict['transfer_function'] = tf_srdb_id

                ParameterDefinition(srdb_id, **definition_dict)
