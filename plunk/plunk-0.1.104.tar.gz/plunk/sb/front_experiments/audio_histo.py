import threading
import av
import cv2
import streamlit as st
from matplotlib import pyplot as plt

from streamlit_webrtc import webrtc_streamer
from streamlit_webrtc import (
    AudioProcessorBase,
    ClientSettings,
    WebRtcMode,
    webrtc_streamer,
)
from streamlit_webrtc import (
    RTCConfiguration,
    WebRtcMode,
    WebRtcStreamerContext,
    webrtc_streamer,
)


RTC_CONFIGURATION = RTCConfiguration(
    {'iceServers': [{'urls': ['stun:stun.l.google.com:19302']}]}
)


def process_audio(frame: av.AudioFrame) -> av.AudioFrame:
    raw_samples = frame.to_ndarray()
    # sound = pydub.AudioSegment(
    #     data=raw_samples.tobytes(),
    #     sample_width=frame.format.bytes,
    #     frame_rate=frame.sample_rate,
    #     channels=len(frame.layout.channels),
    # )
    st.write(raw_samples)
    # sound = sound.apply_gain(gain)

    # Ref: https://github.com/jiaaro/pydub/blob/master/API.markdown#audiosegmentget_array_of_samples  # noqa
    # channel_sounds = sound.split_to_mono()
    # channel_samples = [s.get_array_of_samples() for s in channel_sounds]
    # new_samples: np.ndarray = np.array(channel_samples).T
    # new_samples = new_samples.reshape(raw_samples.shape)

    # new_frame = av.AudioFrame.from_ndarray(new_samples, layout=frame.layout.name)
    # new_frame.sample_rate = frame.sample_rate
    return raw_samples


webrtc_streamer(
    key='audio-filter',
    mode=WebRtcMode.SENDRECV,
    rtc_configuration=RTC_CONFIGURATION,
    audio_frame_callback=process_audio,
    async_processing=True,
)
