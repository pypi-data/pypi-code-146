from typing import Any, Optional, Tuple, Union
from .uaengine import UaEngine, UaNodeEngine, UaRpcEngine
import opcua
from opcua import ua


# for backward compatibility 
class UaCom(UaEngine):
    """ Built an UaEngine with OPC-UA connection """
    def __init__(self, **kwargs):
        engine = UaEngine.new(None, UaEngine.Config(**kwargs))
        self.__dict__.update( engine.__dict__)
        
    


class UAReadCollector:
    """ A Collector to read the value of multiple opc-ua nodes in one roundtrip 
    
    Args:
        uaclient (:class:`opcua.Client`)
    """
    def __init__(self, uaclient: opcua.Client) -> None:
        params =  ua.ReadParameters()
        params.uaclient = uaclient
        self._keys = list()
        self._params = params
                
    def add(self, node) -> None:
        """ Add a UaNode to the queue 
        
        Args:
            node (:class:`pydevmgr.UaNode`): node to add in the key. 
                Note this is a pydevmgr UaNode and not an opcua.Node
        """
        rv = ua.ReadValueId()
        rv.NodeId = node.uanodeid
        #rv.AttributeId = ua.AttributeIds.Value
        rv.AttributeId = node.config.attribute
        self._params.NodesToRead.append(rv)
        self._keys.append(node)
    
    def read(self, data: dict) -> None:
        """ read all data from server and feed result in the input dictionary """
        result = self._params.uaclient.read(self._params)
        for key,r in zip(self._keys, result):
            r.StatusCode.check()
            data[key] =  r.Value.Value 

class UAWriteCollector:
    """ A Collector to write the value of multiple opc-ua nodes in one roundtrip 
    
    Args:
        uaclient (:class:`opcua.Client`)
    """
    def __init__(self, uaclient: opcua.Client) -> None:
        params =  ua.WriteParameters()
        params.NodesToWrite = []        
        params.uaclient = uaclient
        self._params = params
        
        
    def add(self, node, value: Any) -> None:   
        """ Add a node and its attached value to the queue 
        
        Args:
            node (:class:`pydevmgr.UaNode`): node to add in the key. 
                Note this is a pydevmgr UaNode and not an opcua.Node
            value (any): value to be writen 
        
        """ 
        wv = ua.WriteValue()
        wv.NodeId = node.uanodeid
        wv.AttributeId = ua.AttributeIds.Value
        wv.AttributeId = node.config.attribute 
        self._params.NodesToWrite.append(wv)
        wv.Value = node._parse_value_for_ua(value)
    
    def write(self) -> None:
        """ Write all values to server """
        params = self._params
        result = params.uaclient.write(params)
        for r in result: 
            r.check()

class UaComHandler:
    """ Ua Communication handler from engine structure 
        
        The engine structure must contains client communication
        At least 
            .client 
            and 
            .node_client for node related methods 
    
    """
    @staticmethod
    def connect( engine: Union[UaEngine, UaNodeEngine]):        
        engine.client.connect()
    
    @staticmethod
    def disconnect( engine: Union[UaEngine, UaNodeEngine]):  
        engine.client.disconnect()      
    
    @staticmethod
    def is_connect( engine: Union[UaEngine, UaNodeEngine]):
        client = engine.client
        if client is None:
            return False
        if client.uaclient and client.uaclient._uasocket:
            t = client.uaclient._uasocket._thread
            return t and t.is_alive()
        return False

    @staticmethod
    def get_server_id(engine: UaNodeEngine) -> Any:
        """ Return a unique server identification. shall be any hashable object """ 
        try:
            return engine.node_client._sid_
        except AttributeError:
            pass 
       
        # The only way I found is this one if their is a connection
        if engine.node_client.server._uasocket:
            if engine.node_client.server._uasocket._socket.socket.fileno()>0:
                sid = engine.node_client.server._uasocket._socket.socket.getpeername()

                engine.node_client._sid_ = sid
                return sid
        # unconnected sid, should not really mater what the output is (except None reserved for aliases)
        return 999        

    @staticmethod
    def get_nodeid(engine):
        return engine.node_client.nodeid

    @staticmethod 
    def call_method( engine: UaRpcEngine, *args) -> int:
        return engine.node_client.call_method(engine.method_id, *args)
    
    @staticmethod
    def get_value( engine: UaNodeEngine) -> Any:
        """ get the node value from OPC-UA server """
        return engine.node_client.get_value()
    
    @staticmethod
    def get_attribute( engine: UaNodeEngine, a:str):
        """ get the node attribute from OPC-UA server """
        
        result = engine.node_client.get_attribute(a)
        return result.Value.Value
    
    @staticmethod
    def set_attribute(engine: UaNodeEngine, a: ua.AttributeIds, value: Any):
        if a == ua.AttributeIds.Value:
            return engine.node_client.set_value(value)
        else:
            return engine.node_client.set_attribute(a, value)
    
    @staticmethod
    def set_value( engine: UaNodeEngine, datavalue: ua.DataValue) -> None:
        """ set the node value to server 
        
        Args:
            datavalue (:class:`ua.DataValue`): DataValue as returned by the method :meth:`UaNodeEngine.parse_value`
        """
        engine.node_client.set_attribute(ua.AttributeIds.Value, datavalue)
    
    @staticmethod
    def read_collector( engine: UaNodeEngine) -> UAReadCollector:
        """ Return a :class:`UAReadCollector` to collect nodes for reading node values on the server """
        return UAReadCollector(engine.node_client.server)
    
    @staticmethod     
    def write_collector( engine: UaNodeEngine) -> UAWriteCollector:
        """ Return a :class:`UAWriteCollector` to collect nodes for writing node values on the server """
        return UAWriteCollector(engine.node_client.server)

    @staticmethod
    def parse_value(engine, value: Any) -> ua.DataValue:
        """ parse a value to a  :class:`ua.DataValue` 
        
        Args:
            value (int, float, str, :class:`ua.Variant`,  :class:`ua.DataValue`)
                note if int, to remove ambiguity between int64, int32, the real variant is asked to 
                the server the first time than cashed. This should rarely append as UA type will be  
                parsed through the :class:`pydevmgr.UaNode`.
                
        """
        if isinstance(value, (int,)):
            # remove embiguity between int64 and int32, int16
            # we need to ask the variant_type on the server
            if engine._ua_variant_type is None:
                engine._ua_variant_type = engine.node_client.get_data_type_as_variant_type()
            datavalue = ua.DataValue(ua.Variant(value, engine._ua_variant_type))
        elif isinstance(value, ua.DataValue):
            datavalue = value
        elif isinstance(value, ua.Variant):
            datavalue = ua.DataValue(value)
        else:
            datavalue = ua.DataValue(value)
        return datavalue 


