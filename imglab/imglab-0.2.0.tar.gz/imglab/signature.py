import base64
import hmac
import hashlib


def generate(source, path, encoded_params=None):
    """Returns a generated signature for a source, path and encoded parameters

    :Examples:
        >>> from imglab import signature, Source
        >>> source = Source("assets", secure_key="55IX1RVlDHpgl/4D", secure_salt="ITvYA2lPfyz0w8/v")
        >>> signature.generate(source, "example.jpeg")
        'QFEVlDWgK289HYKr2KJdwtPC-I7LS195hSVQhS1UsRA'

    :param source: The source used to generate the signature
    :type source: class:`imglab.Source`
    :param path: The path of the resource
    :type path: str
    :param encoded_params: Encoded query params of the URL to generate the signature, defaults to None
    :type encoded_params: str, optional
    :return: A string with the signature encoded using Base64 to be used in a imglab URL
    :rtype: str
    """
    decoded_secure_key = base64.b64decode(source.secure_key.encode())
    decoded_secure_salt = base64.b64decode(source.secure_salt.encode())

    data = b"%s/%s" % (decoded_secure_salt, path.encode())
    data = b"%s?%s" % (data, encoded_params.encode()) if encoded_params else data

    digest = hmac.new(decoded_secure_key, data, hashlib.sha256).digest()

    return base64.urlsafe_b64encode(digest).rstrip(b"=").decode()
