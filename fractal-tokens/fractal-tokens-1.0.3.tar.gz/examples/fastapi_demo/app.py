from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_demo.utils import get_token_payload, rsa_key_pair

from fractal_tokens.services.generic import TokenPayload
from fractal_tokens.services.jwt.asymmetric import AsymmetricJwtTokenService

app = FastAPI()

# key pair will renew everytime you restart the app, store externally to reuse
private_key, public_key = rsa_key_pair()

token_service = AsymmetricJwtTokenService(
    issuer="example", private_key=private_key, public_key=public_key
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/login")
def login(data: OAuth2PasswordRequestForm = Depends()):
    # do login logic
    return {
        "token": token_service.generate(
            {
                "sub": data.username,
            }
        )
    }


@app.get("/protected")
def protected(
    payload: TokenPayload = Depends(get_token_payload(token_service=token_service)),
):
    return {"Protected": "Data", "TokenPayload": payload}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="localhost", port=8000, reload=True)
