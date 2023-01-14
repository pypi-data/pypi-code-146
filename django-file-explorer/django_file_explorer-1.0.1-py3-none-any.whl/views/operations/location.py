""" 
Author:		 Muhammad Tahir Rafique
Date:		 2023-01-04 10:45:31
Project:	 File Explorer
Description: Provide class to perform location related operations.
"""

import os
import shutil
import tempfile
import datetime

from explorer.views.extractor.location import LocationDataExtractor

class LocationOperations(LocationDataExtractor):
    def __init__(self, volume_info, location_path) -> None:
        """Perovide location related operations."""
        # INITALIZING CLASS
        LocationDataExtractor.__init__(self, os.path.join(volume_info['path'], location_path))
        self._volume_name = volume_info['name']
        self._volume_path = volume_info['path']
        self._rel_location_path = location_path
        return None

    def getRelLocationPath(self):
        """Getting relative location path."""
        return self._rel_location_path

    def getVolumePath(self):
        """Getting volume path."""
        return self._volume_path
    
    def getVolumeName(self):
        """Getting volume name."""
        return self._volume_name

    def getData(self):
        """Getting list of files."""
        # GETTING FILE LIST
        file_data = self.getFiles()

        # GETTING DIR LIST
        dir_data = self.getDirectories()

        # APPENDING INFORMATION
        data_list = dir_data + file_data

        # ADDING EXTRA INFORMATION IN DATA
        location = self.getRelLocationPath()
        volume_name = self.getVolumeName()
        for data in data_list:
            # GETTING RELATIVE PATH
            name = data['name']
            rel_path = os.path.join(location, name)

            # MAKING URL
            url = f'volume={volume_name}&location={rel_path}'

            # ADDING INFORMATION
            data['url'] = url
        return data_list

    def getDataSummary(self):
        """Getting summary of the data."""
        # GETTING FILE LIST
        file_data = self.getFiles()

        # GETTING DIR LIST
        dir_data = self.getDirectories()

        # GETTING COUNT
        count = {'file': len(file_data), 'directory': len(dir_data)}
        return count

    def getNavigationBarData(self):
        """Getting navigationbar data."""
        # GRTTING INFORMATION
        location = self.getRelLocationPath()
        volume_name = self.getVolumeName()

        # MAKING NAVIGATION BAR
        sep_locations = location.split(os.path.sep)
        nev_location_list = [{'name': volume_name, 'url': f'volume={volume_name}'}]
        rel_loc = ''
        for loc in sep_locations:
            if loc == '':
                continue
            rel_loc = os.path.join(rel_loc, loc)
            nev_location_list.append({'name': loc, 'url': f'volume={volume_name}&location={rel_loc}'})
        return nev_location_list

    def _deleteFiles(self, path_list):
        """Deleting file or dir."""
        for file_path in path_list:
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                else:
                    shutil.rmtree(file_path, ignore_errors=True)
            except:
                pass
        return None

    def _zipFile(self, file_paths):
        """Zip file or dir."""
        # CHECKING FILE
        if len(file_paths) == 1:
            # CHECKING FILE OR DIR
            if os.path.isfile(file_paths[0]):
                return file_paths[0]

        # MAKING COPY OF FILE IN TEMP DIR
        tmp_dir = tempfile.gettempdir()
        content_dir = os.path.join(tmp_dir, datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
        os.makedirs(content_dir)

        # IF SINGLE DIRECTORY
        if len(file_paths) == 1:
            file_name = os.path.basename(file_paths[0])
            zip_dir = os.path.join(content_dir, file_name)
        else:
            zip_dir = content_dir

        # COPYING FILE TO ZIP DIR
        for file_path in file_paths:
            # GETTING FILE NAME
            file_name = os.path.basename(file_path)

            # COPYING FILES
            dst_path = os.path.join(content_dir, file_name)
            if os.path.isfile(file_path):
                shutil.copy(file_path, dst_path)
            else:
                shutil.copytree(file_path, dst_path)

        # ZIPPING LOCATION
        shutil.make_archive(zip_dir, 'zip', zip_dir)
        return zip_dir + '.zip'

    def performAction(self, path_list, action):
        """Performing action on the paths."""
        # PERFORMING OPERATION
        zip_file_path = None
        if action == 'delete':
            self._deleteFiles(path_list)
        elif action == 'download':
            try:
                zip_file_path = self._zipFile(path_list)
            except:
                pass
        else:
            pass
        return zip_file_path