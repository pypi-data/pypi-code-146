'''
Contains classes for interactions with declarations on NetOrca
'''
from netorca_sdk.base import BaseObj

class ApplicationObj(BaseObj):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
