from typing import Any, Dict, List, Mapping, Optional, Sequence, Set, Type, Union

from fastapi.encoders import jsonable_encoder
from pydantic import AnyUrl, Extra, Field, constr, root_validator, validator

from aiosox.utils import BaseModel

from .bindings import ApiServerBindings, ChannelBindings
from .channel import ApiChannel
from .message import ApiMessage, CorrelationId, MessageBindings, MessageTrait
from .operation import OperationBindings, OperationTrait
from .parameter import ApiParameter
from .reference import Reference
from .schema import ApiSchema
from .security import ApiSecurityScheme
from .server import ApiServer

ComponentKey = str


class ApiComponents(BaseModel):
    """
    Holds a set of reusable objects for different aspects of the AsyncAPI specification. All
    objects defined within the components object will have no effect on the API unless they
    are explicitly referenced from properties outside the components object.
    """

    schemas: Optional[Dict[ComponentKey, Union[ApiSchema, Reference]]] = None
    """
    An object to hold reusable Schema Objects.
    """

    servers: Optional[Dict[ComponentKey, Union[ApiServer, Reference]]] = None
    """
    An object to hold reusable Server Objects.
    """

    channels: Optional[Dict[ComponentKey, ApiChannel]] = None
    """
    An object to hold reusable Channel Item Objects.
    """

    messages: Optional[Dict[ComponentKey, Union[ApiMessage, Reference]]] = None
    """
    An object to hold reusable Message Objects.
    """

    security_schemes: Optional[Dict[ComponentKey, Union[ApiSecurityScheme, Reference]]] = None
    """
    An object to hold reusable Security Scheme Objects.
    """

    parameters: Optional[Dict[ComponentKey, Union[ApiParameter, Reference]]] = None
    """
    An object to hold reusable Parameter Objects.
    """

    correlationIds: Optional[Dict[ComponentKey, Union[CorrelationId, Reference]]] = None
    """
    An object to hold reusable Correlation ID Objects.
    """

    operationTraits: Optional[Dict[ComponentKey, Union[OperationTrait, Reference]]] = None
    """
    An object to hold reusable Operation Trait Objects.
    """

    messageTraits: Optional[Dict[ComponentKey, Union[MessageTrait, Reference]]] = None
    """
    An object to hold reusable Message Trait Objects.
    """

    serverBindings: Optional[Dict[ComponentKey, Union[ApiServerBindings, Reference]]] = None
    """
    An object to hold reusable Server Bindings Objects.
    """

    channelBindings: Optional[Dict[ComponentKey, Union[ChannelBindings, Reference]]] = None
    """
    An object to hold reusable Channel Bindings Objects.
    """

    operationBindings: Optional[Dict[ComponentKey, Union[OperationBindings, Reference]]] = None
    """
    An object to hold reusable Operation Bindings Objects.
    """

    messageBindings: Optional[Dict[str, Union[MessageBindings, Reference]]] = None
    """
    An object to hold reusable Message Bindings Objects.
    """

    class Config:
        extra = Extra.forbid
        schema_extra = {
            "examples": [
                {
                    "components": {
                        "schemas": {
                            "Category": {
                                "type": "object",
                                "properties": {
                                    "id": {"type": "integer", "format": "int64"},
                                    "name": {"type": "string"},
                                },
                            },
                            "Tag": {
                                "type": "object",
                                "properties": {
                                    "id": {"type": "integer", "format": "int64"},
                                    "name": {"type": "string"},
                                },
                            },
                        },
                        "servers": {
                            "development": {
                                "url": "development.gigantic-server.com",
                                "description": "Development server",
                                "protocol": "amqp",
                                "protocolVersion": "0.9.1",
                            }
                        },
                        "channels": {
                            "user/signedup": {
                                "subscribe": {
                                    "message": {"$ref": "#/components/messages/userSignUp"}
                                }
                            }
                        },
                        "messages": {
                            "userSignUp": {
                                "summary": "Action to sign a user up.",
                                "description": "Multiline description of what this action does.\nHere you have another line.\n",
                                "tags": [{"name": "user"}, {"name": "signup"}],
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
                            }
                        },
                        "parameters": {
                            "userId": {
                                "description": "Id of the user.",
                                "schema": {"type": "string"},
                            }
                        },
                        "correlationIds": {
                            "default": {
                                "description": "Default Correlation ID",
                                "location": "$message.header#/correlationId",
                            }
                        },
                        "messageTraits": {
                            "commonHeaders": {
                                "headers": {
                                    "type": "object",
                                    "properties": {
                                        "my-app-header": {
                                            "type": "integer",
                                            "minimum": 0,
                                            "maximum": 100,
                                        }
                                    },
                                }
                            }
                        },
                    }
                }
            ]
        }
