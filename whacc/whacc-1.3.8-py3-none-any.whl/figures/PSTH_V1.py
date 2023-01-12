from whacc import utils, image_tools
import os
import copy
import numpy as np
import matplotlib.pyplot as plt
from tqdm.auto import tqdm

from natsort import natsorted, ns

# from tensorflow.keras.models import Model
import pytz
import matplotlib.pyplot as plt
from whacc import image_tools
from whacc import utils
import os
import scipy.io as spio
import h5py
# from tqdm.notebook import tqdm

import numpy as np
import mat73
import numpy as np
import scipy.stats
from numpy import trapz

# U_file = '/Users/phil/Downloads/touch_pole.mat'
# touch_mat = utils.loadmat(U_file)
# dict_list = []
# for k in touch_mat['tStruct']:
#     dict_list.append(utils._todict(k))
# dict_list[0].keys()
#
#
# U_file = '/Users/phil/Downloads/interneurons.mat'
# # U_ARRAY = mat73.loadmat(U_file)
# touch_mat = utils.loadmat(U_file)
# dict_list = []
# for k in touch_mat['U']:
#     dict_list.append(utils._todict(k))
# d = dict_list[-1]
#
# utils.info(d)
# utils.info(d['whisker'])
# utils.info(d['meta'])
# touch_mat['U']

def mean_confidence_interval(data, confidence=0.95):
    a = 1.0 * np.array(data)
    n = len(a)
    m, se = np.mean(a), scipy.stats.sem(a)
    h = se * scipy.stats.t.ppf((1 + confidence) / 2., n-1)
    return m, m-h, m+h

def CI(data):
    out = []
    for k in data:
        out.append(mean_confidence_interval(k))
    return out

def get_h5_trial_nums(h5):
    w_file_name_nums = utils.getkey(h5, 'file_name_nums')
    w_frame_nums = utils.getkey(h5, 'frame_nums')
    trial_inds = (np.cumsum(w_frame_nums) - w_frame_nums[0]).astype(int)
    w_trials = w_file_name_nums[trial_inds]
    return w_trials

def trial_inds_to_ms_inds(frame_nums, trial_inds):
    out = []
    for i, k in enumerate(frame_nums):
        if i in trial_inds:
            out.append(np.ones(k))
        else:
            out.append(np.zeros(k))
    return np.concatenate(out).astype(bool)

def get_onset_inds(x):
    return np.where(np.diff(np.concatenate(([0], 1 * (x)))) == 1)[0]

def get_in_range_inds(pole_onset, pole_offset, frame_nums, add_onset, add_offset=0):
    inds = []
    for ii, (i1, i2) in enumerate(utils.loop_segments(frame_nums)):
        tmp1 = np.zeros(i2 - i1)
        tmp1[add_onset + pole_onset[ii]:add_offset + +pole_offset[ii]] = 1
        inds.append(tmp1)
    inds = np.concatenate(inds)
    return inds
""" steps 
1) Find my U array and determine which data is actually curated by hand for my data
2) generate the H5s (should already be done) and insert the hand contacts into the h5 files, also do this will all of samsons data
3) make a figure using foo functions for PSTH with, peak, length of time of signal, onset time, and area under curve,
set sig portion by hand
"""

U_file = '/Volumes/GoogleDrive-114825029448473821206/.shortcut-targets-by-id/1xP-YUP9Yb9blCvX4WR5BWkeDsl3e8nKa/Phil_Iam/U_array_defined_PTITmanualCompare.mat'
U_file = '/Volumes/GoogleDrive-114825029448473821206/.shortcut-targets-by-id/1xP-YUP9Yb9blCvX4WR5BWkeDsl3e8nKa/Phil_Iam/U_array_defined_ManualSet_18includesallcontacts.mat'
U_ARRAY = mat73.loadmat(U_file)

U_cell_nums = []
for c in U_ARRAY['U']:
    U_cell_nums.append(int(c['cellNum']))

# h5 = '/Volumes/GoogleDrive-114825029448473821206/My Drive/Session21_V2_FINISHED/Session21/AH1184X08062021x21_final_combined.h5'
# utils.open_folder(h5)
bd = '/Volumes/GoogleDrive-114825029448473821206/.shortcut-targets-by-id/1pUteMEgx37rAyqujJWxVN9-ywFAqaxhF/WhACC_PROCESSING_FOLDER/Finished_Sessions/'
final_h5s = utils.get_files(bd, '*final_combined.h5')

cell_list = utils.sort([1, 9, 19, 21, 77, 94])
cell_list = np.sort([int(k.split('_final_combined.h5')[0].split('x')[-1]) for k in final_h5s])
cell_list = np.intersect1d(U_cell_nums, cell_list)
# cell_list = [21]
# good_cells =[9,  19,  65,  73,  83, 103, 106, 114]
# bad_cells = [105, 94, 77, 33, 31, 23, 21, 14, 1]


h5_list = utils.sort(utils.lister_it(final_h5s, ['Session' + str(k) + '/' for k in cell_list]))
W = dict()
W['meta'] = dict()

start_pad = 100
end_pad = 350
utils.print_list_with_inds(c['varNames'])
whacc_label_key = 'yhat_by_trial_temp_model_with_nans'
whacc_label_key = 'YHAT__optuna_samson_all_sessions_8_full_trials_each__weightedx2_V1_002_model'
whacc_thresh = 0.5


def get_aligned_contacts_from_U_cell(c):
    S_ctk = np.asarray([tmp1.T.flatten() for tmp1 in c['S_ctk']])
    contacts = np.nansum([S_ctk[10], S_ctk[13]], axis=0)

def foo_operate_on_pred(x, smooth_by):
    utils.smooth(x, smooth_by)
    return x


cell_nums_tmp = [1,   9,   14,  19, 21, 23,  31, 65,  73,  77,  83,  94,  103, 105, 106, 114]
phils_onsets =  [101, 100, 110, 98, 99, 100, 90, 100, 105, 105, 109, 124, 110, 114, 111, 118]
onsets_by_hand = dict()
for i, k in enumerate(cell_nums_tmp):
    onsets_by_hand[k] =phils_onsets[i]

smooth_by = 11

for (h5, cell_num) in zip(h5_list, tqdm(cell_list)):
    if cell_num == 21:
        asdf
    cust_onset = onsets_by_hand[cell_num]

    # load the proper cell from U array and init the dict
    W[cell_num] = dict()
    cell_ind = np.where(cell_num == np.asarray(U_cell_nums))[0][0]
    c = U_ARRAY['U'][cell_ind]

    # get index for human and whacc TRIAL data (U array and H5 file respectively)
    h_trials = c['meta']['usedTrialNums'].astype(int)
    w_trials = get_h5_trial_nums(h5)
    intersecting_trials, h_trial_inds, w_trial_inds = np.intersect1d(h_trials, w_trials, return_indices=True)

    # get the index for the corresponding ms data
    h_frame_nums_temp = np.asarray([c['R_ntk'].shape[0]] * c['R_ntk'].shape[1])  # NOTE this uses data from the U array that is a 2D matrix and thus for sessions with different trials lengths you will have ot add in the frame nums here.
    h_ms_inds = trial_inds_to_ms_inds(h_frame_nums_temp, h_trial_inds)
    frame_nums = h_frame_nums_temp[h_trial_inds]  # index out proper frame_nums

    w_frame_nums_temp = utils.getkey(h5, 'frame_nums').astype(int)
    w_ms_inds = trial_inds_to_ms_inds(w_frame_nums_temp, w_trial_inds)
    w_frame_nums = w_frame_nums_temp[w_trial_inds]  # index out proper frame_nums
    assert np.all(frame_nums == w_frame_nums), "frame nums don't match this should never happen"

    # first index out all the human data we are using "h_trial_inds" for these
    pole_onset = (c['meta']['poleOnset'] * 1000).astype(int)[h_trial_inds]
    pole_offset = (c['meta']['poleOffset'] * 1000).astype(int)[h_trial_inds]

    onset_diff = int(np.median(pole_onset)- cust_onset)
    pole_onset = pole_onset-onset_diff
    pole_offset = pole_offset-onset_diff
    # pole_offset[:]= 1500

    # now do the same for WhACC data, using "w_trial_inds" for these
    "__________________"
    # pole_out_of_range_mask
    in_range = get_in_range_inds(pole_onset, pole_offset, frame_nums, add_onset=0, add_offset=0)
    # next index the human ms data using "h_ms_inds"
    # utils.overwrite_h5_key(h5, 'in_range', 'in_range')
    S_ctk = np.asarray([tmp1.T.flatten() for tmp1 in c['S_ctk']])

    h_labels = np.nansum([S_ctk[10], S_ctk[13]], axis=0)[h_ms_inds]*in_range



    spikes = c['R_ntk'].T.flatten()[h_ms_inds]*1000

    # next index the WhACC ms data using "w_ms_inds"
    ####_____####_____####_____####_____####_____####_____
    labels_tmp = utils.getkey(h5, whacc_label_key)
    resorted_inds = np.argsort(w_trials)
    segs = np.asarray(utils.loop_segments(w_frame_nums_temp, 1))
    tmp1 = []
    for i, k in enumerate(resorted_inds):
        tmp1.append(labels_tmp[segs[0, k]:segs[1, k]])
    labels_sorted = np.concatenate(tmp1)
    ####_____####_____####_____####_____####_____####_____
    w_labels = labels_sorted[w_ms_inds]*in_range
    w_labels = foo_operate_on_pred(w_labels, smooth_by)

    h_touch_onset_inds = get_onset_inds(h_labels)
    h_spk_onset = utils.cut_with_nans(spikes, h_touch_onset_inds, start_pad, end_pad=end_pad)


    w_touch_onset_inds = get_onset_inds(w_labels > whacc_thresh)
    w_spk_onset = utils.cut_with_nans(spikes, w_touch_onset_inds, start_pad, end_pad=end_pad)


    W[cell_num]['spikes'] = spikes
    W[cell_num]['w_touch_onset_inds'] = w_touch_onset_inds
    W[cell_num]['h_touch_onset_inds'] = h_touch_onset_inds
    W[cell_num]['w_spk_onset'] = w_spk_onset
    W[cell_num]['h_spk_onset'] = h_spk_onset
    W[cell_num]['h_labels'] = h_labels
    W[cell_num]['w_labels'] = w_labels

    W[cell_num]['h_spk_mean'] = np.nanmean(h_spk_onset, axis=0)
    W[cell_num]['w_spk_mean'] = np.nanmean(w_spk_onset, axis=0)
    W[cell_num]['mouseName'] = c['meta']['mouseName']
    W[cell_num]['cellName'] = c['meta']['cellName']
    W[cell_num]['sessionName'] = c['meta']['sessionName']
    W[cell_num]['usedTrialNums'] = c['meta']['usedTrialNums']
    W[cell_num]['template_img'] = utils.getkey(h5, 'template_img')


    W[cell_num]['in_range'] = in_range
    W[cell_num]['h5_name'] = h5
    W[cell_num]['frame_nums'] = w_frame_nums# frame nums are same for both, asserted above
    W[cell_num]['w_ms_inds'] = w_ms_inds



W['meta']['whacc_thresh'] = whacc_thresh
W['meta']['whacc_label_key'] = whacc_label_key
W['meta']['start_pad'] = start_pad
W['meta']['end_pad'] = end_pad
W['meta']['smooth_by'] = smooth_by
W['meta']['x'] = np.arange(end_pad+start_pad+1)-start_pad


bd= '/Users/phil/Dropbox/HIRES_LAB/WhACC PAPER/small_data'
utils.save_obj(W, bd+os.sep+'W_dict_from_PSTH_V1')
# ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']

def hex_to_rgb(h):
    return list(int(h[i:i+2], 16) for i in (0, 2, 4))

colors = dict()
colors['human'] = hex_to_rgb('1f77b4')
colors['whacc'] = hex_to_rgb('ff7f0e')
for k in colors:
    colors[k] = list(np.asarray(colors[k])/255)


def foo_plot(c, W, data_key, color_in, smooth_by=1, mult_by=1, leg='', ax=None):
    y = np.nanmean(c[data_key], axis=0)
    sd = np.nanstd(c[data_key], axis=0)
    se = sd/np.sqrt(c[data_key].shape[0])
    ci = 1.96*se
    plt.plot(W['meta']['x'], mult_by*utils.smooth(np.nanmean(c[data_key], axis=0), smooth_by), color=color_in+[1], label=leg, axes=ax)
    y_low, y_up = mult_by*utils.smooth(y-ci, smooth_by), mult_by*utils.smooth(y+ci, smooth_by)
    plt.fill_between(W['meta']['x'], y_low, y_up, color=color_in+[.25])
    plt.ylabel('Spk/S')
    plt.xlabel('Time (ms)')
    plt.ylim(np.max([plt.ylim()[0], 0]), plt.ylim()[1])



good_cells =[9,  19,  65,  73,  83, 103, 106, 114]
bad_cells = [105, 94, 77, 33, 31, 23, 21, 14, 1]
selected_cell = [19]

to_loop_cells = cell_list
smooth_by = 7
bd = '/Users/phil/Dropbox/HIRES_LAB/WhACC PAPER/figures/misc/PSTH_final_mod_start_to_1500/'
# utils.clear_dir(bd)
format = 'png'
transparent = True
for ii, cell_num in enumerate(to_loop_cells):

    c = copy.deepcopy(W[cell_num])
    plt.figure(figsize=[10, 6])

    c['title1'] = 'Cell '+str(cell_num)+'  smooth='+str(smooth_by)
    plt.title(c['title1'])

    foo_plot(c, W, 'h_spk_onset', colors['human'], smooth_by=smooth_by, leg='Human')
    foo_plot(c, W, 'w_spk_onset', colors['whacc'], smooth_by=smooth_by, leg='WhACC')
    plt.xlim(-50, 250)
    plt.legend()
    plt.savefig(bd+os.sep+c['title1'] + '.'+format, transparent=transparent, format=format)
    plt.close()

    plt.figure()
    plt.imshow(c['template_img'])

    plt.savefig(bd+os.sep+c['title1'] + '_POLE.'+format, transparent=transparent, format=format)
    plt.close()
utils.open_folder(bd)


# c['h_spk_on_off'] = np.arange(8, 22)
# c['w_spk_on_off'] = np.arange(7, 21)

c['h_spk_on_off_inds'] = np.intersect1d(c['h_spk_on_off'], W['meta']['x'], return_indices=True)[-1]
c['w_spk_on_off_inds'] = np.intersect1d(c['w_spk_on_off'], W['meta']['x'], return_indices=True)[-1]

c['h_sig_area'] = trapz(c['h_spk_mean'][c['h_spk_on_off_inds']])
c['w_sig_area'] = trapz(c['w_spk_mean'][c['w_spk_on_off_inds']])

c['h_sig_peak'] = np.max(c['h_spk_mean'][c['h_spk_on_off_inds']])
c['w_sig_peak'] = np.max(c['w_spk_mean'][c['w_spk_on_off_inds']])

c['h_sig_peak_ind'] = np.argmax(c['h_spk_mean'][c['h_spk_on_off_inds']])
c['w_sig_peak_ind'] = np.argmax(c['w_spk_mean'][c['w_spk_on_off_inds']])

x = c['h_spk_onset'][:, c['h_spk_on_off_inds'][c['h_sig_peak_ind']]]
c['h_sig_peak_ci_95'] = 1.96*(np.std(x)/(np.sqrt(len(x))))
x = c['w_spk_onset'][:, c['w_spk_on_off_inds'][c['w_sig_peak_ind']]]
c['w_sig_peak_ci_95'] = 1.96*(np.std(x)/(np.sqrt(len(x))))


# plt.plot(c['h_sig_peak']-c['w_sig_peak'], )


def foo_plot2(ax_, data_key, xlab, ii):
    # ax_ = ax_flat[0]
    ax_.plot(c['h'+data_key]-c['w'+data_key], ii, '.', color=colors['whacc'])
    ax_.vlines(0, *ax_.get_ylim(), color=colors['human'])
    xl = 1.5*np.max(np.abs(ax_.get_xlim()))
    ax_.set_xlim(-xl, xl)
    ax_.set_xlabel(xlab)
# foo_plot2(ax_flat[0], '_sig_peak', 'asdfasdf', ii)


fig, ax = plt.subplots(1, 6, sharey=True)
ax_flat = ax.flatten()

ax_, data_key, xlab = ax_flat[0], '_sig_peak', 'peak response\n(Spk/S)'

ax_.errorbar(0, ii, xerr=c['h_sig_peak_ci_95'])
ax_.plot(c['h'+data_key]-c['w'+data_key], ii, '.', color=colors['whacc'])
# ax_.vlines(0, *ax_.get_ylim(), color=colors['human'])
xl = 1.5*np.max(np.abs(ax_.get_xlim()))
ax_.set_xlim(-xl, xl)
ax_.set_xlabel(xlab)


'h_spk_onset'
ax_, data_key, xlab = ax_flat[1], '_spk_on_off', 'Onset Latency\n(ms)'

ax_.vlines(0, *ax_.get_ylim(), color=colors['human'])
# ax_.plot(0, *ax_.get_ylim(), '-',color=colors['human'])

ax_.plot(c['h'+data_key][0]-c['w'+data_key][0], ii, '.', color=colors['whacc'])
xl = 1.5*np.max(np.abs(ax_.get_xlim()))
ax_.set_xlim(-xl, xl)
ax_.autoscale(enable=True, axis='y', tight=True)
ax_.set_xlabel(xlab)
ax_.get_ylim()

"""
plot colored Vline at 0 for each 
we could sample 100 times at the same regions to get AUC, and peak to plot confidence intervals of 95% 
onsets cant do this unless we want to automate it
"""



c['h_sig_'] =
c['w_sig_'] =

c['h_sig_'] =
c['w_sig_'] =



# def poison_standard_error(x):
#     return 1.96*np.sqrt(np.mean(x)/len(x))
# def CI(x):
#     out = []
#     for k in x.T:
#         out.append(poison_standard_error(k))
#     return out

# plt.plot(np.nanmean(c['w_spk_onset'], axis=0), color=colors['whacc']+[1])



# plt.fill_between(W['meta']['x'], y, sd, alpha=.25)






plt.plot(np.nanmean(c['h_spk_onset'], axis=0))
plt.plot(np.nanmean(c['w_spk_onset'], axis=0))



# plt.figure()
    # plt.title(cell_num)
    # plt.plot(np.nanmean(h_spk_onset, axis=0))







bad_cells = [105, 94, 77, 33, 31, 23, 21, 14, 1]
good_cells =[9,  19,  65,  73,  83, 103, 106, 114]

for cell_num in bad_cells:
    cell_ind = np.where(cell_num == np.asarray(U_cell_nums))[0][0]
    c = U_ARRAY['U'][cell_ind]
    print(c['meta']['mouseName'], c['meta']['sessionName'])

for cell_num in good_cells:
    cell_ind = np.where(cell_num == np.asarray(U_cell_nums))[0][0]
    c = U_ARRAY['U'][cell_ind]
    print(c['meta']['mouseName'], c['meta']['sessionName'])


utils.update_whacc()
