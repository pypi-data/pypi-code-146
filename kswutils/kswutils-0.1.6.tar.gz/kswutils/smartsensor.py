import os
from datetime import datetime

import numpy as np
import pandas as pd

from .fileio import FileIO


# SHEET NAME
ACCELERATION_SHEET = 'Accelerometer'
MAGNETICFIELD_SHEET = 'Magnetometer'
# LOWPOWER_ACCELERATION_SHEET = 'Low power accelerometer'
MICROPHONE_SHEET = 'Microphone'

# DATA COLUMN NAME
# acceleration
AX_COL = 'Ax [g]'
AY_COL = 'Ay [g]'
AZ_COL = 'Az [g]'
# magnetic filed
BX_COL = 'Bx [μTesla]'
BY_COL = 'By [μTesla]'
BZ_COL = 'Bz [μTesla]'
# time
TIME_COL = 'Time [sec]'
# microphone sound
SOUND_COL = 'Sound [SPL]'


class SmartSensor:
    def __init__(self, filepath) -> None:
        self.xls = pd.ExcelFile(filepath)

    def get_acceleration(self):
        return pd.read_excel(self.xls, ACCELERATION_SHEET)

    def get_magneticfield(self):
        return pd.read_excel(self.xls, MAGNETICFIELD_SHEET)

    def get_microphone(self):
        return pd.read_excel(self.xls, MICROPHONE_SHEET)

    # def get_acceleration_lowpwer(self):
    #     return pd.read_excel(self.xls, LOWPOWER_ACCELERATION_SHEET)

    # Get acceleration components
    def get_Ax(self):
        return self.get_acceleration()[AX_COL].to_numpy()

    def get_Ay(self):
        return self.get_acceleration()[AY_COL].to_numpy()

    def get_Az(self):
        return self.get_acceleration()[AZ_COL].to_numpy()

    # Get magnetic file components
    def get_Bx(self):
        return self.get_magneticfield()[BX_COL].to_numpy()

    def get_By(self):
        return self.get_magneticfield()[BY_COL].to_numpy()

    def get_Bz(self):
        return self.get_magneticfield()[BZ_COL].to_numpy()

    # Get sound
    def get_Sound(self):
        return self.get_microphone()[SOUND_COL].to_numpy()

    # # Get low power acceleration Az
    # def get_Az_lp(self):
    #     return self.get_acceleration_lowpwer()[AZ_COL].to_numpy()

    # Get sampling rate
    # accelerometor  # 3611.1111
    def get_sample_rate_accelerometor(self):
        a = self.get_acceleration()
        diff = a[TIME_COL][1] - a[TIME_COL][0]
        return 1 / diff

    # magnetometer  # 334.3673
    def get_sample_rate_magnetometer(self):
        b = self.get_magneticfield()
        diff = b[TIME_COL][1] - b[TIME_COL][0]
        return 1 / diff

    # Get total sampling duration
    # Should be same for the accelerometer and magnetometer
    # accelerometor
    def get_sample_duration_accelerometor(self):
        a = self.get_acceleration()
        timestamp = a['Timestamp'].copy().dropna()

        ts1 = timestamp.iloc[0].split('.')[0].strip()
        ts2 = timestamp.iloc[-1].split('.')[0].strip()

        dt1 = datetime.strptime(ts1, '%y-%m-%d %H:%M:%S')
        dt2 = datetime.strptime(ts2, '%y-%m-%d %H:%M:%S')
        return (dt2-dt1).total_seconds()

    # magnetometer
    def get_sample_duration_magnetometer(self):
        b = self.get_magneticfield()
        timestamp = b['Timestamp'].copy().dropna()

        ts1 = timestamp.iloc[0].split('.')[0].strip()
        ts2 = timestamp.iloc[-1].split('.')[0].strip()

        dt1 = datetime.strptime(ts1, '%y-%m-%d %H:%M:%S')
        dt2 = datetime.strptime(ts2, '%y-%m-%d %H:%M:%S')
        return (dt2-dt1).total_seconds()


def combine_data(folder, tag='Az'):
    files = FileIO.get_subdirectories(folder)

    data_ls = []

    print('Concatenate files...')
    for f in files:
        print(os.path.basename(f))
        try:
            smartsensor = SmartSensor(f)
        except:
            continue

        if tag == 'Az':
            data = smartsensor.get_Az()
            data_ls.append(data)

        elif tag == 'Ax':
            data = smartsensor.get_Ax()
            data_ls.append(data)

        elif tag == 'Ay':
            data = smartsensor.get_Ay()
            data_ls.append(data)

        elif tag == 'Bz':
            data = smartsensor.get_Bz()
            data_ls.append(data)

        elif tag == 'Bx':
            data = smartsensor.get_Bx()
            data_ls.append(data)

        elif tag == 'By':
            data = smartsensor.get_By()
            data_ls.append(data)

        elif tag == 'Sound':
            data = smartsensor.get_Sound()
            data_ls.append(data)

    return np.concatenate(data_ls)


def save_pkl(inpdir, outdir, name, tag):
    """
    tag (string): 'Az', 'Bz', 'Sound'
    """

    print('Input:', inpdir)
    data = combine_data(inpdir, tag=tag)

    savepath = os.path.join(outdir, name + '.pickle')
    FileIO.write_pickle(data, savepath=savepath)
    print('Saved to:', outdir)
    return None
