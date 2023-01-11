import numpy as np


def merge_signal_chunks(signal_chunks):
    """Merges all signal chunks for a given signal row.

    Args:
        signal_chunks: chunks of a signal, the signal is split in chunks due to MQTT maximum size per package

    Return:
        merged element.
    """

    signal_chunks = sorted(signal_chunks, key=lambda d: d['part_index'])
    data = []
    for i in range(len(signal_chunks[0]["data"])):
        data.append([])
    for i in range(0, len(signal_chunks)):
        for j, dimension_signal_sample in enumerate(signal_chunks[i]["data"]):
            data[j] = np.concatenate((data[j], dimension_signal_sample["values"]), axis=0)
            data[j] = list(data[j])
    signal_chunks[0]["data"] = [{"values": dimension, "index": i} for i, dimension in enumerate(data)]
    signal_chunks[0]["previous_part_index"] = 0
    return signal_chunks[0]


def get_fft_as_np_array(bigquery_fft):
    fft_per_dimensions = []
    for dimension in bigquery_fft:
        fft_dimension = []
        for z in dimension["values"]:
            fft_dimension.append(np.complex128(complex(float(z["real"]), float(z["imag"]))))
        fft_per_dimensions.append(np.array(fft_dimension))

    return np.array(fft_per_dimensions)

