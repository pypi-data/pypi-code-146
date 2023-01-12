import logging
import textwrap
from collections import namedtuple
from datetime import datetime
from functools import partial
from pathlib import Path
from typing import List, Dict, NamedTuple, Union, Tuple, Literal

import pem
from OpenSSL.crypto import (
    load_certificate,
    FILETYPE_PEM,
    X509Store,
    X509StoreContext,
    X509StoreContextError,
)
from cryptography.hazmat._oid import NameOID
from cryptography.x509.base import Version
from cryptography.x509.oid import ExtendedKeyUsageOID
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives.serialization import (
    load_pem_private_key,
    Encoding,
    ParameterFormat,
    load_pem_parameters,
)
from cryptography.x509 import (
    Certificate,
    load_pem_x509_certificate,
    BasicConstraints,
    ExtensionNotFound,
    Extension,
    KeyUsage,
    ExtendedKeyUsage,
)
from pem import AbstractPEMObject
from treelib import Tree
from twisted.internet import ssl
from twisted.internet._sslverify import (
    Certificate as TxCertificate,
    OpenSSLDiffieHellmanParameters,
)
from twisted.python.filepath import FilePath

logger = logging.getLogger(__name__)


class PEM_CHECK_TYPE:
    CHECK_TYPE_SSL_SERVER_IDENTITY = 0
    CHECK_TYPE_SSL_CLIENT_IDENTITY = 1
    CHECK_TYPE_SSL_MTLS_CA = 2
    CHECK_TYPE_SSL_MTLS_PEER = 3


PemSimpleBank = namedtuple(
    "PemSimpleBank",
    [
        "privateKeys",
        "certificates",
        "rootCAs",
        "intermediateCAs",
        "bundleFilePath",
    ],
    defaults=([], [], [], [], ""),
)


class PemBank:
    MAX_COUNT = 99

    def __init__(
        self,
        pemSimpleBank: PemSimpleBank,
        pemMap: Dict[AbstractPEMObject, Certificate],
    ):
        self._pemSimpleBank = pemSimpleBank
        self._pemMap = pemMap
        self._trustTree = Tree()

    @property
    def trustChains(self) -> List[List[str]]:
        # chains in x509 common names
        return self._trustTree.paths_to_leaves()

    @property
    def privateKeys(self):
        return self._pemSimpleBank.privateKeys

    @property
    def certificates(self):
        return self._pemSimpleBank.certificates

    @property
    def rootCAs(self):
        return self._pemSimpleBank.rootCAs

    @property
    def intermediateCAs(self):
        return self._pemSimpleBank.intermediateCAs

    @property
    def bundleFilePath(self):
        return self._pemSimpleBank.bundleFilePath

    def check(
        self,
        checkType: PEM_CHECK_TYPE,
        showCheck: bool = True,
        targetHostname: str = None,
    ) -> bool:
        if checkType in [
            PEM_CHECK_TYPE.CHECK_TYPE_SSL_SERVER_IDENTITY,
            PEM_CHECK_TYPE.CHECK_TYPE_SSL_CLIENT_IDENTITY,
        ]:
            result = []
            result.append(self._checkExtendedKeyUsage(checkType))
            result.append(self._checkTrustChain(showCheck))

            if False in result:
                return False
            return True

        if checkType == PEM_CHECK_TYPE.CHECK_TYPE_SSL_MTLS_CA:
            return self._checkNumberLimits(
                maxCertificateCount=0,
                maxPrivateKeyCount=0,
                maxRootCACount=self.MAX_COUNT,
                maxIntermediateCACount=0,
            )

        if checkType == PEM_CHECK_TYPE.CHECK_TYPE_SSL_MTLS_PEER:
            return self._checkNumberLimits(
                maxCertificateCount=self.MAX_COUNT,
                maxPrivateKeyCount=0,
                maxRootCACount=0,
                maxIntermediateCACount=0,
            )

    def _checkExtendedKeyUsage(
        self,
        usageType: Literal[
            PEM_CHECK_TYPE.CHECK_TYPE_SSL_SERVER_IDENTITY,
            PEM_CHECK_TYPE.CHECK_TYPE_SSL_CLIENT_IDENTITY,
        ],
    ) -> bool:
        certificate: AbstractPEMObject = self._pemSimpleBank.certificates[0]
        certificateParsed: Certificate = self._pemMap[certificate]

        x509Version = X509Util.getX509Version(certificateParsed)
        if x509Version != Version.v3.name:
            logger.error(
                f"The server certificate from bundle "
                f"{self._pemSimpleBank.bundleFilePath} should be in "
                f"version x509 v3, got '{x509Version}'"
            )
            return False

        usages = X509Util.getExtendedKeyUsages(certificateParsed)

        if usageType == PEM_CHECK_TYPE.CHECK_TYPE_SSL_SERVER_IDENTITY:
            success = ExtendedKeyUsageOID.SERVER_AUTH in usages
            if not success:
                logger.error(
                    f"The server certificate from bundle "
                    f"'{self._pemSimpleBank.bundleFilePath}' should contain "
                    f"'serverAuth' in extended key usage, got"
                    f"{usages}"
                )
            return success

        if usageType == PEM_CHECK_TYPE.CHECK_TYPE_SSL_CLIENT_IDENTITY:
            success = ExtendedKeyUsageOID.CLIENT_AUTH in usages
            if not success:
                logger.error(
                    f"The client certificate from bundle "
                    f"'{self._pemSimpleBank.bundleFilePath}' should contain "
                    f"'clientAuth' in extended key usage, got"
                    f"{usages}"
                )
            return success

        logger.error(
            f"invalid usageType '{usageType}' to check extended key usage with."
        )
        return False

    def _checkTrustChain(self, showCheck: bool) -> bool:
        self._trustTree = self._buildTrustChain()

        if len(self.trustChains) != 1:
            logger.error(
                f"1 and only 1 chain of trust is established, "
                f"got {len(self.trustChains)} "
                f"in '{self._pemSimpleBank.bundleFilePath}'"
            )
            return False

        # e.g. x509 certificate common names in order of
        #  root CA -> intermediate -> sub-intermediate -> cert
        trustChainInCommonName = self.trustChains[0]

        # drop root CA
        trustChainInCommonName.pop(0)
        # drop certificate
        trustChainInCommonName.pop()

        # sort intermediate CAs in bank
        self._pemSimpleBank.intermediateCAs.clear()
        for intermediateCACommonName in reversed(
            trustChainInCommonName
        ):  # bottom to top
            self._pemSimpleBank.intermediateCAs.append(
                self._trustTree.nodes[intermediateCACommonName].tag
            )

        # verify the chain by openssl
        if not self._verifyTrustChain():
            logger.error(
                f"PEM bundle failed trust chain check with openssl"
                f"in file {self._pemSimpleBank.bundleFilePath}"
            )
            return False

        return True

    def _verifyTrustChain(self) -> bool:
        numberCheckPass = self._checkNumberLimits(
            maxCertificateCount=1,
            maxPrivateKeyCount=1,
            maxIntermediateCACount=self.MAX_COUNT,
            maxRootCACount=1,
        )
        if not numberCheckPass:
            return False

        store = X509Store()

        rootCert = load_certificate(
            FILETYPE_PEM, self._pemSimpleBank.rootCAs[0].as_bytes()
        )
        store.add_cert(rootCert)

        for intermediateCA in self._pemSimpleBank.intermediateCAs:
            intermediateCAObject = load_certificate(
                FILETYPE_PEM, intermediateCA.as_bytes()
            )
            store.add_cert(intermediateCAObject)

        untrustedCert = load_certificate(
            FILETYPE_PEM, self._pemSimpleBank.certificates[0].as_bytes()
        )
        storeCtx = X509StoreContext(store, untrustedCert)
        try:
            storeCtx.verify_certificate()
            return True
        except X509StoreContextError:
            logger.error(
                f"PEM bundle failed to establish chain of trust in "
                f"{self._pemSimpleBank.bundleFilePath}"
            )
            return False

    def _buildTrustChain(self) -> Tree:
        trustTree = Tree()

        numberCheckPass = self._checkNumberLimits(
            maxCertificateCount=1,
            maxPrivateKeyCount=1,
            maxIntermediateCACount=self.MAX_COUNT,
            maxRootCACount=1,
        )
        if not numberCheckPass:
            return trustTree

        # add root CA as root node
        caCert: AbstractPEMObject = self._pemSimpleBank.rootCAs[0]
        caCertParsed: Certificate = self._pemMap.get(caCert)
        caCommonName = X509Util.getCommonName(caCertParsed)
        trustTree.create_node(tag=caCert, identifier=caCommonName)

        # add intermediate CAs to the root node
        for intermediateCA in self._pemSimpleBank.intermediateCAs:
            intermediateCA: AbstractPEMObject = intermediateCA
            intermediateCAParsed: Certificate = self._pemMap.get(intermediateCA)
            commonName = X509Util.getCommonName(intermediateCAParsed)
            trustTree.create_node(
                tag=intermediateCA,
                identifier=commonName,
                parent=caCommonName,
            )

        # add certificate to the root node
        cert: AbstractPEMObject = self._pemSimpleBank.certificates[0]
        certParsed: Certificate = self._pemMap.get(cert)
        certificateCommonName = X509Util.getCommonName(certParsed)
        trustTree.create_node(
            tag=cert,
            identifier=certificateCommonName,
            parent=caCommonName,
        )

        # correct parent-child relations for all non-rootCA nodes
        # 1) correct certificate
        certificateIssuer = X509Util.getIssuer(certParsed)
        trustTree.move_node(certificateCommonName, certificateIssuer)
        # 2) correct intermediates
        for intermediateCA in self._pemSimpleBank.intermediateCAs:
            intermediateCAParsed: Certificate = self._pemMap.get(intermediateCA)
            commonName = X509Util.getCommonName(intermediateCAParsed)
            issuer = X509Util.getIssuer(intermediateCAParsed)

            trustTree.move_node(commonName, issuer)

        return trustTree

    def _checkNumberLimits(
        self,
        maxCertificateCount,
        maxIntermediateCACount,
        maxPrivateKeyCount,
        maxRootCACount,
    ) -> bool:
        result = True
        if len(self._pemSimpleBank.privateKeys) > maxPrivateKeyCount:
            logger.error(
                f"PEM bundle should contain no more than {maxPrivateKeyCount} "
                f"private keys, "
                f"got {len(self._pemSimpleBank.privateKeys)} "
                f"in {self._pemSimpleBank.bundleFilePath}"
            )
            result = False
        if len(self._pemSimpleBank.certificates) > maxCertificateCount:
            logger.error(
                f"PEM bundle should contain no more than {maxCertificateCount} "
                f"certificates, "
                f"got {len(self._pemSimpleBank.certificates)} "
                f"in {self._pemSimpleBank.bundleFilePath}"
            )
            result = False
        if len(self._pemSimpleBank.intermediateCAs) > maxIntermediateCACount:
            logger.error(
                f"PEM bundle should contain no more than "
                f"{maxIntermediateCACount} intermediate CAs, "
                f"got {len(self._pemSimpleBank.intermediateCAs)} "
                f"in {self._pemSimpleBank.bundleFilePath}"
            )
            result = False
        if len(self._pemSimpleBank.rootCAs) > maxRootCACount:
            logger.error(
                f"PEM bundle should contain no more than {maxRootCACount} "
                f"root CAs "
                f"got {len(self._pemSimpleBank.rootCAs)} "
                f"in {self._pemSimpleBank.bundleFilePath}"
            )
            result = False

        return result


class X509Util:
    @staticmethod
    def getCommonName(x509: Certificate) -> str:
        return x509.subject.get_attributes_for_oid(NameOID.COMMON_NAME)[0].value

    @staticmethod
    def getSubject(x509: Certificate) -> str:
        return str(x509.subject)

    @staticmethod
    def getIssuer(x509: Certificate) -> str:
        return x509.issuer.get_attributes_for_oid(NameOID.COMMON_NAME)[0].value

    @staticmethod
    def getIsCA(x509: Certificate) -> bool:
        try:
            basicConstraintExtension: Extension = (
                x509.extensions.get_extension_for_class(BasicConstraints)
            )
            return basicConstraintExtension.value.ca

        except ExtensionNotFound:
            return False

    @staticmethod
    def getNotValidBefore(x509: Certificate) -> datetime:
        return x509.not_valid_before

    @staticmethod
    def getNotValidAfter(x509: Certificate) -> datetime:
        return x509.not_valid_after

    @staticmethod
    def getExtendedKeyUsages(x509: Certificate) -> List:
        try:
            extension: Extension = x509.extensions.get_extension_for_class(
                ExtendedKeyUsage
            )
            return extension.value._usages

        except ExtensionNotFound:
            return []

    @staticmethod
    def getX509Version(x509: Certificate) -> str:
        return x509.version.name


class PemBundleError(Exception):
    pass


class PemBundleParser:
    def __init__(self):
        self._pemMap = {}
        self._pem = None

        self._privateKeys: List[AbstractPEMObject] = []
        self._certificates: List[AbstractPEMObject] = []
        self._rootCAs: List[AbstractPEMObject] = []
        self._intermediateCAs: List[AbstractPEMObject] = []

    def parse(self, pemFilePath: str) -> PemBank:
        self._loadPemBundleFile(pemFilePath)

        # simple classification for PemSimpleBank
        inspectedPems = set([])
        for pemSection, parsedPem in self._pemMap.items():
            # if private key
            if hasattr(parsedPem, "private_bytes"):
                self._privateKeys.append(pemSection)
                inspectedPems.add(pemSection)

            # if x509 certificate
            if isinstance(parsedPem, Certificate):
                commonName = X509Util.getCommonName(parsedPem)
                issuer = X509Util.getIssuer(parsedPem)
                isCA = X509Util.getIsCA(parsedPem)

                if isCA:
                    if commonName == issuer:
                        # found root CA
                        self._rootCAs.append(pemSection)
                        inspectedPems.add(pemSection)
                    else:
                        # found intermediate CA
                        self._intermediateCAs.append(pemSection)
                        inspectedPems.add(pemSection)
                else:
                    self._certificates.append(pemSection)
                    inspectedPems.add(pemSection)

        pemSimpleBank = PemSimpleBank(
            privateKeys=self._privateKeys,
            certificates=self._certificates,
            rootCAs=self._rootCAs,
            intermediateCAs=self._intermediateCAs,
            bundleFilePath=pemFilePath,
        )

        return PemBank(pemSimpleBank, self._pemMap)

    def _loadPemBundleFile(self, pemFilePath):
        try:
            pemFile = Path(pemFilePath)
            if not pemFile.is_file() or not pemFile.exists():
                logger.error("Pem bundle '%s' is not found", pemFilePath)
        except Exception:
            logger.error("Pem bundle '%s' is not found", pemFilePath)

        self._pem = pem.parse_file(pemFilePath)
        for p in self._pem:
            # supported types:
            #   x509 certificates
            #   private keys
            for loadMethod in [
                load_pem_x509_certificate,
                partial(load_pem_private_key, password=None),
            ]:
                try:
                    parsed = loadMethod(p.as_bytes())
                    self._pemMap[p] = parsed
                except ValueError:
                    # on parse error from loadMethod
                    continue

        # check if every PEM section is loaded
        if len(self._pemMap) != len(self._pem):
            unknownSections = set(self._pem) - self._pemMap.keys()
            unknownSectionHeads = [
                f"{s.as_text()[: min(50, len(s.as_text()))]}..."
                for s in unknownSections
            ]
            logger.exception(
                f"unknown PEM section(s) in file {pemFilePath}: "
                f"{unknownSectionHeads}"
            )
            raise


PemInfo = namedtuple(
    "PemInfo",
    ["pemType", "pemStart", "pemEnding", "summary", "pemFor"],
    defaults=(None, None, None, {}, None),
)


class PemViewer:
    PEM_TYPE_PRIVATE_KEY = "private key"
    PEM_TYPE_CERTIFICATE = "certificate"
    PEM_TYPE_DH_PARAMETER = "Diffie-Hellman parameter"

    FOR_PRIVATE_KEY = "private key"
    FOR_SERVER_CERTIFICATE = "server certificate"
    FOR_CLIENT_CERTIFICATE = "client certificate"
    FOR_INTERMEDIATE_CA = "intermediate CA"
    FOR_ROOT_CA = "root CA"
    FOR_MTLS_CA = "mTLS CA"
    FOR_MTLS_PEER = "mTLS peer certificate"
    FOR_DH_PARAMETER = "Diffie-Hellman parameter"

    def __init__(self, pemBundleFilePath: str):
        self._pemBundleFilePath: str = pemBundleFilePath
        self._inspections: Dict[bytes, PemInfo] = {}

    def log(self, pemBundleName: str):
        defaultLogLevel = logging.root.level
        messageHeader = f"{pemBundleName} PEM bundle contains: \n"
        messages = []
        for pemInfo in self._inspections.values():
            summary = [
                textwrap.indent(f"{key}: '{value}'", "  ")
                for key, value in pemInfo.summary.items()
            ]

            summaryLine = "\n".join(summary)
            if defaultLogLevel < logging.INFO:
                messages.append(
                    (
                        f" A {pemInfo.pemType} for {pemInfo.pemFor.upper()} with\n"
                        f"{summaryLine}\n"
                        f" from PEM section "
                        f"'{pemInfo.pemStart} ... {pemInfo.pemEnding}'"
                    )
                )
            else:
                message = f"a {pemInfo.pemType} for {pemInfo.pemFor.upper()}"
                if pemInfo.pemType == self.PEM_TYPE_CERTIFICATE:
                    message += f" with subject {pemInfo.summary['subject']}"
                messages.append(message)

        if defaultLogLevel < logging.INFO:
            seperator = "\n"
        else:
            seperator = ", "

        outMsg = messageHeader + seperator.join(messages)

        for index, line in enumerate(outMsg.splitlines()):
            logger.log(defaultLogLevel, ("    " if index else "") + line)

    def _getPemStart(self, pemBytes: bytes) -> str:
        return pemBytes[: min(50, len(pemBytes))].decode().replace("\n", "")

    def _getPemEnding(self, pemBytes: bytes) -> str:
        return pemBytes[-min(50, len(pemBytes)) :].decode().replace("\n", "")

    def viewPrivateKey(self, pemBytes: bytes, pemFor: str = None):
        key = load_pem_private_key(pemBytes, password=None)
        pemInfo = PemInfo(
            pemFor=pemFor,
            pemType=self.PEM_TYPE_PRIVATE_KEY,
            pemStart=self._getPemStart(pemBytes),
            pemEnding=self._getPemEnding(pemBytes),
            summary={"publicKey": key.public_key()},
        )
        self._inspections[pemBytes] = pemInfo

    def viewCertificate(self, pemBytes: bytes, pemFor: str = None):
        cert = load_pem_x509_certificate(pemBytes)
        pemInfo = PemInfo(
            pemFor=pemFor,
            pemType=self.PEM_TYPE_CERTIFICATE,
            pemStart=self._getPemStart(pemBytes),
            pemEnding=self._getPemEnding(pemBytes),
            summary={
                "subject": X509Util.getSubject(cert),
                "issuer": X509Util.getIssuer(cert),
                "notValidBefore": X509Util.getNotValidBefore(cert),
                "notValidAfter": X509Util.getNotValidAfter(cert),
                "isCa": X509Util.getIsCA(cert),
                "x509Version": X509Util.getX509Version(cert),
                "extendedKeyUsage": X509Util.getExtendedKeyUsages(cert),
            },
        )
        self._inspections[pemBytes] = pemInfo

    def viewDiffieHellmanParameter(self, pemBytes: bytes, pemFor: str = None):
        dhParam = load_pem_parameters(pemBytes)
        pemInfo = PemInfo(
            pemFor=pemFor,
            pemType=self.PEM_TYPE_DH_PARAMETER,
            pemStart=self._getPemStart(pemBytes),
            pemEnding=self._getPemEnding(pemBytes),
            summary={"length": dhParam.generate_private_key().key_size},
        )
        self._inspections[pemBytes] = pemInfo


def parseTrustRootFromBundle(pemFilePath: str) -> List[TxCertificate]:
    # parse PEM format
    parser = PemBundleParser()
    bank = parser.parse(pemFilePath)
    bank.check(PEM_CHECK_TYPE.CHECK_TYPE_SSL_MTLS_CA)

    pemInspector = PemViewer(pemFilePath)
    # load certificates in the PEM bundle file
    trustedPeerAuthorities = []
    for trustedPeerCertificateAuthorityPEM in bank.rootCAs:
        pemBytes = trustedPeerCertificateAuthorityPEM.as_bytes()
        trustedPeerAuthorities.append(ssl.Certificate.loadPEM(pemBytes))
        pemInspector.viewCertificate(pemBytes, pemFor=pemInspector.FOR_MTLS_CA)
    pemInspector.log(pemBundleName="mTLS trusted CA")

    return trustedPeerAuthorities


PrivateKeyWithFullChain = namedtuple(
    "PrivateKeyWithFullChain",
    ["privateKey", "certificate", "intermediateCAs", "rootCA"],
    defaults=[None, None, [], None],
)


def parsePemBundleForServer(pemFilePath: str) -> PrivateKeyWithFullChain:
    parser = PemBundleParser()
    bank = parser.parse(pemFilePath)
    bank.check(PEM_CHECK_TYPE.CHECK_TYPE_SSL_SERVER_IDENTITY)

    pemViewer = PemViewer(pemFilePath)

    key = bank.privateKeys[0]
    pemViewer.viewPrivateKey(key.as_bytes(), pemFor=pemViewer.FOR_PRIVATE_KEY)

    cert = bank.certificates[0]
    pemViewer.viewCertificate(
        cert.as_bytes(), pemFor=pemViewer.FOR_SERVER_CERTIFICATE
    )

    intermediates = bank.intermediateCAs
    for intermediate in intermediates:
        pemViewer.viewCertificate(
            intermediate.as_bytes(), pemFor=pemViewer.FOR_INTERMEDIATE_CA
        )

    root = bank.rootCAs[0]
    pemViewer.viewCertificate(root.as_bytes(), pemFor=pemViewer.FOR_ROOT_CA)

    pemViewer.log(pemBundleName="TLS Server")

    return PrivateKeyWithFullChain(
        privateKey=key,
        certificate=cert,
        intermediateCAs=intermediates,
        rootCA=root,
    )


def parsePemBundleForClient(pemFilePath: str) -> PrivateKeyWithFullChain:
    parser = PemBundleParser()
    bank = parser.parse(pemFilePath)
    bank.check(PEM_CHECK_TYPE.CHECK_TYPE_SSL_CLIENT_IDENTITY)

    pemViewer = PemViewer(pemFilePath)

    key = bank.privateKeys[0]
    pemViewer.viewPrivateKey(key.as_bytes(), pemFor=pemViewer.FOR_PRIVATE_KEY)

    cert = bank.certificates[0]
    pemViewer.viewCertificate(
        cert.as_bytes(), pemFor=pemViewer.FOR_CLIENT_CERTIFICATE
    )

    intermediates = bank.intermediateCAs
    for intermediate in intermediates:
        pemViewer.viewCertificate(
            intermediate.as_bytes(), pemFor=pemViewer.FOR_INTERMEDIATE_CA
        )

    root = bank.rootCAs[0]
    pemViewer.viewCertificate(root.as_bytes(), pemFor=pemViewer.FOR_ROOT_CA)

    pemViewer.log(pemBundleName="TLS Client")

    return PrivateKeyWithFullChain(
        privateKey=key,
        certificate=cert,
        intermediateCAs=intermediates,
        rootCA=root,
    )


def generateDiffieHellmanParameterBytes(
    outputFilePath: str, length=2048
) -> bytes:
    p = dh.generate_parameters(2, length)
    dhBytes = p.parameter_bytes(Encoding.PEM, ParameterFormat.PKCS3)
    with open(outputFilePath, "wb") as outputPem:
        outputPem.write(dhBytes)
    return dhBytes


def parseDiffieHellmanParameter(
    pemFilePath: str,
) -> OpenSSLDiffieHellmanParameters:
    file = FilePath(pemFilePath)
    pemViewer = PemViewer(pemFilePath)
    pemViewer.viewDiffieHellmanParameter(
        file.getContent(), pemFor=pemViewer.FOR_DH_PARAMETER
    )

    pemViewer.log(pemBundleName="Diffie-Hellman Parameter")
    return ssl.DiffieHellmanParameters.fromFile(file)


def parsePemBundleForTrustedPeers(pemFilePath: str) -> List[Certificate]:
    parser = PemBundleParser()
    bank = parser.parse(pemFilePath)
    bank.check(PEM_CHECK_TYPE.CHECK_TYPE_SSL_MTLS_PEER)

    trustedPeerCertificates = bank.certificates

    pemViewer = PemViewer(pemFilePath)
    for trustedPeerCertificate in trustedPeerCertificates:
        pemViewer.viewCertificate(
            trustedPeerCertificate.as_bytes(), pemFor=pemViewer.FOR_MTLS_PEER
        )

    pemViewer.log(pemBundleName="mTLS trusted peers")

    return trustedPeerCertificates
