import socket
import ssl
from typing import Any, Dict

from chaoslib.exceptions import ActivityFailed
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes

__all__ = ["get_certificate_info"]


# copied mostly from this awesome piece
# https://github.com/dspruell/tls-probe/blob/main/tls_probe.py
def get_certificate_info(host: str, port: int = 443) -> Dict[str, Any]:
    """
    Extract certificate information from the remote connection.
    """
    context = ssl.create_default_context()
    context.verify_mode = ssl.CERT_REQUIRED
    context.check_hostname = True

    with socket.create_connection((host, port)) as sock:
        conn_info = dict(conn={}, cert={"fingerprints": {}, "extensions": {}})
        with context.wrap_socket(sock, server_hostname=host) as secsock:
            cert = secsock.getpeercert(binary_form=True)
            if not cert:
                raise ActivityFailed(
                    f"endpoint {host}:{port} has no certificate"
                )

            cert_data = x509.load_der_x509_certificate(cert, default_backend())

            conn_info["conn"].update(  # type: ignore
                {
                    "version": secsock.version(),
                    "remote_addr": ":".join(
                        [str(_) for _ in secsock.getpeername()]
                    ),
                }
            )

            sig_hash = cert_data.signature_hash_algorithm.name  # type: ignore
            conn_info["cert"].update(  # type: ignore
                {
                    "issuer": cert_data.issuer.rfc4514_string(),
                    "subject": cert_data.subject.rfc4514_string(),
                    "serial_int": cert_data.serial_number,
                    "version": cert_data.version.name,
                    "signature_hash": sig_hash,
                    "not_valid_before": cert_data.not_valid_before.isoformat(),
                    "not_valid_after": cert_data.not_valid_after.isoformat(),
                }
            )

            conn_info["cert"]["fingerprints"].update(  # type: ignore
                {
                    "md5": cert_data.fingerprint(hashes.MD5()).hex(),
                    "sha1": cert_data.fingerprint(hashes.SHA1()).hex(),
                    "sha256": cert_data.fingerprint(hashes.SHA256()).hex(),
                }
            )

            for ext in cert_data.extensions:
                if ext.oid._name in ("subjectAltName",):
                    names = []  # type: ignore
                    conn_info["cert"]["extensions"].update(  # type: ignore
                        {
                            ext.oid._name: names,
                        }
                    )
                    for g in ext.value._general_names:
                        names.append(g.value)

        return conn_info
