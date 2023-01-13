from typing import Tuple

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat

from ..utils import bytes_to_int, int_to_bytes

_CURVE = ec.SECP256R1()


__all__ = ['new_key_pair', 'new_shared_key']


def new_key_pair() -> Tuple[bytes, bytes]:
    """Generate a pair of asymmetric key.

    :return (private_key, public_key)
    """
    private_key = ec.generate_private_key(_CURVE)
    public_key = private_key.public_key()

    sk = private_key.private_numbers().private_value
    sk_bytes = int_to_bytes(sk)
    pk_bytes = public_key.public_bytes(Encoding.X962,
                                       PublicFormat.CompressedPoint)
    return sk_bytes, pk_bytes


def new_shared_key(sk_bytes: bytes, pk_bytes: bytes) -> bytes:
    """Generate a shared key from a pair of asymmetric key."""
    pub_key = ec.EllipticCurvePublicKey.from_encoded_point(_CURVE, pk_bytes)
    sk = bytes_to_int(sk_bytes)
    priv_key = ec.derive_private_key(sk, _CURVE)

    shared_key = priv_key.exchange(ec.ECDH(), pub_key)

    digest = hashes.Hash(hashes.SHA256())
    digest.update(shared_key)
    return digest.finalize()
