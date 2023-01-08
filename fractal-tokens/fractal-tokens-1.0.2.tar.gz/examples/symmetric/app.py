import uuid

from fractal_tokens.services.jwt.symmetric import SymmetricJwtTokenService

if __name__ == "__main__":
    token_service = SymmetricJwtTokenService(issuer="example", secret_key="**SECRET**")

    token = token_service.generate(
        {
            "sub": str(uuid.uuid4()),
        }
    )
    print("token:", token)

    payload = token_service.verify(token)
    print("payload:", payload)
