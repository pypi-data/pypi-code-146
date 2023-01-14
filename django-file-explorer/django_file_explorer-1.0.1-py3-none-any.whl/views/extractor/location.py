""" 
Author:		 Muhammad Tahir Rafique
Date:		 2023-01-05 10:50:48
Project:	 File Explorer
Description: Provide function to extract the data from the location.
"""

import os
import datetime

def argsort(seq):
    return sorted(range(len(seq)), key=seq.__getitem__)

def sort_files(sort_array, array_to_sort, mode='a'):
    """Sort the second list accoring to first list.
    mode: a (assending), d (decending)
    """
    # GETTING SORTING IDX
    sort_idx = argsort(sort_array)
    if mode == 'd':
        sort_idx = sort_idx[::-1]

    # LOOPING THROUGH TO MAKE NEW LIST
    new_list = []
    for idx in sort_idx:
        new_list.append(array_to_sort[idx])
    return new_list

class LocationDataExtractor():
    def __init__(self, location_path) -> None:
        """
        Extract the data from the location.
        """
        self._location_path = location_path
        return None

    def getLocationPath(self):
        """Getting location path."""
        return self._location_path

    def isLocationFile(self):
        """Check weather the given location is file."""
        return os.path.isfile(self.getLocationPath())

    def getFiles(self):
        """Getting list of file in directory."""
        # GETTING LIST OF DIR
        location_path = self.getLocationPath()
        list_dir = os.listdir(location_path)

        # SEPRATING FILES AND DIRS
        file_list, deactive_file_list, file_ctime_list = [], [], []
        for dir in list_dir:
            path = os.path.join(location_path, dir)
            if os.path.isfile(path): # If file.
                try:
                    # GETTING TIME
                    ctime = os.path.getctime(path)
                    file_ctime_list.append(ctime)
                    ftime = datetime.datetime.fromtimestamp(ctime)
                    creation_time = ftime.strftime("%d-%b-%Y %I:%M %p")

                    # GETTING SIZE
                    size = os.path.getsize(path)

                    # APPENDING INFORMATION
                    file_list.append({'name': dir, 'type': 'file', 'valid': True, 'creation_time': creation_time, 'size': size})
                except:
                    deactive_file_list.append({'name': dir, 'type': 'file', 'valid': False})
        
        # PERFORMING SORTING
        file_list = sort_files(file_ctime_list, file_list, mode='d')
        file_list += deactive_file_list
        return file_list

    def getDirectories(self):
        """Getting list of all directory."""
        # GETTING LIST OF DIR
        location_path = self.getLocationPath()
        list_dir = os.listdir(location_path)

        # SEPRATING FILES AND DIRS
        file_list, deactive_file_list, file_ctime_list = [], [], []
        for dir in list_dir:
            path = os.path.join(location_path, dir)
            if not os.path.isfile(path): # If not a file.
                try:
                    # GETTING TIME
                    ctime = os.path.getctime(path)
                    file_ctime_list.append(ctime)
                    ftime = datetime.datetime.fromtimestamp(ctime)
                    creation_time = ftime.strftime("%d-%b-%Y %I:%M %p")

                    # GETTING SIZE
                    size = os.path.getsize(path)

                    # APPENDING INFORMATION
                    file_list.append({'name': dir, 'type': 'directory', 'valid': True, 'creation_time': creation_time, 'size': size})
                except:
                    deactive_file_list.append({'name': dir, 'type': 'directory', 'valid': False})
        
        # PERFORMING SORTING
        file_list = sort_files(file_ctime_list, file_list, mode='d')
        file_list += deactive_file_list
        return file_list