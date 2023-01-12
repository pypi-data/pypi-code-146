import os
from tomwer.core.tomwer_object import TomwerObject


class TomwerVolumeBase(TomwerObject):
    def get_identifier(self):
        return self.get_identifier()

    def _clear_heavy_cache(self):
        """util user"""
        self.data = None
        self.metadata = None

    def format_output_location(location: str, volume):
        if not isinstance(volume, TomwerVolumeBase):
            raise TypeError(
                f"volume is expected to be an instance of {TomwerVolumeBase}"
            )

        keywords = {
            "volume_data_parent_folder": volume.volume_data_parent_folder(),
        }
        for keyword, value in keywords.items():
            if value is None:
                continue
            try:
                location = location.format(**{keyword: value})
            except KeyError:
                pass
        return location

    def volume_data_parent_folder(self):
        if self.data_url is None:
            raise ValueError("data_url doesn't exists")
        else:
            return os.path.dirname(self.data_url.file_path())

    def __str__(self) -> str:
        try:
            return self.get_identifier().to_str()
        except Exception:
            return super().__str__()
