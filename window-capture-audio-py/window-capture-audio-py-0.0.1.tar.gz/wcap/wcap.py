import wcap_core
from enum import Enum
import numpy as np

__all__ = ["WCAP", "WAVE_FORMAT", "init_audio", "get_audio_pcm", "get_audio_ieee_float"]

def init_audio(hwnd:int, wave_format:str):
    ret = wcap_core.init_audio(hwnd, wave_format)
    if ret == -1:
        raise Exception(f"hwnd is initialized: {hwnd}")

def get_audio_pcm(hwnd:int)->np.ndarray[np.int16]:
    """
    if returned array is empty, shows it fails or no audio data.
    """
    return wcap_core.get_audio_pcm(hwnd)

def get_audio_ieee_float(hwnd:int)->np.ndarray[np.float32]:
    """
    if returned array is empty, shows it fails or no audio data.
    """
    return wcap_core.get_audio_ieee_float(hwnd)

def delete_audio(hwnd:int):
    ret = wcap_core.delete_audio(hwnd)
    if ret == -1:
        raise Exception(f"hwnd is not existed: {hwnd}")

class WAVE_FORMAT:
    WAVE_FORMAT_PCM="WAVE_FORMAT_PCM"
    WAVE_FORMAT_IEEE_FLOAT="WAVE_FORMAT_IEEE_FLOAT"
    

class WCAP:
    def __init__(self, hwnd, wave_format:str):
        self.hwnd = hwnd
        self.wave_format = wave_format
        print("before get_audio_pcm")
        init_audio(hwnd, wave_format)
        print("after get_audio_pcm")
        if self.wave_format==WAVE_FORMAT.WAVE_FORMAT_PCM:
            self.func_get_audio = get_audio_pcm
        elif self.wave_format==WAVE_FORMAT.WAVE_FORMAT_IEEE_FLOAT:
            self.func_get_audio = get_audio_ieee_float
        else:
            raise Exception("Unknown wave format: "+wave_format)
        
    def get_audio(self)->np.ndarray:
        return self.func_get_audio(self.hwnd)
        
        
            
