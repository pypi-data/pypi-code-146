from grai_schemas.models import GraiNodeMetadata, GraiEdgeMetadata
from typing import Union
from pydantic import BaseModel


class Metadata(BaseModel):
    grai: Union[GraiNodeMetadata, GraiEdgeMetadata]
