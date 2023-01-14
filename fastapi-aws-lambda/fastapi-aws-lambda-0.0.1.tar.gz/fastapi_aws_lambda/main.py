"""Main Module"""
from typing import Optional
from datetime import datetime
from hashlib import sha256
from json import loads
from odmantic import Model, Field as oField, AIOEngine
from pydantic import BaseModel, EmailStr, Field
from jose import jwt
from fastapi import FastAPI, Request, Response, HTTPException, Depends, status, Body
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from motor.motor_asyncio import AsyncIOMotorClient as Async
from fastapi_aws_lambda.config import Settings


class UserModel(Model):
    """Base User Model"""
    email: EmailStr = oField(...)
    password: str = oField(...)
    token: Optional[str] = oField(default=None)


class UserSchema(BaseModel):
    """User Schema View"""
    email: EmailStr = Field(...)
    password: str = Field(...)
    token: Optional[str] = Field(default=None)

    def __init__(self, **data):
        """The access token is generated using the hash of the password as the key"""
        super().__init__(**data)
        self.password = sha256(self.password.encode()).hexdigest()
        self.token = jwt.encode(
            {"email": self.email, "password": data["password"]}, self.password
        )


class RequestLog(BaseModel):
    """Request Schema model for logging requests"""
    method: str = Field(...)
    url: str = Field(...)
    status_code: int = Field(...)
    headers: dict = Field(...)
    time_data: str = Field(
        default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )


class RequestLogModel(Model):
    """RequestLog Database model"""
    method: str = oField(...)
    url: str = oField(...)
    status_code: int = oField(...)
    headers: dict = oField(...)
    time_data: str = oField(...)

class APILambda(FastAPI):
    """FastAPI Serverless class"""
    def __init__(self, mongo_url: Optional[str] = None, **kwargs):
        """Basic authentification and logging middleware"""
        super().__init__(**kwargs)
        self.title = "FastAPI Serverless"
        self.description = "A Wrapper for FastAPI to run on AWS Lambda"
        self.version = "0.0.1"
        self.oauth2_scheme = OAuth2PasswordBearer(tokenUrl="oauth2/token")
        self.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        if mongo_url is None:
            mongo_url = Settings().DATABASE_URL
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
        self.database = AIOEngine(
            client=Async(mongo_url), database=mongo_url.split("/")[-1].split("?")[0]
        )

        @self.middleware("http")
        async def log_requests(request: Request, call_next):
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
                    await self.database.save(RequestLogModel(**log.dict()))
                    return Response(
                        content=body,
                        status_code=response.status_code,
                        headers=response.headers,
                    )
            except HTTPException as exc:
                print(exc)
                return await call_next(request)

        @self.get("/docs/dashboard", include_in_schema=False)
        async def dashboard_api():
            """Logs of all requests"""
            instances = await self.database.find(RequestLogModel)
            response = [loads(instance.json()) for instance in instances]
            return JSONResponse(response)

        @self.post("/oauth2/token", response_class=JSONResponse)
        async def login_for_access_token(
            form_data: OAuth2PasswordRequestForm = Depends(),
        ):
            """Login for access token"""
            user = await self.database.find_one(UserModel, UserModel.email == form_data.username)
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
        async def user_info(token: str = Depends(self.oauth2_scheme)):
            """User info endpoint"""
            try:
                user = await self.database.find_one(UserModel, UserModel.token == token)
                return jwt.decode(token, user.password, algorithms=["HS256"])
            except HTTPException as exc:
                print(exc)
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={"detail": "Incorrect email or password"},
                )

        @self.post("/oauth2/authorize")
        async def register(body=Body(...)):
            """ **The request body must have the following fields:**
            - 📧 email: string
            - 🔒 password: string"""
            user_dict = loads(body)
            if await self.database.find_one(UserModel, UserModel.email == user_dict["email"]):
                return JSONResponse(
                    status_code=status.HTTP_409_CONFLICT,
                    content={"detail": "User already exists"},
                )
            user = UserSchema(**user_dict)
            await self.database.save(UserModel(**user.dict()))
            return {"message": "User created successfully"}
