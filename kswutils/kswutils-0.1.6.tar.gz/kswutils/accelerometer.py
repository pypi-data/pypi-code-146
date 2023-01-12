import os

import numpy as np

from .fileio import FileIO
from .calculator import isfloat


class Accelerometer:
    def __init__(self, filepath) -> None:
        self.filepath = filepath

    def get_A(self):
        acc = []
        with open(self.filepath, 'r') as f:
            for i, line in enumerate(f):
                if isfloat(line.strip('\n').split('\t')[0]):
                    acc.append(float(line.strip('\n').split('\t')[1]))
        return np.array(acc)

    def get_sample_rate(self):
        c = 0
        ts = []
        with open(self.filepath, 'r') as f:
            for i, line in enumerate(f):
                if isfloat(line.strip('\n').split('\t')[0]):
                    ts.append(float(line.strip('\n').split('\t')[0]))
                    c += 1
                if c == 2:
                    sr = 1 / (ts[1] - ts[0])
                    break
        return sr


def combine_data(folder):
    files = FileIO.get_subdirectories(folder)

    acc_ls = []

    print('Concatenate files...')
    for f in files:
        if f.endswith('.lvm'):
            print(os.path.basename(f))

            accelerometer = Accelerometer(f)
            acc_ls.append(accelerometer.get_A())

    return np.concatenate(acc_ls)


def save_pkl(inpdir, outdir, name):
    print('Input:', inpdir)
    data = combine_data(inpdir)

    savepath = os.path.join(outdir, name + '.pickle')
    FileIO.write_pickle(data, savepath=savepath)
    print('Saved to:', outdir)
    return None
