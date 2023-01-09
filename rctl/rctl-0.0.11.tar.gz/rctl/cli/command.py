import logging
import os
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class CmdBase(ABC):
    def __init__(self, args):
        self.args = args

    def do_run(self):
        return self.run()
            
    @abstractmethod
    def run(self):
        pass


