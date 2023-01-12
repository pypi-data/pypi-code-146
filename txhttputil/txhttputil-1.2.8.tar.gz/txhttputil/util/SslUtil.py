import logging
from binascii import hexlify
from typing import List, Set, Optional

from OpenSSL import crypto
from OpenSSL import SSL
from OpenSSL.crypto import FILETYPE_PEM
from twisted.internet._sslverify import (
    PrivateCertificate,
    optionsForClientTLS,
    KeyPair,
    Certificate,
    TLSVersion,
    _setAcceptableProtocols,
    ClientTLSOptions,
    OpenSSLCertificateOptions,
)
from twisted.internet.interfaces import IOpenSSLContextFactory
from twisted.internet.ssl import CertificateOptions
from twisted.python.randbytes import secureRandom

from twisted.web.client import _requireSSL
from twisted.web.iweb import IPolicyForHTTPS
from zope.interface import implementer

from txhttputil.util.PemUtil import (
    parseTrustRootFromBundle,
    parsePemBundleForClient,
    PrivateKeyWithFullChain,
    parsePemBundleForTrustedPeers,
)

logger = logging.getLogger(__name__)


@implementer(IOpenSSLContextFactory)
class _CertificateOptions(CertificateOptions):
    trustedPeers: List[Certificate] = None
    trustedPeersASN1Bytes: Set[bytes] = None

    def _makeContext(self):
        ctx = self._contextFactory(self.method)
        ctx.set_options(self._options)
        ctx.set_mode(self._mode)

        if self.certificate is not None and self.privateKey is not None:
            ctx.use_certificate(self.certificate)
            ctx.use_privatekey(self.privateKey)
            for extraCert in self.extraCertChain:
                ctx.add_extra_chain_cert(extraCert)
            # Sanity check
            ctx.check_privatekey()

        verifyFlags = SSL.VERIFY_NONE
        if self.verify:
            verifyFlags = SSL.VERIFY_PEER
            if self.requireCertificate:
                verifyFlags |= SSL.VERIFY_FAIL_IF_NO_PEER_CERT
            if self.verifyOnce:
                verifyFlags |= SSL.VERIFY_CLIENT_ONCE
            self.trustRoot._addCACertsToContext(ctx)

        def verifyCallback(
            conn: SSL.Connection,
            cert: crypto.X509,
            errno: int,
            depth: int,
            preverify_ok: int,
        ):
            # https://www.openssl.org/docs/man1.1.1/man3/X509_STORE_CTX_verify_cb.html
            #  The ok parameter to the callback indicates the value
            #  the callback should return to retain the default behaviour.
            #  If it is zero then an error condition is indicated.
            #  If it is 1 then no error occurred.
            #  If the flag X509_V_FLAG_NOTIFY_POLICY is set
            #  then ok is set to 2 to indicate the policy checking is complete.

            FAIL = 0

            # only check peer's cert - not other certs in trust chain
            #  e.g. cert -> intermediate A -> intermediate B -> root CA
            #  depth  0            1                2            3
            if depth != 0:
                # pass through the result
                return preverify_ok

            # if peer verify is disabled
            if self.trustedPeersASN1Bytes is None:
                # pass through the result
                return preverify_ok

            # if verify failed
            if preverify_ok == FAIL:
                # pass through the result
                return preverify_ok

            # get PEM from public key
            sessionPeerPublickeyBytes = crypto.dump_publickey(
                crypto.FILETYPE_ASN1, cert.get_pubkey()
            )

            # check if peer is in trust list
            if sessionPeerPublickeyBytes not in self.trustedPeersASN1Bytes:
                logger.error(
                    f"mTLS peer verify failed at depth '{depth}', presenting "
                    f"certificate '{cert.get_subject()}'"
                )
                return FAIL

            # peer verified, pass through the result
            logger.debug(
                f"mTLS peer verify success at depth '{depth}', presenting "
                f"certificate '{cert.get_subject()}'"
            )
            return preverify_ok

        ctx.set_verify(verifyFlags, verifyCallback)
        if self.verifyDepth is not None:
            ctx.set_verify_depth(self.verifyDepth)

        # Until we know what's going on with
        # https://twistedmatrix.com/trac/ticket/9764 let's be conservative
        # in naming this; ASCII-only, short, as the recommended value (a
        # hostname) might be:
        sessionIDContext = hexlify(secureRandom(7))
        # Note that this doesn't actually set the session ID (which had
        # better be per-connection anyway!):
        # https://github.com/pyca/pyopenssl/issues/845

        # This is set unconditionally because it's apparently required for
        # client certificates to work:
        # https://www.openssl.org/docs/man1.1.1/man3/SSL_CTX_set_session_id_context.html
        ctx.set_session_id(sessionIDContext)

        if self.enableSessions:
            ctx.set_session_cache_mode(SSL.SESS_CACHE_SERVER)
        else:
            ctx.set_session_cache_mode(SSL.SESS_CACHE_OFF)

        if self.dhParameters:
            ctx.load_tmp_dh(self.dhParameters._dhFile.path)
        ctx.set_cipher_list(self._cipherString.encode("ascii"))

        self._ecChooser.configureECDHCurve(ctx)

        if self._acceptableProtocols:
            # Try to set NPN and ALPN. _acceptableProtocols cannot be set by
            # the constructor unless at least one mechanism is supported.
            _setAcceptableProtocols(ctx, self._acceptableProtocols)

        return ctx


def buildCertificateOptionsForTwisted(
    privateKeyWithFullChain: PrivateKeyWithFullChain,
    trustRoot=None,
    trustedPeerCertificates: List[Certificate] = None,
    raiseMinimumTo=TLSVersion.TLSv1_2,
    lowerMaximumSecurityTo=TLSVersion.TLSv1_3,
    acceptableProtocols=None,
    dhParameters=None,
) -> CertificateOptions:
    twistedLoadedChain = PrivateKeyWithFullChain(
        privateKey=KeyPair.load(
            privateKeyWithFullChain.privateKey.as_bytes(), FILETYPE_PEM
        ).original,
        certificate=Certificate.loadPEM(
            privateKeyWithFullChain.certificate.as_bytes()
        ).original,
        intermediateCAs=[
            Certificate.loadPEM(intermediateCA.as_bytes()).original
            for intermediateCA in privateKeyWithFullChain.intermediateCAs
        ],
        rootCA=Certificate.loadPEM(
            privateKeyWithFullChain.rootCA.as_bytes()
        ).original,
    )

    if acceptableProtocols is None:
        acceptableProtocols = [b"http/1.1"]

    if trustedPeerCertificates is not None:
        # load PEMs to ASN1 bytes
        _CertificateOptions.trustedPeers = trustedPeerCertificates
        _CertificateOptions.trustedPeersASN1Bytes = set([])
        for trustedPeer in _CertificateOptions.trustedPeers:
            # load as a pyopenssl cert
            certificate: crypto.X509 = crypto.load_certificate(
                crypto.FILETYPE_PEM, trustedPeer.as_bytes()
            )
            # get publickey in ASN1 bytes
            publicKey: bytes = crypto.dump_publickey(
                crypto.FILETYPE_ASN1, certificate.get_pubkey()
            )
            # add publickey to trusted peers
            _CertificateOptions.trustedPeersASN1Bytes.add(publicKey)

    return _CertificateOptions(
        privateKey=twistedLoadedChain.privateKey,
        certificate=twistedLoadedChain.certificate,
        extraCertChain=twistedLoadedChain.intermediateCAs,
        trustRoot=trustRoot,
        raiseMinimumTo=raiseMinimumTo,
        lowerMaximumSecurityTo=lowerMaximumSecurityTo,
        acceptableProtocols=acceptableProtocols,
        dhParameters=dhParameters,
    )


@implementer(IPolicyForHTTPS)
class MutualAuthenticationPolicyForHTTPS:
    def __init__(
        self,
        clientCertificate: PrivateCertificate = None,
        trustRoot=None,
        trustedPeers=None,
    ):
        self._extraCertificateOptions = {}

        if clientCertificate is not None:
            self._clientCertificate = clientCertificate
            self._extraCertificateOptions.update(
                privateKey=clientCertificate.privateKey.original,
                certificate=clientCertificate.original,
            )
        self._trustRoot = trustRoot
        self._trustedPeers = trustedPeers
        self._trustedPeersASN1Bytes = None

        if trustedPeers is not None:
            self._trustedPeersASN1Bytes = set([])
            for trustedPeer in self._trustedPeers:
                # load as a pyopenssl cert
                certificate: crypto.X509 = crypto.load_certificate(
                    crypto.FILETYPE_PEM, trustedPeer.as_bytes()
                )
                # get publickey in ASN1 bytes
                publicKey: bytes = crypto.dump_publickey(
                    crypto.FILETYPE_ASN1, certificate.get_pubkey()
                )
                # add publickey to trusted peers
                self._trustedPeersASN1Bytes.add(publicKey)

        # verify enabled
        self._verifyFlags = SSL.VERIFY_PEER
        # verifyOnce:
        self._verifyFlags |= SSL.VERIFY_CLIENT_ONCE
        if self._trustRoot or self._trustedPeers:
            # verify mTLS peer
            self._verifyFlags |= SSL.VERIFY_FAIL_IF_NO_PEER_CERT

    @_requireSSL
    def creatorForNetloc(self, hostname, port):
        certificateOptions = OpenSSLCertificateOptions(
            trustRoot=self._trustRoot,
            acceptableProtocols=[b"http/1.1"],
            **self._extraCertificateOptions,
        )
        context = certificateOptions.getContext()

        def verifyCallback(
            conn: SSL.Connection,
            cert: crypto.X509,
            errno: int,
            depth: int,
            preverify_ok: int,
        ):
            # same as `_CertificateOptions._makeContext.verifyCallback`

            # https://www.openssl.org/docs/man1.1.1/man3/X509_STORE_CTX_verify_cb.html
            #  The ok parameter to the callback indicates the value
            #  the callback should return to retain the default behaviour.
            #  If it is zero then an error condition is indicated.
            #  If it is 1 then no error occurred.
            #  If the flag X509_V_FLAG_NOTIFY_POLICY is set
            #  then ok is set to 2 to indicate the policy checking is complete.

            FAIL = 0

            # only check peer's cert - not other certs in trust chain
            #  e.g. cert -> intermediate A -> intermediate B -> root CA
            #  depth  0            1                2            3
            if depth != 0:
                # pass through the result
                return preverify_ok

            # if peer verify is disabled
            if self._trustedPeersASN1Bytes is None:
                # pass through the result
                return preverify_ok

            # if verify failed
            if preverify_ok == FAIL:
                # pass through the result
                return preverify_ok

            # get PEM from public key
            sessionPeerPublickeyBytes = crypto.dump_publickey(
                crypto.FILETYPE_ASN1, cert.get_pubkey()
            )

            # check if peer is in trust list
            if sessionPeerPublickeyBytes not in self._trustedPeersASN1Bytes:
                logger.error(
                    f"mTLS peer verify failed at depth '{depth}', presenting "
                    f"certificate '{cert.get_subject()}'"
                )
                return FAIL

            # peer verified, pass through the result
            logger.debug(
                f"mTLS peer verify success at depth '{depth}', presenting "
                f"certificate '{cert.get_subject()}'"
            )
            return preverify_ok

        context.set_verify(self._verifyFlags, verifyCallback)
        return ClientTLSOptions(hostname, context)


def buildSSLContextFactoryForMutualTLS(
    sslClientCertificateBundleFilePath: Optional[str],
    sslTrustedPeerCertificateAuthorityBundleFilePath: Optional[str],
    sslMutualTLSTrustedPeerCertificateBundleFilePath: Optional[str],
) -> MutualAuthenticationPolicyForHTTPS:
    trustRoot = None
    if sslTrustedPeerCertificateAuthorityBundleFilePath:
        trustRoot = parseTrustRootFromBundle(
            sslTrustedPeerCertificateAuthorityBundleFilePath
        )
    clientCertificate = None
    if sslClientCertificateBundleFilePath is not None:
        bank: PrivateKeyWithFullChain = parsePemBundleForClient(
            sslClientCertificateBundleFilePath
        )
        clientKeyCertificateBytes: bytes = bank.privateKey.as_bytes()
        clientKeyCertificateBytes += b"\n"
        clientKeyCertificateBytes += bank.certificate.as_bytes()
        clientCertificate = PrivateCertificate.loadPEM(
            clientKeyCertificateBytes
        )

    trustedPeerCertificates = None
    if sslMutualTLSTrustedPeerCertificateBundleFilePath is not None:
        trustedPeerCertificates = parsePemBundleForTrustedPeers(
            sslMutualTLSTrustedPeerCertificateBundleFilePath
        )

    return MutualAuthenticationPolicyForHTTPS(
        clientCertificate=clientCertificate,
        trustRoot=trustRoot,
        trustedPeers=trustedPeerCertificates,
    )
