# -*- coding: utf-8 -*-

"""
Module to compare two HDF5 format files.
Adapted from https://gitlab.obspm.fr/slion/hdf5_compare and https://github.com/NeurodataWithoutBorders/diff
"""

import logging
import sys

import h5py
import numpy

class Hdf5Reader:
    def __init__(self, logger=logging):
        self.logger = logger

    def open_hdf5_file(self, filepath):
        """
        Read the HDF5 file

        :return: HDF5 file
        """
        try:
            hdf5_file = h5py.File(filepath, 'r')
            return hdf5_file
        except IOError:
            self.logger.error("Unable to open file '%s'" % filepath)
            sys.exit(1)

    def read_attributes(self, hval):
        """
        Read the group/dataset attributes

        :return: the group/dataset attributes
        """
        attr = {}
        for k in hval.attrs:
            attr[k] = type(hval.attrs[k])
        return attr

    def read_group(self, hval):
        """
        Extract a summary of the group

        :return: Summary of the group
        """

        return {'attr': self.read_attributes(hval), 'htype': 'group'}

    def read_data(self, hval):
        """
        Extract a summary of the dataset

        :return: Summary of the dataset
        """
        data_value = hval[()]  # hval.value has been deprecated
        return {'attr': self.read_attributes(hval),
                'value': data_value,
                'htype': 'dataset',
                'dtype': type(data_value)}

    #
    def evaluate_group(self, path, grp):
        """
        Creates and returns a summary description for every element in a group

        :param path: Path in the group
        :param grp:
        :return:
        """
        result = {}
        for k, v in grp.items():
            if isinstance(v, h5py.Dataset):
                result[k] = self.read_data(v)
            elif isinstance(v, h5py.Group):
                result[k] = self.read_group(v)
            else:
                raise Exception('Unknown h5py type: %s (%s -- %s)' % (type(v), path, k))
        return result


class Hdf5Diff(Hdf5Reader):
    def __init__(self, filepath1, filepath2, group_path1, group_path2,
        exclude_attr=[], logger=logging):
        # set up the logger
        super().__init__(logger)

        # store the file/group paths
        self.filepath1 = filepath1
        self.filepath2 = filepath2
        self.group_path1 = group_path1
        self.group_path2 = group_path2

        # create a list to store the result of the files comparison
        self.diff_list = []

        # store the attribute to ignore
        self.exclude_attr = exclude_attr

    def compare_dataset(self, path, name, dataset1, dataset2):
        # compare dtypes
        if dataset1[name]['dtype'] != dataset2[name]['dtype']:
            d1 = dataset1[name]['dtype']
            d2 = dataset2[name]['dtype']
            self.register_diff(path, 'DIFF_DTYPE', (d1, d2), )

        # compare values
        v1 = dataset1[name]['value']
        v2 = dataset2[name]['value']
        try:
            if not numpy.allclose(v1, v2, equal_nan=True):
                raise ValueError
        except ValueError:
            self.register_diff(path + name, 'DIFF_DATA', (v1, v2))
        except TypeError:
            # Try to compare row by row (only if same length)
            if v1.shape != v2.shape:
                self.register_diff(path + name, 'DIFF_DATA', (v1, v2))
            else:
                for i in range(v1.shape[0]):
                    if len(numpy.array(v1[i]).shape) > 0:
                        if any(v1[i] != v2[i]):
                            self.register_diff(path + name, 'DIFF_DATA', (v1, v2))
                            break
                    else:
                        if v1[i] != v2[i]:
                            self.register_diff(path + name, 'DIFF_DATA', (v1, v2))
                            break
        except:
            raise Exception(f'Datasets {path+name} cannot be compared')
        else:
            pass

        # compare attributes
        for k in dataset1[name]['attr']:
            if self.exclude_attr and k in self.exclude_attr:
                continue
            if k not in dataset2[name]['attr']:
                self.register_diff(path + name, 'DIFF_UNIQ_ATTR', (k,), file_id=1)

        for k in dataset2[name]['attr']:
            if self.exclude_attr and k in self.exclude_attr:
                continue
            if k not in dataset1[name]['attr']:
                self.register_diff(path + name, 'DIFF_UNIQ_ATTR', (k,), file_id=2)

        for k in dataset1[name]['attr']:
            if self.exclude_attr and k in self.exclude_attr:
                continue
            if k in dataset2[name]['attr']:
                v1 = dataset1[name]['attr'][k]
                v2 = dataset2[name]['attr'][k]
                if v1 != v2:
                    self.register_diff(path + name, 'DIFF_ATTR_DTYPE', (k, v1, v2))

    def compare_group(self, path, name, desc1, desc2):

        # compare attributes
        for k in desc1[name]['attr']:
            if self.exclude_attr and k in self.exclude_attr:
                continue
            if k not in desc2[name]['attr']:
                self.register_diff(path + name, 'DIFF_UNIQ_ATTR', (k,), file_id=1)
        for k in desc2[name]['attr']:
            if self.exclude_attr and k in self.exclude_attr:
                continue
            if k not in desc1[name]['attr']:
                self.register_diff(path + name, 'DIFF_UNIQ_ATTR', (k,), file_id=2)

    def register_diff(self, path, error_code, values, file_id=None):

        error_messages = {
            'DIFF_OBJECTS': '[{path}] Different element types: {values[0]} and {values[1]}',
            'DIFF_UNIQUE': '[{path}] Element {values[0]} only in file {file_id}',
            'DIFF_UNIQ_ATTR': '[{path}] Attribute {values[0]} only in file {file_id}',
            'DIFF_ATTR_DTYPE': '[{path}] Attribute {values[0]} has different type: {values[1]} and {values[2]}',
            'DIFF_DATA': '[{path}] Different data: {values[0]} and {values[1]}',
            'DIFF_DTYPE': '[{path}] Different dtypes: {values[0]} and {values[1]}',
        }

        error_message = error_messages.get(error_code, None)

        if error_message is None:
            raise Exception('Unknown error_code %s' % (error_code,))

        content = {'path': path, 'values': values, 'error_code': error_code}

        if file_id is not None:
            content['file_id'] = file_id

        # store the error
        self.diff_list.append(content)

        # and send logs
        self.logger.info(error_message.format(path=path, values=values, file_id=file_id))

    def diff_groups(self, grp1, grp2, path='/'):
        self.logger.debug('Examining ' + path)

        # get the groups content
        desc1 = self.evaluate_group(path, grp1)
        desc2 = self.evaluate_group(path, grp2)

        # create a list to store common parts
        common = []

        # loop over group 1 and store the common keys
        for k in desc1:
            if k in desc2:
                common.append(k)
            else:
                self.register_diff(path, 'DIFF_UNIQUE', (k,), file_id=1)

        # get the keys specific to the group 2
        for k in desc2:
            if k not in desc1:
                self.register_diff(path, 'DIFF_UNIQUE', (k,), file_id=2)

        # loop over common keys
        for name in common:
            self.logger.debug('\t' + name)

            # compare types
            h1 = desc1[name]['htype']
            h2 = desc2[name]['htype']
            if h1 != h2:
                self.register_diff(path, 'DIFF_OBJECTS', (h1, h2), )
                # different hdf5 types -- don't try to compare further
                continue

            # call the appropriate method(s) depending on the node type
            if desc1[name]['htype'] == 'dataset':
                # handle dataset
                self.compare_dataset(path, name, desc1, desc2)
            elif desc1[name]['htype'] == 'group':
                # handle groups
                self.compare_group(path, name, desc1, desc2)
                # recurse into subgroup
                self.diff_groups(grp1[name], grp2[name], path=path + name + '/')
            else:
                # handle unrecognized hdf5 objects
                self.logger.warning("Element is not a recognized type (%s) and isn't being evaluated" % h1)
                continue

    def diff_files(self):
        self.logger.debug("Comparing '%s' and '%s'" % (self.filepath1, self.filepath2))
        group1 = self.open_hdf5_file(self.filepath1)[self.group_path1]
        group2 = self.open_hdf5_file(self.filepath2)[self.group_path2]

        self.diff_groups(group1, group2)
        return self.diff_list
