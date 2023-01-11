from platon import (
    IPCProvider,
    Web3,
)
from platon.middleware import (
    gplaton_poa_middleware,
)
from platon.providers.ipc import (
    get_dev_ipc_path,
)

w3 = Web3(IPCProvider(get_dev_ipc_path()))
w3.middleware_onion.inject(gplaton_poa_middleware, layer=0)
