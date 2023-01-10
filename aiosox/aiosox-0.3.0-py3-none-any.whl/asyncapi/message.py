from typing import Any, Dict, List, Mapping, Optional, Sequence, Set, Type, Union

from fastapi.encoders import jsonable_encoder
from pydantic import AnyUrl, Extra, Field, constr, root_validator, validator

from aiosox.utils import BaseModel

from .bindings import (
    HttpChannelBinding,
    HttpMessageBinding,
    KafkaChannelBinding,
    KafkaMessageBinding,
    WebSocketsChannelBinding,
    WebSocketsMessageBinding,
)
from .enums import (
    ApiSecuritySchemeLocation,
    ApiSecuritySchemesType,
    ApiServerProtocol,
    JSONReference,
)
from .reference import Reference
from .schema import ApiSchema, JsonSchemaObject
from .tag import ApiTag


class CorrelationId(BaseModel):
    """
    An object that specifies an identifier at design time that can used for message tracing
    and correlation. For specifying and computing the location of a Correlation ID, a runtime
    expression is used.
    This object can be extended with Specification Extensions.
    """

    description: Optional[str] = None
    """
    An optional description of the identifier. CommonMark syntax can be used for rich text
    representation.
    """

    location: str
    """
    **REQUIRED**. A runtime expression that specifies the location of the correlation ID.
    """

    class Config:
        extra = Extra.forbid
        schema_extra = {
            "examples": [
                {
                    "description": "Default Correlation ID",
                    "location": "$message.header#/correlationId",
                }
            ]
        }


class MessageBindings(BaseModel):
    """
    Map describing protocol-specific definitions for a message.
    """

    http: Optional[HttpMessageBinding] = None
    """
    Protocol-specific information for an HTTP message, i.e., a request or a response.
    """

    ws: Optional[WebSocketsMessageBinding] = None
    """
    Protocol-specific information for a WebSockets message.
    """

    kafka: Optional[KafkaMessageBinding] = None


class MessageExample(BaseModel):
    """
    Message Example Object represents an example of a Message Object and MUST
    contain either headers and/or payload fields.
    """

    headers: Optional[Dict[str, Union[ApiSchema, Reference]]] = None
    """
    The value of this field MUST validate against the Message Object's headers field.
    """

    payload: Optional[ApiSchema] = None
    """
    The value of this field MUST validate against the Message Object's payload field.
    """

    name: Optional[str] = None
    """
    A machine-friendly name.
    """

    summary: Optional[str] = None
    """
    A short summary of what the example is about.
    """

    class Config:
        extra = Extra.forbid
        schema_extra = {
            "examples": [
                {
                    "name": "SimpleSignup",
                    "summary": "A simple UserSignup example message",
                    "headers": {
                        "correlationId": "my-correlation-id",
                        "applicationInstanceId": "myInstanceId",
                    },
                    "payload": {
                        "user": {"someUserKey": "someUserValue"},
                        "signup": {"someSignupKey": "someSignupValue"},
                    },
                }
            ]
        }


class MessageTrait(BaseModel):
    """
    Describes a trait that MAY be applied to a Message Object. This object MAY contain
    any property from the Message Object, except payload and traits.
    If you're looking to apply traits to an operation, see the Operation Trait Object.
    """

    headers: Optional[Union[ApiSchema, Reference]] = None
    """
    Schema definition of the application headers. Schema MUST be of type "object". It
    MUST NOT define the protocol headers.
    """

    correlationId: Optional[Union[CorrelationId, Reference]] = None
    """
    Definition of the correlation ID used for message tracing or matching.
    """

    schemaFormat: Optional[str] = None
    """
    A string containing the name of the schema format/language used to define the message
    payload. If omitted, implementations should parse the payload as a Schema object.
    """

    contentType: Optional[str] = None
    """
    The content type to use when encoding/decoding a message's payload. The value MUST be
    a specific media type (e.g. application/json). When omitted, the value MUST be the
    one specified on the defaultContentType field.
    """

    name: Optional[str] = None
    """
    A machine-friendly name for the message.
    """

    title: Optional[str] = None
    """
    A human-friendly title for the message.
    """

    summary: Optional[str] = None
    """
    A short summary of what the message is about.
    """

    description: Optional[str] = None
    """
    A verbose explanation of the message. CommonMark syntax can be used for rich text
    representation.
    """

    tags: Optional[List[ApiTag]] = None
    """
    A list of tags for API documentation control. Tags can be used for logical grouping
    of operations.
    """

    bindings: Optional[Union[MessageBindings, Reference]] = None
    """
    A map where the keys describe the name of the protocol and the values describe
    protocol-specific definitions for the message.
    """

    examples: Optional[List[MessageExample]] = None
    """
    List of examples.
    """

    class Config:
        extra = Extra.forbid
        schema_extra = {
            "examples": [
                {
                    "schemaFormat": "application/vnd.apache.avro+json;version=1.9.0",
                    "contentType": "application/json",
                }
            ]
        }


 


class ApiMessage(BaseModel):
    """
    Describes a message received on a given channel and operation.
    """

    headers: Optional[Union[ApiSchema, Reference]] = None

    payload: Optional[ApiSchema] = None

    correlationId: Optional[Union[CorrelationId, Reference]] = None

    schemaFormat: Optional[str] = None

    contentType: Optional[str] = None

    name: Optional[str] = None

    title: Optional[str] = None

    summary: Optional[str] = None

    description: Optional[str] = None

    tags: Optional[List[ApiTag]] = None

    bindings: Optional[Union[MessageBindings, Reference]] = None

    examples: Optional[List[MessageExample]] = None

    traits: Optional[List[Union[MessageTrait, Reference]]] = None

    x_response: Optional[ApiSchema] = Field(alias="x-response")

    class Config:
        extra = Extra.forbid
