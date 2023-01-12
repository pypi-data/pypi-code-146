from twisted.web import resource
from twisted.web.server import NOT_DONE_YET


class RedirectToHttpsResource(resource.Resource):
    """
    I redirect to the same path at a given URL scheme
    @param newScheme: scheme to redirect to (e.g. https)
    """

    isLeaf = 0
    newScheme = b'https'

    def __init__(self, newPort):
        resource.Resource.__init__(self)
        self.newPort = newPort

    def render(self, request):
        newURLPath = request.URLPath()

        # TODO Double check that == gives the correct behaviour here
        if newURLPath.scheme == self.newScheme:
            raise ValueError("Redirect loop: we're trying to redirect"
                             " to the same URL scheme in the request")

        newURLPath.scheme = self.newScheme
        newURLPath.netloc = b'%s:%s' % (newURLPath.netloc.split(b':')[0],
                                        str(self.newPort).encode())

        request.redirect(str(newURLPath).encode())
        request.finish()
        return NOT_DONE_YET

    def getChild(self, name, request):
        return self
