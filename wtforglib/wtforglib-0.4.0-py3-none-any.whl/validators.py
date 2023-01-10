from urllib.parse import urlparse


def url_validator(url: str) -> bool:
    """Validate url."""
    try:
        parsed = urlparse(url)
        return all([parsed.scheme, parsed.netloc])
    except Exception:
        return False
