from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GetViewableDataResponse(TcBaseObj):
    """
    Output structure for getViewableData operation.
    
    :var output: List of ViewerData objects, one for each input object.
    :var serviceData: The service data contains any partial errors which may have been encountered during processing.
    All BusinessObjects which are returned are added to the serviceData plainObjects list.
    """
    output: List[ViewerData] = ()
    serviceData: ServiceData = None


@dataclass
class TypeToNamedRefPair(TcBaseObj):
    """
    The 'TypeToNamedRefPair' structure contains the Named Reference type string, as well as a list of file tickets that
    Named Reference type, so the client may download the files.
    
    :var namedRefType: The named reference type string. For example for an MSWord dataset, it might have a Named
    Reference with type word.
    :var fileTickets: List of file ticket strings.
    """
    namedRefType: str = ''
    fileTickets: List[str] = ()


@dataclass
class ViewerData(TcBaseObj):
    """
    The ViewerData structure contains all the data required in order for a client to present viewable data for the
    input object in a client.
    
    :var inputObj: The input object which this output represents.
    :var viewerID: The target viewer ID to load in the client.
    :var viewableObj: The target object to view.  If it's a dataset, then the viewableNameRefs field may be populated
    depending on the defaultViewerConfig.VIEWERCONFIG (or <viewer config id>.VIEWERCONFIG) preference that defines the
    rules for viewing an object.
    :var traversal: The list of objects traversed from the input object to the viewable object.
    :var viewableNamedRefs: List of viewable named references.  This structure includes the named reference string and
    a list of 'fileTickets' so the client may download the files.
    
    This field is only populated if the 'viewableObj' is a Dataset type, and the rules define its named references as
    being viewable.
    """
    inputObj: BusinessObject = None
    viewerID: str = ''
    viewableObj: BusinessObject = None
    traversal: List[BusinessObject] = ()
    viewableNamedRefs: List[TypeToNamedRefPair] = ()
