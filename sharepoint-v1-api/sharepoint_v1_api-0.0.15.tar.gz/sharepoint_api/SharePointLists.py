from .SharePointList import SharePointList, CasesList
from typing import List

class SharePointLists:

    _lists = None

    def __init__(self, lists):
        self._lists = lists

    def __str__(self):
        lists = ''
        for _list in self.all_lists:
            lists = lists+str(_list.Title)+'\n'
        return lists

    @property
    def all_lists(self) -> List[SharePointList]:
        '''
            Get list of all SharePointList objects
        '''
        if self._lists is None:
            self._lists = []
        return self._lists

    @property
    def all_list_titles(self) -> str:
        '''
            Get list of all SharePointList objects
        '''
        
        return [_list.Title for _list in self.all_lists]


    def get_list(self, key, SPListType: SharePointList=SharePointList) -> SharePointList:
        '''
            Get SharePointList by:
                - Index: int
                - List title: str
        '''
        if isinstance(key, int):
            return self.all_lists[key]
        elif isinstance(key, str):
            for list_object in self.all_lists:
                if list_object.Title == key:
                    return list_object
            raise KeyError("No list with title '{0}'".format(key))
        raise KeyError

    def get_cases_list(self, key) -> CasesList:
        '''
            Get SharePointList by:
                - Index: int
                - List title: str
        '''

        list_object = self.get_list(key, SPListType=CasesList)

        return CasesList(list_object.sharepoint_site, list_object.settings)
