from abc import ABC, abstractmethod
import logging

class Storage(ABC):

    def __new__(cls, *args, **kw):
        
        
        if 'storage_type' in kw:
            storage_type = kw['storage_type'].lower()
        else:
            storage_type = "filesystem"

        # Create a map of all subclasses based on storage_type property (present on each subclass)
        subclass_map = {subclass.storage_type: subclass for subclass in cls.__subclasses__()}


        # Select the proper subclass based on
        subclass = subclass_map[storage_type]
        instance = super(Storage, subclass).__new__(subclass)
        return instance
    
    def __init__(self, base_path, storage_type = None):
        self.base_path = base_path
        super().__init__()

    @abstractmethod
    def list_files(self):
        pass

    @abstractmethod
    def save(self, name, path, metadata):
        pass