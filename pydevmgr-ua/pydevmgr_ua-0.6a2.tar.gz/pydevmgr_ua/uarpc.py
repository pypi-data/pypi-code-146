from pydevmgr_core import BaseRpc
from .register import register 
from .uaengine import UaRpcEngine
from .uacom import UaComHandler

from opcua import ua
from typing import  Any

class UaRpcConfig(BaseRpc.Config, UaRpcEngine.Config):
    type: str = 'Ua'

@register        
class UaRpc(BaseRpc):
    """ Object representing a value rpc node in opc-ua server """
    Config = UaRpcConfig
    Engine = UaRpcEngine 
    com_handler = UaComHandler()
    
    
    @property
    def sid(self) -> Any:
        return self.com_handler.get_server_id( self.engine) 
    
    @property
    def uanodeid(self) -> ua.NodeId:
        return self.com_handler.get_nodeid( self.engine)
        
    def get_error_txt(self, rpc_error: int) -> str:
        """ get a text description of the rpc_error code 
        
        See the enumerator RPC_ERROR attribute 
        
        Args:
            rpc_error (int): rpc error code  
        """
        return 'unknown error'
    
    def fcall(self, *args) -> int:
        """ call method on serser, the arguments has been parsed before """ 
        return self.com_handler.call_method( self.engine, *args)
    
    
  
