

from vxquant.model.exchange import vxAccountInfo
from vxsched import vxengine 
from vxsched.rpc import rpcwrapper


@rpcwrapper.register
def create_account(account_id, init_balance=1000000, on_error='skip') -> vxAccountInfo:
    
    