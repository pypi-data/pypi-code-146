import numpy as np
from know.base import SlabsIter
from taped import LiveWf, chunk_indices
from know.audio_to_store import get_resource


if __name__ == '__main__':
    # print(f"starting")
    # live_source = LiveWf

    # live_source = get_resource(live_source, dflt_callback=LiveWf)
    # chk_size = 100_000
    # end_idx = 800_000
    # logger = print
    # # session_id: SessionId = int(time() * 1000)
    # with live_source:
    #     # range(start, stop, step)
    #     for i, (bt, tt) in enumerate(chunk_indices(chk_size=chk_size, end_idx=end_idx)):
    #         if logger:
    #             logger(f"{i=}: {bt=}, {tt=}")
    #             print(np.mean(live_source[bt:tt]))

    from know.audio_to_store import *

    wfs = demo_live_data_acquisition(
        live_source=LiveWf(
            input_device_index=None,  # if None, will try to guess the device index
            sr=44100,
            sample_width=2,
            chk_size=4096,
            stream_buffer_size_s=60,
        ),
        store=mk_session_block_wf_store(
            rootdir=None,  # will choose one for you
            # template examples: '{session}_{block}.wav' '{session}/d/{block}.pcm', '{session}/{block}', 'demo/s_{session}/blocks/{block}.wav'
            template='{session}/d/{block}.pcm',  #
            pattern=r'\d+',
            value_trans=int,
        ),
        chk_size=100_000,
        end_idx=300_000,
        logger=print,
    )
    print(f'{len(wfs)=}')
