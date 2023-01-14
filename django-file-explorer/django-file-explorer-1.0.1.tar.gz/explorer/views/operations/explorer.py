""" 
Author:		 Muhammad Tahir Rafique
Date:		 2023-01-04 11:40:18
Project:	 File Explorer Lib
Description: Provide class to perform explorer related operations.
"""

import os

from django.core.paginator import Paginator

from explorer.views.validator.request import Validator
from explorer.views.utils.path import is_path_exists

class ExplorerOperations(Validator):
    def __init__(self, request, max_row_on_page=12, max_page_link=3) -> None:
        """
        Perform different operations.
        """
        Validator.__init__(self, request)
        self._max_row_on_page = max_row_on_page
        self._max_page_link = max_page_link
        return None

    def getMaxRowOnPage(self):
        """Getting maximum number of rows."""
        return self._max_row_on_page

    def getMaxPageLink(self):
        """Getting maximum number pager to display on paginator."""
        return self._max_page_link

    def getVolumeInfo(self):
        """Getting information of current selected volume."""
        # GETTING INFORMATION
        volume = self.getVolume()
        info = self.getInfo()

        # IF VOLUME IS GIVEN
        if volume:
            vol_info = info[volume]
            vol_info['name'] = volume
            return vol_info

        # GETTING VOLUME PATH
        vol_info = None
        vol_name = None
        vol_active = False
        for name, value in info.items():
            if value['active']: # Checking is volume active
                vol_active = True # Just for returning correct error if occure.
                if is_path_exists(value['path']): # Checking if path exists or not.
                    vol_name = name
                    vol_info = value
                    break
        
        # IF PATH IS NONE
        if vol_info is None:
            if vol_active:
                self.updateMessage('Active Volumes path does not exists.')
            else:
                self.updateMessage('All Volumes are deactive.')
            return None

        # APPENFING NAME INFORMATION
        vol_info['name'] = vol_name
        return vol_info

    def getLocationPath(self):
        """Get location information from request."""
        # GETTING LOCATION
        location = self.getLocation()

        # ADDING EXCEPTION
        if location is None:
            location = ''
        return location

    def getVolumeData(self):
        """Getting volume data."""
        # GETTING INFORMATION
        info = self.getInfo()
        volume_info = self.getVolumeInfo()

        volume_data = []
        # LOOPING THROUGH EACH VOLUME
        for name, data in info.items():
            # CHECKING PATH
            error = None
            path = data['path']
            if not is_path_exists(path): # Disabling volume if its path does not exists.
                error = 'path does not exists'
            
            # CHECKING ACTIVENESS
            active = data['active']
            if not active:
                error = 'disable by admin' # Disabling volume if it is inactive by admin.
            
            # CHECKING SELECTION
            selected = False
            if name == volume_info['name']:
                selected = True

            # UPDATING INFORMATION
            volume_data.append({
                'name': name,
                'selected': selected,
                'error': error,
                'url': f'?volume={name}'
            })
        return volume_data

    def getActionData(self):
        """Getting action data."""
        # GETTING INFORMATION
        volume_info = self.getVolumeInfo()
        return volume_info['actions']

    def getPageData(self, data_list):
        """Getting data in django pagination data."""
        # GETTING PAGE NUMBER INHARATED FROM PARENT
        page_number = self.getPageNumber()

        # MAKING DJANGO PAGINATOR
        p = Paginator(data_list, self.getMaxRowOnPage())
        page_data = p.get_page(page_number)
        return page_data

    def getPaginationData(self, page_data):
        """Generating context for the paginator."""
        # CHECKING WEATHER THE PAGINATOR REQUIRED
        if page_data.paginator.num_pages == 1:
            return None

        # GETTING VOLUME AND LOCATIO INFORMATION
        volume_name = self.getVolumeInfo()['name']
        location_path = self.getLocationPath()
        
        # EMPTY PAGINATOR DATA
        max_page_link = self.getMaxPageLink()
        paginator_data = {}

        # GETTING PREVIOUS PAGE LINK
        if page_data.has_previous():
            pg_num = page_data.previous_page_number()
            paginator_data['previous_page'] = {'url': f'?volume={volume_name}&location={location_path}&page={pg_num}'}

        # GETTING NEXT PAGE LINK
        if page_data.has_next():
            pg_num = page_data.next_page_number()
            paginator_data['next_page'] = {'url': f'?volume={volume_name}&location={location_path}&page={pg_num}'}

        # GETTING START PAGE LINK
        current_page_number = page_data.number
        mid_point = max_page_link // 2
        start_page_link = current_page_number - mid_point
        if start_page_link < 1:
            start_page_link = 1

        # GETTING LAST PAGE LINK
        last_page_link = current_page_number + mid_point
        if last_page_link > page_data.paginator.num_pages:
            last_page_link = page_data.paginator.num_pages
        
        # LOOPING TO GET MIDDLE PAGES
        middle_pages = []
        for page in range(start_page_link, last_page_link+1):
            # GETTING SELECTED STATUS
            if page == current_page_number:
                selected = 'active'
            else:
                selected = 'deactive'

            middle_pages.append({
                'number': page,
                'selected': selected,
                'url': f'?volume={volume_name}&location={location_path}&page={page}'
            })
        paginator_data['middle_pages'] = middle_pages
        return paginator_data

    def getCheckedFilePath(self, data_list):
        """Getting file paths which are check on frontend."""
        # GETTING CHECKBOX
        check_idx = self.getCheckboxIdx()

        # GETTING PAGE DATA
        page_data = self.getPageData(data_list)

        # GETTING VOLUME AND LOCATON PATH
        volume_path = self.getVolumeInfo()['path']
        location = self.getLocationPath()

        # MAKING FILE PATHS
        path_list = []
        for idx in check_idx:
            # GETTING SINGLE DATA
            data = page_data[idx]
            
            # MAKING PATH
            path_list.append(
                os.path.join(volume_path, location, data['name'])
            )
        return path_list