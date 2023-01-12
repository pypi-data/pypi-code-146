"""
 * Created by Synerty Pty Ltd
 *
 * This software is open source, the MIT license applies.
 *
 * Website : http://www.synerty.com
 * Support : support@synerty.com
"""

from txhttputil.site.ResourceUtil import RESOURCES
from txhttputil.site.StaticFileResource import StaticFileResource
from txhttputil.site.StaticFileMultiPath import StaticFileMultiPath
from txhttputil.site.AuthUserDetails import AuthUserDetails


class RootResource(StaticFileResource):
    """ Root Resource

    This resource is the root or subroot of a resource tree.
    It first looks for resources created with "createRoot
    """


def createRootResource(userAccess: AuthUserDetails, staticFileRoot: StaticFileMultiPath):
    rootResource = RootResource(userAccess, staticFileRoot=staticFileRoot)
    callResourceCreators(RESOURCES, rootResource, userAccess)

    return rootResource
