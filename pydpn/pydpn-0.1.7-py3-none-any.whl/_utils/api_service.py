from typing import Union, List, Dict, Literal
from dataclasses import dataclass


class ApiService:
    def __init__(
        self,
        serviceName: str,
        refUrl: str,
        apiRoute: str,
        requestMethod: Literal["GET", "POST"],
        responseType: type,
        responseContent,
        returnType: type,
        responseAlias: dict = {},
        setValue: bool = False,
        postData: dict = {},
    ) -> None:
        self.serviceName: str = serviceName
        self.refUrl: str = refUrl
        self.apiRoute: str = apiRoute
        self.requestMethod = requestMethod
        self.responseType: type = responseType
        self.responseContent: Union[str, dict, list[dict]] = responseContent
        self.returnType: type = returnType
        self.responseAlias: dict = responseAlias
        self.setValue: bool = setValue
        self.postData: dict = postData
