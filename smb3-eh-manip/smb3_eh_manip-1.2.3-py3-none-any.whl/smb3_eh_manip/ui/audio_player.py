import logging
import time
from multiprocessing import Process, Value

from smb3_eh_manip.util import events, settings
from smb3_eh_manip.util.settings import ACTION_FRAMES, FREQUENCY

DEFAULT_AUDIO_CUE_PATH = "data/audio_cue.wav"
AUDIO_CUE_PATH = settings.get("audio_cue_path", fallback=DEFAULT_AUDIO_CUE_PATH)


def play_audio_cue(play):
    from pygame import mixer

    mixer.init()
    mixer.music.load(AUDIO_CUE_PATH)
    while True:
        play_sound = False
        with play.get_lock():
            if play.value == 1:
                play.value = 0
                play_sound = True
        if play_sound:
            mixer.music.play()
        else:
            time.sleep(0.001)


class AudioPlayer:
    def __init__(self):
        self.trigger_frames = []
        self.play = Value("i", 0)
        self.play_process = Process(target=play_audio_cue, args=(self.play,))
        self.play_process.daemon = True
        self.play_process.start()
        events.listen(events.AddActionFrame, self.handle_add_action_frame)
        events.listen(events.LagFramesObserved, self.handle_lag_frames_observed)

    def reset(self):
        self.play.value = 0
        self.trigger_frames = []
        for action_frame in ACTION_FRAMES:
            self.add_action_frame(action_frame)
        logging.info(f"Audio trigger frames set to {self.trigger_frames}")

    def add_action_frame(self, action_frame):
        for increment in range(4, -1, -1):
            self.trigger_frames.append(action_frame - increment * FREQUENCY)

    def tick(self, current_frame):
        if self.trigger_frames and self.trigger_frames[0] <= current_frame:
            self.trigger_frames.pop(0)
            with self.play.get_lock():
                self.play.value = 1

    def handle_add_action_frame(self, event: events.AddActionFrame):
        self.add_action_frame(event.action_frame)
        self.trigger_frames.sort()

    def handle_lag_frames_observed(self, event: events.LagFramesObserved):
        self.trigger_frames = [
            frame + event.observed_lag_frames for frame in self.trigger_frames
        ]
