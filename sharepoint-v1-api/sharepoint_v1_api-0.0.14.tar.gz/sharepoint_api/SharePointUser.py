class SharePointUser:

    settings = None
    _users = None
    sharepoint_site = None

    def __init__(self, settings: dict = None):
        self.settings = settings

    @property
    def Id(self):
        if self.settings is None:
            return None
        return self.settings['Id']

    @property
    def Title(self):
        if self.settings is None:
            return None
        return self.settings['Title']

    @property
    def UserName(self):
        if self.settings is None:
            return None
        return self.settings['Email'].split('@')[0].lower()

    @property
    def Email(self):
        if self.settings is None:
            return None
        return self.settings['Email']    

