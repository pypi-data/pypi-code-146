from alidaargparser import get_asset_property
from .storages.storage import Storage
from .metadata.metadata import Metadata
from .notifier import Notifier

class GOManager:
    
    def __init__(self) -> None:
        self.storage = Storage(base_path=get_asset_property(asset_name="go_manager", property="base_path"), 
                                storage_type=get_asset_property(asset_name="go_manager", property="storage_type"))
        self.notifier = Notifier(get_asset_property(asset_name="go_manager", property="topic"))
        self.outputs = {}

    def save(self, path, metadata=None):
        metadata.set_extension_based_on_path(path)
        metadata.set_filename_based_on_path(path)
        self.outputs[metadata.get_name()] = {"path": path, 
                                            "metadata": metadata }
        self.storage.save(metadata=metadata, path=path)

        self.notifier.something_has_changed(metadata)

    def update(self, name):
        path = self.outputs[name]["path"]
        metadata = self.outputs[name]["metadata"]
        self.save(path, metadata)
        self.notifier.something_has_changed(metadata)

    def remove(self, name):
        path = self.outputs[name]["path"]
        self.storage.remove(path)

    def list_outputs(self):
        files = self.storage.list_files()

        return files
