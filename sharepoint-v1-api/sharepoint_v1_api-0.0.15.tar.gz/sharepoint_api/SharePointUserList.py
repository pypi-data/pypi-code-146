class SharePointUserList:

    _users = []
    sharepoint_site = ''

    def __init__(self, sharepoint_site, users):
        self._users = users
        self.sharepoint_site = sharepoint_site

    def __str__(self):
        n_users = len(self._users)
        if n_users == 1:
            return 'A list of 1 user'

        return f'A list of {n_users} users'
    
    def get_user_by_username(self, name):
        for user in self._users:
            if name == user.UserName:
                return user
        return

    def get_user_by_id(self, user_id):
        for user in self._users:
            if user_id == user.Id:
                return user
        return

