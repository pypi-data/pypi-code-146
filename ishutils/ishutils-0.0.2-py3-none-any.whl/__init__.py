__version__: str = "0.0.2"


from ._config import Config

config = Config()


from .action.confirm import confirm
from .action.cp import copy
from .action.download import download
from .action.extract import extract
from .action.move import move
from .action.remove import remove
from .action.run import run
