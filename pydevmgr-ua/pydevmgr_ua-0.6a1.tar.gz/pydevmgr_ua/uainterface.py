from pydevmgr_core import  BaseInterface
from .register import register 
from .uacom import UaComHandler
from .uanode import UaNode
from .uaengine import UaEngine
from .uarpc import UaRpc

class UaInterfaceConfig(BaseInterface.Config, UaEngine.Config,  extra="allow"):
    Node = UaNode.Config
    Rpc = UaRpc.Config

    type: str = "Ua"
    prefix: str = "" # prefix added to com.prefix 
     
@register    
class UaInterface(BaseInterface):
    """ Interface containing :class:`pydevmgr_ua.UaNode` or :class:`pydevmgr_ua.UaRpcNode` objects
    
    Each :class:`pydevmgr_ua.UaNode` will inerit from the Ua Client communication and will have the
       UA prefix of the interface  
    
    Note, the .com attribute is a (sub)UaCom object built from the com class argument 
        
    The UA prefix can be defined in the interface config or in the com object or in both:
    
    
    e.g. on the example bellow the 3 UaInterface instances will have the same prefix
    
    :: 
       
       from pydevmgr_ua import UaCom, UaInterface
       i1 = UaInterface(prefix="MAIN.stat" ,  com=UaCom(prefix="") )
       i2 = UaInterface(prefix="stat" ,  com=UaCom(prefix="MAIN") )
       i3 = UaInterface(prefix="" ,  com=UaCom(prefix="MAIN.stat") )
       
       assert i1.com.prefix == i2.com.prefix
       assert i2.com.prefix == i3.com.prefix
    
    
    Args:
        
        key (str): a unique key defining the interface. This is generally the same key as the host 
                  :class:`Device`. e.g. mgr.motor1.key ==  mgr.motor1.stat.key == mgr.motor1.cfg.key
        config (optional, :class:`pydevmgr_ua.UaInterface.Config`): configuration of the interface 
        com (optional, :class:`UaCom`, :class:`opcua.Client`, dict, str): 
            - if str create a :class:`UaCom` from the str address 
            - if :class:`opcua.Client` wrap it in a :class:`UaCom`
            - if :class:`UaCom` use it
        * *kwargs: If configuration is  None they are used to build the config otherwise they are ignored 
    
            
    """
           
    Config = UaInterfaceConfig
    Engine = UaEngine
    Node = UaNode
    Rpc = UaRpc
    com_handler = UaComHandler() 

