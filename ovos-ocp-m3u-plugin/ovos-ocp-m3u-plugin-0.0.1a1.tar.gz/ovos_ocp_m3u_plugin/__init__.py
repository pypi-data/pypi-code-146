import requests
from ovos_plugin_manager.templates.ocp import OCPStreamExtractor


class OCPPlaylistExtractor(OCPStreamExtractor):
    def __init__(self, ocp_settings=None):
        super().__init__(ocp_settings)
        self.settings = self.ocp_settings.get("m3u", {})

    @property
    def supported_seis(self):
        """
        skills may return results requesting a specific extractor to be used

        plugins should report a StreamExtractorIds (sei) that identifies it can handle certain kinds of requests

        any streams of the format "{sei}//{uri}" can be handled by this plugin
        """
        return ["m3u", "pls"]

    def validate_uri(self, uri):
        """ return True if uri can be handled by this extractor, False otherwise"""
        return "pls" in uri or ".m3u" in uri

    def extract_stream(self, uri, video=True):
        """ return the real uri that can be played by OCP """
        return self.get_playlist_stream(uri)

    @staticmethod
    def get_playlist_stream(uri):
        # .pls and .m3u are not supported by gui player, parse the file
        txt = requests.get(uri).text
        for l in txt.split("\n"):
            if l.startswith("http"):
                return {"uri": l}
        return {"uri": uri}

