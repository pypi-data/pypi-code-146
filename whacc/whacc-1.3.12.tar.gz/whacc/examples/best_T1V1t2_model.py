# from google.colab import drive
# # drive.mount('/content/gdrive')
# drive._mount('/content/gdrive')
import shap

import pdb
import lightgbm as lgb
from datetime import datetime, timedelta

from whacc import model_maker

from whacc.model_maker import *


import h5py

from tqdm.autonotebook import tqdm


import pickle
from whacc import utils, image_tools, transfer_learning, analysis
import matplotlib.pyplot as plt

from sklearn.utils import class_weight
import os
import copy
import numpy as np

from pathlib import Path
import shutil
import zipfile
import pytz
import json
from math import isclose, sqrt
from IPython import display


import pandas as pd
import time


import seaborn as sns
from matplotlib.collections import PathCollection
import itertools

from natsort import os_sorted
import joblib
import seaborn as sns

import multiprocessing
# from natsort import os_sorted
from natsort import natsorted, ns
## get feature names



def foo_plot2():
    from matplotlib import cm

    early_stopping_num = 500
    x = np.diff(1-d['auc'])
    peaks = np.where(x>0.001)[0]+1
    loop_peaks = np.diff([0]+list(peaks)+[len(d['auc'])])
    fig, ax1 = plt.subplots(figsize=[20, 5])
    ax2 = ax1.twinx()
    tot = len(loop_peaks)

    inds = np.linspace(.15, .95, len(loop_peaks))
    Blues = cm.get_cmap('Blues')([inds])
    Reds = cm.get_cmap('Reds')([inds])

    for i, (k1, k2) in enumerate(utils.loop_segments(loop_peaks)):
        c1 = i+1/tot

        d2 = {'auc':d['auc'][k1:k2], 'touch_count_errors_per_touch':d['touch_count_errors_per_touch'][k1:k2]}
        color = Blues[0][i]
        ax1.set_ylabel('1-auc', color=color)  # we already handled the x-label with ax1
        ax1.plot(1-d2['auc'], color=color)
        ax1.tick_params(axis='y', labelcolor=color)


        color = Reds[0][i]
        ax2.set_xlabel('touch_count_errors_per_touch')
        ax2.set_ylabel('touch_count_errors_per_touch', color=color)
        ax2.plot(d2['touch_count_errors_per_touch'], color=color)
        ax2.tick_params(axis='y', labelcolor=color)

        L = len(d2['auc'])

        b = np.argmin(np.flip(1-d2['auc'][-early_stopping_num:]))
        b = np.flip(np.arange(early_stopping_num))[b]
        a = b+L-early_stopping_num
        ax1.plot(a, 1-d2['auc'][a], 'g.')

        b = np.argmin(np.flip(d2['touch_count_errors_per_touch'][-early_stopping_num:]))
        b = np.flip(np.arange(early_stopping_num))[b]
        a = b+L-early_stopping_num
        ax2.plot(a, d2['touch_count_errors_per_touch'][a], 'g.')
    ax1.set_ylim([0.00055, .0008])
    ax2.set_ylim([.05, .065])


    ax1.set_ylim([0.00, .00075])
    ax2.set_ylim([.05, .095])

#     ax1.set_ylim([0.00, 1-.98])
#     ax2.set_ylim([.05, .3])
    plt.grid()
    return ax1, ax2

def foo_plot():
    early_stopping_num = 500

    fig, ax1 = plt.subplots(figsize=[20, 5])
    color = 'tab:blue'
    ax1.set_ylabel('1-auc', color=color)  # we already handled the x-label with ax1
    ax1.plot(1-d['auc'], color=color)
    ax1.tick_params(axis='y', labelcolor=color)
    plt.ylim([0.00055, .0008])
    # plt.ylim([0.00055, .0006])
    # plt.ylim([0.000, .002])
    # plt.ylim([0.000, .008])
    ax2 = ax1.twinx()
    color = 'tab:red'
    ax2.set_xlabel('touch_count_errors_per_touch')
    ax2.set_ylabel('touch_count_errors_per_touch', color=color)
    ax2.plot(d['touch_count_errors_per_touch'], color=color)
    ax2.tick_params(axis='y', labelcolor=color)
    # plt.ylim([.028, .034])
    # plt.ylim([.028, .044])
    plt.ylim([.05, .065])
    # plt.ylim([.04, .14])
    # plt.ylim([.056, .0571])
    L = len(d['auc'])

    b = np.argmin(np.flip(1-d['auc'][-early_stopping_num:]))
    b = np.flip(np.arange(early_stopping_num))[b]
    a = b+L-early_stopping_num
    ax1.plot(a, 1-d['auc'][a], 'g.')

    b = np.argmin(np.flip(d['touch_count_errors_per_touch'][-early_stopping_num:]))
    b = np.flip(np.arange(early_stopping_num))[b]
    a = b+L-early_stopping_num
    ax2.plot(a, d['touch_count_errors_per_touch'][a], 'g.')

    plt.grid()
    # plt.xlim([L-early_stopping_num+1, L+5])
    # plt.xlim([L-401, L+5])
    # plt.xlim([L-1001, L+5])

    # plt.xlim([3500, 4300])


    plt.plot()

    ax2.axhline(np.min(d['touch_count_errors_per_touch']), color='k')
    print(np.min(d['touch_count_errors_per_touch']))
    plt.figure()
    plt.plot(d['best_threshold'])
    plt.ylim([.1, 1])
    plt.grid()
    """
    one thing to test is if optuna is saving the best AUC or if it is following the early stopping from the light GBM 
    """

#
# bd = r'Q:\WhACC_DATA_FINAL_WITH_AUG\LGBM_models_for_cnn_comparison_V1\\'
# bd = r'Q:\WhACC_DATA_FINAL_WITH_AUG\LGBM_models_for_cnn_comparison_early_stop_500_V2\\'
# bd = r'Q:\WhACC_DATA_FINAL_WITH_AUG\LGBM_models_for_cnn_comparison_T1V1t2_V3\\'

bd = '/Volumes/GoogleDrive-114825029448473821206/My Drive/LIGHT_GBM/models_2/LGBM_models_for_cnn_comparison_T1V1t2_V3'

results_list = []
for k in utils.sort(utils.get_files(bd, '*_model_results.pkl')):
    results_list.append(utils.load_obj(k))


val_auc = np.asarray([k['metrics']['auc'] for k in results_list])
test_auc = np.asarray([k['metrics_test']['auc'] for k in results_list])
val_TCE = np.asarray([k['metrics']['touch_count_errors_per_touch'] for k in results_list])
test_TCE = np.asarray([k['metrics_test']['touch_count_errors_per_touch'] for k in results_list])

val_auc = np.asarray([k['metrics']['auc'] for k in results_list])
test_auc = np.asarray([k['metrics_test']['auc'] for k in results_list])
val_TCE = np.asarray([k['metrics']['touch_count_errors_per_touch'] for k in results_list])
test_TCE = np.asarray([k['metrics_test']['touch_count_errors_per_touch'] for k in results_list])


val_TCE_min = np.asarray([min(k) for k in val_TCE])
inds = np.where(val_TCE_min<.04)[0]
# inds = [66]
# inds = [8]
val_auc_min = np.asarray([min(1-np.asarray(k)) for k in val_auc])
inds = np.where(val_auc_min<.000769)[0]
inds = [78]

d = dict()
d['auc'] = np.concatenate(val_auc[inds])
d['touch_count_errors_per_touch'] = np.concatenate(val_TCE[inds])
ax1, ax2 = foo_plot2()
ax1.set_ylim([0.00, 0.002])
ax1.set_ylim([0.0006, 0.001])
ax2.set_ylim([.025, .06])


d = dict()
d['auc'] = np.concatenate(test_auc[inds])
d['touch_count_errors_per_touch'] = np.concatenate(test_TCE[inds])
ax1, ax2 = foo_plot2()
ax1.set_ylim([0.005, 0.015])
ax2.set_ylim([.14, .22])

"""
inds = [78]
This is ind 78 and the best model based on AUC for val data, 
so this is what I will choose to be fair since the other (CNN) 
models were chosen based on this same criteria. 

"""
