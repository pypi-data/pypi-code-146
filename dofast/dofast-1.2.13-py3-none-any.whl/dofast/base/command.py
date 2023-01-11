#!/usr/bin/env python3
from typing import List, Union, Callable, Set, Dict, Tuple, Optional
from codefast.patterns.factory_method import Command
from abc import abstractmethod

class CliCommand(Command):
    """命令行命令"""

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def _execute(self, func):
        pass 
    
    def execute(self):
        self._execute()
        
        