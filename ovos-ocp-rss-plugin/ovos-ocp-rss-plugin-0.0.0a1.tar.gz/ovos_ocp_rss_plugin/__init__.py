import feedparser

from ovos_plugin_manager.templates.ocp import OCPStreamExtractor


class OCPRSSFeedExtractor(OCPStreamExtractor):
    def __init__(self, ocp_settings=None):
        super().__init__(ocp_settings)
        self.settings = self.ocp_settings.get("rss", {})

    @property
    def supported_seis(self):
        """
        skills may return results requesting a specific extractor to be used

        plugins should report a StreamExtractorIds (sei) that identifies it can handle certain kinds of requests

        any streams of the format "{sei}//{uri}" can be handled by this plugin
        """
        return ["rss"]

    def extract_stream(self, uri, video=True):
        """ return the real uri that can be played by OCP """
        return self.get_rss_first_stream(uri)

    @staticmethod
    def get_rss_first_stream(feed_url):
        try:
            # extract_streams RSS or XML feed
            data = feedparser.parse(feed_url.strip())
            # After the intro, find and start the news uri
            # select the first link to an audio file

            for meta in data['entries'][0]['links']:
                if 'audio' in meta['type']:
                    # TODO return duration for proper display in UI
                    duration = meta.get('length')
                    meta["uri"] = link['href']
                    return meta
        except Exception as e:
            pass
        return {}
