# valid settings under OCP section in mycroft.conf
OCPYoutubeExtractorConfig = {
    "youtube": {
        # alternative libs supported instead of youtube-dl
        "youtube_backend": "youtube-dl",
        # how to handle live streams from channel url
        # url = f"https://www.youtube.com/c/{channel_name}/live"
        "youtube_live_backend": "redirect",
        # several forks supported
        # NOTE: handles more than youtube streams
        "ydl_backend": "yt-dlp"
    }
}
