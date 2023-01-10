from .dataset.dataset import *  # noqa: F403
from .connection.url import *  # noqa: F403
from .logging.log import *  # noqa: F403
from .storage.remotefunction import *  # noqa: F403

__all__ = ['Dataset', 'URL', 'RemoteFunction']   # noqa: F405
__version__ = '0.5.4'

# attach a global Logger to the manager
Logger = Handler()    # noqa: F405


# ipython magic
def load_ipython_extension(ipython):
    from remotemanager.jupyter.magic import RCell
    ipython.register_magics(RCell)
