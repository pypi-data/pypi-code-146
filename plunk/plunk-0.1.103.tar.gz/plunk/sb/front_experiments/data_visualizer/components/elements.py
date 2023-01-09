from dataclasses import dataclass
from streamlitfront.elements import TextInput, FileUploader
from front.elements import InputBase
from hear import WavLocalFileStore
import pandas as pd
import soundfile as sf

from dol import FilesOfZip, wrap_kvs, filt_iter
from io import BytesIO


def my_obj_of_data(b):
    return sf.read(BytesIO(b), dtype='float32')[0]


# @wrap_kvs(obj_of_data=lambda b: sf.read(BytesIO(b), dtype="int16")[0])
@wrap_kvs(obj_of_data=my_obj_of_data)
@filt_iter(filt=lambda x: not x.startswith('__MACOSX') and x.endswith('.wav'))
class WfStore(FilesOfZip):
    """Waveform access. Keys are .wav filenames and values are numpy arrays of int16 waveform."""

    pass


@dataclass
class ZipWavDataLoader(FileUploader):
    # root_dir: str = None

    def __post_init__(self):
        # super().__post_init__()
        self.store = WfStore(self.output)

        # self.annots = pd.read_csv(self.annot_path)

    def render(self):
        print('done!')
        return len(self.store)


@dataclass
class DataLoader2(TextInput):
    # root_dir: str = None
    paths: str = None

    # def __post_init__(self):
    #     # super().__post_init__()
    #     # self.store = WavLocalFileStore(self.root_dir)

    #     # self.annots = pd.read_csv(self.annot_path)
    #     pass

    def render(self):
        print('done!')
        return len(self.output)
