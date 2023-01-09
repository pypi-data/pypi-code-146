from pydevmgr_core import BaseDevice
from .register import register
from .uacom import UaComHandler
from .uainterface import UaInterface
from .uanode import UaNode
from .uarpc import UaRpc
from .uaengine import UaEngine

@register
class UaDevice(BaseDevice):
    Node = UaNode
    Rpc = UaRpc
    Interface = UaInterface
    Engine = UaEngine
    com_handler = UaComHandler
    
    class Config(BaseDevice.Config, UaEngine.Config):
        Node = UaNode.Config
        Interface = UaInterface.Config
        Rpc = UaRpc.Config


    def connect(self):
        """ Connect to the OPC-UA client """
        return self.com_handler.connect(self.engine)
        
    def disconnect(self):
        """ Connect from the  OPC-UA client """
        return self.com_handler.disconnect(self.engine)
    
    def is_connected(self):
        return self.com_handler.is_connect(self.engine)
    
    
