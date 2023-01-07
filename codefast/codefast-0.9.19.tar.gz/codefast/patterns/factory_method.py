#!/usr/bin/env python3
import os
from abc import ABC, abstractmethod

class Command(ABC):

    @abstractmethod
    def execute(self):
        pass

class HelpCommand(Command):
    """帮助命令"""

    def execute(self):
        print("Help information:")
        print("  -h: show help information")


class CommandFactory(ABC):
    """命令工厂抽象类"""

    @abstractmethod
    def create_command(self, *args):
        pass


class HelpCommandFactory(CommandFactory):
    """帮助命令工厂"""

    def create_command(self, *args):
        return HelpCommand()


class CommandFactoryRegistry:
    """命令工厂注册器"""

    _registry = {}

    @classmethod
    def register_factory(cls, name:str, factory):
        cls._registry[name] = factory

    @classmethod
    def create_command(cls, name:str, *args):
        if name not in cls._registry:
            raise ValueError("Unsupported command")

        return cls._registry[name].create_command(*args)


if __name__ == "__main__":
    # 注册命令工厂
    CommandFactoryRegistry.register_factory("-h", HelpCommandFactory())
    # 创建命令
    cmd1 = CommandFactoryRegistry.create_command("-h", HelpCommandFactory())
    cmd1.execute()
    
