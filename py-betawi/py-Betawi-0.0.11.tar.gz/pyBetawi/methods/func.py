import asyncio

from .changer import Changers

try:
    from youtubesearchpython import VideosSearch
except ImportError:
    print("'youtube-search-python' tidak terinstall\nmungkin beberapa modul tidak akan berjalan")
    VideosSearch = None


izzy = Changers()


class Funci(object):
    def yt_info_query(self, query: str):
        results = VideosSearch(query, limit=1)
        for result in results.result()["result"]:
            title = result["title"]
            duration_min = result["duration"]
            thumbnail = result["thumbnails"][0]["url"].split("?")[0]
            videoid = result["id"]
            if str(duration_min) == "None":
                duration_sec = 0
            else:
                duration_sec = int(izzy.time_to_seconds(duration_min))
        return title, duration_min, duration_sec, thumbnail, videoid
    
    def yt_info_id(self, videoid):
        url = f"https://www.youtube.com/watch?v={videoid}"
        results = VideosSearch(url, limit=1)
        for result in results.result()["result"]:
            title = result["title"]
            duration_min = result["duration"]
            thumbnail = result["thumbnails"][0]["url"].split("?")[0]
            if str(duration_min) == "None":
                duration_sec = 0
            else:
                duration_sec = int(izzy.time_to_seconds(duration_min))
        return title, duration_min, duration_sec, thumbnail
    
    def yt_info_query_slider(self, query: str, query_type: int):
        a = VideosSearch(query, limit=10)
        result = (a.result()).get("result")
        title = result[query_type]["title"]
        duration_min = result[query_type]["duration"]
        videoid = result[query_type]["id"]
        thumbnail = result[query_type]["thumbnails"][0]["url"].split("?")[0]
        if str(duration_min) == "None":
            duration_sec = 0
        else:
            duration_sec = int(izzy.time_to_seconds(duration_min))
        return title, duration_min, duration_sec, thumbnail, videoid


    async def get_m3u8(self, videoid):
        link = f"https://www.youtube.com/watch?v={videoid}"
        proc = await asyncio.create_subprocess_exec(
            "yt-dlp",
            "-g",
            "-f",
            "best[height<=?720][width<=?1280]",
            f"{link}",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await proc.communicate()
        if stdout:
            return 1, stdout.decode().split("\n")[0]
        else:
            return 0, stderr.decode()