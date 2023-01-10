#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from poppy.core.command import Command

class RapCommands(Command):
    """
    Manage the commands relative to the FILM module.
    """
    __command__ = "rap"
    __command_name__ = "rap"
    __parent__ = "master"
    __parent_arguments__ = ["base"]
    __help__ = """
        Commands relative to the RAP module, responsible for 
        processing RPW L0, L1 and HK data.
    """


