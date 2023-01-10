from typing import List, Optional, Union

from pydantic import Extra

from aiosox.utils import BaseModel

from .bindings import (
    HttpOperationBinding,
    KafkaOperationBinding,
    WebSocketsOperationBinding,
)
from .message import ApiMessage
from .reference import Reference
from .tag import ApiTag


class OperationBindings(BaseModel):
    """
    Map describing protocol-specific definitions for a operation.
    """

    http: Optional[HttpOperationBinding] = None
    """
    Protocol-specific information for an HTTP operation.
    """

    socketio: Optional[WebSocketsOperationBinding] = None
    """
    Protocol-specific information for a WebSockets operation.
    """

    kafka: Optional[KafkaOperationBinding] = None
    """
    Protocol-specific information for a Kafka operation.
    """


class OperationTrait(BaseModel):
    """
    Describes a trait that MAY be applied to an Operation Object. This object MAY contain any
    property from the Operation Object, except message and traits.
    """

    operationId: Optional[str] = None
    """
    Unique string used to identify the operation. The id MUST be unique among all operations described
    in the API. The operationId value is case-sensitive. Tools and libraries MAY use the operationId to
    uniquely identify an operation, therefore, it is RECOMMENDED to follow common programming naming
    conventions.
    """

    summary: Optional[str] = None
    """
    A short summary of what the operation is about.
    """

    description: Optional[str] = None
    """
    A verbose explanation of the operation. CommonMark syntax can be used for rich text representation.
    """

    tags: Optional[List[ApiTag]] = None
    """
    A list of tags for API documentation control. Tags can be used for logical grouping of operations.
    """

    bindings: Optional[Union[OperationBindings, Reference]] = None
    """
    A map where the keys describe the name of the protocol and the values describe protocol-specific
    definitions for the operation.
    """

    class Config:
        extra = Extra.forbid
        schema_extra = {"examples": [{"bindings": {"amqp": {"ack": False}}}]}


class ApiOperation(BaseModel):
    """Describes a publish or a subscribe operation. This provides a place to document
    how and why messages are sent and received.
    For example, an operation might describe a chat application use case where a user
    sends a text message to a group. A publish operation describes messages that are
    received by the chat application, whereas a subscribe operation describes messages
    that are sent by the chat application."""

    operationId: Optional[str] = None
    """
    Unique string used to identify the operation. The id MUST be unique among all
    operations described in the API. The operationId value is case-sensitive. Tools and
    libraries MAY use the operationId to uniquely identify an operation, therefore, it
    is RECOMMENDED to follow common programming naming conventions.
    """

    summary: Optional[str] = None
    """
    A short summary of what the operation is about.
    """

    description: Optional[str] = None
    """
    A verbose explanation of the operation. CommonMark syntax can be used for rich
    text representation.
    """

    tags: Optional[List[ApiTag]] = None
    """
    A list of tags for API documentation control. Tags can be used for logical grouping
    of operations.
    """

    bindings: Optional[Union[OperationBindings, Reference]] = None
    """
    A map where the keys describe the name of the protocol and the values describe
    protocol-specific definitions for the operation.
    """

    traits: Optional[List[Union[OperationTrait, Reference]]] = None
    """
    A list of traits to apply to the operation object. Traits MUST be merged into the
    operation object using the JSON Merge Patch algorithm in the same order they are
    defined here.
    """

    message: Optional[Union[ApiMessage, Reference]] = None
    """
    A definition of the message that will be published or received by this operation.
    Map containing a single oneOf key is allowed here to specify multiple messages.
    However, a message MUST be valid only against one of the message objects.
    """

    class Config:
        extra = Extra.forbid
        schema_extra = {
            "examples": [
                {
                    "operationId": "registerUser",
                    "summary": "Action to sign a user up.",
                    "description": "A longer description",
                    "tags": [{"name": "user"}, {"name": "signup"}, {"name": "register"}],
                    "message": {
                        "headers": {
                            "type": "object",
                            "properties": {
                                "applicationInstanceId": {
                                    "description": "Unique identifier for a given instance of the publishing application",
                                    "type": "string",
                                }
                            },
                        },
                        "payload": {
                            "type": "object",
                            "properties": {
                                "user": {"$ref": "#/components/schemas/userCreate"},
                                "signup": {"$ref": "#/components/schemas/signup"},
                            },
                        },
                    },
                    "bindings": {"amqp": {"ack": False}},
                    "traits": [{"$ref": "#/components/operationTraits/kafka"}],
                }
            ]
        }
