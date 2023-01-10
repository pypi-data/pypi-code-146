import enum
import json

import requests
from ovos_plugin_manager.templates.ocp import OCPStreamExtractor
from ovos_utils.log import LOG
from pytube import YouTube
from tutubo.models import Channel


class YoutubeBackend(str, enum.Enum):
    YDL = "youtube-dl"
    PYTUBE = "pytube"
    INVIDIOUS = "invidious"
    WEBVIEW = "webview"


class YdlBackend(str, enum.Enum):
    YDL = "youtube-dl"
    YDLC = "youtube-dlc"
    YDLP = "yt-dlp"
    AUTO = "auto"


class YoutubeLiveBackend(str, enum.Enum):
    REDIRECT = "redirect"  # url = f"https://www.youtube.com/c/{channel_name}/live"
    YDL = "youtube-dl"  # same as above, but always uses YoutubeBackend.YDL internally
    PYTUBE = "pytube"


class OCPYoutubeExtractor(OCPStreamExtractor):
    ydl = None
    live = None
    pytube = None
    invidious = None

    @classmethod
    def init_extractors(cls):
        cls.ydl = OCPYDLExtractor()
        cls.live = OCPYoutubeChannelLiveExtractor()
        cls.pytube = OCPPytubeExtractor()
        cls.invidious = OCPInvidiousExtractor()

    def __init__(self, ocp_settings=None):
        super().__init__(ocp_settings)
        self.settings = self.ocp_settings.get("youtube", {})
        # migrate old style OCP fields into youtube settings
        for k in ["youtube_backend", "youtube_live_backend",
                  "invidious_host", "ydl_backend", "proxy_invidious"]:
            if k not in self.settings:
                self.settings[k] = self.ocp_settings.get(k)

    @property
    def supported_seis(self):
        """
        skills may return results requesting a specific extractor to be used

        plugins should report a StreamExtractorIds (sei) that identifies it can handle certain kinds of requests

        any streams of the format "{sei}//{uri}" can be handled by this plugin
        """
        return ["youtube", "ydl", "youtube.channel.live",
                "pytube", "invidious"]

    def validate_uri(self, uri):
        """ return True if uri can be handled by this extractor, False otherwise"""
        return any([uri.startswith(sei) for sei in self.supported_seis]) or \
               self.is_youtube(uri)

    def extract_stream(self, uri, video=True):
        """ return the real uri that can be played by OCP """
        if uri.startswith("youtube//"):
            uri = uri.replace("youtube//", "")

        if uri.startswith("youtube.channel.live//"):
            return self.live.extract_stream(uri, video)

        if self.settings.get("youtube_backend") == YoutubeBackend.WEBVIEW or \
                self.settings.get("youtube_backend") == YoutubeBackend.INVIDIOUS or \
                uri.startswith("invidious//"):
            return self.invidious.extract_stream(uri, video)
        elif self.settings.get("youtube_backend") == YoutubeBackend.PYTUBE or \
                uri.startswith("pytube//"):
            return self.pytube.extract_stream(uri, video)
        else:
            # youtube-dl by default
            return self.ydl.extract_stream(uri, video)

    # helpers
    @staticmethod
    def parse_title(title):
        # this is a very hacky imple,mentation that kinda works
        # TODO - lang support should be added and this refactored

        # try to extract_streams artist from title
        delims = [":", "|", "-"]
        removes = ["(Official Video)", "(Official Music Video)",
                   "(Lyrics)", "(Official)", "(Album Stream)",
                   "(Legendado)"]
        removes += [s.replace("(", "").replace(")", "") for s in removes] + \
                   [s.replace("[", "").replace("]", "") for s in removes]
        removes += [s.upper() for s in removes] + [s.lower() for s in removes]
        removes += ["(HQ)", "()", "[]", "- HQ -"]
        for d in delims:
            if d in title:
                for k in removes:
                    title = title.replace(k, "")
                artist = title.split(d)[0]
                title = "".join(title.split(d)[1:])
                title = title.strip() or "..."
                artist = artist.strip() or "..."
                return title, artist
        return title.replace(" - Topic", ""), ""

    @staticmethod
    def is_youtube(url):
        # TODO localization
        if not url:
            return False
        return "youtube.com/" in url or "youtu.be/" in url


class OCPYDLExtractor(OCPYoutubeExtractor):

    @property
    def supported_seis(self):
        """
        skills may return results requesting a specific extractor to be used

        plugins should report a StreamExtractorIds (sei) that identifies it can handle certain kinds of requests

        any streams of the format "{sei}//{uri}" can be handled by this plugin
        """
        return ["ydl"]

    def extract_stream(self, uri, video=True):
        """ return the real uri that can be played by OCP """
        if uri.startswith("ydl//"):
            uri = uri.replace("ydl//", "")
        meta = self.get_ydl_stream(uri, audio_only=not video)
        if not meta:
            LOG.error("ydl stream extraction failed!!!")
        return meta

    def get_ydl_stream(self, url, audio_only=False, ydl_opts=None, best=True):
        ydl_opts = ydl_opts or {
            "quiet": True,
            "hls_prefer_native": True,
            "verbose": False,
            "format": "best"
        }
        backend = self.settings.get("ydl_backend") or YdlBackend.AUTO
        if backend == YdlBackend.AUTO:
            try:
                import yt_dlp as youtube_dl
            except:
                import youtube_dl
        elif backend == YdlBackend.YDLP:
            import yt_dlp as youtube_dl
        elif backend == YdlBackend.YDLC:
            import youtube_dlc as youtube_dl
        elif backend == YdlBackend.YDL:
            import youtube_dl
        else:
            raise ValueError("invalid youtube-dl backend")

        kmaps = {"duration": "duration",
                 "thumbnail": "image",
                 "uploader": "artist",
                 "title": "title",
                 'webpage_url': "url"}
        info = {}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            meta = ydl.extract_info(url, download=False)
            for k, v in kmaps.items():
                if k in meta:
                    info[v] = meta[k]

            if "entries" in meta:
                meta = meta["entries"][0]

            info["uri"] = self._select_ydl_format(meta, audio_only=audio_only,
                                                  best=best)
            title, artist = self.parse_title(info["title"])
            info["title"] = title
            info["artist"] = artist or info.get("artist")
            info["is_live"] = meta.get("is_live", False)
        return info

    # helpers
    @staticmethod
    def _select_ydl_format(meta, audio_only=False, preferred_ext=None, best=True):
        if not meta.get("formats"):
            # not all extractors return same format dict
            if meta.get("url"):
                return meta["url"]
            raise ValueError

        fmts = meta["formats"]
        if audio_only:
            # skip any stream that contains video
            fmts = [f for f in fmts if f.get('vcodec', "") == "none"]
        else:
            # skip video only streams (no audio / progressive streams only)
            fmts = [f for f in fmts if f.get('acodec', "") != "none"]

        if preferred_ext:
            fmts = [f for f in meta["formats"]
                    if f.get('ext', "") == preferred_ext] or fmts

        # last is best (higher res)
        if best:
            return fmts[-1]["url"]
        return fmts[0]["url"]


class OCPYoutubeChannelLiveExtractor(OCPYoutubeExtractor):

    @property
    def supported_seis(self):
        """
        skills may return results requesting a specific extractor to be used

        plugins should report a StreamExtractorIds (sei) that identifies it can handle certain kinds of requests

        any streams of the format "{sei}//{uri}" can be handled by this plugin
        """
        return ["youtube.channel.live"]

    def extract_stream(self, uri, video=True):
        """ return the real uri that can be played by OCP """
        uri = uri.replace("youtube.channel.live//", "")
        if self.settings.get("youtube_live_backend") == YoutubeLiveBackend.PYTUBE:
            return self.get_pytube_channel_livestreams(uri)
        else:
            return self.get_youtube_live_from_redirect(uri)

    @staticmethod
    def get_pytube_channel_livestreams(url):
        yt = Channel(url)
        for v in yt.videos_generator():
            if v.vid_info.get('playabilityStatus', {}).get('liveStreamability'):
                title, artist = OCPYoutubeExtractor.parse_title(v.title)
                yield {
                    "url": v.watch_url,
                    "title": title,
                    "artist": artist,
                    "is_live": True,
                    "image": v.thumbnail_url,
                    "length": v.length * 1000
                }

    @staticmethod
    def get_youtube_live_from_redirect(url):
        # TODO improve channel name handling
        url = url.split("?")[0]
        if "/c/" in url or "/channel/" in url or "/user/" in url:
            channel_name = url.split("/channel/")[-1].split("/c/")[-1].split("/user/")[-1].split("/")[0]
        else:
            channel_name = url.split("/")[-1]

        # we see different patterns randomly used in the wild
        # i do not know a easy way to check which are valid for a channel
        # lazily try: except: and hail mary
        try:
            # seems to work for all channels
            url = f"https://www.youtube.com/{channel_name}/live"
            return super().extract_stream(url)
        except:
            # works for some channels only
            url = f"https://www.youtube.com/c/{channel_name}/live"
            return super().extract_stream(url)


class OCPInvidiousExtractor(OCPYoutubeExtractor):

    @property
    def supported_seis(self):
        """
        skills may return results requesting a specific extractor to be used

        plugins should report a StreamExtractorIds (sei) that identifies it can handle certain kinds of requests

        any streams of the format "{sei}//{uri}" can be handled by this plugin
        """
        return ["invidious"]

    def extract_stream(self, url, video=True):
        """ return the real uri that can be played by OCP """

        if url.startswith("invidious//"):
            url = url.replace("invidious//", "")

        local = "true" if self.settings.get("proxy_invidious", True) else "false"

        vid_id = url.split("watch?v=")[-1].split("&")[0]

        data = {}

        for host in self.get_invidious_hosts():
            LOG.debug(f"Trying invidious host: {host}")
            api = f"{host}/api/v1/videos/{vid_id}"
            try:
                r = requests.get(api, timeout=3)
                # TODO seems like apparently valid json fails to parse sometimes?
                data = json.loads(r.text)
            except Exception as e:
                LOG.error(f"request failed for: {api}  - ({e})")
            if data and "error" not in data:
                if data.get("liveNow"):
                    # TODO invidious backend can not handle lives, what do?
                    stream = f"https://www.youtube.com/watch?v={vid_id}"
                    return {
                        "uri": stream,
                        "title": data.get("title"),
                        "image": host + data['videoThumbnails'][0]["url"],
                        "playback": 5  # PlaybackType.WEBVIEW
                    }
                elif self.settings.get("youtube_backend") == YoutubeBackend.WEBVIEW:
                    stream = f"{host}/watch?v={vid_id}"
                else:
                    stream = f"{host}/latest_version?id={vid_id}&itag=22&local={local}&subtitles=en"

                if not video:
                    pass  # TODO

                return {
                    "uri": stream,
                    "title": data.get("title"),
                    "image": host + data['videoThumbnails'][0]["url"],
                    "length": data['lengthSeconds']
                }

        return {}

    def get_invidious_hosts(self):
        # proxy via invidious instance
        # public instances: https://docs.invidious.io/Invidious-Instances.md
        # self host: https://github.com/iv-org/invidious
        host = self.settings.get("invidious_host")
        if not host:
            # hosted by a OpenVoiceOS member
            hosts = ["https://video.strongthany.cc"]
            try:
                api_url = "https://api.invidious.io/instances.json?pretty=1&sort_by=type,health"
                hosts += ["http://" + h[0] for h in requests.get(api_url).json()]
            except:
                pass
        else:
            hosts = [host]
        return hosts


class OCPPytubeExtractor(OCPYoutubeExtractor):

    @property
    def supported_seis(self):
        """
        skills may return results requesting a specific extractor to be used

        plugins should report a StreamExtractorIds (sei) that identifies it can handle certain kinds of requests

        any streams of the format "{sei}//{uri}" can be handled by this plugin
        """
        return ["pytube"]

    def extract_stream(self, uri, video=True):
        """ return the real uri that can be played by OCP """
        if uri.startswith("pytube//"):
            uri = uri.replace("pytube//", "")
        return self.get_pytube_stream(uri, audio_only=not video)

    @staticmethod
    def get_pytube_stream(url, audio_only=False, best=True):
        yt = YouTube(url)
        s = None
        if audio_only:
            s = yt.streams.filter(only_audio=True).order_by('abr')
        if not s:
            s = yt.streams.filter(progressive=True).order_by('resolution')

        if best:  # best quality
            s = s.last()
        else:  # fastest
            s = s.first()

        info = {
            "uri": s.url,
            "url": yt.watch_url,
            "title": yt.title,
            "author": yt.author,
            "image": yt.thumbnail_url,
            "length": yt.length * 1000
        }
        title, artist = OCPYoutubeExtractor.parse_title(info["title"])
        info["title"] = title
        info["artist"] = artist or info.get("author")
        return info


OCPYoutubeExtractor.init_extractors()
