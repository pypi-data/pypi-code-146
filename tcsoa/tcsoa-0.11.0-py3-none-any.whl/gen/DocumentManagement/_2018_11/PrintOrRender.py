from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ContainsRenderableFilesResponse(TcBaseObj):
    """
    Contains Renderable Files Response structure consisting of a list of renderable files and the service data.
    
    :var objectsWithRenderableFiles: A list of objects (from 'selectedObjects') that contain renderable files.
    :var serviceData: Standard return; includes any error information.
    """
    objectsWithRenderableFiles: List[BusinessObject] = ()
    serviceData: ServiceData = None
