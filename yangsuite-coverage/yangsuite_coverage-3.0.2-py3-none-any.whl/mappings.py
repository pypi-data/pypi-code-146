#! /usr/bin/env python
# Copyright 2021 Cisco Systems Inc, All rights reserved.
import os
import io
import uuid
import pandas as pd

from yangsuite import get_logger

log = get_logger(__name__)


class MappingException(Exception):
    pass


class MibYangWriter:

    writers = {}

    def __init__(
        self, map_file, user, mib_paths=[], yang_paths=[], mod_xp={}, mod=''
            ):
        self.user = user
        self.module_matches = mod_xp
        self.module = mod
        self.map_file = map_file
        self.mib_paths = mib_paths
        self.yang_paths = yang_paths

    @classmethod
    def get(
        cls, map_file, user, mib_paths=[], yang_paths=[], mod_xp='', mod=''
            ):
        writer = cls.writers.get((map_file, user))
        if not writer:
            writer = cls(map_file, user, mib_paths, yang_paths, mod_xp, mod)
            cls.writers[(map_file, user)] = writer
        return writer

    @classmethod
    def delete(cls, map_file, user):
        if (map_file, user) in cls.writers:
            del cls.writers[(map_file, user)]

    @classmethod
    def get_mapping_data(cls, file_ref):
        mib_paths = []
        mib_path_to_yang_path = {}
        modules_to_matched_xpaths = {}
        yang_paths = []
        path = ''

        if isinstance(file_ref, io.StringIO):
            path = file_ref
        elif os.path.isfile(file_ref):
            path = file_ref

        if path:
            mapped_df = cls.read_map_file(path)

            for dfrow in mapped_df.iterrows():
                row = dfrow[1].to_dict()
                oid = row.get('OID')
                xpath = row.get('YANG Xpath')
                model = row.get('YANG Module')
                if xpath:
                    mib_path_to_yang_path[oid] = xpath
                    modules_to_matched_xpaths[xpath] = model
                    yang_paths.append({
                        'label': xpath,
                        'value': xpath,
                        'model': model,
                        'id': uuid.uuid4().__str__()
                    })
                mib_paths.append({
                    'oid': oid,
                    'value': oid,
                    'id': uuid.uuid4().__str__()
                })

        return (
            mib_paths,
            yang_paths,
            mib_path_to_yang_path,
            modules_to_matched_xpaths
        )

    @classmethod
    def read_map_file(self, filepath):
        try:
            if os.path.isfile(filepath):
                # open and read
                mapped_df = pd.read_csv(
                    filepath,
                    keep_default_na=False,
                    index_col=False,
                )
                return mapped_df
        except Exception:
            if os.path.isfile(filepath):
                # open and read
                mapped_df = pd.read_excel(
                    filepath,
                    sheet_name='Mapped',
                    keep_default_na=False,
                    engine='openpyxl',
                )
                return mapped_df
        return None

    def _write_xlsx(self, mapped_df):
        """Not writing xlsx files right now."""
        writer = pd.ExcelWriter(self.map_file, engine='xlsxwriter')
        mapped_df.to_excel(writer, sheet_name='Mapped', index=False)

        bold = writer.book.add_format({'bold': True})
        s1 = writer.sheets['Mapped']
        s1.set_column(0, 1, 75)
        s1.set_row(0, None, bold)

        writer.save()

    def _write_csv(self, mapped_df):
        mapped_df.to_csv(
            self.map_file,
            index=False
        )
        if not os.path.isfile(self.map_file):
            raise MappingException('Save mapping file failed.')

    def save_mapping_in_csv(
            self, oid=None, ypath=None, mib_to_yang_paths={}
    ):
        """Save a mapping in the local mapping file repository

        Args:
            oid (str): Identifier in MIB hierarchy
            ypath (str): YANG XPath
            mib_to_yang_paths (dict): OIDs mapped to YANG XPaths
        """
        # TODO: oid and ypath not used.
        if os.path.isfile(self.map_file):
            # open and read
            mapped_df = self.read_map_file(self.map_file)
            for oid, xpath in mib_to_yang_paths.items():
                if xpath:
                    if mapped_df.loc[mapped_df['OID'] == oid].empty:
                        # new walk with existing map file
                        mapped_df.loc[len(mapped_df.index)] = [
                            oid, xpath, self.module
                        ]
                    elif mapped_df.loc[
                        mapped_df['OID'] == oid, 'YANG Xpath'
                    ].values[0] == xpath:
                        # unchanged mapping
                        continue
                    else:
                        # new mapping
                        mapped_df.loc[
                            mapped_df['OID'] == oid, 'YANG Xpath'
                        ] = xpath
                        mapped_df.loc[
                            mapped_df['OID'] == oid, 'YANG Module'
                        ] = self.module
        else:
            mapped_dict = {'OID': [], 'YANG Xpath': [], 'YANG Module': []}
            for mib_path in self.mib_paths:
                oid = mib_path['oid']
                if oid in mib_to_yang_paths and mib_to_yang_paths[oid]:
                    mapped_dict['OID'].append(oid)
                    mapped_dict['YANG Xpath'].append(
                        mib_to_yang_paths[oid]
                    )
                    module = self.module_matches.get(mib_to_yang_paths[oid])
                    mapped_dict['YANG Module'].append(module or self.module)
                else:
                    mapped_dict['OID'].append(oid)
                    mapped_dict['YANG Xpath'].append('')
                    mapped_dict['YANG Module'].append('')

            if len(mapped_dict['OID']) == 0 and oid:
                mapped_dict['OID'] = [oid]
                mapped_dict['YANG Xpath'] = [ypath]
                mapped_dict['YANG Module'].append('')

            mapped_df = pd.DataFrame(mapped_dict)
        self._write_csv(mapped_df)

    def delete_mapping_in_csv(self, oid):
        """Delete a single mapping by removing YANG XPath from target row

        Args:
            oid (str): Identifier in MIB hierarchy
            mib_file (str): MIB module name
            yang_module (str): YANG module name
        """
        if os.path.exists(self.map_file):
            mapped_df = self.read_map_file(self.map_file)
            # Find xpath at OID row
            ypath = mapped_df.loc[mapped_df.OID == oid]
            if len(ypath) == 0:
                raise KeyError('OID "{0}" not found'.format(oid))
            # Unset YANG Xpath for that OID
            mapped_df.loc[mapped_df.OID == oid, 'YANG Xpath'] = ''
            mapped_df.loc[mapped_df.OID == oid, 'YANG Module'] = ''

            self._write_csv(mapped_df)


def process_import_data(file_data, file_path, user):
    """Extract MIB/YANG paths and mappings from frontend data

    Args:
        file_data (list): List of mapped and unmapped dict.

    Returns:
        tuple: OIDs list, YANG XPaths list, and MIB to YANG path map
    """
    yang_paths = []
    mib_paths = []
    mib_to_yang_paths = {}

    for data in file_data:
        if 'mapped' in data and isinstance(data['mapped'], str):
            # string buffer
            with open(file_path, 'w') as fd:
                fd.write(data['mapped'])
            break
        elif isinstance(data, dict):
            mapped = data['mapped']
            for mapping in mapped:
                if len(mapping) >= 2:
                    oid = mapping[0]
                    ypath = mapping[1]
                elif len(mapping) == 1:
                    oid = mapping[0]
                    ypath = None
                else:
                    log.error('Invalid mapping {0}'.format(str(mapping)))
                    continue
                if oid == 'OID':
                    # header row
                    continue
                if ypath:
                    mib_to_yang_paths[oid] = ypath
                mib_paths.append({
                    'oid': oid,
                    'value': oid,
                    # Random ID to help frontend rendering
                    'id': uuid.uuid4().__str__()
                })

        myw = MibYangWriter.get(
            file_path,
            user,
            mib_paths,
            yang_paths
        )
        myw.save_mapping_in_csv(mib_to_yang_paths=mib_to_yang_paths)

    return (mib_paths, yang_paths, mib_to_yang_paths)


def show_mapping_data(filepath, user):
    if not os.path.isfile(filepath):
        raise MappingException('Cannot locate {0}'.format(filepath))
    myw = MibYangWriter(filepath, user)
    return myw.get_mapping_data(myw.map_file)
