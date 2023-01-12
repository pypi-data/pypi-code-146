""" 
Author:		 Muhammad Tahir Rafique
Date:		 2023-01-03 10:27:24
Project:	 File Explorer
Description: Provide class to validate the user request.
"""

from explorer.views.extractor.request import RequestDataExtractor
from explorer.views.extractor.user import UserDataExtractor

from explorer.views.utils.path import is_path_exists

class Validator(RequestDataExtractor, UserDataExtractor):
    def __init__(self, request) -> None:
        """
        Validate the user request. If request is invalid then error is 
        send to frontend. It will validate both GET and POST request.
        """
        RequestDataExtractor.__init__(self, request)
        UserDataExtractor.__init__(self, request.user)

        self._message = None
        self._info = None
        return None

    def getMessage(self):
        """Return the message if exist otherwise return None."""
        return self._message
    
    def updateMessage(self, message):
        """Update the message."""
        self._message = message
        return None

    def getUserInfo(self):
        """Fatch the user information."""
        if self._info is None:
            self._info = self.getInfo()
        return self._info

    def isVolumeValid(self):
        """Check weather the volume is valid or not."""
        # COLLECTING INFORMATION
        info = self.getUserInfo()
        volume = self.getVolume()
        method = self.getRequestMethod()

        # IMPLIMENTING CONDITIONS
        volume_list = list(info.keys())
        valid = False
        if len(volume_list) == 0:
            valid = False
            message = 'No Volume assigned. Please contact admin.'
        elif method == 'GET':
            if volume is None:
                any_ative = False
                for vol in volume_list:
                    if info[vol]['active']:
                        any_ative = True
                        break
                if any_ative:
                    valid =  True
                else:
                    valid = False
                    message = 'All Volumes are deactive.'
            elif volume in volume_list:
                if info[volume]['active']: # Checking volume is active or not
                    if is_path_exists(info[volume]['path']):
                        valid = True
                    else:
                        valid = False
                        message = f'Volume {volume} path does not exists.'
                else:
                    valid = False
                    message = f'Volume {volume} is not active.'
            else:
                valid = False
                message = f'Invalid Volume: {volume}'
        elif method == 'POST':
            if volume in volume_list:
                valid = True
            else:
                valid = False
                message = f'Invalid Volume: {volume}'
        else:
            self.updateMessage(f'Invalid Request Method: {method}')
            valid = False

        # UPDATING MESSAGE
        if not valid:
            self.updateMessage(message)
        return valid

    def isActionValid(self):
        """Check weather the action is valid or not."""
        # COLLECTING INFORMATION
        info = self.getUserInfo()
        volume = self.getVolume()
        action = self.getAction()
        method = self.getRequestMethod()

        # IMPLIMENTING CONDITIONS
        valid = False
        if method == 'GET':
            valid = True
        elif method == 'POST':
            actions = info[volume]['actions']
            if action is None:
                valid = False
            elif action in actions:
                valid = True
            else:
                valid = False
        else:
            self.updateMessage(f'Invalid Request Method: {method}')
            valid = False

        # UPDATING MESSAGE
        if not valid:
            self.updateMessage(f'Invalid Action: {action}')
        return valid

    def isLocationValid(self):
        """Check weather the action is valid or not."""
        # COLLECTING INFORMATION
        info = self.getUserInfo()
        volume = self.getVolume()
        location = self.getLocation()
        method = self.getRequestMethod()

        # IMPLIMENTING CONDITIONS
        valid = False
        if (method == 'GET') or (method == 'POST'):
            if location is None:
                valid = True
            else:
                valid = is_path_exists(info[volume]['path'], location)
        else:
            self.updateMessage(f'Invalid Request Method: {method}')
            valid = False

        # UPDATING MESSAGE
        if not valid:
            self.updateMessage(f'Invalid Location: {location}')
        return valid

    def isCheckboxValid(self):
        """Check weather the action is valid or not."""
        # COLLECTING INFORMATION
        checbox_idx = self.getCheckboxIdx()
        method = self.getRequestMethod()

        # IMPLIMENTING CONDITIONS
        valid = False
        if method == 'GET': # Ignore in GET request
            valid = True
        elif method == 'POST':
            if len(checbox_idx) == 0:
                valid = False
            else:
                valid = True
        else:
            self.updateMessage(f'Invalid Request Method: {method}')
            valid = False

        # UPDATING MESSAGE
        if not valid:
            self.updateMessage(f'Invalid Checkbox Idx')
        return valid

    def isValid(self):
        """Check all request input and validate it."""
        # MAKING SEQUENCE
        sequence = [
            self.isVolumeValid,
            self.isActionValid,
            self.isLocationValid,
            self.isCheckboxValid,
        ]
        
        # PERFORMING OPERATIONS
        for operation in sequence:
            valid = operation()
            if not valid:
                break
        return valid