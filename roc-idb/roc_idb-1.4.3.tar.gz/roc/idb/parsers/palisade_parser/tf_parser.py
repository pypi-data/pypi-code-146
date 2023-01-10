#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__all__ = [
    'TFParser',
]


class TFParser:
    """
    Mixin class used to parse transfer functions
    """

    def create_tf(self):
        """
        Extract and create packets with TF (PALISADE_ID, Raw, Eng)
        """

        self.tf_dict = {}

        palisade_tf_dict = {}

        # loop over nodes
        for child in self._findall(
            self.root, './/{0}CalibrationDefinition', '',
        ):
            palisade_id = child.attrib['ID']
            palisade_tf_dict.setdefault(palisade_id, [])
            for subchild in self._findall(child, './/{0}Tab', '',):
                palisade_tf_dict[palisade_id].append(
                    {'raw': subchild.attrib['X'], 'eng': subchild.attrib['Y']}
                )

        # loop over the srdb_ids and retrieve the node info
        for palisade_id in palisade_tf_dict:
            for srdb_id in self.generate_srdb_ids_from_palisade_id(
                palisade_id
            ):
                self.tf_dict[srdb_id] = palisade_tf_dict[palisade_id]
