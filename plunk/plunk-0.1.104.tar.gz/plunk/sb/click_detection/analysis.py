import pandas as pd
import numpy as np
from adtk.detector import PersistAD, InterQuartileRangeAD
from adtk.transformer import DoubleRollingAggregate as DRA
from adtk.detector import OutlierDetector
from adtk.visualization import plot
from adtk.detector import LevelShiftAD
from adtk.detector import VolatilityShiftAD

DFLT_DETECTOR = VolatilityShiftAD(c=20.0, side='positive', window=20)


def arr_to_df(arr):
    df = pd.DataFrame(arr)
    n_index = pd.to_datetime(df.index)
    df.index = n_index

    return df


def event_detector(arr, model=DFLT_DETECTOR):
    df = arr_to_df(arr)
    anomalies = model.fit_detect(df)

    return anomalies


def mark_events(arr, ts):
    vlines = np.zeros_like(arr)
    for event in ts:
        vlines[event] = 1.0
    return vlines


def detection_plot(arr, model=DFLT_DETECTOR):
    df = arr_to_df(arr)
    anomalies = event_detector(arr, model)

    plot(df, anomaly=anomalies, anomaly_color='red', figsize=(15, 6))
