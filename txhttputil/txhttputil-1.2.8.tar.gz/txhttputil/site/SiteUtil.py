"""
 * Created by Synerty Pty Ltd
 *
 * This software is open source, the MIT license applies.
 *
 * Website : http://www.synerty.com
 * Support : support@synerty.com
"""

import logging
import platform
from typing import Optional

from twisted.internet import reactor
from twisted.internet._sslverify import trustRootFromCertificates
from twisted.web import server

from txhttputil.login_page.LoginElement import LoginElement
from txhttputil.site.AuthCredentials import (
    AllowAllAuthCredentials,
    AuthCredentials,
)
from txhttputil.site.AuthSessionWrapper import FormBasedAuthSessionWrapper
from txhttputil.site.FileUploadRequest import FileUploadRequest
from txhttputil.site.RedirectToHttpsResource import RedirectToHttpsResource
from txwebsocket.txws import WebSocketUpgradeHTTPChannel

from txhttputil.util.PemUtil import (
    PEM_CHECK_TYPE,
    parseTrustRootFromBundle,
    parsePemBundleForServer,
    parsePemBundleForTrustedPeers,
    parseDiffieHellmanParameter,
)
from txhttputil.util.SslUtil import (
    buildCertificateOptionsForTwisted,
)

logger = logging.getLogger(__name__)


def setupSite(
    name: str,
    rootResource,
    portNum: int = 8000,
    credentialChecker: AuthCredentials = AllowAllAuthCredentials(),
    enableLogin=True,
    SiteProtocol=WebSocketUpgradeHTTPChannel,
    redirectFromHttpPort: Optional[int] = None,
    enableSsl: Optional[bool] = False,
    sslEnableMutualTLS: Optional[bool] = False,
    sslBundleFilePath: Optional[str] = None,
    sslMutualTLSCertificateAuthorityBundleFilePath: Optional[str] = None,
    sslMutualTLSTrustedPeerCertificateBundleFilePath: Optional[str] = None,
    dhParamPemFilePath: Optional[str] = None,
):
    """Setup Site
    Sets up the web site to listen for connections and serve the site.
    Supports customisation of resources based on user details

    @return: Port object
    """
    logger.info(
        f"setting up http server '{name}' on port {portNum}, "
        f"with ssl '{'on' if enableSsl else 'off'}', "
        f"with ssl PEM bundle from '{sslBundleFilePath}', "
        f"with mTLS '{'on' if enableSsl else 'off'}', "
        f"with mTLS CA bundle from '{sslMutualTLSCertificateAuthorityBundleFilePath}', "
        f"with mTLS trusted peer bundle from '{sslMutualTLSTrustedPeerCertificateBundleFilePath}', "
        f"with Diffie-Hellman parameter from '{dhParamPemFilePath}'"
    )
    if redirectFromHttpPort is not None:
        setupSite(
            name="%s https redirect" % name,
            rootResource=RedirectToHttpsResource(portNum),
            portNum=redirectFromHttpPort,
            enableLogin=False,
        )

    LoginElement.siteName = name

    if enableLogin:
        protectedResource = FormBasedAuthSessionWrapper(
            rootResource, credentialChecker
        )
    else:
        logger.critical("Resource protection disabled NO LOGIN REQUIRED")
        protectedResource = rootResource

    site = server.Site(protectedResource)
    site.protocol = SiteProtocol
    site.requestFactory = FileUploadRequest

    if enableSsl:
        proto = "https"

        trustedCertificateAuthorities = None
        if sslEnableMutualTLS:
            trustedCertificateAuthorities = parseTrustRootFromBundle(
                sslMutualTLSCertificateAuthorityBundleFilePath
            )
            trustedCertificateAuthorities = trustRootFromCertificates(
                trustedCertificateAuthorities
            )

        privateKeyWithFullChain = parsePemBundleForServer(sslBundleFilePath)

        trustedPeerCertificates = None
        if sslMutualTLSTrustedPeerCertificateBundleFilePath is not None:
            trustedPeerCertificates = parsePemBundleForTrustedPeers(
                sslMutualTLSTrustedPeerCertificateBundleFilePath
            )

        dhParameters = None
        if dhParamPemFilePath is not None:
            dhParameters = parseDiffieHellmanParameter(dhParamPemFilePath)

        contextFactory = buildCertificateOptionsForTwisted(
            privateKeyWithFullChain,
            trustRoot=trustedCertificateAuthorities,
            trustedPeerCertificates=trustedPeerCertificates,
            dhParameters=dhParameters,
        )
        sitePort = reactor.listenSSL(portNum, site, contextFactory)

    else:
        proto = "http"
        sitePort = reactor.listenTCP(portNum, site)

    if platform.system() is "Linux":
        import subprocess

        ip = (
            subprocess.getoutput("/sbin/ifconfig").split("\n")[1].split()[1][5:]
        )
    else:
        ip = "0.0.0.0"

    logger.info(
        "%s is alive and listening on %s://%s:%s",
        name,
        proto,
        ip,
        sitePort.port,
    )
    return sitePort
