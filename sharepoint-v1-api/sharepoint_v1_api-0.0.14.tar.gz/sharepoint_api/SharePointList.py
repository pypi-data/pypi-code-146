# from .SharePointAPI import SharePointAPI as SP
from sharepoint_api.SharePointTimeRegistration import TimeRegistration
from .SharePointListItem import SharePointListItem, SharepointSiteCase
from typing import List
import json

class SharePointList:
    '''
    '''

    settings = {}
    _items = None
    sharepoint_site = ""
    SPItem = SharePointListItem

    CHANGE_DETECTED = False
    SAVE_ON_CHANGE = False
    JSON_FILENAME = None

    def __init__(self, sharepoint_site, settings: dict = None, items: List[SPItem] = None):
        self.sharepoint_site = sharepoint_site
        self.settings = settings
        self._items = items

    def __str__(self):
        items = ''
        for _item in self.all_items:
            items = items+str(_item.Title)+'\n'
        return items

    def __del__(self):
        if self.CHANGE_DETECTED and self.SAVE_ON_CHANGE and self.JSON_FILENAME is not None:
            print('Change was definiteley detected')
            print('Saving items')
            self.save_as_json(self.JSON_FILENAME)

    @property
    def all_items(self) -> List[SPItem]:
        '''
            Get list of all SharePointListItem objects
        '''
        if self._items is None:
            self._items = []
        return self._items

    @property
    def Title(self) -> str:
        return self.settings['Title']

    @property
    def guid(self):
        return self.settings['Id']

    def append_items(self, items):

        if isinstance(items, list):
            for item in items:
                item._list = self
            _items = self.all_items.extend(items)
            self.CHANGE_DETECTED = True
        elif isinstance(items, self.SPItem):
            items._list = self
            _items = self.all_items.append(items)
            self.CHANGE_DETECTED = True

    def get_item_by_name(self, name):
        '''
        '''
        for item in self.all_items:
            if name ==item.Title:
                return item
        return None

    def get_item_by_id(self, id):
        '''
        '''
        for item in self._items:
            if id ==item.Id:
                return item
        return None

    def get_items_by_assigned_id(self, id) -> List[SPItem]:
        '''
        '''
        items = []
        for item in self._items:
            if id == item.ResponsibleId:
                items.append(item)
        return items

    def save_as_json(self, file_name):

        out_dict = {
            'sharepoint_site': self.sharepoint_site,
            'GUID': self.guid,
            'Settings': self.settings,
            "cases": [{'settings': case.settings, 'versions': case._versions} for case in self.all_items]
            }

        with open(file_name, 'w') as fp:
            json.dump(out_dict, fp)
        
        self.CHANGE_DETECTED = False


class CasesList(SharePointList):
    SPItem = SharepointSiteCase

class TimeRegistrationList(SharePointList):
    SPItem = TimeRegistration
