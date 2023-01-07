from fractal_tokens.services.jwt.asymmetric import AsymmetricJwtTokenService


def rsa_key_pair():
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.primitives.asymmetric import rsa

    key = rsa.generate_private_key(
        backend=default_backend(),
        public_exponent=65537,
        key_size=512,  # use at least 4096 in production
    )

    private_key = key.private_bytes(
        serialization.Encoding.PEM,
        serialization.PrivateFormat.PKCS8,
        serialization.NoEncryption(),
    ).decode("utf-8")

    return private_key, key.public_key()


if __name__ == "__main__":
    private_key, public_key = rsa_key_pair()
    token_service = AsymmetricJwtTokenService(
        issuer="example", private_key=private_key, public_key=public_key
    )

    token = token_service.generate({})
    print("token:", token)

    payload = token_service.verify(token)
    print("payload:", payload)
