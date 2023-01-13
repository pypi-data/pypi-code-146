import os

from . import config
from .helpers import parseRecipeHeader


class Defaults:
    def __init__(self, name='o2-dataflow'):
        self.name = name
        filename = 'defaults-%s.sh' % name
        self.path = os.path.join(config.ali_prefix, 'alidist', filename)
        parsed = parseRecipeHeader(self.path)
        self.disable = parsed['disable']
