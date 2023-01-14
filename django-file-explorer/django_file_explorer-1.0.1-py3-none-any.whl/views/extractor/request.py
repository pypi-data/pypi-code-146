""" 
Author:		 Muhammad Tahir Rafique
Date:		 2023-01-02 11:35:18
Project:	 File Explorer
Description: Provide function to extract usefull information from the request.
"""

class RequestDataExtractor():
    def __init__(self, request) -> None:
        """This class will receive request object and get usefull information from it."""
        self._request = request
        return None
    
    def getRequestMethod(self):
        """Getting request method."""
        return self._request.method

    def _getFieldValue(self, field_name):
        """Getting single value using field name."""
        # GETTING METHOD
        method = self.getRequestMethod()

        # GETTING DATA
        if method == 'GET':
            data = self._request.GET.get(field_name)
        else:
            data = self._request.POST.get(field_name)
        return data

    def getVolume(self):
        """Get volume information from request."""
        return self._getFieldValue('volume')

    def getAction(self):
        """Get action information from request."""
        return self._getFieldValue('action')

    def getLocation(self):
        """Get location information from request."""
        return self._getFieldValue('location')

    def getPageNumber(self):
        """Get page number information from request."""
        return self._getFieldValue('page')

    def getCheckboxIdx(self):
        """Getting list of checkbox idx."""
        check_idx = self._request.POST.getlist('check_idx')
        check_idx = [int(idx) for idx in check_idx]
        return check_idx
