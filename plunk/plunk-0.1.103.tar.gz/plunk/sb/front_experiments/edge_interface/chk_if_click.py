from hear import WavSerializationTrans, WavLocalFileStore
from forged.clickify import clickify, pad_to_length

# data prep
my_wav_store = WavLocalFileStore('./data/ClickDetection')
click_template = my_wav_store['base_click.wav']
wf_base = my_wav_store['wf_base.wav']
long_click = pad_to_length(click_template, len(wf_base))

# place clicks at arbitrary timestamps
timestamps = [2000, 10000, 20000, 40000, 60000]
wf_with_clicks = clickify(wf_base, timestamps, long_click, click_marker=None)


if __name__ == '__main__':

    print(len(wf_with_clicks))
