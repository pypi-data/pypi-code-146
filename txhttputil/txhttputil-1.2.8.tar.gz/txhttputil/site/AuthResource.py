""" 
 * view.common.uiobj.Style.py
 *
 *  Copyright Synerty Pty Ltd 2013
 *
 *  This software is proprietary, you are not free to copy
 *  or redistribute this code in any format.
 *
 *  All rights to this software are reserved by 
 *  Synerty Pty Ltd
 *
"""
from twisted.web._flatten import flattenString
from twisted.web.resource import Resource
from twisted.web.server import NOT_DONE_YET

from txhttputil.login_page.LoginElement import LoginElement


class LoginResource(Resource):
    isLeaf = True

    def render_GET(self, request):
        return self._renderLogin(request)

    def render_POST(self, request):
        return self._renderLogin(request, failed=True)

    def _renderLogin(self, request, failed=False):
        request.responseHeaders.setRawHeaders("authorization", ["basic"])

        def write(data):
            request.write(b'<!DOCTYPE html>\n')
            request.write(data)
            request.finish()

        def error(failure):
            request.write('<!DOCTYPE html>\n')
            if failure.printDetailedTraceback():
                request.request.write(failure.printDetailedTraceback())
            request.finish()

        d = flattenString(request, LoginElement(failed=failed))
        d.addCallbacks(write, error)

        return NOT_DONE_YET



class LoginSucceededResource(Resource):
    isLeaf = True

    def render_GET(self, request):
        return self._render(request)

    def render_POST(self, request):
        return self._render(request)

    def _render(self, request):
        request.redirect(request.uri)
        request.finish()
        return NOT_DONE_YET
