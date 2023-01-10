from typing import Optional

from pydantic import Extra, Field

from aiosox.utils import BaseModel

from .enums import HttpOperationBindingType, WebSocketsMethod
from .schema import ApiSchema


class HttpChannelBinding(BaseModel):
    """
    This document defines how to describe HTTP-specific information on AsyncAPI.
    This object MUST NOT contain any properties. Its name is reserved for future use.
    """

    class Config:
        extra = Extra.forbid


class HttpMessageBinding(BaseModel):
    """
    This object contains information about the message representation in HTTP.
    """

    headers: Optional[ApiSchema] = None
    """
    A Schema object containing the definitions for HTTP-specific headers. This
    schema MUST be of type object and have a properties key.
    """

    bindingVersion: Optional[str] = None
    """
    The version of this binding. If omitted, "latest" MUST be assumed.
    """

    class Config:
        extra = Extra.forbid


class HttpServerBinding(BaseModel):
    """
    This document defines how to describe HTTP-specific information on AsyncAPI.
    This object MUST NOT contain any properties. Its name is reserved for future use.
    """

    class Config:
        extra = Extra.forbid


class HttpOperationBinding(BaseModel):
    """
    This document defines how to describe HTTP-specific information on AsyncAPI.
    """

    param_type: HttpOperationBindingType = Field(alias="type")
    """
    **REQUIRED**. Type of operation. Its value MUST be either request or response.
    """

    method: Optional[str] = None
    """
    When type is request, this is the HTTP method, otherwise it MUST be ignored.
    Its value MUST be one of GET, POST, PUT, PATCH, DELETE, HEAD, OPTIONS, CONNECT, and TRACE.
    """

    query: Optional[ApiSchema] = None
    """
    A Schema object containing the definitions for each query parameter.
    This schema MUST be of type object and have a properties key.
    """

    bindingVersion: Optional[str] = None
    """
    The version of this binding. If omitted, "latest" MUST be assumed.
    """

    class Config:
        extra = Extra.forbid
        schema_extra = {
            "examples": [
                {
                    "type": "request",
                    "method": "GET",
                    "query": {
                        "type": "object",
                        "required": ["companyId"],
                        "properties": {
                            "companyId": {
                                "type": "number",
                                "minimum": 1,
                                "description": "The Id of the company.",
                            }
                        },
                        "additionalProperties": False,
                    },
                    "bindingVersion": "0.1.0",
                }
            ]
        }


class WebSocketsChannelBinding(BaseModel):
    """
    When using WebSockets, the channel represents the connection. Unlike other
    protocols that support multiple virtual channels (topics, routing keys, etc.)
    per connection, WebSockets doesn't support virtual channels or, put it another
    way, there's only one channel and its characteristics are strongly related to
    the protocol used for the handshake, i.e., HTTP.
    """

    method: Optional[WebSocketsMethod] = None
    """
    The HTTP method to use when establishing the connection. Its value MUST be
    either GET or POST.
    """

    query: Optional[ApiSchema] = None
    """
    A Schema object containing the definitions for each query parameter. This
    schema MUST be of type object and have a properties key.
    """

    headers: Optional[ApiSchema] = None
    """
    A Schema object containing the definitions of the HTTP headers to use when
    establishing the connection. This schema MUST be of type object and have a
    properties key.
    """

    bindingVersion: Optional[str] = None
    """
    The version of this binding. If omitted, "latest" MUST be assumed.
    """


class WebSocketsMessageBinding(BaseModel):
    """
    This document defines how to describe WebSockets-specific information on AsyncAPI.
    This object MUST NOT contain any properties. Its name is reserved for future use.
    """

    class Config:
        extra = Extra.forbid


class WebSocketsOperationBinding(BaseModel):
    """
    This document defines how to describe WebSockets-specific information on AsyncAPI.
    This object MUST NOT contain any properties. Its name is reserved for future use.
    """
    headers: Optional[ApiSchema] = None
    """
    A Schema object containing the definitions of the HTTP headers to use when
    establishing the connection. This schema MUST be of type object and have a
    properties key.
    """
    class Config:
        extra = Extra.forbid


class WebSocketsServerBinding(BaseModel):
    """
    This document defines how to describe WebSockets-specific information on AsyncAPI.
    This object MUST NOT contain any properties. Its name is reserved for future use.
    """

    class Config:
        extra = Extra.forbid


class KafkaChannelBinding(BaseModel):
    """
    This document defines how to describe Kafka-specific information on AsyncAPI.
    This object MUST NOT contain any properties. Its name is reserved for future use.
    """

    class Config:
        extra = Extra.forbid


class KafkaMessageBinding(BaseModel):
    """
    This object contains information about the message representation in Kafka.
    """

    key: Optional[ApiSchema] = None
    """
    The message key. NOTE: You can also use the reference object way.
    """

    bindingVersion: Optional[str] = None
    """
    The version of this binding. If omitted, "latest" MUST be assumed.
    """

    class Config:
        extra = Extra.forbid


class KafkaServerBinding(BaseModel):
    """
    This document defines how to describe Kafka-specific information on AsyncAPI.
    This object MUST NOT contain any properties. Its name is reserved for future use.
    """

    class Config:
        extra = Extra.forbid


class KafkaOperationBinding(BaseModel):
    """
    This document defines how to describe Kafka-specific information on AsyncAPI.
    """

    groupId: Optional[ApiSchema] = None
    """
    Id of the consumer group.
    """

    clientId: Optional[ApiSchema] = None
    """
    Id of the consumer inside a consumer group.
    """

    bindingVersion: Optional[str] = None
    """
    The version of this binding. If omitted, "latest" MUST be assumed.
    """

    class Config:
        extra = Extra.forbid


class ChannelBindings(BaseModel):
    """
    Map describing protocol-specific definitions for a channel.
    """

    http: Optional[HttpChannelBinding] = None
    """
    Protocol-specific information for an HTTP channel.
    """

    ws: Optional[WebSocketsChannelBinding] = None
    """
    Protocol-specific information for a WebSockets channel.
    """
    socketio: Optional[WebSocketsChannelBinding] = None
    """
    Protocol-specific information for a Socket Io channel.
    """

    kafka: Optional[KafkaChannelBinding] = None

    class Config:
        extra = Extra.forbid


class ApiServerBindings(BaseModel):
    """
    Map describing protocol-specific definitions for a server.
    """

    http: Optional[HttpServerBinding] = None
    """
    Protocol-specific information for an HTTP server.
    """

    ws: Optional[WebSocketsServerBinding] = None
    """
    Protocol-specific information for a WebSockets server.
    """

    kafka: Optional[KafkaServerBinding] = None
    """
    Protocol-specific information for a Kafka server.
    """

    class Config:
        extra = Extra.forbid
