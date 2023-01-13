#
#  Copyright (c) 2018-2022 Renesas Inc.
#  Copyright (c) 2018-2022 EPAM Systems Inc.
#
"""aos-keys cloud API implementations."""
from urllib.parse import urljoin

from requests import post
from requests.exceptions import SSLError
from requests_pkcs12 import get

from aos_keys.common import ca_certificate, AosKeysError
from aos_keys.key_manager import extract_cloud_domain_from_cert

_ME_CERT_ENDPOINT = '/api/v3/users/me/'
_UPLOAD_USER_CERTIFICATE = '/api/v3/user-certificates/'


INVALID_TOKEN_ERROR = AosKeysError(
    'FORBIDDEN status was received from the AosEdge Cloud!',
    help_text='Access token is wrong or already used',
)


def get_user_info_by_cert(pkcs12_path: str):
    """Get user info from the Cloud by user certificate.

    Args:
        pkcs12_path: Full path to user certificate in pkcs12 format.

    Returns:
        Json response from cloud
    """
    domain = extract_cloud_domain_from_cert(pkcs12_path)
    with ca_certificate() as server_certificate_path:
        response = get(
            urljoin(f'https://{domain}:10000', _ME_CERT_ENDPOINT),
            pkcs12_filename=pkcs12_path,
            pkcs12_password='',
            verify=server_certificate_path,
        )
        response.raise_for_status()
        return response.json()


def receive_certificate_by_token(domain: str, token: str, csr: str) -> str:
    """Get user info from the Cloud by user certificate.

    Args:
        domain: Domain to request client certificate.
        token: Authentication  one-time user token.
        csr: User CSR in PEM format.

    Returns:
        The user certificate issued by the AosEdge Cloud
    """
    try:
        with ca_certificate() as server_certificate_path:
            upload_response = post(
                urljoin(f'https://{domain}', _UPLOAD_USER_CERTIFICATE),
                json={'csr': csr},
                headers={
                    'Content-Type': 'application/json; charset=UTF-8',
                    'Referer': f'https://{domain}',
                    'Authorization': f'Token {token}',
                },
                verify=server_certificate_path,
            )
            if upload_response.status_code == 403:
                raise INVALID_TOKEN_ERROR
            upload_response.raise_for_status()

    except SSLError:
        # Try using system root certificate storage as the trusted sources instead of the AosEdge root certificate
        upload_response = post(
            urljoin(f'https://{domain}', _UPLOAD_USER_CERTIFICATE),
            json={'csr': csr},
            headers={
                'Content-Type': 'application/json; charset=UTF-8',
                'Referer': f'https://{domain}',
                'Authorization': f'Token {token}',
            },
        )
        if upload_response.status_code == 403:
            raise INVALID_TOKEN_ERROR
        upload_response.raise_for_status()

    return upload_response.json()['certificate']
