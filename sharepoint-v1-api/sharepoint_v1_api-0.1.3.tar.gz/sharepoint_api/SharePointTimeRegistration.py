from datetime import datetime

from sharepoint_api.SharePointListItem import SharePointListItem
# from .SharePointAPI import SharePointAPI as SP

class TimeRegistration(SharePointListItem):
    ''' 
    '''

    _DoneBy = None

    @property
    def Created(self) -> datetime:
        'Timestamp of when the item was created'
        if 'DoneDate' not in self.settings:
            return None
        elif self.settings['DoneDate'] is None:
            return None
        else:
            return datetime.strptime(self.settings['DoneDate'], '%Y-%m-%dT%H:%M:%SZ')
    
    @property
    def Hours(self) -> str:
        return self.settings['Hours']

    @property
    def DoneById(self) -> str:
        return self.settings['DoneById']

    @property
    def DoneBy(self) -> str:
        if not self._DoneBy:
            user_list = self.sp.get_users(self.sharepoint_site)
            self._DoneBy = user_list.get_user_by_id(self.DoneById)
        return self._DoneBy
    
    @property
    def DoneUsername(self) -> str:
        return self.DoneBy.UserName

    @property
    def CaseId(self) -> str:
        return self.settings['CaseId']
    
    @property
    def WorkPackageId(self) -> str:
        return self.settings['WorkPackageId']
    
