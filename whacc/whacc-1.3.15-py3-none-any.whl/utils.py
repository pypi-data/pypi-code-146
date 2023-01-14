from whacc.feature_maker import convert_h5_to_feature_h5, standard_feature_generation2  # , load_selected_features
from whacc.pole_tracker import PoleTracking
from whacc import model_maker
import shutil

import numpy as np
import os
import sys
import glob
from natsort import natsorted, ns
import scipy.io as spio
import h5py
import matplotlib.pyplot as plt
import pandas as pd

import copy
import time
from whacc import image_tools
import whacc
import platform
import subprocess
from scipy.signal import medfilt, medfilt2d
import pickle
from tqdm.autonotebook import tqdm

from datetime import timedelta, datetime
import pytz
import warnings
import cv2

from pathlib import Path
import urllib.request
from zipfile import ZipFile

"""
Arrow Symbol	Arrow Type	Alt Code
↑	Upwards Arrow	24
↓	Downwards Arrow	25
→	Rightwards Arrow	26
←	Leftwards Arrow	27


plt.imshow(tmp2, interpolation='nearest', aspect='auto')

color codes 
https://www.webucator.com/article/python-color-constants-module/


https://stackoverflow.com/questions/18596410/importerror-no-module-named-mpl-toolkits-with-maptlotlib-1-3-0-and-py2exe
import importlib
importlib.import_module('mpl_toolkits').__path__

import mpl_toolkits


"""


def zorder(ax, zorder):
    plt.setp(ax.lines, zorder=zorder)
    plt.setp(ax.collections, zorder=zorder)

def NANify_data(tvt_x, tvt_y, tvt_fn, numpy_seed = 42):
    nan_array_border_inds = load_nan_border_index()
    tvt_x_naned = []
    for data in tqdm(tvt_x):
        data = copy.deepcopy(data)
        np.random.seed(numpy_seed)
        inds = np.random.choice(nan_array_border_inds.shape[0], data.shape[0])
        replace_with_nans = nan_array_border_inds[inds]
        data[replace_with_nans] = np.nan
        tvt_x_naned.append(data)
    del data

    for i, nan_data in enumerate(tqdm(tvt_x_naned)):
        tvt_x[i] = np.vstack([tvt_x[i], tvt_x_naned[i]])
        tvt_y[i] = np.concatenate([tvt_y[i], tvt_y[i]])
        tvt_fn[i] = np.concatenate([tvt_fn[i], tvt_fn[i]])
    return tvt_x, tvt_y, tvt_fn

def quick_spliter(split_nums, len_array):
    l_nums = np.sum(split_nums)
    count = 1 + (len_array // l_nums)

    inds = np.ones(l_nums)
    for ii, (i1, i2) in enumerate(loop_segments(split_nums)):
        inds[i1:i2] = ii
    inds = np.asarray(list(inds) * count)
    inds = inds[:len_array]

    bool_inds_arrays = []
    for k in range(len(split_nums)):
        bool_inds_arrays.append(np.asarray(k == inds))
    bool_inds_arrays = np.asarray(bool_inds_arrays)

    frame_nums = []
    for b in bool_inds_arrays:
        b2 = group_consecutives(b, 0)[0]
        frame_nums.append([len(k) for k in b2 if np.all(k)])

    return bool_inds_arrays, frame_nums


def load_training_and_curated_data(h5_list, labels_key, train_val_split=[7, 3], nan_ify_data=True, new_data_weight=2):
    print('loading original training data...')
    tvt_x, tvt_y, tvt_fn = load_training_data()
    og_lens = [len(k) for k in tvt_y]


    print('loading your curated data...')
    for h5 in tqdm(h5_list):
        data = getkey(h5, 'final_features_2105')
        labels = getkey(h5, labels_key)
        bool_inds, frame_nums = quick_spliter(train_val_split, len(labels))

        if np.sum(labels == -1) > 0:
            print(h5 + " this file has -1's in its labels...")
            assert False, h5 + " this file has -1's in its labels..."

        i1, i2 = bool_inds
        tvt_x[0] = np.vstack((tvt_x[0], data[i1]))
        tvt_y[0] = np.concatenate((tvt_y[0], labels[i1]))
        tvt_fn[0] = np.concatenate((tvt_fn[0], frame_nums[0]))

        tvt_x[1] = np.vstack((tvt_x[1], data[i2]))
        tvt_y[1] = np.concatenate((tvt_y[1], labels[i2]))
        tvt_fn[1] = np.concatenate((tvt_fn[1], frame_nums[1]))
    if nan_ify_data:
        print('NANifying data this is memory intensive and may take up to 1-2 min...')
        tvt_x, tvt_y, tvt_fn = NANify_data(tvt_x, tvt_y, tvt_fn)

    tvt_w = []
    for i, k in enumerate(tvt_y):
        x = np.ones_like(k)*new_data_weight
        x[:og_lens[i]] = 1
        tvt_w.append(x)

    return tvt_x, tvt_y, tvt_fn, tvt_w

def _single_to_list_input_checker(in_, len_list):
    in_ = make_list(in_, suppress_warning=True)

    if len(in_) == 1:
        in_=in_*len_list
    else:
        assert len(in_) == len_list, """'_single_to_list_input_checker' length of input list and the set rquirment dont match"""
    return in_

def download_all_whacc_data(overwrite=False, download_inds=0):

    overwrite = _single_to_list_input_checker(overwrite, 3)
    download_inds = _single_to_list_input_checker(download_inds, 3)

    download_resnet_model(overwrite[0], download_inds[0])
    download_training_data(overwrite[1], download_inds[1])
    download_extra_LGBM_models(overwrite[2], download_inds[2])



def load_training_data():
    bd = get_whacc_path() + os.sep + '/whacc_data/training_data'
    if not os.path.isdir(bd):
        print('Auto downloading training data, this will only run once')
        download_training_data()

    tvt_x = load_obj(bd + os.sep + 'tvt_x.pkl')
    tvt_y = load_obj(bd + os.sep + 'tvt_y.pkl')
    tvt_fn = load_obj(bd + os.sep + 'tvt_fn.pkl')

    return tvt_x, tvt_y, tvt_fn


def download_data_dict():
    d = dict()
    d['resnet_model'] = ['https://www.dropbox.com/sh/knq6la5fcu73zk5/AABQuMmxm4msVbWIddl9x1v3a?dl=1',
                         'https://www.dropbox.com/s/k0398tchgk20lkv/final_resnet50V2_full_model.zip?dl=1']
    d['split_by_trial_2105_data'] = ['https://www.dropbox.com/sh/07uavloxi3ugnjy/AAABU4nsRkJJ4TtkBGxh7zIHa?dl=1']
    d['extra_LGBM_models'] = ['https://www.dropbox.com/sh/l5yuw3r2hqdhrw0/AABSq2L9265cWzAs6AgJOS9Va?dl=1']

    d['example_MP4s'] = ['https://www.dropbox.com/sh/bv5wectlbugacef/AAAuueROhu_rHmMZjdVgGly_a?dl=1']

    return d


def download_example_mp4s(dst, overwrite=False, link_ind=0):
    d = download_data_dict()
    filename = get_whacc_path() + os.sep + '/whacc_data/example_MP4s.zip'
    if os.path.isdir(dst):
        if overwrite:
            shutil.rmtree(dst)
        else:
            print('example_MP4s are already downloaded, if you want to overwrite it set overwrite to True')
            return
    # make_path(dst)
    print('downloading example_MP4s...')
    url = d['example_MP4s'][link_ind]
    urllib.request.urlretrieve(url, filename)
    with ZipFile(filename, 'r') as zipObj:
        print('unzipping file ...')
        zipObj.extractall(path=dst)
    print('deleting zip file ...')
    os.remove(filename)
    print('Done')

def download_extra_LGBM_models(overwrite_model=False, link_ind=0):
    d = download_data_dict()
    filename = get_whacc_path() + os.sep + '/whacc_data/final_model/extra_LGBM_models.zip'
    dst = filename[:-4]
    if os.path.isdir(dst):
        if overwrite_model:
            shutil.rmtree(dst)
        else:
            print('extra_LGBM_models is already downloaded, if you want to overwrite it set overwrite to True')
            return
    # make_path(dst)
    print('downloading extra_LGBM_models...')
    url = d['extra_LGBM_models'][link_ind]
    urllib.request.urlretrieve(url, filename)
    with ZipFile(filename, 'r') as zipObj:
        print('unzipping file ...')
        zipObj.extractall(path=dst)
    print('deleting zip file ...')
    os.remove(filename)
    print('Done')


def download_training_data(overwrite_model=False, link_ind=0):
    d = download_data_dict()
    filename = get_whacc_path() + os.sep + '/whacc_data/training_data.zip'
    dst = filename[:-4]
    if os.path.isdir(dst):
        if overwrite_model:
            shutil.rmtree(dst)
        else:
            print('training data is already downloaded, if you want to overwrite it set overwrite to True')
            return
    # make_path(dst)
    print('downloading training data (3GB)...')
    url = d['split_by_trial_2105_data'][link_ind]
    urllib.request.urlretrieve(url, filename)
    with ZipFile(filename, 'r') as zipObj:
        print('unzipping file ...')
        zipObj.extractall(path=dst)
    print('deleting zip file ...')
    os.remove(filename)
    print('Done')


def download_resnet_model(overwrite_model=False, link_ind=0):
    d = download_data_dict()

    filename = get_whacc_path() + os.sep + '/whacc_data/final_model/final_resnet50V2_full_model.zip'
    dst = filename[:-4]
    if os.path.isdir(dst):
        if overwrite_model:
            shutil.rmtree(dst)
        else:
            print('model is already downloaded, if you want to overwrite it set overwrite to True')
            return
    print('downloading model zip file (100mb)...')
    url = d['resnet_model'][link_ind]
    urllib.request.urlretrieve(url, filename)
    with ZipFile(filename, 'r') as zipObj:
        print('unzipping file ...')
        zipObj.extractall(path=dst)
    print('deleting zip file ...')
    os.remove(filename)
    print('Done')


def equal_distance_pole_sample(h5, num_videos=100, equal_x=True, inds_to_bad_trials=None):
    frame_nums = getkey(h5, 'frame_nums')
    if inds_to_bad_trials is None:
        inds_to_bad_trials = np.zeros_like(frame_nums)
    inds_to_bad_trials = np.asarray(inds_to_bad_trials).astype(bool)
    locations_x_y = getkey(h5, 'locations_x_y')
    xy_ind = 1
    if equal_x:
        xy_ind = 0
    fnl = loop_segments(frame_nums, 1)  # get frame num segments

    mid = (np.mean(fnl[0][:2]) + fnl[0]).astype(int)  # get the index to the middle of trial to get the x position
    x_poles = np.asarray(locations_x_y)[mid, xy_ind].astype(float)  # grab middle x positions
    x_poles[inds_to_bad_trials] = np.nan  # remove trials we don't want for any reason

    arg_xpoles = np.argsort(x_poles)  # get sorted order
    if np.any(inds_to_bad_trials):
        arg_xpoles = arg_xpoles[:-np.sum(inds_to_bad_trials)]  # remove the nans at the beginning if there are any

    idx = np.round(np.linspace(0, len(arg_xpoles) - 1, num_videos)).astype(int)

    out = (arg_xpoles[idx]).astype(int)
    u_out = unique_keep_order(out)
    if len(u_out) != len(out):
        warnings.warn(
            'less viable trials than requested, everything will work fine but there will be less trials in the output')
    return u_out


def make_transfer_learning_data(h5_list, start_frame, end_frame, num_videos=100, equal_x=True, inds_to_bad_trials=None,
                                vid_dir=None, save_dir=None, final_trimmed_h5_name=None, overwrite=False,
                                model_full_file_name=None, smooth_by=5):
    if inds_to_bad_trials is None:
        inds_to_bad_trials = [None]*len(h5_list)
    for ii, h5 in enumerate(make_list(h5_list)):
        equal_x_trial_inds = equal_distance_pole_sample(h5, num_videos=num_videos, equal_x=equal_x, inds_to_bad_trials=inds_to_bad_trials[ii])
        num_trials_per_session = len(equal_x_trial_inds)

        new_h5_name = os.path.dirname(h5) + os.sep + "TEMP_TL_DATA_" + os.path.basename(h5)[:-3]
        if save_dir is None:
            save_dir = os.path.dirname(h5)
        if final_trimmed_h5_name is None:
            final_trimmed_h5_name = save_dir + os.sep + "TL_DATA_" + os.path.basename(h5)
        if os.path.isfile(final_trimmed_h5_name):
            assert overwrite, 'File ' + final_trimmed_h5_name + ' exists, set overwrite to True of you want to overwrite it'
            os.remove(final_trimmed_h5_name)
        make_path(save_dir)

        keys = print_h5_keys(h5, 1, 0)
        # check basis keys that we need
        check_keys = ['template_img', 'full_file_names', 'frame_nums', 'final_features_2105']
        check_keys_need = [k in keys for k in check_keys]
        assert np.all(
            check_keys_need), """'template_img', 'full_file_names', 'final_features_2105' and 'frame_nums' must be present, something is wrong with the H5 file..."""
        # check keys to know if we have to re track to get images etc.
        check_keys = ['images']
        check_keys_no_rerun = [k in keys for k in check_keys]

        # assert np.all(check_keys_no_rerun)==False and vid_dir is not None,  """'images' key not present please set 'vid_dir'"""

        if vid_dir is None and 'images' not in keys:
            assert False, """'images' key not present please set 'vid_dir'"""

        new_frame_nums = np.asarray([end_frame - start_frame] * num_trials_per_session)
        if model_full_file_name is None:
            mod = model_maker.load_final_light_GBM()
        else:
            mod = load_obj(model_full_file_name)
        images = []
        final_features_2105 = []
        pred_labels = []


        if smooth_by > (end_frame - start_frame):
            tmp_smooth_by = copy.deepcopy(smooth_by)
            smooth_by = end_frame - start_frame
            warnings.warn(
                'length of sequential frames selected is smaller than the default/set smoothing kernel of '+str(tmp_smooth_by)+', setting smoothing kernel to ' + str(
                    smooth_by))
        loop_segs = np.asarray(loop_segments(getkey(h5, 'frame_nums'), True))[:, equal_x_trial_inds]

        with h5py.File(h5, 'r') as h_read:
            for i, (k1, k2) in enumerate(zip(loop_segs[0], loop_segs[1])):
                if 'images' in keys:
                    images.append(h_read['images'][k1:k2][start_frame:end_frame])
                x = h_read['final_features_2105'][k1:k2][start_frame:end_frame]
                final_features_2105.append(x)
                y = smooth(mod.predict(x), smooth_by)
                y = ((y>.5)*1).astype(int)
                pred_labels.append(y)
        if 'images' in keys:
            images = np.vstack(images)
        final_features_2105 = np.vstack(final_features_2105)
        pred_labels = np.concatenate(pred_labels)

        with h5py.File(final_trimmed_h5_name, 'w') as h:
            h['frame_nums'] = new_frame_nums
            h['labels'] = pred_labels
            h['template_img'] = getkey(h5, 'template_img')
            if 'images' in keys:
                h['images'] = images
            h['final_features_2105'] = final_features_2105

        if 'images' not in keys:
            selected_videos = np.asarray(h5_string_switcher(getkey(h5, 'full_file_names')))[equal_x_trial_inds]
            selected_videos = [norm_path(vid_dir + os.sep + vid) for vid in selected_videos]
            select_frame_inds = np.arange(start_frame - 2, end_frame)  # 2 on the left for 3lag data

            # select_frame_inds = None

            pt = PoleTracking(video_directory=vid_dir, template_png_full_name=getkey(h5, 'template_img'),
                              select_frame_inds=select_frame_inds, skip_check_if_FPS_is_an_int=True)
            pt.save_base_name = os.path.basename(new_h5_name)
            pt.video_files = selected_videos
            pt.track_all_and_save()

            # set h5 we just made via pole tracker -- delete when done
            h5_in = pt.full_h5_name
            # make 3lag image data saved as the final H5 since we want these images to curate later
            h5_3lag = h5_in.replace('.h5', '_3lag.h5')
            image_tools.convert_to_3lag(h5_in, h5_3lag)

            x = np.zeros_like(select_frame_inds)
            x[2:2 + end_frame - start_frame] = 1
            inds = np.asarray(list(x) * len(selected_videos)).astype(bool)
            L = len(getkey(final_trimmed_h5_name, 'labels'))
            assert L == np.sum(inds), """Length of labels and inds don't match"""
            inds2 = np.where(inds)[0]

            with h5py.File(final_trimmed_h5_name, 'r+') as h_dst:
                with h5py.File(h5_3lag, 'r') as h_src:
                    h_dst['images'] = h_src['images'][inds2]
            os.remove(h5_in)
            os.remove(h5_3lag)


def check_vids_for_issues_based_on_FPS_as_an_int(video_files):
    bad_inds = []
    for video_file in tqdm(video_files):
        video = cv2.VideoCapture(video_file)
        if video.isOpened() == True:
            frame_numbers = int(video.get(7))
            fps = video.get(5)
            if not fps == int(fps):
                print("for file " + os.path.basename(video_file) +
                      " FPS is not an integer, this usually indicates a problem with the video. TOTAL FRAMES = "
                      + str(frame_numbers))
                bad_inds.append(True)
                # print('removing file ' + os.path.basename(
                #     video_file) + ' because skip_if_FPS_is_not_int is set to True')
            else:
                bad_inds.append(False)
    return bad_inds


# def check_vids_for_issues_based_on_FPS_as_an_int(video_files):
#     all_videos = []
#     for video_file in tqdm(video_files):
#         video = cv2.VideoCapture(video_file)
#         if video.isOpened() == True:
#             frame_numbers = int(video.get(7))
#             fps = video.get(5)
#             if not fps == int(fps):
#                 print("for file " + os.path.basename(video_file) +
#                       " FPS is not an integer, this usually indicates a problem with the video. TOTAL FRAMES = "
#                       + str(frame_numbers))
#                 # print('removing file ' + os.path.basename(
#                 #     video_file) + ' because skip_if_FPS_is_not_int is set to True')
#             else:
#                 all_videos.append(video_file)
#     return all_videos


def unique_keep_order(x):
    indexes = np.unique(x, return_index=True)[1]
    out = np.asarray([x[index] for index in sorted(indexes)]).astype(int)
    return out


def hex_to_rgb(h):
    h = ''.join(h.split('#'))
    return list(int(h[i:i + 2], 16) for i in (0, 2, 4))


def intersect_data_with_nans(src_data_inds, data_to_match_inds, data=None):
    """

    Parameters
    ----------
    src_data_inds :  come from the data you want to use; inds, trial nums or frame nums, or raw inds; must be unique
    data_to_match_inds : 'src_data_inds' will be forced to match 'data_to_match_inds' index, length and order, inds, trial nums or frame nums, or raw inds; must be unique
    data : matches 'data_to_match_inds' but is the actaul

    Returns
    -------
    index data from data array 'data' that matches the length of 'data_to_match_inds'

    Examples
    ________
    data_inds =      np.asarray([12, 11, 13, 14, 15,      17])
    match_set_inds = np.asarray([11, 12,     14, 15, 16,  17,  18,  19,  20])
    data = np.asarray([9,8,2,3,4,7,5,6,4,5,6,7,8,9,92,1,1,56,33,44,55,66,77])

    out = utils.intersect_data_with_nans(data_inds, match_set_inds, data=None)
    print(np.vstack((out, match_set_inds)))

    out = utils.intersect_data_with_nans(match_set_inds, data_inds, data=None)
    print(np.vstack((out, data_inds)))

    data_inds_data = data[data_inds]
    match_set_inds_data = data[match_set_inds]
    out = utils.intersect_data_with_nans(data_inds, match_set_inds, data=data_inds_data)
    print(np.vstack((out, match_set_inds_data)))

    data_inds_data = data[data_inds]
    match_set_inds_data = data[match_set_inds]
    out = utils.intersect_data_with_nans(match_set_inds, data_inds, data=match_set_inds_data)
    print(np.vstack((out, data_inds_data)))

    """
    assert len(src_data_inds) == len(set(src_data_inds)), 'data_inds contains duplicates, this is not allowed'
    assert len(data_to_match_inds) == len(
        set(data_to_match_inds)), 'match_set_inds contains duplicates, this is not allowed'
    if data is None:
        data = src_data_inds
    match_inds = []
    for k in data_to_match_inds:
        if k in src_data_inds and not np.isnan(k):
            x = k == src_data_inds
            match_inds.append(np.where(x)[0][0].astype(float))
        else:
            match_inds.append(np.nan)
    out = index_with_nans(data, match_inds)
    return out


#
# def intersect_data_with_nans(data_inds, match_set_inds, data=None):
#     """
#     Parameters
#     ----------
#     data_inds : a list of trial numbers or time points for example or raw inds that come from the data you want to use
#     match_set_inds : a list of trial numbers or time points for example or raw inds that come from the list you want to match the length of
#     data : optional data to extract, otherwise it will treat 'data_inds' as 'data'
#
#     Examples
#     ________
#     data_inds =      np.asarray([11, 12, 13,  14, 15,     17])
#     match_set_inds = np.asarray([11, 12,     14, 15, 16,  17,  18,  19,  20])
#
#     out = intersect_data_with_nans(data_inds, match_set_inds, data=None)
#
#     print(np.vstack((out, match_set_inds)))
#
#     >> [[11. 12. 13. 14. nan 17. nan nan nan] # data from 'data_inds' that matches the shape and poistion of 'match_set_inds'
#         [11. 12. 14. 15. 16. 17. 18. 19. 20.]] # but has nan values where that data is missing for 'data_inds'
#
#     Returns
#     -------
#     indexed data that matched the length of 'match_set_inds
#     """
#     if data is None:
#         data = data_inds
#     ind1, ind2 = intersect_with_nans(data_inds, match_set_inds)
#     out = index_with_nans(data, ind2)
#     return out

def index_with_nans(x, inds):
    return [np.nan if np.isnan(k) else x[int(k)] for k in inds]


def intersect_with_nans(arr1, arr2):
    a, b, c = np.intersect1d(arr1, arr2, return_indices=True)
    b2 = np.ones_like(arr1) * np.nan
    b2[b] = b
    c2 = np.ones_like(arr2) * np.nan
    c2[c] = c
    return b2, c2


def find_step_onset(x):
    x = np.asarray(x).astype(float)
    x -= np.average(x)
    step = np.hstack((np.ones(len(x)), -1 * np.ones(len(x))))
    dary_step = np.convolve(x, step, mode='valid')
    step_indx = np.argmax(dary_step)
    return step_indx


def getkey(h5_list, key_name=None):
    """
    Parameters
    ----------
    h5_list : list
        list of full paths to H5 file(s).
    key_name : str
        default 'labels', the key to get the data from the H5 file
    """

    h5_list = make_list(h5_list, suppress_warning=True)
    if key_name is None:
        print_h5_keys(h5_list[0])
        return None
    for i, k in enumerate(h5_list):
        with h5py.File(k, 'r') as h:
            try:
                x = h[key_name][:]
            except:
                x = h[key_name]

            if i == 0:
                out = np.asarray(x)
            else:
                out = np.concatenate((out, x))
    return out


#
# def h5_to_U_array_contacts_transfer(c, h5_file, pred_array, replace_missing_data_with=-1, just_return_trial_inds=False):
#     """
#     note if you want the index instead use...
#     out = h5_to_U_array_contacts_transfer(c, h5_file, pred_array, replace_missing_data_with =-999)
#     index = out!=-999
#
#     Parameters
#     ----------
#     c : single cell from U array...
#         U_ARRAY = mat73.loadmat(U_file)
#         c = U_ARRAY[index_to_neuron]
#     h5_file :
#     pred_array : array matching (normally source from) h5_file that you will index out,
#     replace_missing_data_with : default -1, for any non overlapping data this value will be used instead
#
#     Returns
#     -------
#     w2h_labels
#     an array indexing out 'pred_array' that matches the Uarray format data
#
#     """
#     w_file_name_nums = image_tools.get_h5_key_and_concatenate(h5_file, 'file_name_nums')
#     # w_trials = np.unique(w_file_name_nums).astype(int)
#     indexes = np.unique(w_file_name_nums, return_index=True)[1]
#     w_trials = np.asarray([w_file_name_nums[index] for index in sorted(indexes)]).astype(int)
#
#     h_trials = c['meta']['usedTrialNums'].astype(int)
#     h_len_each = c['S_ctk'].shape[1]
#
#     wh_inds = []  # w-->h insert
#     for i, k in enumerate(h_trials):
#         if k in w_trials:
#             wh_inds.append(np.where(k == w_trials)[0][0])
#         else:
#             wh_inds.append(np.nan)
#
#     if just_return_trial_inds:
#         return wh_inds
#
#     w2h_labels = []
#     for k in wh_inds:
#         if not np.isnan(k):
#             w2h_labels.append(pred_array[k * h_len_each:(k + 1) * h_len_each])
#         else:
#             w2h_labels.append(np.ones(h_len_each) * replace_missing_data_with)
#     w2h_labels = np.concatenate(w2h_labels)
#     return w2h_labels
#


def Uarray_cell_labels_to_H5_file(c, h5):
    """
    I think this is the working version
    Parameters
    ----------
    c :
    h5 :

    Returns
    -------

    """
    full_file_names = h5_string_switcher(getkey(h5, 'full_file_names'))
    assert len(full_file_names) == len(np.unique(
        full_file_names)), 'your h5 file has duplicate video files that it processed, you will have to create a new H5 file and start over, sorry'
    w_trials_frames = getkey(h5, 'file_name_nums')
    w_trials = unique_keep_order(w_trials_frames)
    w_frame_nums = getkey(h5, 'frame_nums')

    h_frame_nums = [int(c['t'])] * int(c['k'])
    h_trials = c['meta']['usedTrialNums']
    S_ctk = np.asarray([tmp1.T.flatten() for tmp1 in c['S_ctk']])
    h_labels = np.nansum([S_ctk[10], S_ctk[13]], axis=0)
    try:
        ind_human_to_whacc_trials = intersect_data_with_nans(h_trials, w_trials, data=np.arange(
            len(h_trials)))  # this may need to be "h_trials" here not "w_trials"
    except:
        print(
            'i changed above code this is just in case it fails, you can change the above line "data=np.arange(len(h_trials))" to "data=np.arange(len(w_trials))"')
        assert False, 'see above printed message'

    matching_labels_for_whacc_h5 = []
    w_fn = np.asarray(loop_segments(w_frame_nums, 1))
    h_fn = np.asarray(loop_segments(h_frame_nums, 1))

    for i, k in enumerate(ind_human_to_whacc_trials):
        if not np.isnan(k):
            x = h_labels[h_fn[0, k]:h_fn[1, k]]
        else:
            x = np.ones(w_fn[1, i] - w_fn[0, i]) * -1
        matching_labels_for_whacc_h5.append(x)
    matching_labels_for_whacc_h5 = np.concatenate(matching_labels_for_whacc_h5)
    return matching_labels_for_whacc_h5


def h5_to_U_array_cell(c, h5, w_labels):
    if isinstance(w_labels, str):
        getkey(h5, w_labels)
    full_file_names = h5_string_switcher(getkey(h5, 'full_file_names'))
    assert len(full_file_names) == len(np.unique(
        full_file_names)), 'your h5 file has duplicate video files that it processed, you will have to create a new H5 file and start over, sorry'

    w_trials_frames = getkey(h5, 'file_name_nums')
    w_trials = unique_keep_order(w_trials_frames)
    w_frame_nums = getkey(h5, 'frame_nums')

    h_frame_nums = [int(c['t'])] * int(c['k'])
    h_trials = c['meta']['usedTrialNums']
    S_ctk = np.asarray([tmp1.T.flatten() for tmp1 in c['S_ctk']])
    # h_labels = np.nansum([S_ctk[10], S_ctk[13]], axis=0)

    ind_whacc_to_human_trials = intersect_data_with_nans(w_trials, h_trials, data=np.arange(len(w_trials)))

    matching_labels_for_cell = []
    w_fn = np.asarray(loop_segments(w_frame_nums, 1))
    h_fn = np.asarray(loop_segments(h_frame_nums, 1))

    for i, k in enumerate(ind_whacc_to_human_trials):
        if not np.isnan(k):
            x = w_labels[w_fn[0, k]:w_fn[1, k]]  # h_fn
        else:
            x = np.ones(h_fn[1, i] - h_fn[0, i]) * -1  # w_fn
        matching_labels_for_cell.append(x)
    matching_labels_for_cell = np.concatenate(matching_labels_for_cell)
    return matching_labels_for_cell


# def U_array_to_h5_contacts_transfer(c, h5_file, replace_missing_data_with=-1, just_return_trial_inds=False):
#     """
#     note if you want the index instead use...
#     out = U_array_to_h5_contacts_transfer(c, h5_file, replace_missing_data_with =-999)
#     index = out!=-999
#
#     Parameters
#     ----------
#     c : single cell from U array...
#         U_ARRAY = mat73.loadmat(U_file)
#         c = U_ARRAY[index_to_neuron]
#     h5_file :
#     replace_missing_data_with : default -1, for any non overlapping data this value will be used instead
#
#     Returns
#     -------
#     h2w_labels
#     an array indexing out human contacts from c (from the U) that matches the format of the H5 file
#
#     """
#     # w_frame_nums = image_tools.get_h5_key_and_concatenate(h5_file, 'frame_nums').astype(int)
#     w_file_name_nums = image_tools.get_h5_key_and_concatenate(h5_file, 'file_name_nums')
#     # w_trials = np.unique(w_file_name_nums).astype(int)
#     indexes = np.unique(w_file_name_nums, return_index=True)[1]
#     w_trials = np.asarray([w_file_name_nums[index] for index in sorted(indexes)]).astype(int)
#
#     h_trials = c['meta']['usedTrialNums'].astype(int)
#
#     hw_inds = []  # h-->w insert... human to whacc
#     for i, k in enumerate(w_trials):
#         if k in h_trials:
#             hw_inds.append(np.where(k == h_trials)[0][0])
#         else:
#             hw_inds.append(np.nan)
#     if just_return_trial_inds:
#         return hw_inds
#
#     h_labels = np.nan_to_num(c['S_ctk'][10]) + np.nan_to_num(c['S_ctk'][13])
#     h_labels[h_labels > 0] = 1
#     h_labels = h_labels.T.flatten()
#     h_len_each = c['S_ctk'].shape[1]
#
#     h2w_labels = []
#     for k in hw_inds:
#         if not np.isnan(k):
#             h2w_labels.append(h_labels[k * h_len_each:(k + 1) * h_len_each])
#         else:
#             h2w_labels.append(np.ones(h_len_each) * replace_missing_data_with)
#     h2w_labels = np.concatenate(h2w_labels)
#     return h2w_labels


def loop_segment_chunks(len_array, chunk_size):
    return loop_segments(chunk_segments(len_array, chunk_size))


def chunk_segments(len_array, chunk_size):
    out = [chunk_size] * (len_array // chunk_size)
    if len_array % chunk_size > 0:
        out.append(len_array % chunk_size)
    return out


def num_chunks(len_array, chunk_size):
    return len_array // chunk_size + 1 * (len_array % chunk_size > 0)


def cut_with_nans(x, inds, start_pad, end_pad=None):
    inds = np.asarray(make_list(inds, True)) + start_pad
    if end_pad is None:
        end_pad = start_pad
    x = np.concatenate((np.ones(start_pad) * np.nan, x, np.ones(end_pad) * np.nan))
    x_out = []
    for k in inds:
        i1 = np.max([0, k - start_pad])
        i2 = k + end_pad + 1
        x_out.append(x[i1:i2])
    return np.asarray(x_out)


def h5_string_switcher(list_in):
    list_in = make_list(list_in)
    print(type(list_in[0]))
    if 'bytes' in str(type(list_in[0])).lower():
        print('DECODE switching from bytes to string')
        out = [k.decode("ascii", "ignore") for k in list_in]
    elif type(list_in[0]) == str:
        print('ENCODE switching from string to bytes')
        out = [k.encode("ascii", "ignore") for k in list_in]
    else:
        print('not bytes or string format, returning input')
        return list_in
    return out


# def h5_string_switcher(list_in):
#     list_in = make_list(list_in)
#     if type(list_in[0]) == bytes:
#         print('DECODE switching from bytes to string')
#         out = [k.decode("ascii", "ignore") for k in list_in]
#     elif type(list_in[0]) == str:
#         print('ENCODE switching from string to bytes')
#         out = [k.encode("ascii", "ignore") for k in list_in]
#     else:
#         print('not bytes or string format, returning input')
#         return list_in
#     return out
def foo_predict_mods(mod_list, h5_list, chunk_size=10000, front_append='YHAT__', back_append=''):
    print("""WARNING THIS FUNCTION IS DEPRECIATED PLEASE JUST USE, 'predict_mods', CALLING 'predict_mods'""")
    predict_mods(mod_list, h5_list, chunk_size=chunk_size, front_append=front_append, back_append=back_append)

def predict_mods(mod_list, h5_list, chunk_size=10000, front_append='YHAT__', back_append=''):
    for mod_str in make_list(mod_list, True):
        mod = load_obj(mod_str)
        for h5 in make_list(h5_list, True):
            with h5py.File(h5, 'r') as h:
                yhat = []
                len_data = list(h['final_features_2105'].shape)[0]
                for i1, i2 in loop_segment_chunks(len_data, chunk_size):
                    fd = h['final_features_2105'][i1:i2]
                    yhat.append(mod.predict(fd))
            yhat = np.concatenate(yhat)
            write_key = front_append + os.path.basename(mod_str).split('.')[0] + back_append
            overwrite_h5_key(h5, write_key, yhat)


def foo_predict_v2(mod, h5_dir, write_key='temp_yhat', chunk_size=10000):
    for h5 in get_h5s(h5_dir):
        with h5py.File(h5, 'r') as h:
            yhat = []
            len_data = list(h['final_features_2105'].shape)[0]
            for i1, i2 in loop_segment_chunks(len_data, chunk_size):
                fd = h['final_features_2105'][i1:i2]
                yhat.append(mod.predict(fd))
            yhat = np.vstack(yhat)
            overwrite_h5_key(h5, write_key, yhat)


# def foo_predict(mod, h5_dir, write_key='temp_yhat'):
#     for h5 in get_h5s(h5_dir):
#         fd = image_tools.get_h5_key_and_concatenate(h5, 'final_features_2105')
#         yhat = mod.predict(fd)
#         overwrite_h5_key(h5, write_key, yhat)


def crop_image_from_top_left(im, crop_top_left, size_crop, inflation=1):
    """This is an accessory function to track to improve tracking speed. This crops the initial large image into a smaller one, based on the inflation rate.
        Inflation rate of 3 = 3 x 3 template image size around the first guessed pole location.

        Parameters
        ----------
        im :

        crop_top_left :

        size_crop :

        inflation :
             (Default value = 3)

        Returns
        -------

        """
    inflation_shift = np.floor((np.asarray(size_crop) * (inflation - 1)) / 2).astype(int)

    size_crop = np.asarray(size_crop) * inflation
    imshape = np.asarray(im.shape[:2])

    # adjust for inflation and make copies of origianl crop inds
    crop_top_left = crop_top_left - inflation_shift
    crop_top_left2 = crop_top_left.copy()
    crop_bottom_right = crop_top_left + np.asarray(size_crop)
    crop_bottom_right2 = crop_bottom_right.copy()

    # adjust crop in case of out of bounds
    crop_top_left[crop_top_left < 0] = 0
    crop_bottom_right[crop_bottom_right > imshape] = np.asarray(imshape)[crop_bottom_right > imshape]

    # for placing cropped image in random noise image tensor (we do this in case of out of bounds issues all outputs are the same size)
    TL_adj = crop_top_left - crop_top_left2

    c_cropped = im[crop_top_left[0]:crop_bottom_right[0], crop_top_left[1]:crop_bottom_right[1], ...].astype(
        'uint8')

    # make random noise image tensor
    crop_dim = list(c_cropped.shape)
    crop_dim[:2] = size_crop.tolist()
    cropped_image = np.random.randint(256, size=crop_dim).astype('uint8')

    if len(crop_dim) > 2:  # crop 3D or more
        cropped_image[TL_adj[0]:TL_adj[0] + c_cropped.shape[0], TL_adj[1]:TL_adj[1] + c_cropped.shape[1],
        ...] = c_cropped
    else:  # crop 2D
        cropped_image[TL_adj[0]:TL_adj[0] + c_cropped.shape[0],
        TL_adj[1]:TL_adj[1] + c_cropped.shape[1]] = c_cropped

    return cropped_image, crop_top_left2, crop_bottom_right2


def insert_images_into_feature_data_h5(h5, mp4_bd, image_key='images'):
    frame_nums = image_tools.get_h5_key_and_concatenate(h5, 'frame_nums')
    # max_val_stack = image_tools.get_h5_key_and_concatenate(h5, 'max_val_stack')
    locations_x_y = image_tools.get_h5_key_and_concatenate(h5, 'locations_x_y')
    template_img = image_tools.get_h5_key_and_concatenate(h5, 'template_img')
    img_size = list(template_img.shape[:2])
    mp4_list = [mp4_bd + os.sep + os.path.basename(k.decode("ascii", "ignore")) for k in
                image_tools.get_h5_key_and_concatenate(h5, 'full_file_names')]

    h5_creator = image_tools.h5_iterative_creator(h5,
                                                  overwrite_if_file_exists=False,
                                                  max_img_height=img_size[0],
                                                  max_img_width=img_size[1],
                                                  close_and_open_on_each_iteration=True,
                                                  color_channel=True,
                                                  add_to_existing_H5=True,
                                                  ignore_image_range_warning=False,
                                                  dtype_img=h5py.h5t.STD_U8BE,
                                                  dtype_labels=h5py.h5t.STD_I32LE,
                                                  image_key_name=image_key,
                                                  label_key_name='TRASH')

    del_h5_key(h5, h5_creator.img_key)
    del_h5_key(h5, h5_creator.label_key_name)
    del_h5_key(h5, 'multiplier')

    for i, (k1, k2) in enumerate(tqdm(loop_segments(frame_nums), total=len(frame_nums))):
        video_file = mp4_list[i]
        video = cv2.VideoCapture(video_file)
        tmp_location = locations_x_y[k1:k2]
        if (video.isOpened() == False):
            print('error opening video file')
        frame_numbers = int(video.get(7))
        images = []
        for fn in range(frame_numbers):
            video.set(cv2.CAP_PROP_POS_FRAMES, fn)
            success, og_frame = video.read()
            locations = tmp_location[fn]
            crop_img, crop_top_left2, crop_bottom_right2 = crop_image_from_top_left(og_frame,
                                                                                    [locations[1], locations[0]],
                                                                                    img_size)
            images.append(crop_img)
        images = np.asarray(images)
        h5_creator.add_to_h5(images, -1 * np.ones(images.shape[0]))


def clear_dir(dir_in):
    rmtree(dir_in)
    make_path(dir_in)


def rmtree(dir_in):
    if os.path.isdir(dir_in):
        shutil.rmtree(dir_in)


def norm_path(path_in, sep=None):
    add_start = ''
    if sep == None:
        sep = os.sep
    if path_in[0] == '/' or path_in[0] == '\\':
        add_start = sep
    tmp_list = '\\'.join([k for k in path_in.split('/') if len(k) > 0])
    final_list = [k for k in tmp_list.split('\\') if len(k) > 0]
    return add_start + sep.join(final_list)


def h5_to_dict(h5_in, exclude_keys=['final_features_2105', 'images', 'FD__original', 'CNN_pred']):
    """

    Parameters
    ----------
    h5_in :
    exclude_keys : by default excludes all the alrge data in the H5 file, set to "[]" to get the entire H5

    Returns
    -------

    """
    d = dict()
    if exclude_keys is None:
        exclude_keys = []
    with h5py.File(h5_in, 'r') as h:
        for k in h.keys():
            if k not in exclude_keys:
                d[k] = h[k][:]
    return d


def smooth(y, window, mode='same'):  # $%
    if window == 1:
        return y
    box = np.ones(window) / window
    y_smooth = np.convolve(y, box, mode=mode)
    return y_smooth
# def smooth_predictions(h5_list, window, ):
#     h5_list = make_list(h5_list, True)
#     for h5 in h5_list:


def make_path(name_in):
    Path(name_in).mkdir(parents=True, exist_ok=True)


def sort(x):
    return natsorted(x, alg=ns.FLOAT | ns.UNSIGNED)
    # return natsorted(x, alg=ns.REAL)


def split_list_inds(x, split_ratio):
    split_ratio = split_ratio / np.sum(split_ratio)
    L = len(x)
    mixed_inds = np.random.choice(L, L, replace=False)
    out = np.split(mixed_inds, np.ceil(L * np.cumsum(split_ratio[:-1])).astype('int'))
    return out


def split_list(x, split_ratio):
    inds = split_list_inds(x, split_ratio)
    out = []
    for k in inds:
        tmp1 = []
        for k2 in k:
            tmp1.append(x[k2])
        out.append(tmp1)
    return out


def make_final_predictions_GBM(h5_in_list, thresh=None, write_to_h5=True, overwrite_if_exists=False,
                               proba_key='yhat_proba', label_key='yhat', smooth_by=5):
    h5_in_list = make_list(h5_in_list)
    mod = model_maker.load_final_light_GBM()
    if thresh is None:
        thresh = 0.5
        # thresh = mod.FINAL_THRESHOLD_with_7_smooth
    for h5_in in h5_in_list:
        print(h5_in)
        tmp1 = h5_key_exists(h5_in, proba_key)
        tmp2 = h5_key_exists(h5_in, label_key)
        if not overwrite_if_exists:
            if tmp1 or tmp2:
                warnings.warn(
                    '\nKEY EXISTS NOT WRITTING FOR ' + h5_in + '\noverwrite_if_exists is FALSE\nproba_key exist --> ' + str(
                        tmp1) + '\nlabel_key exists --> ' + str(tmp2))
        with h5py.File(h5_in, 'r+') as h:
            x = image_tools.get_h5_key_and_concatenate(h5_in, 'final_features_2105')
            yhat = mod.predict(x)
            final_yhat = []
            for k1, k2 in loop_segments(h['frame_nums']):
                final_yhat.append(smooth(yhat[k1:k2], window=smooth_by))
            final_yhat = np.concatenate(final_yhat)
            if write_to_h5:
                overwrite_h5_key(h5_in, proba_key, final_yhat)
                overwrite_h5_key(h5_in, label_key, (final_yhat > thresh).astype(int))


def info(x):
    if isinstance(x, dict):
        print('type is dict')
        get_dict_info(x)
    elif isinstance(x, list):
        try:
            x = copy.deepcopy(np.asarray(x))
            print('type is list, converting a copy to numpy array to print this info')
            np_stats(x)
        except:
            print(
                "type is a list that can't be converted to a numpy array for printing info or maybe data format is not compatible")

    elif type(x).__module__ == np.__name__:
        print('type is np array')
        np_stats(x)
    else:
        try:
            print('type is ' + str(type(x)) + ' will try printing using "get_class_info2" ')
            get_class_info2(x)
        except:
            print('cant find out what to do with input of type')
            print(type(x))


def get_time_string(time_zone_string='America/Los_Angeles'):
    tz = pytz.timezone(time_zone_string)
    loc_dt = pytz.utc.localize(datetime.utcnow())
    current_time = loc_dt.astimezone(tz)
    todays_version = current_time.strftime("%Y_%m_%d_%H_%M_%S")
    return todays_version


def batch_process_videos_on_colab(bd, local_temp_dir, video_batch_size=2, RESNET_MODEL=None,
                                  copy_image_files_to_final_h5=True, copy_feature_data_to_final_h5=False,
                                  custom_image_extract_size=None, skip_if_FPS_is_not_int=True,
                                  skip_check_if_FPS_is_an_int=True):
    """
    use utils.make_mp4_list_dict to make lists of the mp4 files first, it can be run on the master directory and will index all folders with MP4 files
    Parameters
    ----------
    bd :
    local_temp_dir :
    video_batch_size :
    RESNET_MODEL :
    copy_image_files_to_final_h5 :
    copy_feature_data_to_final_h5 : copy the 2048 original feature data to the final H5, only needed for model testing and building
    custom_image_extract_size :

    Returns
    -------

    """

    time_str = get_time_string()
    bd_base_name = os.path.basename(os.path.normpath(bd))
    # load model once in the beginning
    if RESNET_MODEL is None:  # default ot the resnet model made with whacc
        RESNET_MODEL = model_maker.load_final_model()  # NOTE: there will be a warning since this likely isn't optimized for GPU, this is fine
    time_dict = {'num_files': [], 'time_copy_to_local': [], 'time_all': [], 'time_to_track': [], 'time_to_3lag': [],
                 'time_to_features': [], 'time_to_all_features': [], 'time_to_cut_features': []}
    time_df = None
    while True:  # keep going until there are no more files to process

        grab_file_list = True
        while grab_file_list:  # continuously look for files to run
            # get files that tell us which mp4s to process
            list_of_file_dicts = np.asarray(get_files(bd, '*file_list_for_batch_processing.pkl'))
            # sort it by the newest first since we we edit it each time (becoming the newest file)
            # this ensures we finished one set completely first
            inds = np.flip(np.argsort([os.path.getctime(k) for k in list_of_file_dicts]))
            list_of_file_dicts = list_of_file_dicts[inds]
            if len(list_of_file_dicts) == 0:
                print('FINISHED PROCESSING')
                return time_df
                # assert False, "FINISHED PROCESSING no more files to process"
            # load file dictionary
            file_dict = load_obj(list_of_file_dicts[0])
            # get base directory for current videos we are processing
            mp4_bd = os.path.dirname(list_of_file_dicts[0])

            if skip_if_FPS_is_not_int and not file_dict['bad_vids_have_been_moved']:
                # if np.any(file_dict['FPS_check_bad_vid_inds']):
                for bad_i, is_bad in enumerate(file_dict['FPS_check_bad_vid_inds']):
                    if is_bad:
                        x = mp4_bd + os.sep + os.path.basename(file_dict['mp4_names'][bad_i])
                        bad_mp4_dir = x.replace(bd_base_name, bd_base_name + '_BAD_MP4s')
                        Path(os.path.dirname(bad_mp4_dir)).mkdir(parents=True, exist_ok=True)
                        # x = os.sep + os.path.basename(file_dict['mp4_names'][bad_i])
                        shutil.move(x, bad_mp4_dir)
                        file_dict['is_processed'][bad_i] = True
                file_dict['bad_vids_have_been_moved'] = True

            # copy folder structure for the finished mp4s and predictions to go to
            copy_folder_structure(bd, os.path.normpath(bd) + '_FINISHED')
            # check if all the files have already been processes
            if np.all(file_dict['is_processed'] == True):
                x = list_of_file_dicts[0]  # copy instruction file with list of mp4s to final directory we are finished
                shutil.move(x, x.replace(bd_base_name, bd_base_name + '_FINISHED'))
                x = os.path.dirname(x) + os.sep + 'template_img.png'
                shutil.move(x, x.replace(bd_base_name, bd_base_name + '_FINISHED'))
            else:
                grab_file_list = False  # ready to run data
        start = time.time()
        time_list = [start]
        # overwrite local folder to copy files to
        if os.path.exists(local_temp_dir):
            shutil.rmtree(local_temp_dir)
        Path(local_temp_dir).mkdir(parents=True, exist_ok=True)
        # copy over mp4s and template image to local directory
        x = os.sep + 'template_img.png'
        template_dir = local_temp_dir + x
        shutil.copy(mp4_bd + x, template_dir)
        process_these_videos = np.where(file_dict['is_processed'] == False)[0][:video_batch_size]  # fix001 - make not
        # equal to True so that skip string can be in there
        for i in process_these_videos:
            x = os.sep + os.path.basename(file_dict['mp4_names'][i])
            shutil.copy(mp4_bd + x, local_temp_dir + x)
        time_list.append(time.time())  #
        # fix001 - delete the file here from the directory but save the name of it and the order it
        # track the mp4s for the pole images
        PT = PoleTracking(video_directory=local_temp_dir, template_png_full_name=template_dir,
                          custom_image_extract_size=custom_image_extract_size,
                          skip_check_if_FPS_is_an_int=skip_check_if_FPS_is_an_int)

        PT.track_all_and_save()
        time_list.append(time.time())
        # convert the images to '3lag' images
        #  h5_in = '/Users/phil/Desktop/temp_dir/AH0407x160609.h5'
        h5_in = PT.full_h5_name
        h5_3lag = h5_in.replace('.h5', '_3lag.h5')
        image_tools.convert_to_3lag(h5_in, h5_3lag)
        time_list.append(time.time())

        # convert to feature data
        # h5_3lag = '/Users/phil/Desktop/temp_dir/AH0407x160609_3lag.h5'
        h5_feature_data = h5_3lag.replace('.h5', '_feature_data.h5')
        in_gen = image_tools.ImageBatchGenerator(500, h5_3lag, label_key='labels')
        convert_h5_to_feature_h5(RESNET_MODEL, in_gen, h5_feature_data)
        time_list.append(time.time())

        # h5_feature_data = '/Users/phil/Desktop/temp_dir/AH0407x160609_3lag_feature_data.h5'
        # generate all the modified features (41*2048)+41 = 84,009

        # #######BELOW commented out
        # standard_feature_generation(h5_feature_data)
        # #######ABOVE commented out
        ######### standard_feature_generation2(h5_feature_data, write_final_to_h5 = True, delete_temp_h5 = True)
        ######### time_list.append(time.time())

        # # #######BELOW commented out
        # all_x = load_selected_features(h5_feature_data)
        # # #######ABOVE commented out
        # delete the big o' file
        file_nums = str(process_these_videos[0] + 1) + '_to_' + str(process_these_videos[-1] + 1) + '_of_' + str(
            len(file_dict['is_processed']))
        h5_final = h5_in.replace('.h5', '_final_to_combine_' + file_nums + '.h5')

        standard_feature_generation2(h5_feature_data, write_to_this_h5=h5_final, write_final_to_h5=True,
                                     delete_temp_h5=True)
        CNN_pred = image_tools.get_h5_key_and_concatenate(h5_feature_data, 'CNN_pred').flatten()
        overwrite_h5_key(h5_final, 'CNN_pred', CNN_pred)

        time_list.append(time.time())

        # print(h5_final)
        # with h5py.File(h5_final, 'w') as h:
        #     h['final_3095_features'] = all_x

        copy_over_all_non_image_keys(h5_in, h5_final)

        if copy_image_files_to_final_h5:
            images = image_tools.get_h5_key_and_concatenate(h5_3lag, 'images')
            overwrite_h5_key(h5_final, 'images', images)
            del images

        # delete 3lag don't it need anymore
        os.remove(h5_3lag)

        # then if you want you can copy the images too maybe just save as some sort of mp4 IDK
        ##### time_list.append(time.time())
        if copy_feature_data_to_final_h5:
            FD__original = image_tools.get_h5_key_and_concatenate(h5_feature_data, 'FD__original')
            overwrite_h5_key(h5_final, 'FD__original', FD__original)
            del FD__original
        os.remove(h5_feature_data)  #########################################removing for now but may want to keep?????
        x = os.path.dirname(list_of_file_dicts[0]) + os.sep
        dst = x.replace(bd_base_name, bd_base_name + '_FINISHED') + os.path.basename(h5_final)
        shutil.copy(h5_final, dst)

        for k in process_these_videos:  # save the dict file so that we know the video has been processed
            file_dict['is_processed'][k] = True
        save_obj(file_dict, list_of_file_dicts[0])

        # move the mp4s to the alt final dir
        for i in process_these_videos:
            x = mp4_bd + os.sep + os.path.basename(file_dict['mp4_names'][i])
            final_mp4_dir = x.replace(bd_base_name, bd_base_name + '_FINISHED_MP4s')
            Path(os.path.dirname(final_mp4_dir)).mkdir(parents=True, exist_ok=True)
            shutil.move(x, final_mp4_dir)
        time_list.append(time.time())

        time_array = np.diff(time_list)
        df_name_list = ['copy mp4s to local', 'track the pole', 'convert to 3lag', 'create feature data (CNN)',
                        'engineer all features', 'copy  h5 and mp4s to final destination',
                        'number of files']

        len_space = ' ' * max(len(k) + 4 for k in df_name_list)
        print('operation                                 total     per file')
        to_print = ''.join([(k2 + len_space)[:len(len_space)] + str(timedelta(seconds=k)).split(".")[
            0] + '   ' + str(timedelta(seconds=k3)).split(".")[0] + '\n' for k, k2, k3 in
                            zip(time_array, df_name_list, time_array / len(process_these_videos))])
        print(to_print)
        print('TOTAL                                     total     per file')
        print(len_space + str(timedelta(seconds=int(np.sum(time_array)))).split(".")[0] + '   ' +
              str(timedelta(seconds=np.sum(time_array) / len(process_these_videos))).split(".")[0])

        time_array = np.concatenate((time_array, [len(process_these_videos)]))
        if time_df is None:
            time_df = pd.DataFrame(time_array[None, :], columns=df_name_list)
        else:
            tmp_df = pd.DataFrame(time_array[None, :], columns=df_name_list)
            time_df = time_df.append(tmp_df, ignore_index=True)
        save_obj(time_df, os.path.normpath(bd) + '_FINISHED' + os.sep + 'time_df_' + time_str + '.pkl')


# def batch_process_videos_on_colab(bd, local_temp_dir, video_batch_size=30):
#     bd_base_name = os.path.basename(os.path.normpath(bd))
#     # load model once in the beginning
#     RESNET_MODEL = model_maker.load_final_model()  # NOTE: there will be a warning since this likely isn't optimized for GPU, this is fine
#     fd = load_feature_data()  # load feature data info
#     while True:  # once a   ll files are
#         time_list = []
#         start = time.time()
#         grab_file_list = True
#         while grab_file_list:  # continuously look for files to run
#             # get files that tell us which mp4s to process
#             list_of_file_dicts = np.asarray(get_files(bd, '*file_list_for_batch_processing.pkl'))
#             # sort it by the newest first since we we edit it each time (becoming the newest file)
#             # this ensures we finished one set completely first
#             inds = np.flip(np.argsort([os.path.getctime(k) for k in list_of_file_dicts]))
#             list_of_file_dicts = list_of_file_dicts[inds]
#             if len(list_of_file_dicts) == 0:
#                 print('FINISHED PROCESSING')
#                 assert False, "FINISHED PROCESSING no more files to process"
#             # load file dictionary
#             file_dict = load_obj(list_of_file_dicts[0])
#             # get base directory for current videos we are processing
#             mp4_bd = os.path.dirname(list_of_file_dicts[0])
#             # copy folder structure for the finished mp4s and predictions to go to
#             copy_folder_structure(bd, os.path.normpath(bd) + '_FINISHED')
#             # check if all the files have already been processes
#             if np.all(file_dict['is_processed'] == True):
#                 x = list_of_file_dicts[
#                     0]  # copy the instruction file with list of mp4s to final directory we are finished
#                 shutil.move(x, x.replace(bd_base_name, bd_base_name + '_FINISHED'))
#                 x = os.path.dirname(x) + os.sep + 'template_img.png'
#                 shutil.move(x, x.replace(bd_base_name, bd_base_name + '_FINISHED'))
#             else:
#                 grab_file_list = False  # ready to run data
#
#         # overwrite local folder to copy files to
#         if os.path.exists(local_temp_dir):
#             shutil.rmtree(local_temp_dir)
#         Path(local_temp_dir).mkdir(parents=True, exist_ok=True)
#         # copy over mp4s and template image to local directory
#         x = os.sep + 'template_img.png'
#         template_dir = local_temp_dir + x
#         shutil.copy(mp4_bd + x, template_dir)
#         process_these_videos = np.where(file_dict['is_processed'] == False)[0][:video_batch_size]
#         for i in process_these_videos:
#             x = os.sep + os.path.basename(file_dict['mp4_names'][i])
#             shutil.copy(mp4_bd + x, local_temp_dir + x)
#
#         # track the mp4s for the pole images
#         PT = PoleTracking(video_directory=local_temp_dir, template_png_full_name=template_dir)
#         PT.track_all_and_save()
#
#         # convert the images to '3lag' images
#         #  h5_in = '/Users/phil/Desktop/temp_dir/AH0407x160609.h5'
#         h5_in = PT.full_h5_name
#         h5_3lag = h5_in.replace('.h5', '_3lag.h5')
#         image_tools.convert_to_3lag(h5_in, h5_3lag)
#
#         # convert to feature data
#         # h5_3lag = '/Users/phil/Desktop/temp_dir/AH0407x160609_3lag.h5'
#         h5_feature_data = h5_3lag.replace('.h5', '_feature_data.h5')
#         in_gen = image_tools.ImageBatchGenerator(500, h5_3lag, label_key='labels')
#         convert_h5_to_feature_h5(RESNET_MODEL, in_gen, h5_feature_data)
#
#         # delete 3lag don't it need anymore
#         os.remove(h5_3lag)
#         # h5_feature_data = '/Users/phil/Desktop/temp_dir/AH0407x160609_3lag_feature_data.h5'
#         # generate all the modified features (41*2048)+41 = 84,009
#         standard_feature_generation(h5_feature_data)
#         all_x = load_selected_features(h5_feature_data)
#         # delete the big o' file
#         file_nums = str(process_these_videos[0] + 1) + '_to_' + str(process_these_videos[-1] + 1) + '_of_' + str(
#             len(file_dict['is_processed']))
#         h5_final = h5_in.replace('.h5', '_final_to_combine_' + file_nums + '.h5')
#         print(h5_final)
#         with h5py.File(h5_final, 'w') as h:
#             h['final_3095_features'] = all_x
#         copy_over_all_non_image_keys(h5_in, h5_final)
#         # then if you want you can copy the images too maybe just save as some sort of mp4 IDK
#         os.remove(h5_feature_data)
#         x = os.path.dirname(list_of_file_dicts[0]) + os.sep
#         dst = x.replace(bd_base_name, bd_base_name + '_FINISHED') + os.path.basename(h5_final)
#         shutil.copy(h5_final, dst)
#
#         for k in process_these_videos:  # save the dict file so that we know the video has been processed
#             file_dict['is_processed'][k] = True
#         save_obj(file_dict, list_of_file_dicts[0])
#
#         # move the mp4s to the final dir
#         for i in process_these_videos:
#             x = mp4_bd + os.sep + os.path.basename(file_dict['mp4_names'][i])
#             shutil.move(x, x.replace(bd_base_name, bd_base_name + '_FINISHED'))
#         time_list.append(time.time() - start)


def auto_combine_final_h5s(bd, delete_extra_files=True):
    """

    Parameters
    ----------
    bd : just put your base directory, it will automatically load the pkl file and check if all the videos are processed
    if that is the case it will combine them and by default
    delete_extra_files : delete the files after combining the final one.
    Returns
    -------

    """
    finished_sessions = get_files(bd, '*file_list_for_batch_processing.pkl')
    for f in finished_sessions:
        file_dict = load_obj(f)
        if np.all(file_dict['is_processed'] == True):
            h5_file_list_to_combine = sort(get_files(os.path.dirname(f), '*_final_to_combine_*'))
            if len(h5_file_list_to_combine) > 0:
                combine_final_h5s(h5_file_list_to_combine, delete_extra_files=delete_extra_files)


# def iterative_add_large_data_to_h5():


def combine_final_h5s(h5_file_list_to_combine, delete_extra_files=False):
    h5_file_list_to_combine = sort(h5_file_list_to_combine)
    fn = h5_file_list_to_combine[0].split('final')[0] + 'final_combined.h5'
    h5c = image_tools.h5_iterative_creator(fn,
                                           overwrite_if_file_exists=True,
                                           max_img_height=1,
                                           max_img_width=2105,
                                           close_and_open_on_each_iteration=True,
                                           color_channel=False,
                                           add_to_existing_H5=False,
                                           ignore_image_range_warning=False,
                                           dtype_img=h5py.h5t.IEEE_F32LE,
                                           dtype_labels=h5py.h5t.IEEE_F32LE,
                                           image_key_name='final_features_2105')

    for k in tqdm(h5_file_list_to_combine):
        with h5py.File(k, 'r') as h:
            final_features_2105 = h['final_features_2105'][:]
            h5c.add_to_h5(final_features_2105, np.ones(final_features_2105.shape[0]) * -1)

    with h5py.File(fn, 'r+') as h:
        del h['labels']
        if h5_key_exists(h5_file_list_to_combine[0], 'images'):
            for i, k in enumerate(tqdm(h5_file_list_to_combine)):
                images = image_tools.get_h5_key_and_concatenate(k, 'images')
                if i == 0:
                    max_shape = list(images.shape)
                    max_shape[0] = None

                    h.create_dataset('images',
                                     np.shape(images),
                                     h5py.h5t.STD_U8BE,
                                     maxshape=max_shape,
                                     chunks=True,
                                     data=images)
                else:
                    h['images'].resize(h['images'].shape[0] + images.shape[0], axis=0)
                    h['images'][-images.shape[0]:] = images

        if h5_key_exists(h5_file_list_to_combine[0], 'FD__original'):
            for i, k in enumerate(tqdm(h5_file_list_to_combine)):
                FD__original = image_tools.get_h5_key_and_concatenate(k, 'FD__original')
                if i == 0:
                    max_shape = list(FD__original.shape)
                    max_shape[0] = None

                    h.create_dataset('FD__original',
                                     np.shape(FD__original),
                                     h5py.h5t.STD_U8BE,
                                     maxshape=max_shape,
                                     chunks=True,
                                     data=FD__original)
                else:
                    h['FD__original'].resize(h['FD__original'].shape[0] + FD__original.shape[0], axis=0)
                    h['FD__original'][-FD__original.shape[0]:] = FD__original

    keys = ['file_name_nums', 'frame_nums', 'full_file_names', 'in_range', 'labels',
            'locations_x_y', 'max_val_stack', 'CNN_pred', 'custom_image_extract_size']
    trial_nums_and_frame_nums = []
    for k in h5_file_list_to_combine:
        trial_nums_and_frame_nums.append(image_tools.get_h5_key_and_concatenate(str(k), 'trial_nums_and_frame_nums'))
    trial_nums_and_frame_nums = np.hstack(trial_nums_and_frame_nums)
    overwrite_h5_key(fn, 'trial_nums_and_frame_nums', trial_nums_and_frame_nums)

    with h5py.File(fn, 'r+') as h:
        for k in tqdm(keys):
            if h5_key_exists(h5_file_list_to_combine[0], k):
                out = image_tools.get_h5_key_and_concatenate(h5_file_list_to_combine, k)
                if k == 'full_file_names':
                    out = list(out)
                h[k] = out

    overwrite_h5_key(fn, 'template_img',
                     image_tools.get_h5_key_and_concatenate(h5_file_list_to_combine[0], 'template_img'))
    overwrite_h5_key(fn, 'multiplier', image_tools.get_h5_key_and_concatenate(h5_file_list_to_combine[0], 'multiplier'))

    if delete_extra_files:
        for k in h5_file_list_to_combine:
            os.remove(k)


# def combine_final_h5s(h5_file_list_to_combine, delete_extra_files=False):
#     keys = ['file_name_nums', 'final_features_2105', 'frame_nums', 'full_file_names', 'in_range', 'labels',
#             'locations_x_y', 'max_val_stack']
#     fn = h5_file_list_to_combine[0].split('final')[0] + 'final_combined.h5'
#     trial_nums_and_frame_nums = []
#     for k in h5_file_list_to_combine:
#         trial_nums_and_frame_nums.append(image_tools.get_h5_key_and_concatenate(k, 'trial_nums_and_frame_nums'))
#     trial_nums_and_frame_nums = np.hstack(trial_nums_and_frame_nums)
#
#     with h5py.File(fn, 'w') as h:
#         for k in keys:
#             print(k)
#             out = image_tools.get_h5_key_and_concatenate(h5_file_list_to_combine, k)
#             h[k] = out
#         h['template_img'] = image_tools.get_h5_key_and_concatenate(h5_file_list_to_combine[0], 'template_img')
#         h['multiplier'] = image_tools.get_h5_key_and_concatenate(h5_file_list_to_combine[0], 'multiplier')
#         h['trial_nums_and_frame_nums'] = trial_nums_and_frame_nums
#     if delete_extra_files:
#         for k in h5_file_list_to_combine:
#             os.remove(k)


# def make_mp4_list_dict(video_directory, overwrite=False):
#     video_directory.replace('\\', '/')
#     fn = video_directory + '/' + 'file_list_for_batch_processing.pkl'
#
#     if os.path.isfile(fn) and not overwrite:
#         warnings.warn("warning file already exists! if you overwrite a partially processed directory, you will " \
#                       "experience issues like overwrite errors, and you'll lose your progress. if you are sure you want to overwrite " \
#                       "make sure to delete the corresponding '_FINISHED' directory, and if necessary move the mp4s back " \
#                       "to the processing folder and set overwrite = True")
#         warnings.warn("this above message is in reference to the following directory...\n" + video_directory)
#         print(video_directory)
#
#     else:
#         tmpd = dict()
#         tmpd['original_mp4_directory'] = video_directory
#         tmpd['mp4_names'] = natsorted(glob.glob(video_directory + '/*.mp4'))
#         tmpd['is_processed'] = np.full(np.shape(tmpd['mp4_names']), False)
#         tmpd['NOTES'] = """you can put any notes here directly from the text file if you want to"""
#         tmpd['mp4_names'] = [k.replace('\\', '/') for k in tmpd['mp4_names']]
#         save_obj(tmpd, fn)

def make_mp4_list_dict(video_directory, overwrite=False, time_sleep_between_delete_for_cloud_update=0):
    """

    Parameters
    ----------
    video_directory :  will look in all sub directoriess recurivly
    overwrite : if True will delete file if exists
    time_sleep_between_delete_for_cloud_update : hacky solution to google drive cache issue where the modified data time
    does not update without a time buffer after being delete. only relivent for if you are overwriting existing files, I
    know 30 seconds works here, annoying but not that big of a deal at the end of the day

    Returns
    -------

    """

    video_directory.replace('\\', '/')
    fn = video_directory + '/' + 'file_list_for_batch_processing.pkl'
    # buffer_remove_fn = video_directory + '/trash.pkl'
    if os.path.isfile(fn) and not overwrite:
        warnings.warn("warning file already exists! if you overwrite a partially processed directory, you will " \
                      "experience issues like overwrite errors, and you'll lose your progress. if you are sure you want to overwrite " \
                      "make sure to delete the corresponding '_FINISHED' directory, and if necessary move the mp4s back " \
                      "to the processing folder and set overwrite = True")
        warnings.warn("this above message is in reference to the following directory...\n" + video_directory)
        print(video_directory)

    else:
        if os.path.isfile(fn):
            os.remove(fn)
            time.sleep(time_sleep_between_delete_for_cloud_update)
        tmpd = dict()
        tmpd['original_mp4_directory'] = video_directory
        tmpd['mp4_names'] = sort(glob.glob(video_directory + '/*.mp4'))
        tmpd['is_processed'] = np.full(np.shape(tmpd['mp4_names']), False)
        tmpd['NOTES'] = """you can put any notes here directly from the text file if you want to"""
        print('Performing initial check to see if some MP4s are "bad" by testing if FPS is an int')
        tmpd['FPS_check_bad_vid_inds'] = check_vids_for_issues_based_on_FPS_as_an_int(tmpd['mp4_names'])
        tmpd['bad_vids_have_been_moved'] = False
        tmpd['mp4_names'] = [k.replace('\\', '/') for k in tmpd['mp4_names']]

        save_obj(tmpd, fn)


def _check_pkl(name):
    if name[-4:] != '.pkl':
        return name + '.pkl'
    return name


def save_obj(obj, name):
    with open(_check_pkl(name), 'wb') as f:
        # pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
        pickle.dump(obj, f, protocol=4)


def load_obj(name):
    with open(_check_pkl(name), 'rb') as f:
        return pickle.load(f)


def get_whacc_path():
    path = os.path.dirname(whacc.__file__)
    return path


def load_feature_data():
    x = get_whacc_path() + "/whacc_data/feature_data/"
    d = load_obj(x + 'feature_data_dict.pkl')
    d['final_selected_features'] = np.where(d['final_selected_features_bool'])[0]
    return d


def load_nan_border_index():
    x = get_whacc_path() + "/whacc_data/feature_data/"
    array_out = load_obj(x + 'start_end_nan_locations.pkl')
    return array_out


# def load_top_feature_selection_out_of_ten():
#     fn = get_whacc_path() + "/whacc_data/features_used_in_light_GBM_mods_out_of_10.npy"
#     return np.load(fn)

def get_selected_features(greater_than_or_equal_to=4):
    '''
    Parameters
    ----------
    greater_than_or_equal_to : 0 means select all features, 10 means only the features that were use in EVERY test
    light GBM model. Note: the save Light GBM (model) is trained on greater_than_or_equal_to = 4, so you can change this
    but you will need to retrain the light GBM (model).
    Returns keep_features_index : index to the giant '84,009' features, note greater_than_or_equal_to = 4 return 3095
    features
    -------
    '''

    fd = load_feature_data()
    features_out_of_10 = fd['features_used_of_10']

    keep_features_index = np.where(features_out_of_10 >= greater_than_or_equal_to)[0]

    features_used_of_10_bool = [True if k in x else False for k in range(2048 * 41 + 41)]
    return keep_features_index


def isnotebook():
    try:
        c = str(get_ipython().__class__)
        shell = get_ipython().__class__.__name__
        if 'colab' in c:
            return True
        elif shell == 'ZMQInteractiveShell':
            return True  # Jupyter notebook or qtconsole
        elif shell == 'TerminalInteractiveShell':
            return False  # Terminal running IPython
        else:
            return False  # Other type (?)
    except NameError:
        return False  # Probably standard Python interpreter


# if tqdm_import_helper():
#     from tqdm.notebook import tqdm
# else:
#     from tqdm import tqdm


def four_class_labels_from_binary(x):
    a = np.asarray(x)
    b = np.asarray([0] + list(np.diff(a)))
    c = a + b
    c[c == -1] = 3
    return c


def print_h5_keys(h5file, return_list=False, do_print=True):
    with h5py.File(h5file, 'r') as h:
        x = copy.deepcopy(list(h.keys()))
        if do_print:
            print_list_with_inds(x)
        if return_list:
            return x


def copy_h5_key_to_another_h5(h5_to_copy_from, h5_to_copy_to, label_string_to_copy_from, label_string_to_copy_to=None):
    if label_string_to_copy_to is None:
        label_string_to_copy_to = label_string_to_copy_from
    with h5py.File(h5_to_copy_from, 'r') as h:
        with h5py.File(h5_to_copy_to, 'r+') as h2:
            try:
                h2[label_string_to_copy_to][:] = h[label_string_to_copy_from][:]
            except:
                h2.create_dataset(label_string_to_copy_to, shape=np.shape(h[label_string_to_copy_from][:]),
                                  data=h[label_string_to_copy_from][:])


def lister_it(in_list, keep_strings='', remove_string=None, return_bool_index=False) -> object:
    if len(in_list) == 0:
        print("in_list was empty, returning in_list")
        return in_list

    def index_list_of_strings(in_list2, cmp_string):
        return np.asarray([cmp_string in string for string in in_list2])

    if isinstance(keep_strings, str): keep_strings = [keep_strings]
    if isinstance(remove_string, str): remove_string = [remove_string]

    keep_i = np.asarray([False] * len(in_list))
    for k in keep_strings:
        keep_i = np.vstack((keep_i, index_list_of_strings(in_list, k)))
    keep_i = np.sum(keep_i, axis=0) > 0

    remove_i = np.asarray([True] * len(in_list))
    if remove_string is not None:
        for k in remove_string:
            remove_i = np.vstack((remove_i, np.invert(index_list_of_strings(in_list, k))))
        remove_i = np.product(remove_i, axis=0) > 0

    inds = keep_i * remove_i  # np.invert(remove_i)
    if inds.size <= 0:
        return []
    else:
        out = np.asarray(in_list)[inds]
        if return_bool_index:
            return out, inds
    return out


# def lister_it(in_list, keep_strings=None, remove_string=None):
#     """
#
#     Parameters
#     ----------
#     in_list : list
#     keep_strings : list
#     remove_string : list
#
#     Returns
#     -------
#
#     """
#     if isinstance(keep_strings, str):
#         keep_strings = [keep_strings]
#     if isinstance(remove_string, str):
#         remove_string = [remove_string]
#
#     if keep_strings is None:
#         new_list = copy.deepcopy(in_list)
#     else:
#         new_list = []
#         for L in in_list:
#             for k in keep_strings:
#                 if k in L:
#                     new_list.append(L)
#
#     if remove_string is None:
#         new_list_2 = copy.deepcopy(in_list)
#     else:
#         new_list_2 = []
#         for L in new_list:
#             for k in remove_string:
#                 if k not in L:
#                     new_list_2.append(L)
#     final_list = intersect_lists([new_list_2, new_list])
#     return final_list


def plot_pole_tracking_max_vals(h5_file):
    with h5py.File(h5_file, 'r') as hf:
        for i, k in enumerate(hf['max_val_stack'][:]):
            plt.plot(i, k)


# def get_class_info(c, sort_by_type=True, include_underscore_vars=False, return_name_and_type=False, end_prev_len=40):
#     names = []
#     type_to_print = []
#     for k in dir(c):
#         if include_underscore_vars is False and k[0] != '_':
#             tmp1 = str(type(eval('c.' + k)))
#             type_to_print.append(tmp1.split("""'""")[-2])
#             names.append(k)
#         elif include_underscore_vars:
#             tmp1 = str(type(eval('c.' + k)))
#             type_to_print.append(tmp1.split("""'""")[-2])
#             names.append(k)
#     len_space = ' ' * max(len(k) for k in names)
#     len_space_type = ' ' * max(len(k) for k in type_to_print)
#     if sort_by_type:
#         ind_array = np.argsort(type_to_print)
#     else:
#         ind_array = np.argsort(names)
#
#     for i in ind_array:
#         k1 = names[i]
#         k2 = type_to_print[i]
#         # k3 = str(c[names[i]])
#         k3 = str(eval('c.' + names[i]))
#         k1 = (k1 + len_space)[:len(len_space)]
#         k2 = (k2 + len_space_type)[:len(len_space_type)]
#         if len(k3) > end_prev_len:
#             k3 = '...' + k3[-end_prev_len:]
#         else:
#             k3 = '> ' + k3[-end_prev_len:]
#
#         print(k1 + ' type->   ' + k2 + '  ' + k3)
#     if return_name_and_type:
#         return names, type_to_print

def get_class_info2(c, sort_by=None, include_underscore_vars=False, return_name_and_type=False, end_prev_len=40):
    def get_len_or_shape(x_in):
        which_one = None
        try:
            len_or_shape_out = str(len(x_in))
            which_one = 'length'
            if type(x_in).__module__ == np.__name__:
                len_or_shape_out = str(x_in.shape)
                which_one = 'shape '
        except:
            if which_one is None:
                len_or_shape_out = 'None'
                which_one = 'None  '
        return len_or_shape_out, which_one

    names = []
    len_or_shape = []
    len_or_shape_which_one = []
    type_to_print = []

    for k in dir(c):
        if include_underscore_vars is False and k[0] != '_':

            tmp1 = str(type(eval('c.' + k)))
            type_to_print.append(tmp1.split("""'""")[-2])
            names.append(k)
            a, b = get_len_or_shape(eval('c.' + names[-1]))
            len_or_shape.append(a)
            len_or_shape_which_one.append(b)
        elif include_underscore_vars:
            tmp1 = str(type(eval('c.' + k)))
            type_to_print.append(tmp1.split("""'""")[-2])
            names.append(k)
            a, b = get_len_or_shape(eval('c.' + names[-1]))
            len_or_shape.append(a)
            len_or_shape_which_one.append(b)
    len_space = ' ' * max(len(k) for k in names)
    len_space_type = ' ' * max(len(k) for k in type_to_print)
    len_space_shape = ' ' * max(len(k) for k in len_or_shape)
    if sort_by is None:
        ind_array = np.arange(len(names))
    elif 'type' in sort_by.lower():
        ind_array = np.argsort(type_to_print)
    elif 'len' in sort_by.lower() or 'shape' in sort_by.lower():
        np.warnings.filterwarnings('ignore', category=np.VisibleDeprecationWarning)
        tmp1 = np.asarray([eval(k) for k in len_or_shape])
        tmp1[tmp1 == None] = np.nan
        tmp1 = [np.max(iii) for iii in tmp1]
        ind_array = np.argsort(tmp1)
    elif 'name' in sort_by.lower():
        ind_array = np.argsort(names)
    else:
        ind_array = np.arange(len(names))

    for i in ind_array:
        k1 = names[i]
        k2 = type_to_print[i]
        k5 = len_or_shape[i]
        x = eval('c.' + names[i])
        k3 = str(x)
        k1 = (k1 + len_space)[:len(len_space)]
        k2 = (k2 + len_space_type)[:len(len_space_type)]
        k5 = (k5 + len_space_shape)[:len(len_space_shape)]
        if len(k3) > end_prev_len:
            k3 = '...' + k3[-end_prev_len:]
        else:
            k3 = '> ' + k3[-end_prev_len:]
        print(k1 + ' type->   ' + k2 + '  ' + len_or_shape_which_one[i] + '->   ' + k5 + '  ' + k3)
    if return_name_and_type:
        return names, type_to_print


def get_class_info(c, sort_by_type=True, include_underscore_vars=False, return_name_and_type=False, end_prev_len=40):
    def get_len_or_shape(x_in):
        which_one = None
        try:
            len_or_shape_out = str(len(x_in))
            which_one = 'length'
            if type(x_in).__module__ == np.__name__:
                len_or_shape_out = str(x_in.shape)
                which_one = 'shape '
        except:
            if which_one is None:
                len_or_shape_out = 'None'
                which_one = 'None  '
        return len_or_shape_out, which_one

    names = []
    len_or_shape = []
    len_or_shape_which_one = []
    type_to_print = []

    for k in dir(c):
        if include_underscore_vars is False and k[0] != '_':

            tmp1 = str(type(eval('c.' + k)))
            type_to_print.append(tmp1.split("""'""")[-2])
            names.append(k)
            a, b = get_len_or_shape(eval('c.' + names[-1]))
            len_or_shape.append(a)
            len_or_shape_which_one.append(b)
        elif include_underscore_vars:
            tmp1 = str(type(eval('c.' + k)))
            type_to_print.append(tmp1.split("""'""")[-2])
            names.append(k)
            a, b = get_len_or_shape(eval('c.' + names[-1]))
            len_or_shape.append(a)
            len_or_shape_which_one.append(b)
    len_space = ' ' * max(len(k) for k in names)
    len_space_type = ' ' * max(len(k) for k in type_to_print)
    len_space_shape = ' ' * max(len(k) for k in len_or_shape)
    if sort_by_type:
        ind_array = np.argsort(type_to_print)
    else:
        ind_array = np.argsort(names)

    for i in ind_array:
        k1 = names[i]
        k2 = type_to_print[i]
        k5 = len_or_shape[i]
        x = eval('c.' + names[i])
        k3 = str(x)
        k1 = (k1 + len_space)[:len(len_space)]
        k2 = (k2 + len_space_type)[:len(len_space_type)]
        k5 = (k5 + len_space_shape)[:len(len_space_shape)]
        if len(k3) > end_prev_len:
            k3 = '...' + k3[-end_prev_len:]
        else:
            k3 = '> ' + k3[-end_prev_len:]
        print(k1 + ' type->   ' + k2 + '  ' + len_or_shape_which_one[i] + '->   ' + k5 + '  ' + k3)
    if return_name_and_type:
        return names, type_to_print


def get_dict_info(c, sort_by_type=True, include_underscore_vars=False, return_name_and_type=False, end_prev_len=40):
    names = []
    type_to_print = []
    for k in c.keys():
        if include_underscore_vars is False and str(k)[0] != '_':
            tmp1 = str(type(c[k]))
            type_to_print.append(tmp1.split("""'""")[-2])
            names.append(str(k))
        elif include_underscore_vars:
            tmp1 = str(type(c[k]))
            type_to_print.append(tmp1.split("""'""")[-2])
            names.append(str(k))
    len_space = ' ' * max(len(k) for k in names)
    len_space_type = ' ' * max(len(k) for k in type_to_print)
    if sort_by_type:
        ind_array = np.argsort(type_to_print)
    else:
        ind_array = np.argsort(names)

    for i in ind_array:
        k1 = names[i]
        k2 = type_to_print[i]
        try:
            k3 = str(c[names[i]])
        except:
            k3 = str(c[float(names[i])])
        k1 = (k1 + len_space)[:len(len_space)]
        k2 = (k2 + len_space_type)[:len(len_space_type)]

        if len(k3) > end_prev_len:
            k3 = '...' + k3[-end_prev_len:]
        else:
            k3 = '> ' + k3[-end_prev_len:]

        if 'numpy.ndarray' in k2:
            k4 = str(c[names[i]].shape)
            k4_str = '   shape-> '
        else:
            try:
                k4 = str(len(c[names[i]]))
                k4_str = '   len-> '
            except:
                k4_str = '   None->'
                k4 = 'None'

        print(k1 + ' type->   ' + k2 + k4_str + k4 + '  ' + k3)
    if return_name_and_type:
        return names, type_to_print


# def get_dict_info(c, sort_by_type=True, include_underscore_vars=False, return_name_and_type=False, end_prev_len=40):
#     names = []
#     type_to_print = []
#     for k in c.keys():
#         if include_underscore_vars is False and str(k)[0] != '_':
#             tmp1 = str(type(c[k]))
#             type_to_print.append(tmp1.split("""'""")[-2])
#             names.append(str(k))
#         elif include_underscore_vars:
#             tmp1 = str(type(c[k]))
#             type_to_print.append(tmp1.split("""'""")[-2])
#             names.append(str(k))
#     len_space = ' ' * max(len(k) for k in names)
#     len_space_type = ' ' * max(len(k) for k in type_to_print)
#     if sort_by_type:
#         ind_array = np.argsort(type_to_print)
#     else:
#         ind_array = np.argsort(names)
#
#     for i in ind_array:
#         k1 = names[i]
#         k2 = type_to_print[i]
#         try:
#             k3 = str(c[names[i]])
#         except:
#             k3 = str(c[float(names[i])])
#         k1 = (k1 + len_space)[:len(len_space)]
#         k2 = (k2 + len_space_type)[:len(len_space_type)]
#
#         if len(k3) > end_prev_len:
#             k3 = '...' + k3[-end_prev_len:]
#         else:
#             k3 = '> ' + k3[-end_prev_len:]
#
#
#
#         print(k1 + ' type->   ' + k2 + '  ' + k3)
#     if return_name_and_type:
#         return names, type_to_print


def group_consecutives(vals, step=1):  # row # find_in_a_row # putting this here for searching
    """

    Parameters
    ----------
    vals :
        
    step :
         (Default value = 1)

    Returns
    -------

    """
    run = []
    run_ind = []
    result = run
    result_ind = run_ind
    expect = None
    for k, v in enumerate(vals):
        if v == expect:
            if not (np.isnan(v)):
                # print(v)
                # print(expect)
                run.append(v)
                run_ind.append(k)
        else:
            if not (np.isnan(v)):
                run = [v]
                run_ind = [k]
                result.append(run)
                result_ind.append(run_ind)
        expect = v + step
    # print(result)
    if result == []:
        pass
    elif result[0] == []:
        result = result[1:]
        result_ind = result_ind[1:]
    return result, result_ind


def get_h5s(base_dir, print_h5_list=True):
    """

    Parameters
    ----------
    base_dir :
        

    Returns
    -------

    """
    H5_file_list = []
    for path in Path(base_dir + os.path.sep).rglob('*.h5'):
        H5_file_list.append(str(path.parent) + os.path.sep + path.name)
    H5_file_list.sort()
    if print_h5_list:
        print_list_with_inds(H5_file_list)
    return H5_file_list


def check_if_file_lists_match(H5_list_LAB, H5_list_IMG):
    """

    Parameters
    ----------
    H5_list_LAB :
        
    H5_list_IMG :
        

    Returns
    -------

    """
    for h5_LAB, h5_IMG in zip(H5_list_LAB, H5_list_IMG):
        try:
            assert h5_IMG.split(os.path.sep)[-1] in h5_LAB
        except:
            print('DO NOT CONTINUE --- some files do not match on your lists try again')
            assert (1 == 0)
    print('yay they all match!')


def print_list_with_inds(list_in):
    """

    Parameters
    ----------
    list_in :
        

    Returns
    -------

    """
    _ = [print(str(i) + ' ' + k.split(os.path.sep)[-1]) for i, k in enumerate(list_in)]


def get_model_list(model_save_dir):
    """

    Parameters
    ----------
    model_save_dir :
        

    Returns
    -------

    """
    print('These are all the models to choose from...')
    model_2_load_all = glob.glob(model_save_dir + '/*.ckpt')
    print_list_with_inds(model_2_load_all)
    return model_2_load_all


def recursive_dir_finder(base_path, search_term):
    """enter base directory and search term to find all the directories in base directory
      with files matching the search_term. output a sorted list of directories.
      e.g. -> recursive_dir_finder('/content/mydropbox/', '*.mp4')

    Parameters
    ----------
    base_path :
        
    search_term :
        

    Returns
    -------

    """
    matching_folders = []
    for root, dirs, files in os.walk(base_path):
        if glob.glob(root + '/' + search_term):
            matching_folders.append(root)
    try:
        matching_folders = natsorted(matching_folders)
    except:
        matching_folders = sorted(matching_folders)
    return matching_folders


def get_model_list(model_save_dir):
    """

    Parameters
    ----------
    model_save_dir :
        

    Returns
    -------

    """
    print('These are all the models to choose from...')
    model_2_load_all = sorted(glob.glob(model_save_dir + '/*.ckpt'))
    # print(*model_2_load_all, sep = '\n')
    _ = [print(str(i) + ' ' + k.split(os.path.sep)[-1]) for i, k in enumerate(model_2_load_all)]
    return model_2_load_all


def get_files(base_dir, search_term=''):
    """
base_dir = '/content/gdrive/My Drive/LIGHT_GBM/FEATURE_DATA/'
num_folders_deep = 1
file_list = []
for i, path in enumerate(Path(base_dir + os.sep).rglob('')):
  x = str(path.parent) + os.path.sep + path.name
  if i ==0:
    file_list.append(x)
    cnt = len(x.split(os.sep))
  if (len(x.split(os.sep))-cnt)<=num_folders_deep:
    file_list.append(x)
list(set(file_list))

    Parameters
    ----------
    base_dir :
        
    search_term :

    Returns
    -------

    """
    file_list = []
    for path in Path(base_dir + os.sep).rglob(search_term):
        ##### can I edit this with default depth of one and only look x num folders deep to prevent long searchs in main folders?
        file_list.append(str(path.parent) + os.path.sep + path.name)
    file_list.sort()
    return file_list


'''
these below 3 function used to load mat files into dict easily was found and copied directly from 
https://stackoverflow.com/questions/7008608/scipy-io-loadmat-nested-structures-i-e-dictionaries
and contributed by user -mergen 

to the best of my knowledge code found on stackoverflow is under the creative commons license and as such is legal to 
use in my package. contact phillip.maire@gmail.com if you have any questions. 
'''


def loadmat(filename):
    """this function should be called instead of direct spio.loadmat
    as it cures the problem of not properly recovering python dictionaries
    from mat files. It calls the function check keys to cure all entries
    which are still mat-objects

    if this doesnt work try this
    import mat73
    from whacc import utils
    mat_file = '/Users/phil/Dropbox/U_191028_1154.mat'
    data_dict = mat73.loadmat(mat_file)

    Parameters
    ----------
    filename :
        

    Returns
    -------

    """
    data = spio.loadmat(filename, struct_as_record=False, squeeze_me=True)
    return _check_keys(data)


def _check_keys(dict):
    """checks if entries in dictionary are mat-objects. If yes
    todict is called to change them to nested dictionaries

    Parameters
    ----------
    dict :
        

    Returns
    -------

    """
    for key in dict:
        if isinstance(dict[key], spio.matlab.mio5_params.mat_struct):
            dict[key] = _todict(dict[key])
    return dict


def _todict(matobj):
    """A recursive function which constructs from matobjects nested dictionaries

    Parameters
    ----------
    matobj :
        

    Returns
    -------

    """
    dict = {}
    for strg in matobj._fieldnames:
        elem = matobj.__dict__[strg]
        if isinstance(elem, spio.matlab.mio5_params.mat_struct):
            dict[strg] = _todict(elem)
        else:
            dict[strg] = elem
    return dict


def get_inds_of_inds(a, return_unique_list=False):
    a2 = []
    for k in a:
        a2.append(list(np.where([k == kk for kk in a])[0]))
    try:
        inds_of_inds = list(np.unique(a2, axis=0))
        for i, k in enumerate(inds_of_inds):
            inds_of_inds[i] = list(k)
    except:
        inds_of_inds = list(np.unique(a2))
    if return_unique_list:
        return inds_of_inds, pd.unique(a)
    else:
        return inds_of_inds


def inds_around_inds(x, N):
    """

    Parameters
    ----------
    x : array
    N : window size

    Returns
    -------
    returns indices of arrays where array >0 with borders of ((N - 1) / 2), so x = [0, 0, 0, 1, 0, 0, 0] and N = 3
    returns [2, 3, 4]
    """
    assert N / 2 != round(N / 2), 'N must be an odd number so that there are equal number of points on each side'
    cumsum = np.cumsum(np.insert(x, 0, 0))
    a = (cumsum[N:] - cumsum[:-N]) / float(N)
    a = np.where(a > 0)[0] + ((N - 1) / 2)
    return a.astype('int')


def loop_segments(frame_num_array, returnaslist=False):
    """

    Parameters
    ----------
    frame_num_array :
    num of frames in each trial in a list
    Returns
    -------
    2 lists with the proper index for pulling those trials out one by one in a for loop
    Examples
    ________
    a3 = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    frame_num_array = [4, 5]
    for i1, i2 in loop_segments(frame_num_array):
        print(a3[i1:i2])

    # >>>[0, 1, 2, 3]
    # >>>[4, 5, 6, 7, 8]
    """
    frame_num_array = list(frame_num_array)
    frame_num_array = [0] + frame_num_array
    frame_num_array = np.cumsum(frame_num_array)
    frame_num_array = frame_num_array.astype(int)
    if returnaslist:
        return [list(frame_num_array[:-1]), list(frame_num_array[1:])]
    else:
        return zip(list(frame_num_array[:-1]), list(frame_num_array[1:]))


##_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*##
##_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*##
##_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*##
##_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*##
##_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*##
##_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*##
##_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*##
##_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*##
##_*_*_*_ below programs users will likely not use_*_*_*_*_*_*##
##_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*##
##_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*##
##_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*##
##_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*##
##_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*##
##_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*##
##_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*##
##_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*##


def _get_human_contacts_(all_h5s, return_curator_names=False):
    """
    just used to get array of contacts, not meant to be used long term
    Parameters
    ----------
    all_h5s :

    Returns
    -------

    """
    h_cont = []
    a = [k.split(os.path.sep)[-1].split('_', maxsplit=1)[-1] for k in all_h5s]
    inds_of_inds, list_of_uniq_files = get_inds_of_inds(a, True)

    curator_names = [os.path.basename(os.path.dirname(k)) for k in all_h5s]
    curator_names = np.asarray(curator_names)[np.asarray(inds_of_inds)]
    for i, k in enumerate(inds_of_inds):
        tmp1 = np.array([])
        for ii, kk in enumerate(k):
            with h5py.File(all_h5s[kk], 'r') as h:
                tmp1 = np.vstack([tmp1, h['labels'][:]]) if tmp1.size else h['labels'][:]
        h_cont.append(tmp1)
    if return_curator_names:
        return h_cont, list_of_uniq_files, curator_names[0, :]
    else:
        return h_cont, list_of_uniq_files


def create_master_dataset(h5c, all_h5s_imgs, h_cont, borders=80, max_pack_val=100):
    """
    Parameters
    ----------
    h5c : h5 creator class
    all_h5s_imgs : list of h5s with images
    h_cont : a tensor of human contacts people by frames trial H5 files (down right deep)
    borders : for touch 0000011100000 it will find the 111 in it and get all the bordering areas around it. points are
    unique so 0000011100000 and 0000010100000 will return the same index
    max_pack_val : speeds up the process by transferring data in chunks of this max size instead of building them all up in memory
    it's a max instead of a set value because it can be if the len(IMAGES)%max_pack_val is equal to 0 or 1 it will crash, so I calculate it
    so that it wont crash.

    Returns
    -------create_master_dataset
    saves an H5 file
    Examples
    ________

    all_h5s = utils.get_h5s('/content/gdrive/My Drive/Colab data/curation_for_auto_curator/finished_contacts/')
    all_h5s_imgs = utils.get_h5s('/content/gdrive/My Drive/Colab data/curation_for_auto_curator/H5_data/')
    h_cont = utils._get_human_contacts_(all_h5s)
    h5c = image_tools.h5_iterative_creator('/content/gdrive/My Drive/Colab data/curation_for_auto_curator/test_____.h5',
                                           overwrite_if_file_exists = True,
                                           color_channel = False)
    utils.create_master_dataset(h5c, all_h5s_imgs, h_cont, borders = 80, max_pack_val = 100)
    """
    frame_nums = []
    for k, k2 in zip(all_h5s_imgs, h_cont):
        if len(k2.shape) == 1:
            k2 = np.vstack((k2, k2))
        with h5py.File(k, 'r') as h:
            max_human_label = np.max(k2, axis=0)
            mean_human_label = np.mean(k2, axis=0)
            mean_human_label = (mean_human_label > 0.5) * 1
            b = inds_around_inds(max_human_label, borders * 2 + 1)
            tmp1, _ = group_consecutives(b)
            for tmp2 in tmp1:
                frame_nums.append(len(tmp2))

            pack_every_x = [k for k in np.flip(range(3, max_pack_val + 1)) if len(b) % k >= 2]
            assert pack_every_x, ['chosen H5 file has value of ', len(b), ' and max_pack_val is ', max_pack_val,
                                  ' increase max_pack_val to prevent this error']
            pack_every_x = np.max(pack_every_x)

            # np.max([k for k in np.flip(range(3, 100)) if len(b) % k >= 2])
            new_imgs = np.array([])
            new_labels = np.array([])
            cntr = 0
            for k3 in tqdm(b):
                cntr += 1
                if new_imgs.size:
                    new_imgs = np.concatenate((new_imgs, h['images'][k3][None, :, :, 0]), axis=0)
                    new_labels = np.append(new_labels, max_human_label[k3])
                else:
                    new_imgs = h['images'][k3][None, :, :, 0]
                    new_labels = mean_human_label[k3]
                if cntr >= pack_every_x:  # this makes it ~ 100X faster than stacking up in memory
                    h5c.add_to_h5(new_imgs, new_labels)
                    new_imgs = np.array([])
                    new_labels = np.array([])
                    cntr = 0
            h5c.add_to_h5(new_imgs, new_labels)

    with h5py.File(h5c.h5_full_file_name, 'r+') as h:
        h.create_dataset('frame_nums', shape=np.shape(frame_nums), data=frame_nums)
        h.create_dataset('inds_extracted', shape=np.shape(b), data=b)


def get_time_it(txt):
    """
  Example
  -------
  import re
  import matplotlib.pyplot as plt
  for k in range(8):
    S = 'test '*10**k
    s2 = 'test'
    %time [m.start() for m in re.finditer(S2, S)]

  # then copy it into a string like below

  txt = '''
  CPU times: user 0 ns, sys: 9.05 ms, total: 9.05 ms
  Wall time: 9.01 ms
  CPU times: user 12 µs, sys: 1 µs, total: 13 µs
  Wall time: 15.7 µs
  CPU times: user 48 µs, sys: 3 µs, total: 51 µs
  Wall time: 56.3 µs
  CPU times: user 281 µs, sys: 0 ns, total: 281 µs
  Wall time: 287 µs
  CPU times: user 2.42 ms, sys: 0 ns, total: 2.42 ms
  Wall time: 2.43 ms
  CPU times: user 21.8 ms, sys: 22 µs, total: 21.8 ms
  Wall time: 21.2 ms
  CPU times: user 198 ms, sys: 21.5 ms, total: 219 ms
  Wall time: 214 ms
  CPU times: user 1.83 s, sys: 191 ms, total: 2.02 s
  Wall time: 2.02 s
  '''
  data = get_time_it(txt)
  ax = plt.plot(data[1:])
  plt.yscale('log')
  """
    vars = [k.split('\n')[0] for k in txt.split('Wall time: ')[1:]]
    a = dict()
    a['s'] = 10 ** 0
    a['ms'] = 10 ** -3
    a['µs'] = 10 ** -6
    data = []
    for k in vars:
        units = k.split(' ')[-1]
        data.append(float(k.split(' ')[0]) * a[units])
    return data


def save_what_is_left_of_your_h5_file(H5_file, do_del_and_rename=0):
    tst_cor = []
    with h5py.File(H5_file, 'a') as hf:
        for k in hf.keys():
            if hf.get(k):
                tst_cor.append(0)
            else:
                tst_cor.append(1)
        if any(tst_cor):
            print('Corrupt file found, creating new file')
            H5_fileTMP = H5_file + 'TMP'
            with h5py.File(H5_file + 'TMP', 'w') as hf2:
                for k in hf.keys():
                    if hf.get(k):
                        print('Adding key ' + k + ' to new temp H5 file...')
                        hf2.create_dataset(k, data=hf[k])
                    else:
                        print('***Key ' + k + ' was corrupt, skipping this key...')
                hf2.close()
                hf.close()
            if do_del_and_rename:
                print('Deleting corrupt H5 file')
                os.remove(H5_file)
                print('renaming new h5 file ')
                os.rename(H5_fileTMP, H5_file)
        else:
            print('File is NOT corrupt!')
    print('FINISHED')


def stack_lag_h5_maker(f, f2, buffer=2, shift_to_the_right_by=0):
    """

    Parameters
    ----------
    f : h5 file with SINGLE FRAMES this is meant to be a test program. if used long term I will change this part
    f2 :
    buffer :
    shift_to_the_right_by :

    Returns
    -------

    """
    h5c = image_tools.h5_iterative_creator(f2, overwrite_if_file_exists=True)
    with h5py.File(f, 'r') as h:
        x = h['frame_nums'][:]
        for ii, (k1, k2) in enumerate(tqdm(loop_segments(x), total=len(x))):
            x2 = h['images'][k1:k2]
            if len(x2.shape) == 4:
                x2 = x2[:, :, :, 0]  # only want one 'color' channel
            new_imgs = image_tools.stack_imgs_lag(x2, buffer=2, shift_to_the_right_by=0)
            h5c.add_to_h5(new_imgs, np.ones(new_imgs.shape[0]) * -1)

    # copy over the other info from the OG h5 file
    copy_h5_key_to_another_h5(f, f2, 'labels', 'labels')
    copy_h5_key_to_another_h5(f, f2, 'frame_nums', 'frame_nums')


def diff_lag_h5_maker(f3):
    """
    need to use the stack_lag_h5_maker first and then send a copy of that into this one again these program are only a temp
    solution, if we use these methods for the main model then I will make using them more fluid and not depend on one another
    Parameters
    ----------
    f3 : the file from stack_lag_h5_maker output

    Returns
    -------
    """
    # change color channel 0 and 1 to diff images from color channel 3 so color channels 0, 1, and 2 are 0-2, 1-2, and 2
    with h5py.File(f3, 'r+') as h:
        for i in tqdm(range(h['images'].shape[0])):
            k = copy.deepcopy(h['images'][i])
            for img_i in range(2):
                k = k.astype(float)
                a = k[:, :, img_i] - k[:, :, -1]
                a = ((a + 255) / 2).astype(np.uint8)
                h['images'][i, :, :, img_i] = a


def expand_single_frame_to_3_color_h5(f, f2):
    h5c = image_tools.h5_iterative_creator(f2, overwrite_if_file_exists=True)
    with h5py.File(f, 'r') as h:
        x = h['frame_nums'][:]
        for ii, (k1, k2) in enumerate(tqdm(loop_segments(x), total=len(x))):
            new_imgs = h['images'][k1:k2]
            new_imgs = np.tile(new_imgs[:, :, :, None], 3)
            h5c.add_to_h5(new_imgs, np.ones(new_imgs.shape[0]) * -1)

    # copy over the other info from the OG h5 file
    copy_over_all_non_image_keys(f, f2)
    # copy_h5_key_to_another_h5(f, f2, 'labels', 'labels')
    # copy_h5_key_to_another_h5(f, f2, 'frame_nums', 'frame_nums')


def copy_over_all_non_image_keys(f, f2):
    """

    Parameters
    ----------
    f : source
    f2 : destination

    Returns
    -------

    """
    k_names = print_h5_keys(f, return_list=True, do_print=False)
    k_names = lister_it(k_names, remove_string='MODEL_')
    k_names = lister_it(k_names, remove_string='images')
    with h5py.File(f, 'r') as h:
        with h5py.File(f2, 'r+') as h2:
            for kn in k_names:
                try:
                    h2.create_dataset(kn, data=h[kn])
                except:
                    del h2[kn]
                    h2.create_dataset(kn, data=h[kn])
            # try:
            #     copy_h5_key_to_another_h5(f, f2, kn, kn)
            # except:
            #     del h[kn]
            #     # time.sleep(2)
            #     copy_h5_key_to_another_h5(f, f2, kn, kn)
    if 'frame_nums' not in k_names and 'trial_nums_and_frame_nums' in k_names:
        tnfn = image_tools.get_h5_key_and_concatenate([f], 'trial_nums_and_frame_nums')
        with h5py.File(f2, 'r+') as h:
            try:
                h.create_dataset('frame_nums', data=(tnfn[1, :]).astype(int))
            except:
                del h['frame_nums']
                time.sleep(2)
                h.create_dataset('frame_nums', data=(tnfn[1, :]).astype(int))


def force_write_to_h5(h5_file, data, data_name):
    with h5py.File(h5_file, 'r+') as h:
        try:
            h.create_dataset(data_name, data=data)
        except:
            del h[data_name]
            h.create_dataset(data_name, data=data)


def reduce_to_single_frame_from_color(f, f2):
    h5c = image_tools.h5_iterative_creator(f2, overwrite_if_file_exists=True, color_channel=False)
    with h5py.File(f, 'r') as h:
        try:
            x = h['trial_nums_and_frame_nums'][1, :]
        except:
            x = h['frame_nums'][:]
        for ii, (k1, k2) in enumerate(tqdm(loop_segments(x), total=len(x))):
            new_imgs = h['images'][k1:k2][..., -1]
            # new_imgs = np.tile(new_imgs[:, :, :, None], 3)
            h5c.add_to_h5(new_imgs, np.ones(new_imgs.shape[0]) * -1)

    # copy over the other info from the OG h5 file
    copy_over_all_non_image_keys(f, f2)
    # copy_h5_key_to_another_h5(f, f2, 'labels', 'labels')
    # copy_h5_key_to_another_h5(f, f2, 'frame_nums', 'frame_nums')


def make_all_H5_types(base_dir_all_h5s):
    def last_folder(f):
        tmp1 = str(Path(f).parent.absolute())
        return str(Path(tmp1).parent.absolute()) + os.sep

    for f in get_h5s(base_dir_all_h5s):
        base_f = last_folder(f)
        basename = os.path.basename(f)[:-3] + '_regular.h5'
        basedir = base_f + 'regular' + os.sep
        if not os.path.isdir(basedir):
            os.mkdir(basedir)
        f2 = basedir + basename
        expand_single_frame_to_3_color_h5(f, f2)

        basename = os.path.basename(f)[:-3] + '_3lag.h5'
        basedir = base_f + '3lag' + os.sep
        if not os.path.isdir(basedir):
            os.mkdir(basedir)
        f2 = basedir + basename

        stack_lag_h5_maker(f, f2, buffer=2, shift_to_the_right_by=0)

        basename = os.path.basename(f2)[:-3] + '_diff.h5'
        basedir = base_f + '3lag_diff' + os.sep
        if not os.path.isdir(basedir):
            os.mkdir(basedir)
        f3 = basedir + basename
        shutil.copy(f2, f3)
        diff_lag_h5_maker(f3)


def get_all_label_types_from_array(array):
    all_labels = []
    x1 = copy.deepcopy(array)  # [0, 1]- (no touch, touch)
    all_labels.append(x1)

    x2 = four_class_labels_from_binary(x1)  # [0, 1, 2, 3]- (no touch, touch, onset, offset)
    all_labels.append(x2)

    x3 = copy.deepcopy(x2)
    x3[x3 != 2] = 0
    x3[x3 == 2] = 1  # [0, 1]- (not onset, onset)
    all_labels.append(x3)

    x4 = copy.deepcopy(x2)  # [0, 1]- (not offset, offset)
    x4[x4 != 3] = 0
    x4[x4 == 3] = 1
    all_labels.append(x4)

    x5 = copy.deepcopy(x2)  # [0, 1, 2]- (no event, onset, offset)
    x5[x5 == 1] = 0
    x5[x5 == 2] = 1
    x5[x5 == 3] = 2
    all_labels.append(x5)

    x6 = copy.deepcopy(x2)  # [0, 1, 2]- (no event, onset, offset)
    onset_inds = x6[:-1] == 2
    bool_inds_one_after_onset = np.append(False, onset_inds)
    offset_inds = x6[:-1] == 3
    bool_inds_one_after_offset = np.append(False, offset_inds)
    offset_inds = x6 == 3
    x6[bool_inds_one_after_onset] = 3
    x6[offset_inds] = 4
    x6[bool_inds_one_after_offset] = 5
    all_labels.append(x6)

    x7 = copy.deepcopy(x6)
    x7[x7 == 2] = 0
    x7[x7 == 5] = 0
    x7[x7 == 3] = 2
    x7[x7 == 4] = 3
    all_labels.append(x7)

    resort = [5, 1, 4, 0, 3, 2, 6]
    # resort = range(len(resort))
    a_final = []
    for i in resort:
        a_final.append(all_labels[i])

    return np.asarray(a_final)


def make_alt_labels_h5s(base_dir_all_h5s):
    for f in get_h5s(base_dir_all_h5s):
        basename = '_ALT_LABELS.'.join(os.path.basename(f).split('.'))
        basedir = os.sep.join(f.split(os.sep)[:-2]) + os.sep + 'ALT_LABELS' + os.sep
        if not os.path.isdir(basedir):
            os.mkdir(basedir)
        new_h5_name = basedir + basename

        with h5py.File(f, 'r') as h:

            x1 = copy.deepcopy(h['labels'][:])  # [0, 1]- (no touch, touch)

            x2 = four_class_labels_from_binary(x1)  # [0, 1, 2, 3]- (no touch, touch, onset, offset)

            x3 = copy.deepcopy(x2)
            x3[x3 != 2] = 0
            x3[x3 == 2] = 1  # [0, 1]- (not onset, onset)

            x4 = copy.deepcopy(x2)  # [0, 1]- (not offset, offset)
            x4[x4 != 3] = 0
            x4[x4 == 3] = 1

            x5 = copy.deepcopy(x2)  # [0, 1, 2]- (no event, onset, offset)
            x5[x5 == 1] = 0
            x5[x5 == 2] = 1
            x5[x5 == 3] = 2

            x6 = copy.deepcopy(x2)  # [0, 1, 2]- (no event, onset, offset)
            onset_inds = x6[:-1] == 2
            bool_inds_one_after_onset = np.append(False, onset_inds)
            offset_inds = x6[:-1] == 3
            bool_inds_one_after_offset = np.append(False, offset_inds)
            offset_inds = x6 == 3
            x6[bool_inds_one_after_onset] = 3
            x6[offset_inds] = 4
            x6[bool_inds_one_after_offset] = 5

            x7 = copy.deepcopy(x6)
            x7[x7 == 2] = 0
            x7[x7 == 5] = 0
            x7[x7 == 3] = 2
            x7[x7 == 4] = 3

        with h5py.File(new_h5_name, 'w') as h:
            h.create_dataset('[0, 1]- (no touch, touch)', shape=np.shape(x1), data=x1)
            h.create_dataset('[0, 1, 2, 3]- (no touch, touch, onset, offset', shape=np.shape(x2), data=x2)
            h.create_dataset('[0, 1]- (not onset, onset)', shape=np.shape(x3), data=x3)
            h.create_dataset('[0, 1]- (not offset, offset)', shape=np.shape(x4), data=x4)
            h.create_dataset('[0, 1, 2]- (no event, onset, offset)', shape=np.shape(x5), data=x5)
            h.create_dataset('[0, 1, 2, 3, 4, 5]- (no touch, touch, onset, one after onset, offset, one after offset)',
                             shape=np.shape(x6), data=x6)
            h.create_dataset('[0, 1, 2, 3]- (no touch, touch, one after onset, offset)', shape=np.shape(x7), data=x7)


def intersect_lists(d):
    return list(set(d[0]).intersection(*d))


def get_in_range(H5_list, pole_up_add=200, pole_down_add=0, write_to_h5=True, return_in_range=False):
    all_in_range = []
    for k in H5_list:
        with h5py.File(k, 'r+') as hf:
            new_in_range = np.zeros_like(hf['in_range'][:])
            fn = hf['trial_nums_and_frame_nums'][1, :]
            for i, (i1, i2) in enumerate(loop_segments(fn)):
                x = hf['pole_times'][:, i] + i1
                x1 = x[0] + pole_up_add
                x2 = x[1] + pole_down_add
                x2 = min([x2, i2])
                new_in_range[x1:x2] = 1
            if write_to_h5:
                hf['in_range'][:] = new_in_range
            if return_in_range:
                all_in_range.append(new_in_range)
    if return_in_range:
        return all_in_range


def get_frame_nums(h5_file):
    with h5py.File(h5_file, 'r+') as hf:
        if 'frame_nums' in hf.keys():
            fn = hf['frame_nums'][:]
        elif 'trial_nums_and_frame_nums' in hf.keys():
            fn = hf['trial_nums_and_frame_nums'][1, :]
        else:
            assert False, """h5 file provided does not have 'frame_nums' or 'trial_nums_and_frame_nums'"""
    return fn


def define_in_range(h5_file, pole_up_set_time=0, pole_down_add_to_trigger=0, write_to_h5=True, return_in_range=False,
                    pole_times=None):
    with h5py.File(h5_file, 'r+') as hf:
        if pole_times is None:
            pole_times = hf['pole_times'][:]

        try:
            new_in_range = np.zeros_like(hf['in_range'][:])
        except:
            new_in_range = np.zeros_like(hf['labels'][:])

        fn = get_frame_nums(h5_file)
        for i, (i1, i2) in enumerate(loop_segments(fn)):
            pt = pole_times[:, i] + i1
            x1 = pt[0] + pole_up_set_time
            x2 = pt[1] - pole_down_add_to_trigger
            x2 = min([x2, i2])
            new_in_range[int(x1):int(x2)] = 1
    if write_to_h5:
        overwrite_h5_key(h5_file, 'in_range', new_data=new_in_range)
    if return_in_range:
        return new_in_range


def add_to_h5(h5_file, key, values, overwrite_if_exists=False):
    all_keys = print_h5_keys(h5_file, return_list=True, do_print=False)
    with h5py.File(h5_file, 'r+') as h:
        if key in all_keys and overwrite_if_exists:
            print('key already exists, overwriting value...')
            del h[key]
            h.create_dataset(key, data=values)
        elif key in all_keys and not overwrite_if_exists:
            print("""key already exists, NOT overwriting value..., \nset 'overwrite_if_exists' to True to overwrite""")
        else:
            h.create_dataset(key, data=values)


def bool_pred_to_class_pred_formating(pred):
    pred = pred.flatten()
    zero_pred = np.ones_like(pred) - pred
    x = np.vstack((zero_pred, pred)).T
    return x


def convert_labels_back_to_binary(b, key):
    a = copy.deepcopy(b)
    """
  a is 'bool' array (integers not float predicitons)
  key is the key name of the type of labels being inserted
  can use the key name or the string in the key either will do.
  """
    name_dict = whacc.model_maker.label_naming_shorthand_dict()
    keys = list(name_dict.keys())
    if key == keys[0] or key == name_dict[keys[0]]:
        a[a >= 4] = 0
        a[a >= 2] = 1

    elif key == keys[1] or key == name_dict[keys[1]]:
        a[a >= 3] = 0
        a[a >= 2] = 1

    elif key == keys[2] or key == name_dict[keys[2]]:
        print("""can not convert type """ + key + ' returning None')
        return None
    elif key == keys[3] or key == name_dict[keys[3]]:
        print('already in the correct format')
    elif key == keys[4] or key == name_dict[keys[4]]:
        print("""can not convert type """ + key + ' returning None')
        return None
    elif key == keys[5] or key == name_dict[keys[5]]:
        print("""can not convert type """ + key + ' returning None')
        return None
    elif key == keys[6] or key == name_dict[keys[6]]:
        a[a >= 3] = 0
        one_to_the_left_inds = a == 2
        one_to_the_left_inds = np.append(one_to_the_left_inds[1:], False)
        a[one_to_the_left_inds] = 1
        a[a == 2] = 1
    else:
        raise ValueError("""key does not match. invalid key --> """ + key)
    return a


def update_whacc():
    # filename = get_whacc_path() + os.sep + '/whacc_data/final_model/final_resnet50V2_full_model.zip'
    # dst = filename[:-4]
    # if os.path.isdir(dst):
    #     shutil.rmtree(dst)
    #     print('waiting 10 seconds to allow model to delete')
    # time.sleep(10)

    x = '''python3 "/Users/phil/Dropbox/UPDATE_WHACC_PYPI.py"'''
    out = os.popen(x).read()
    print(out)
    print(
        'please refer to the open terminal window for further details\nrerun utils.download_resnet_model() to put the model file back')


def make_list(x, suppress_warning=False):
    if not isinstance(x, list):
        if not suppress_warning:
            print("""input is supposed to be a list, converting it but user should do this to suppress this warning""")
        if type(x) is np.str_:
            x2 = [x]
        # elif type(x) is np.str_:
        #     pass
        elif 'array' in str(type(x)).lower():
            x2 = list(x)
        elif type(x).__module__ == np.__name__:
            print(type(x))
            assert False, '''see module whacc.utils.make_list, we have not official protocol for this input type ''' + str(
                type(x))
        elif isinstance(x, str):
            x2 = [x]
        else:
            x2 = [x]
        return x2
    else:
        return x


def search_sequence_numpy(arr, seq, return_type='indices'):
    Na, Nseq = arr.size, seq.size
    r_seq = np.arange(Nseq)
    M = (arr[np.arange(Na - Nseq + 1)[:, None] + r_seq] == seq).all(1)

    if return_type == 'indices':
        return np.where(M)[0]
    elif return_type == 'bool':
        return M


def find_trials_with_suspicious_predictions(frame_nums, pred_bool, tmp_weights=[3, 3, 2, 1]):
    all_lens = []
    bins = len(tmp_weights) + 1
    for i, (k1, k2) in enumerate(loop_segments(frame_nums)):
        vals = pred_bool[k1:k2]
        a, b = group_consecutives(vals, step=0)
        y, x = np.histogram([len(k) for k in a], np.linspace(1, bins, bins))
        all_lens.append(y)
    all_lens = np.asarray(all_lens)

    all_lens = all_lens * np.asarray(tmp_weights)
    sorted_worst_estimated_trials = np.flip(np.argsort(np.nanmean(all_lens, axis=1)))
    return sorted_worst_estimated_trials


def assert_path(str_in):
    if os.path.isfile(str_in):
        str_in = os.path.dirname(str_in)
    elif os.path.isdir(str_in):
        pass
    else:
        assert False, 'this is not a path or a file'
    return str_in


def open_folder(path):
    path = assert_path(path)
    if platform.system() == "Windows":
        os.startfile(path)
    elif platform.system() == "Darwin":
        subprocess.Popen(["open", path])
    else:
        subprocess.Popen(["xdg-open", path])


def medfilt_confidence_scores(pred_bool_in, kernel_size_in):
    if pred_bool_in.shape[1] == 1:
        pred_bool_out = medfilt(copy.deepcopy(pred_bool_in), kernel_size=kernel_size_in)
    else:
        pred_bool_out = medfilt2d(copy.deepcopy(pred_bool_in), kernel_size=[kernel_size_in, 1])
    return pred_bool_out


def confidence_score_to_class(pred_bool_in, thresh_in=0.5):
    if pred_bool_in.shape[1] == 1:
        pred_bool_out = ((pred_bool_in > thresh_in) * 1).flatten()
    else:
        pred_bool_out = np.argmax(pred_bool_in, axis=1)
    #     NOTE: threshold is not used for the multi class models
    return pred_bool_out


def process_confidence_scores(pred_bool_in, key_name_in, thresh_in=0.5, kernel_size_in=1):
    pred_bool_out = medfilt_confidence_scores(pred_bool_in, kernel_size_in)
    pred_bool_out = confidence_score_to_class(pred_bool_out, thresh_in)
    L_key_ = '_'.join(key_name_in.split('__')[3].split(' '))
    pred_bool_out = convert_labels_back_to_binary(pred_bool_out, L_key_)
    return pred_bool_out


def copy_folder_structure(src, dst):
    src = os.path.abspath(src)
    src_prefix = len(src) + len(os.path.sep)
    Path(dst).mkdir(parents=True, exist_ok=True)
    for root, dirs, files in os.walk(src):
        for dirname in dirs:
            dirpath = os.path.join(dst, root[src_prefix:], dirname)
            Path(dirpath).mkdir(parents=True, exist_ok=True)


def copy_file_filter(src, dst, keep_strings='', remove_string=None, overwrite=False,
                     just_print_what_will_be_copied=False, disable_tqdm=False, return_list_of_files=False):
    """

    Parameters
    ----------
    return_list_of_files :
    src : source folder
    dst : destination folder
    keep_strings : see utils.lister_it, list of strings to match in order to copy
    remove_string : see utils.lister_it, list of strings to match in order to not copy
    overwrite : will overwrite files if true
    just_print_what_will_be_copied : can just print what will be copied to be sure it is correct
    disable_tqdm : if True it will prevent the TQDM loading bar

    Examples
    ________
    copy_file_filter('/Users/phil/Desktop/FAKE_full_data', '/Users/phil/Desktop/aaaaaaaaaa', keep_strings='/3lag/',
                 remove_string=None, overwrite=True, just_print_what_will_be_copied=False)
    Returns
    -------

    """
    src = src.rstrip(os.sep) + os.sep
    dst = dst.rstrip(os.sep) + os.sep

    all_files_and_dirs = get_files(src, search_term='*')
    to_copy = lister_it(all_files_and_dirs, keep_strings=keep_strings, remove_string=remove_string)

    if just_print_what_will_be_copied:
        _ = [print(str(i) + ' ' + k) for i, k in enumerate(to_copy)]
        if return_list_of_files:
            return to_copy, None
        else:
            return

    to_copy2 = []  # this is so I can tqdm the files and not the folders which would screw with the average copy time.
    for k in to_copy:
        k2 = dst.join(k.split(src))
        if os.path.isdir(k):
            Path(k2).mkdir(parents=True, exist_ok=True)
        else:
            to_copy2.append(k)
    final_copied = []
    for k in tqdm(to_copy2, disable=disable_tqdm):
        k2 = dst.join(k.split(src))
        final_copied.append(k2)
        if overwrite or not os.path.isfile(k2):
            if os.path.isfile(k2):
                os.remove(k2)
            Path(os.path.dirname(k2)).mkdir(parents=True, exist_ok=True)
            shutil.copyfile(k, k2)
        elif not overwrite:
            print('overwrite = False: file exists, skipping--> ' + k2)
    if return_list_of_files:
        return to_copy2, final_copied


def copy_alt_labels_based_on_directory(file_list, alt_label_folder_name='ALT_LABELS'):
    h5_imgs = []
    h5_labels = []
    inds_of_files = []
    for i, k in enumerate(file_list):
        k = k.rstrip(os.sep)
        if os.path.isfile(k):
            fn = os.path.basename(k)
            alt_labels_dir = os.sep.join(k.split(os.sep)[:-2]) + os.sep + alt_label_folder_name + os.sep
            h5_list = get_h5s(alt_labels_dir, 0)
            if 'train' in fn.lower():
                h5_list = lister_it(h5_list, keep_strings='train')
            elif 'val' in fn.lower():
                h5_list = lister_it(h5_list, keep_strings='val')
            if len(h5_list) == 1:
                h5_imgs.append(k)
                h5_labels.append(h5_list[0])
                inds_of_files.append(i)
            else:
                print('File name ' + fn + ' could not find valid match')
                break
    return h5_imgs, h5_labels, inds_of_files


def np_stats(in_arr):
    print('\nmin', np.min(in_arr))
    print('max', np.max(in_arr))
    print('mean', np.mean(in_arr))
    print('shape', in_arr.shape)
    print('len of unique', len(np.unique(in_arr)))
    print('type', type(in_arr))
    try:
        print('Dtype ', in_arr.dtype)
    except:
        pass


def h5_key_exists(h5_in, key_in):
    return key_in in print_h5_keys(h5_in, return_list=True, do_print=False)


def del_h5_key(h5_in, key_in):
    if h5_key_exists(h5_in, key_in):
        with h5py.File(h5_in, 'r+') as h:
            del h[key_in]


def overwrite_h5_key(h5_in, key_in, new_data=None):
    exist_test = h5_key_exists(h5_in, key_in)
    with h5py.File(h5_in, 'r+') as h:
        if exist_test:
            del h[key_in]
        if new_data is not None:
            h[key_in] = new_data


def convert_list_of_strings_for_h5(list_in):
    return [n.encode("ascii", "ignore") for n in list_in]


def intersect_all(arr1, arr2):
    """retun inndex of length len(arr1) instead of numpys length min([len(arr1), len(arr2)])"""
    return [{v: i for i, v in enumerate(arr2)}[v] for v in arr1]


def space_check(path, min_gb=2):
    assert shutil.disk_usage(
        path).free / 10 ** 9 > min_gb, """space_check function: GB limit reached, ending function"""

# "/whacc_data/final_CNN_model_weights/*.hdf5"
#
# git lfs track "whacc_data/*"
