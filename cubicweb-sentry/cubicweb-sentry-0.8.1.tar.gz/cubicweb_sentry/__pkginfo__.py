# pylint: disable=W0622
"""cubicweb-sentry application packaging information"""

modname = "sentry"
distname = "cubicweb-sentry"

numversion = (0, 8, 1)
version = ".".join(str(num) for num in numversion)

license = "LGPL"
author = "LOGILAB S.A. (Paris, FRANCE)"
author_email = "contact@logilab.fr"
description = "support for Sentry (getsentry.com)"
web = "https://forge.extranet.logilab.fr/cubicweb/cubes/%s" % distname

classifiers = [
    "Environment :: Web Environment",
    "Framework :: CubicWeb",
    "Programming Language :: Python",
    "Programming Language :: JavaScript",
]

__depends__ = {"cubicweb": ">= 3.24.0, < 3.39.0", "sentry-sdk": "<1.9.8"}
__recommends__ = {}
