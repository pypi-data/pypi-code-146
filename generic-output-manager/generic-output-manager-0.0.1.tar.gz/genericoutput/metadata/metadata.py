import os 

class Metadata:
    
    def __init__(self, name, type) -> None:
        self.raw = {}
        self.set(name=name, type=type)

    def load_from_json(self, json):
        self.raw = json

    def get_name(self):
        return self.raw['name']

    def set(self, name, type):
        self.raw['name'] = name
        self.raw['type'] = type
    
    def set_extension(self, extension):
        self.raw['extension'] = extension
    
    def set_extension_based_on_path(self, path):
        self.set_extension(path.split(".")[-1])
    
    def set_filename_based_on_path(self, path):
        self.raw['filename'] = os.path.basename(os.path.normpath(path))

    def get_meta_path(self):
        return self.raw['filename'] + ".json"

    def get(self):
        return self.raw
