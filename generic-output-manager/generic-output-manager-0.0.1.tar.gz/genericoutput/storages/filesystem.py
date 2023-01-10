from .storage import Storage
import os
import glob
import shutil
import json


class Filesystem(Storage):
    storage_type = os.path.basename(__file__).split('.py')[0]
    
    def __init__(self, base_path, storage_type=None):
        super().__init__(base_path, storage_type)

    def list_files(self):
        return glob.glob(os.path.join(self.base_path, '*.json'))
    
    def save(self, path, metadata):
        dst = os.path.join(self.base_path, os.path.basename(os.path.normpath(path)))
        shutil.copyfile(path, dst)
        metadataDst = dst + ".json"
        with open(metadataDst, "w") as write_file:
            json.dump(metadata.get(), write_file, indent=4)

    def remove(self, path):
        dst = os.path.join(self.base_path, os.path.basename(os.path.normpath(path)))
        os.remove(dst)
        metadataDst = dst + ".json"
        os.remove(metadataDst)