import feedparser

from ovos_plugin_manager.templates.ocp import OCPStreamExtractor
from ovos_ocp_rss_plugin import OCPRSSFeedExtractor


class OCPNewsExtractor(OCPStreamExtractor):
    NPR_URL = "https://www.npr.org/rss/podcast.php"
    TSF_URL = "https://www.tsf.pt/stream"
    GBP_URL = "http://feeds.feedburner.com/gpbnews"

    def __init__(self, ocp_settings=None):
        super().__init__(ocp_settings)
        self.settings = self.ocp_settings.get("news", {})

    @property
    def supported_seis(self):
        """
        skills may return results requesting a specific extractor to be used

        plugins should report a StreamExtractorIds (sei) that identifies it can handle certain kinds of requests

        any streams of the format "{sei}//{uri}" can be handled by this plugin
        """
        return ["news"]

    def validate_uri(self, uri):
        """ return True if uri can be handled by this extractor, False otherwise"""
        return any([uri.startswith(sei) for sei in self.supported_seis]) or \
               any([uri.startswith(url) for url in [
                   self.TSF_URL, self.GBP_URL, self.NPR_URL
               ]])

    def extract_stream(self, uri, video=True):
        """ return the real uri that can be played by OCP """
        if uri.startswith("news//"):
            uri = uri[6:]
        if uri.startswith(self.NPR_URL):
            return self.npr()
        elif uri.startswith(self.TSF_URL):
            return self.tsf()
        elif uri.startswith(self.GBP_URL):
            return self.gpb()

    @classmethod
    def tsf(cls):
        """Custom inews fetcher for TSF news."""
        feed = (f'{cls.TSF_URL}/audio/{year}/{month:02d}/'
                'noticias/{day:02d}/not{hour:02d}.mp3')
        uri = None
        i = 0
        status = 404
        date = now_local(timezone('Portugal'))
        while status != 200 and i < 6:
            uri = feed.format(hour=date.hour, year=date.year,
                              month=date.month, day=date.day)
            status = requests.get(uri).status_code
            date -= timedelta(hours=1)
            i += 1
        if status != 200:
            return None
        return uri

    @classmethod
    def gpb(cls):
        """Custom news fetcher for GBP news."""
        feed = f'{cls.GBP_URL}/GeorgiaRSS?format=xml'
        data = feedparser.parse(feed)
        next_link = None
        for entry in data['entries']:
            # Find the first mp3 link with "GPB {time} Headlines" in title
            if 'GPB' in entry['title'] and 'Headlines' in entry['title']:
                next_link = entry['links'][0]['href']
                break
        html = requests.get(next_link)
        # Find the first mp3 link
        # Note that the latest mp3 may not be news,
        # but could be an interview, etc.
        mp3_find = re.search(r'href="(?P<mp3>.+\.mp3)"'.encode(), html.content)
        if mp3_find is None:
            return None
        url = mp3_find.group('mp3').decode('utf-8')
        return url

    @classmethod
    def npr(cls):
        url = f"{cls.NPR_URL}?id=500005"
        feed = OCPRSSFeedExtractor.get_rss_first_stream(url)
        if feed:
            return feed["uri"].split("?")[0]
