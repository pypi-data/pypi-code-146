from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ProductImageInfo(TcBaseObj):
    """
    The input structure contains object(s) for which product image is to be set, the business object of the dataset 
    representing the image and the product Bill Of Processes (BOP) context.
    
    :var targetObjects: The list of business objects for which the product image is to be set.
    The valid types are as follows
    - Mfg0BvrProcessStation - process station.
    - Mfg0BvrProcessLine - process line.
    - Mfg0BvrProcessArea - process area.
    - Mfg0BvrPlantBOP - plant Bill Of Processes (BOP). 
    
    
    :var contextProductBOP: The business object representing the top line of the Product Bill Of Processes(BOP). This
    Product BOP is the context for which the product image is set with the targetObjects and is of type
    MEProductBOPRevision.
    This could be NULL provided that there is only one product BOP linked to the plant BOP. In case multiple product
    BOPs are linked then corresponding error will be reported.
    :var imageDataset: The business object of the dataset representing the product image. The same product image will
    be common for all the objects in the input parameter targetObjects.
    """
    targetObjects: List[BusinessObject] = ()
    contextProductBOP: BusinessObject = None
    imageDataset: BusinessObject = None


@dataclass
class TwpInfo(TcBaseObj):
    """
    Structure contains the object and its corresponding Time Way Plan (TWP) information.
    
    :var object: The object for which information is fetched.
    The valid types are 
    - Mfg0BvrProcessStation - process station
    - Mfg0BvrProcessLine - process line
    - Mfg0BvrProcessArea - process area
    - Mfg0BvrPlantBOP - plant bill of process (BOP) or
    - Mfg0BvrOperation - operation.
    
    
    :var detailedInfo: The map of string which is a data identifier and its corresponding Data.
    Description of valid strings and its data 
        "Operations": Represents the operations executed under the station. 
        "ExecutionPositions": Represents the execution positions for the object of TwpInfo stucture.
        "Direction": Represents the direction of the station in the plant.
        "ProductImage": Represents the product image for the station.
        "PlantCarpet": Represents the carpet diagram of the plant.
        "TWPLocationForms": Represents the business objects of the TWP Location form associated with the station.
    """
    object: BusinessObject = None
    detailedInfo: DetailedInformation = None


@dataclass
class TwpInfoInput(TcBaseObj):
    """
    The input structure contains object(s) for which information is required, the list of string specifying what
    information is required and the product Bill Of Process (BOP) context. The object can be process station(s),
    process line(s), process area(s), or plant BOP.
    
    :var requestedObjects: The list of business object for which TWP information is required. The valid types are
    process station, process line, process area or plant Bill Of Process (BOP). 
    :var contextProductBOP: The business object representing the top line of the Product Bill Of Process (BOP). This
    Product BOP is the context for which TWP information is fetched and is of type MEProductBOPRevision   .
    This could be NULL provided that there is only one product BOP linked to the plant BOP. In case multiple product
    BOPs are linked then corresponding error will be reported.
    :var requiredData: List of string specifying what information is required.
    The valid options are:
        OperationDetails: To fetch the operation details of given station.
    Response will consist of information about all the operations under the given station, the allocated time for those
    operations and their execution position. Other station related information such as length, width, X-Y Coordinates
    specifying its location in plant, orientation and direction will also be part of response.
        ExecutionPositions : To fetch the execution positions of the given station.
    Other station related information such as length, width, X-Y Coordinates specifying its location in plant,
    orientation and direction will also be part of response.
        ProductImage : To fetch the product image which will be displayed on the station in TWP view.
        PlantCarpet : To fetch the carpet image of the plant. This image is shown in the TWP view as plant layout.
    """
    requestedObjects: List[BusinessObject] = ()
    contextProductBOP: BusinessObject = None
    requiredData: List[str] = ()


@dataclass
class TwpResponse(TcBaseObj):
    """
    The response contains a structure of the TWP data and the ServiceData. The possible errors reported are:
        251048 - The Plant Bill Of Process (BOP) is linked to multiple Product BOPs. Please select one of the Product
    BOP as context.
        251049 - The input Product Bill Of Process (BOP) and Plant BOP are not linked.
    
    
    :var serviceData: The service data containing partial errors if any.
    :var infoMap: A map of business objects for which TWP information is requested and its corresponding TWP
    information.
    """
    serviceData: ServiceData = None
    infoMap: InformationMap = None


@dataclass
class Data(TcBaseObj):
    """
    The structure holds the property value.
    
    :var dataType: Type of the data. Valid types are "Boolean", "Character", "Integer", "Double", "String", "Tag" and
    "Date". One of the data in this structure need to be accessed based on the data type string.
    :var boolProperties: The list of Boolean values.
    :var charProperties: The string representing the list of characters. Each character in the string is a value of the
    property.
    :var integerProperties: The list of integer values.
    :var doubleProperties: The list of double values.
    :var stringProperties: The list of string values.
    :var tagProperties: The list of business objects.
    :var dateProperties: The list of dates.
    """
    dataType: str = ''
    boolProperties: List[bool] = ()
    charProperties: str = ''
    integerProperties: List[int] = ()
    doubleProperties: List[float] = ()
    stringProperties: List[str] = ()
    tagProperties: List[BusinessObject] = ()
    dateProperties: List[datetime] = ()


"""
The map of string which is a data identifier and its corresponding Data.
"""
DetailedInformation = Dict[str, Data]


"""
A map of business objects for which TWP information is requested and its corresponding TWP information.
"""
InformationMap = Dict[BusinessObject, TwpInfo]
