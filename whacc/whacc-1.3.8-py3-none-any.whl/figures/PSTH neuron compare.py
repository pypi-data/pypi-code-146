

import matplotlib.pyplot as plt
from tqdm.auto import tqdm
from imgaug import augmenters as iaa  # optional program to further augment data

from whacc import utils
import numpy as np
from whacc import image_tools
from natsort import natsorted, ns
import pickle
import pandas as pd
import os
import copy
import seaborn as sns
from keras.preprocessing.image import ImageDataGenerator
import h5py

from whacc import utils, analysis
import h5py
import matplotlib.pyplot as plt
import numpy as np
from sklearn import metrics
from pathlib import Path

import mat73
from whacc import utils
mat_file = '/Users/phil/Dropbox/U_191028_1154.mat'
data_dict = mat73.loadmat(mat_file)

# utils.info(data_dict)

# for k in ['R_ntk', 'S_ctk', 'c', 'cellNum', 'details', 'k', 'meta', 't', 'u', 'varNames', 'whisker']:
#     print('__________________________________________________________________')
#     print(k)
#     utils.info(data_dict['U'][0][k])
"""
LIST OC CELLS 
'R_ntk', 'S_ctk', 'c', 'cellNum', 'details', 'k', 'meta', 't', 'u', 'varNames', 'whisker'

--details-- 


"""

"""
contacts onset 
--  
 'firstTouchOnset',
 'firstTouchOffset',
 'firstTouchAll',
 'lateTouchOnset',
 'lateTouchOffset',
 'lateTouchAll',
 
whisker videos (ensure ell the data is 4000 long) so I can match with the whacc analysis

spikes 

"""
for cell_ind in range(len(data_dict['U'])):
    print('_______________')
    print(cell_ind)
    print(data_dict['U'][cell_ind]['details']['cellNum'])


cell_ind = 19
d = dict()

d['spikes'] = data_dict['U'][cell_ind]['R_ntk']
vars = ['thetaAtBase',
 'velocity', 'amplitude', 'setpoint', 'phase', 'deltaKappa', 'M0Adj', 'FaxialAdj', 'firstTouchOnset', 'firstTouchOffset',
 'firstTouchAll', 'lateTouchOnset', 'lateTouchOffset', 'lateTouchAll', 'PoleAvailable','beamBreakTimes']
for i, k in enumerate(vars):
    d[k] = data_dict['U'][cell_ind]['S_ctk'][i]

d['contacts'] = np.logical_or(d['firstTouchAll'], d['lateTouchAll'])

vars2 = ['trialNumsUseTrials', 'useTrials', 'whiskerTrialNumsUseTrials']
for i, k in enumerate(vars2):
    d[k] = data_dict['U'][cell_ind]['details'][k]

for i, k in enumerate(vars2):
    print('__________________')
    print(k)
    print(d[k].shape)
    print(d[k][-10:])
for k in ['cellCode', 'cellNum', 'depth', 'mouseName', 'sessionName', 'userRemovedTrials', 'whiskerTrialTimeOffset']:
    d[k] = data_dict['U'][cell_ind]['details'][k]
    print('__________________')
    print(k)
    print(d[k])

# tmp1 = utils.loadmat('/Users/phil/Desktop/ConTA_23.mat')
"""
utils.auto_combine_final_h5s('/Volumes/GoogleDrive-114825029448473821206/My Drive/PHILLIP/processing/P1_FINISHED_MP4s/AH0688/170820')
"""

# utils.info(data_dict['U'][cell_ind]['meta'])
#
#
#
# x = np.pad(x, 4, mode='empty')
# x
#
#
#
# x = [0, 0, 1, 1, 1, 0, 0]
# start_pad = 4
# inds = [2, 4]
# # inds = 2
# end_pad = None
def cut_with_nans(x, inds, start_pad, end_pad = None):
    inds = np.asarray(utils.make_list(inds, True)) + start_pad
    if end_pad is None:
        end_pad = start_pad
    x = np.concatenate((np.ones(start_pad)*np.nan, x, np.ones(end_pad)*np.nan))
    x_out = []
    for k in inds:
        i1 = np.max([0, k-start_pad])
        i2 = k+end_pad+1
        x_out.append(x[i1:i2])
    return np.asarray(x_out)

# cut_with_nans(x, inds, start_pad, end_pad = None)


start_pad = 50
end_pad = 250
x_out = []
for x in tqdm(d['contacts'].T):
    inds = np.where(np.diff(np.concatenate(([0], x)))==1)[0]
    if len(inds) != 0:
        x_out.append(cut_with_nans(x, inds, start_pad, end_pad = end_pad))


x2 = np.vstack(x_out)
x3 = np.nanmean(x2, axis=0)

plt.plot(x3)


#
# plt.imshow(d['firstTouchAll'][400:700, :].T)
# plt.imshow(d['lateTouchAll'][400:700, :].T)



# plt.imshow(d['contacts'][400:700, :].T)


# np.where(d['firstTouchOnset'][:, 0]==1)[0]








from whacc import utils
mat_file = '/Users/phil/Dropbox/U_191028_1154.mat'
mat = utils.loadmat(mat_file)





bd = '/Users/phil/Dropbox/'
files = utils.get_files(bd, '*')

out = utils.lister_it(files, ['U_'])
out = utils.lister_it(out, ['.mat'])

for k in out:
    print(k)
