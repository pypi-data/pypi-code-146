import logging
from typing import Optional
from urllib.parse import urlencode

from twisted.internet import reactor, protocol
from twisted.internet.defer import succeed
from twisted.web._newclient import ResponseDone
from twisted.web.client import (
    Agent,
    BrowserLikePolicyForHTTPS,
)
from twisted.web.iweb import IBodyProducer, UNKNOWN_LENGTH
from twisted.web.server import NOT_DONE_YET
from txhttputil.site.BasicResource import BasicResource
from txhttputil.util.DeferUtil import vortexLogFailure
from zope.interface import implementer

from pytmpdir.spooled_named_temporary_file import (
    SpooledNamedTemporaryFile,
)

from txhttputil.util.SslUtil import buildSSLContextFactoryForMutualTLS

logger = logging.getLogger(__name__)


@implementer(IBodyProducer)
class BytesProducer(object):
    def __init__(self, content: SpooledNamedTemporaryFile):
        self.content = content
        self.length = UNKNOWN_LENGTH

    def startProducing(self, consumer):
        # TODO, Properly implement Producer
        self.content.seek(0)
        consumer.write(self.content.read())
        return succeed(None)

    def pauseProducing(self):
        pass

    def stopProducing(self):
        pass


class _ResponseDataRelay(protocol.Protocol):
    def __init__(self, request):
        self._request = request

    def dataReceived(self, data):
        self._request.write(data)

    def connectionLost(self, reason):
        if not reason.check(ResponseDone):
            self._request.response_code = 500
            vortexLogFailure(reason, logger)
        self._request.finish()


class HttpResourceProxy(BasicResource):
    isGzipped = True
    isLeaf = True

    def __init__(
        self,
        serverIp: str,
        serverPort: int,
        useSsl: bool = False,
        sslEnableMutualTLS: bool = False,
        sslClientCertificateBundleFilePath: Optional[str] = None,
        sslMutualTLSCertificateAuthorityBundleFilePath: Optional[str] = None,
        sslMutualTLSTrustedPeerCertificateBundleFilePath: Optional[str] = None,
    ):
        """Constructor

        @param serverIp: The IP or host name of the peek server to download from.
        @param serverPort: The port of the peek servers platform http site.
                            Not the admin site.
        @param useSsl: switch protocols between http and https
        @param sslEnableMutualTLS: switch on or off mTLS
        @param sslClientCertificateBundleFilePath: a PEM bundle file that
                    contains a pair of key and certificate for this web client
        @sslMutualTLSCertificateAuthorityBundleFilePath：CA bundle file path
                                            for TLS client authentication
        """

        self._serverIp = serverIp
        self._serverPort = serverPort
        self._protocol = "https" if useSsl else "http"

        if useSsl and sslEnableMutualTLS:
            self._sslContextFactory = buildSSLContextFactoryForMutualTLS(
                sslClientCertificateBundleFilePath,
                sslMutualTLSCertificateAuthorityBundleFilePath,
                sslMutualTLSTrustedPeerCertificateBundleFilePath,
            )
        else:
            # use default for http or normal https
            self._sslContextFactory = BrowserLikePolicyForHTTPS()

    def render(self, request):
        # Construct an Agent.
        agent = Agent(reactor, contextFactory=self._sslContextFactory)

        url = f"{self._protocol}://{self._serverIp}:{self._serverPort}{request.path.decode()}"
        url += "?" + urlencode({k: v[0] for k, v in request.args.items()})

        headers = request.requestHeaders.copy()
        headers.removeHeader(b"host")  # The agent will reset these.

        d = agent.request(
            request.method,
            url.encode(),
            headers,
            BytesProducer(request.content),
        )

        def good(response):
            request.responseHeaders.setRawHeaders(
                b"content-type", response.headers.getRawHeaders(b"content-type")
            )
            request.response_code = response.code
            response.deliverBody(_ResponseDataRelay(request))

        def bad(failure):
            vortexLogFailure(failure, logger)
            request.response_code = 500
            request.write(str(failure.value).encode())
            request.finish()

        d.addCallbacks(good, bad)

        def closedError(failure):
            logger.error("Got closedError %s" % failure)

        request.notifyFinish().addErrback(closedError)

        return NOT_DONE_YET
