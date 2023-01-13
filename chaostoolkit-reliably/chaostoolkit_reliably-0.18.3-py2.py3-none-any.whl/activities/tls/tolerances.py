from datetime import datetime
from typing import Any, Dict, List, Optional

from chaoslib.exceptions import InvalidActivity
from logzero import logger

from chaosreliably import parse_duration

__all__ = [
    "expire_in_more_than",
    "has_subject_alt_names",
    "has_fingerprint",
    "is_issued_by",
    "verify_tls_cert",
]


def expire_in_more_than(
    duration: str = "7d", value: Optional[Dict[str, Any]] = None
) -> bool:
    """
    Verifies that the certificate expires in more than the given duration.

    The `duration` is expressed as followed: <NUMBER><UNIT> where
    <UNIT> is one of `"s"`, `"m"`, `"d"` or `"w"`. For example, in more
    than a week can be expressed as `"7d"` or `"1w"`.
    """
    v = value["cert"]["not_valid_after"]  # type: ignore
    logger.debug(f"Cert expires on {v}")
    delta = parse_duration(duration)
    expiry_date = datetime.fromisoformat(v)
    return (datetime.utcnow() + delta) < expiry_date


def has_subject_alt_names(
    alt_names: List[str],
    strict: bool = True,
    value: Optional[Dict[str, Any]] = None,
) -> bool:
    """
    Validates the certficate covers at least the given list of alternative
    names. If `strict` is set, then the list of exported names must be exactly
    the provided ones.
    """
    subaltnames = value["cert"]["extensions"].get(  # type: ignore
        "subjectAltName"
    )
    if not subaltnames and alt_names:
        logger.debug("Certificate exposes no alternative subject names")
        return False

    exported = set(subaltnames)
    logger.debug(f"Alt names: {exported} / Expected alt names: {alt_names}")
    if strict:
        return subaltnames == alt_names  # type: ignore

    return set(alt_names).issubset(exported)


def has_fingerprint(
    fingerprint: str,
    hash: str = "sha256",
    value: Optional[Dict[str, Any]] = None,
) -> bool:
    """
    Validate the fingerprint of the certificate. The hash is one of
    `"md5"`, `"sha1"` or `"sha256"`.
    """
    if hash not in ("md5", "sha1", "sha256"):
        raise InvalidActivity(
            "invalid `hash` value in the `has_fingerprint` tolerance"
        )

    fp = value["cert"]["fingerprints"].get(hash)  # type: ignore
    return fp == fingerprint  # type: ignore


def is_issued_by(issuer: str, value: Optional[Dict[str, Any]] = None) -> bool:
    """
    Validate the issue of the certificate.
    """
    return value["cert"]["issuer"] == issuer  # type: ignore


def verify_tls_cert(
    expire_after: str = "7d",
    alt_names: Optional[List[str]] = None,
    fingerprint_sha256: Optional[str] = None,
    issuer: Optional[str] = None,
    value: Optional[Dict[str, Any]] = None,
) -> bool:
    """
    Performs a range of checks on the certificate of the remote endpoint:

    * that we are beyond a certain duration of the certificate expiricy date
    * that the certificate exports the right alternative names
    * the fingerprint of the certificate
    * the certificate was issued by the right issuer

    If any of these values is not set (the default), the according
    check is not performed. This doesn't apply to the expiration date which
    is always checked.
    """
    if expire_in_more_than(expire_after, value) is False:
        return False

    if alt_names not in ("", None):  # type: ignore
        if (
            has_subject_alt_names(alt_names, True, value)  # type: ignore
            is False
        ):
            return False

    if fingerprint_sha256:
        if has_fingerprint(fingerprint_sha256, "sha256", value) is False:
            return False

    if issuer:
        if is_issued_by(issuer, value) is False:
            return False

    return True
