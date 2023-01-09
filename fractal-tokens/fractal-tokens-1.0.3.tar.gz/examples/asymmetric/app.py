from asymmetric.utils import rsa_key_pair

from fractal_tokens.services.jwt.asymmetric import AsymmetricJwtTokenService

if __name__ == "__main__":
    private_key, public_key = rsa_key_pair()
    token_service = AsymmetricJwtTokenService(
        issuer="example", private_key=private_key, public_key=public_key
    )

    token = token_service.generate({})
    print("token:", token)

    payload = token_service.verify(token)
    print("payload:", payload)
