class Config:
    ask: bool = True


config: Config = Config()


from .ask import confirm
from .cp import copy
from .mv import move
from .net import download
from .rm import remove
from .run import execute
