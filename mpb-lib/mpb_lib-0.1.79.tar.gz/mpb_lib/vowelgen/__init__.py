#coding:utf-8
# vowelgen
#
# 母音(アイウエ)を生成するプログラム。
#
# Copyright (c) 2021 Atsush Shibata(shivata@m-info.co.jp)
#
# Released under the MIT license.

import numpy as np
from scipy.io.wavfile import write as wavwrite
import IPython

from mpb_lib.vowelgen.twotube import Class_TwoTube
from mpb_lib.vowelgen.glottal import Class_Glottal
from mpb_lib.vowelgen.HPF import Class_HPF

glo=Class_Glottal()   # instance as glottal voice source
hpf=Class_HPF()       # instance for mouth radiation effect

def generate_vowel(L1_a, A1_a, L2_a, A2_a, length=50):
    twotube  =  Class_TwoTube(L1_a,L2_a,A1_a,A2_a)
    yg_repeat=glo.make_N_repeat(repeat_num=length) # input source of two tube model
    y2tm=twotube.process(yg_repeat)
    yout=hpf.iir1(y2tm)

    sampling_rate=48000
    wavwrite("vowel.wav", sampling_rate, (yout*2**15).astype(np.int16))
    return IPython.display.Audio("vowel.wav")