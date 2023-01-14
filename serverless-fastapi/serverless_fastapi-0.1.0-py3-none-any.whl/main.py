"""FastAPI Serverless main module"""
from typing import Optional, Callable
from io import BytesIO
from json import loads
from datetime import datetime
from hashlib import sha256
from jose import jwt
from pydantic import BaseModel, Field, EmailStr
from fastapi import FastAPI, Request, HTTPException, status, Depends, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from odmantic import AIOEngine, Model, Field as oField
from motor.motor_asyncio import AsyncIOMotorClient as Async
from serverless_fastapi.config import env
from serverless_fastapi.db import DBCredentials
from serverless_fastapi.mangum import Mangum

class User(Model):
    email: EmailStr = oField(...)
    password: str = oField(...)
    token: Optional[str] = oField(default=None)

    def token_(self):
        return jwt.encode(
            {"email": self.email, "password": self.password},
            sha256(self.password.encode()).hexdigest(),
        )


class UserSchema(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)
    token: Optional[str] = Field(default=None)

    def __init__(self, **data):
        super().__init__(**data)
        self.password = sha256(self.password.encode()).hexdigest()
        self.token = jwt.encode(
            {"email": self.email, "password": data["password"]}, self.password
        )


class RequestLog(BaseModel):
    """Request log Schema model"""

    method: str = Field(...)
    url: str = Field(...)
    status_code: int = Field(...)
    headers: dict = Field(...)
    time_data: str = Field(
        default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )


class RequestLogModel(Model):
    """Request log Database model"""

    method: str = oField(...)
    url: str = oField(...)
    status_code: int = oField(...)
    headers: dict = oField(...)
    time_data: str = oField(...)


class ServerlessFastAPI(FastAPI):
    """FastAPI Serverless class"""

    def __init__(self, mongo_url: Optional[str] = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title = "FastAPI Serverless"
        self.description = "A Wrapper for FastAPI to run on AWS Lambda"
        self.version = "0.0.1"
        self.oauth2_scheme = OAuth2PasswordBearer(tokenUrl="oauth2/token")
        if mongo_url is None:
            mongo_url = env.DATABASE_URL
        self.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        self.title = "FastAPI Serverless"
        self.description = "FastAPI Serverless"
        self.version = "0.0.1"
        self.db = AIOEngine(
            client=Async(mongo_url), database=mongo_url.split("/")[-1].split("?")[0]
        )

        @self.middleware("http")
        async def log_requests(request: Request, call_next:Callable):
            """Logins requests middleware"""
            try:
                if request.url.path in [
                    "/docs",
                    "/docs/dashboard",
                    "/redoc",
                    "/openapi.json",
                    "/favicon.ico",
                ]:
                    return await call_next(request)
                elif request.url.hostname == "localhost":
                    return await call_next(request)
                else:
                    response = await call_next(request)
                    body = b""
                    headers = dict(request.headers)
                    async for chunk in response.body_iterator:
                        body += chunk
                    log = RequestLog(
                        method=request.method,
                        url=str(request.url),
                        status_code=response.status_code,
                        headers=headers,
                    )
                    await self.db.save(RequestLogModel(**log.dict()))
                    return Response(
                        content=body,
                        status_code=response.status_code,
                        headers=response.headers,
                    )
            except HTTPException as exc:
                print(exc)
                return await call_next(request)

        @self.get("/docs/dashboard", include_in_schema=False)
        async def dashboard_api(request:Request):
            """Logs of all requests"""
            try:
                bearer = request.headers.get("Authorization")
                if bearer is None:
                    return JSONResponse(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        content={"detail": "Unauthorized", "type": "error"},
                    )
                token = bearer.split(" ")[1]
                credentials = DBCredentials(database_url=mongo_url)
                if token != credentials.token:
                    return JSONResponse(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        content={"detail": "Unauthorized", "type": "error"},
                    )
                instances = await self.db.find(RequestLogModel)
                response = [loads(instance.json()) for instance in instances]
                return JSONResponse(response)
            except Exception as exc:
                print(exc)
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={"detail": "Unauthorized", "type": "error"},
                )
                
        @self.post("/oauth2/token", response_class=JSONResponse)
        async def login_for_access_token(
            form_data: OAuth2PasswordRequestForm = Depends(),
        ):
            user = await self.db.find_one(User, User.email == form_data.username)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Incorrect email or password",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            if user.password != sha256(form_data.password.encode()).hexdigest():
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={"detail": "Incorrect email or password"},
                )
            return {"access_token": user.token, "token_type": "bearer"}

        @self.get("/oauth2/userinfo")
        async def read_users_me(token: str = Depends(self.oauth2_scheme)):
            try:
                user = await self.db.find_one(User, User.token == token)
                token_data = jwt.decode(token, user.password, algorithms=["HS256"])
                return token_data["email"]
            except Exception as exc:
                print(exc)
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={"detail": "Incorrect email or password"},
                )

        @self.post("/oauth2/authorize")
        async def register(user: UserSchema):
            if await self.db.find_one(User, User.email == user.email):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT, detail="User already exists"
                )
            await self.db.save(User(**user.dict()))
            return {"message": "User created successfully"}


class Handler(Mangum):
    """Mangum Handler"""

    def __init__(self, app: ServerlessFastAPI, *args, **kwargs):
        super().__init__(app, *args, **kwargs)