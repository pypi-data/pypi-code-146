from pydevmgr_core import BaseNode
from .register import register 
from .uacom import UaComHandler, UAReadCollector, UAWriteCollector
from .uaengine import UaNodeEngine

from opcua import ua
from typing import Any
from pydantic import validator

class UaNodeConfig(BaseNode.Config, UaNodeEngine.Config):
    type: str = 'Ua'
    attribute: ua.AttributeIds = ua.AttributeIds.Value
    
    @validator("attribute", pre=True)
    def _validate_attribute(cls, value):
        if isinstance(value, str):
            return getattr(ua.AttributeIds, value)
        return value 


@register        
class UaNode(BaseNode):
    """ Object representing a value node in opc-ua server

    This is an interface representing one single value (node) in an OPC-UA server. 
    
    Args:
    
        key (str, optional): The string key representing the node in its context. If none a unique 
                   string key is build.
        config (optional, :class:`pydevmgr_ua.UaNode.Config`, dict): Config for the node
            includes: 
                - suffix (str): the node suffix in the OPC-UA server
                - attribute (uaAttributeIds) 
        
        For other arguments please see :class:`pydevmgr_core.BaseNode` documentation
                
    .. note::
            
                Several parser to ua Variant are defined in pydevmgr_ua and can be set with the `parser` argument: 
                
                - UaInt16, INT    (INT is an alias as TwinCat defines it)
                - UaInt32, DINT
                - UaInt64, LINT
                - UaUInt16, UINT
                - UaUInt32, UDINT
                - UaUInt64, ULINT
                - UaFloat, REAL
                - UaDouble, LREAL
                
                can also be created by VariantParser('Int16')                
                
    Example:
    
    In the example bellow it is assumed that the OPC UA server as a nodesid "ns=4;s=MAIN.Tamp001" node
    defined.
    
    ::
    
        >>> from pydevmgr_ua import UaNode, UaCom
        >>> com = UaCom(address=="opc.tcp://localhost:4840", namespace=4, prefix="MAIN")
        >>> temp = UaNode("temperature" , com=com, suffix="Temp001")
        >>> temp.get()
        
    Alternatively the com can be created on-the-fly
    

    One can build a UaInterface for several node 
    
    ::
    
        from pydevmgr_ua import UaInterface, UaNode, UaCom 
        from pydevmgr_core.nodes import Formula1
        
        class MyInterface(UaInterface):            
            temp_volt = UaNode.Config(suffix="Temp001")
            humidity = UaNode.Config(suffix="Humidity001")
            
            temp_kelvin = Formula1.Config(node="temp_volt", formula="230 + 1.234 * t", varname="t")
        
        com = UaCom(address= "opc.tcp://localhost:4840", namespace=4, prefix="MAIN")
        sensors = MyInterface('sensors', com=com)
        
                                    
    """
    Config = UaNodeConfig
    Engine = UaNodeEngine
    
    com_handler = UaComHandler()

    @property
    def sid(self) -> Any:
        return self.com_handler.get_server_id( self.engine) 
    
    @property
    def uanodeid(self) -> ua.NodeId:
        return self.com_handler.get_nodeid( self.engine)
               
    def read_collector(self) -> UAReadCollector:
        """ Return a :class:`UAReadCollector` object to queue nodes for reading """
        return self.com_handler.read_collector(self.engine)
    
    def write_collector(self) -> UAWriteCollector:
        """ Return a :class:`UAWriteCollector` object to queue nodes and values for writing """
        return self.com_handler.write_collector(self.engine)
    
    def fget(self) -> Any:
        """ get the value from server """
        return self.com_handler.get_attribute( self.engine, self.config.attribute)
    
    def fset(self, value: Any) -> None:
        """ set the value on server 
        
        Args:
            value (any): if :attr:`~UaNode.parser` is defined it is used to parse the value
                can be str, float, int, or :class:`ua.Variant` or  :class:`ua.DataValue` 
        """
        a = self.config.attribute
        datavalue = self._parse_value_for_ua(value) # is the node as a parser it as already been parsed 
        self.com_handler.set_attribute( self.engine, a, datavalue)    
            
    def _parse_value_for_ua(self, value: Any) -> None:
        return self.com_handler.parse_value(self.engine, value)
        
