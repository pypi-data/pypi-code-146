import vlc
from smb3_eh_manip.util import settings


class VideoPlayer:
    def __init__(self, player_video_path, offset_frames):
        self.player_video_path = player_video_path
        self.player_seek_to_time = int(
            offset_frames * settings.NES_MS_PER_FRAME
        ) + settings.get_int("latency_ms")
        self.media_player = vlc.MediaPlayer()
        self.media_player.video_set_scale(
            float(settings.get("video_player_scale", fallback=1))
        )
        self.reset()

    def play(self):
        self.media_player.set_pause(False)

    def reset(self):
        self.media_player.set_media(vlc.Media(self.player_video_path))
        self.media_player.play()
        self.media_player.set_pause(True)
        self.media_player.set_time(self.player_seek_to_time)

    def terminate(self):
        self.media_player.stop()
