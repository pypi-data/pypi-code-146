import shutil

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

from whacc import utils
import h5py
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
def foo_save(name_in, data):
    tmp1 = os.path.dirname(name_in)
    Path(tmp1).mkdir(parents=True, exist_ok=True)
    np.save(name_in, data)
from tqdm.contrib import tzip
"""
basically most of what I did is on colab 
code is kinda all over the place 
1) I took the 3lag full session H5 datasets and save frame nums, labels and frame nums to s folder structure as .NPY files
2) I then augmented the full session (didn't cut session off here because I want the final features to have little or no NAN values when shifitng and rolling 
3) in colab I then converted those full sessions to 2048 using GPU for all session 8 normal and 80 augmented 
4) in colab with CPU sessions I generated the final 2105 features
5) no I have to save the raw frame number   

"""
"""
################################################################################################
make the majority labels and the individual labels
################################################################################################
"""
bd = '/Volumes/GoogleDrive-114825029448473821206/My Drive/LIGHT_GBM/H5_data/3lag_numpy_aug_for_final_LGBM/'
image_dir = bd + '/images/'
label_dir = bd + '/labels/'
image_files = natsorted(utils.get_files(image_dir, '*.npy'), alg=ns.REAL)

all_h5s = utils.get_h5s('/Volumes/GoogleDrive-114825029448473821206/My Drive/Colab data/curation_for_auto_curator/finished_contacts/')
h_cont, list_of_uniq_files, curator_names = utils._get_human_contacts_(all_h5s, return_curator_names = True)


for i, k in enumerate(list_of_uniq_files): # make sure they match
    to_end = len(k[:-4])
    print(k[:to_end])
    kk = os.path.basename(image_files[i])
    print(kk[:to_end])
    assert kk[:to_end] == k[:to_end], 'files do not match'
    print('___')

for i, k in enumerate(h_cont):
    majority_labels = 1*(np.mean(k, axis=0)>.5)
    kk = os.path.basename(image_files[i])[:-4]
    foo_save(label_dir+'/'+kk, majority_labels)

for ii, name in enumerate(curator_names):
    for i, k in enumerate(h_cont):
        kk = os.path.basename(image_files[i])[:-4]
        labels_2_save = k[ii]
        foo_save(bd+'/individual_labels/'+name+'/'+kk, labels_2_save)


"""
################################################################################################
Save images and augmented images as numpy in different folders
################################################################################################
"""

# h5_meta_data = '/Users/phil/Dropbox/Colab data/H5_data/regular/AH0407_160613_JC1003_AAAC_regular.h5'
# h5_frames = '/Users/phil/Dropbox/Colab data/H5_data/3lag/AH0407_160613_JC1003_AAAC_3lag.h5'
# h5_frames = '/Users/phil/Dropbox/Colab data/H5_data/ALT_LABELS_FINAL_PRED/AH0407_160613_JC1003_AAAC_ALT_LABELS.h5'

border = 80
d_list = ['/Users/phil/Dropbox/Colab data/H5_data/regular/',
          '/Users/phil/Dropbox/Colab data/H5_data/3lag/',
          '/Users/phil/Dropbox/Colab data/H5_data/ALT_LABELS_FINAL_PRED/',
          '/Users/phil/Dropbox/Colab data/H5_data/ALT_LABELS']

h5_meta_images_labels = []
for k in d_list: # just save all the dat to numpy in different folders
    sorted_files = natsorted(utils.get_h5s(k), alg=ns.REAL)
    h5_meta_images_labels.append(sorted_files)

cnt = 0
for h5_meta_data, h5_frames, h5_labels2, h5_labels in tqdm(np.asarray(h5_meta_images_labels).T):
    cnt+=1
    print(cnt)
    if cnt >=7:
        h5_meta_data, h5_frames, h5_labels2, h5_labels = str(h5_meta_data), str(h5_frames), str(h5_labels), str(h5_labels2)

        y = image_tools.get_h5_key_and_concatenate(h5_labels, '[0, 1]- (no touch, touch)')
        OG_frame_nums = image_tools.get_h5_key_and_concatenate(h5_meta_data, 'frame_nums')
        images = image_tools.get_h5_key_and_concatenate(h5_frames, 'images')

        end_name = os.path.basename(h5_frames)[:-3]
        save_dir = '/Volumes/GoogleDrive-114825029448473821206/My Drive/LIGHT_GBM/H5_data/3lag_numpy_aug_for_final_LGBM/'
        name = save_dir + '/images/' + end_name
        if not os.path.isfile(name):
            foo_save(name, images)

            name = save_dir + '/frame_nums/' + end_name
            foo_save(name, OG_frame_nums)

            # name = save_dir + '/labels/' + end_name ##### WRONGGGGGGGG
            # foo_save(name, y)

        for aug_num in tqdm(range(10)): # Augment images
            name = save_dir + '/images_AUG_'+ str(aug_num) +'/' + end_name
            if not os.path.isfile(name):
                datagen = ImageDataGenerator(rotation_range=360,  #
                                                width_shift_range=.1,  #
                                                height_shift_range=.1,  #
                                                shear_range=.00,  #
                                                zoom_range=.25,
                                                brightness_range=[0.2, 1.2])  #
                gaussian_noise = iaa.AdditiveGaussianNoise(loc = 0, scale=3)
                num_aug = 1


                aug_img_stack = []
                for image, label in zip(images, y):
                    aug_img, _ = image_tools.augment_helper(datagen, num_aug, 0, image, label)
                    aug_img = gaussian_noise.augment_images(aug_img) # optional
                    aug_img_stack.append(aug_img)

                aug_img_stack = np.squeeze(np.asarray(aug_img_stack))
                foo_save(name, aug_img_stack)
        del images



# RESNET_MODEL = model_maker.load_final_model()
# features = model.predict(x)
"""
################################################################################################
################################################################################################
these are all the inds to the good videos so I can multiply the labels by this and it will 
cancel out all the bad videos by setting the labels to 0 so border extraction will not happen on them!
################################################################################################
################################################################################################
"""


from scipy import stats
ind_naming = '/keep_inds_no_skip_frames/'
bd = '/Volumes/GoogleDrive-114825029448473821206/My Drive/LIGHT_GBM/H5_data/3lag_numpy_aug_for_final_LGBM/frame_nums'
bd2 = '/Volumes/GoogleDrive-114825029448473821206/My Drive/LIGHT_GBM/H5_data/3lag_numpy_aug_for_final_LGBM/'
all_fn  =[]
sorted_files = natsorted(utils.get_files(bd, '*.npy'), alg=ns.REAL)
for k in sorted_files:
    fn = np.load(k, allow_pickle=True)
    all_fn.append(fn)
    mode = stats.mode(fn)[0][0]
    good_vids = fn==mode
    label_multiply_by = []
    for ii, num_frames in enumerate(fn):
        if good_vids[ii]:
            label_multiply_by.append([1] * num_frames)
        else:
            label_multiply_by.append([0] * num_frames)
    label_multiply_by = np.concatenate(label_multiply_by)
    save_name = bd2 +ind_naming+ '/' + os.path.basename(k)
    if '________________________AH1120_200322' in os.path.basename(k): # remove samsons bad data
        print('AH1120_200322    AH1120_200322    AH1120_200322    AH1120_200322    AH1120_200322    ')
        label_multiply_by = label_multiply_by*0 # remove all of one of samson's datasets
    foo_save(save_name, label_multiply_by)




"""
################################################################################################
################################################################################################
these are all the inds to the good videos so I can multiply the labels by this and it will 
cancel out all the bad videos by setting the labels to 0 so border extraction will not happen on them!
################################################################################################
################################################################################################
"""

from scipy import stats
ind_naming = '/keep_inds_no_skip_frames/'
ind_naming = 'keep_inds_no_pole_hair_no_skip_frames_for_SPLIT_BY_TRIAL'
bd = '/Volumes/GoogleDrive-114825029448473821206/My Drive/LIGHT_GBM/H5_data/3lag_numpy_aug_for_final_LGBM/frame_nums'
bd2 = '/Volumes/GoogleDrive-114825029448473821206/My Drive/LIGHT_GBM/H5_data/3lag_numpy_aug_for_final_LGBM/'
all_fn = []
sorted_files = natsorted(utils.get_files(bd, '*.npy'), alg=ns.REAL)
for k in sorted_files:
    fn = np.load(k, allow_pickle=True)
    all_fn.append(fn)
    mode = stats.mode(fn)[0][0]
    good_vids = fn==mode
    label_multiply_by = []
    for ii, num_frames in enumerate(fn):
        if good_vids[ii]:
            label_multiply_by.append([1] * num_frames)
        else:
            label_multiply_by.append([0] * num_frames)
    label_multiply_by = np.concatenate(label_multiply_by)
    save_name = bd2 +ind_naming+ '/' + os.path.basename(k)
    if 'AH1120_200322' in os.path.basename(k): # remove samsons bad data
        print('AH1120_200322    AH1120_200322    AH1120_200322    AH1120_200322    AH1120_200322    ')
        label_multiply_by = label_multiply_by*0 # remove all of one of samson's datasets

    foo_save(save_name, label_multiply_by)

"""
######################## make inds for training data for comparing to CNN ##############################################
"""
bd = '/Volumes/GoogleDrive-114825029448473821206/My Drive/LIGHT_GBM/H5_data/3lag_numpy_aug_for_final_LGBM/keep_inds_no_pole_hair_no_skip_frames/80_border/T_V_TS_set_inds/'
bd = '/Volumes/GoogleDrive-114825029448473821206/My Drive/LIGHT_GBM/H5_data/3lag_numpy_aug_for_final_LGBM/keep_inds_no_skip_frames/80_border/T_V_TS_set_inds/'
for k in utils.get_files(bd, '*.npy'):
    inds = np.load(k, allow_pickle=True)
    inds = np.sort(np.concatenate(inds))

"""
"""
# bd = '/Users/phil/Dropbox/HIRES_LAB/GitHub/Phillip_AC/model_testing/all_data/all_models/regular_80_border/data/3lag/'
# for k in utils.get_h5s(bd):
#     utils.print_h5_keys(k)
#
#
#
# h5 = '/Users/phil/Dropbox/HIRES_LAB/GitHub/Phillip_AC/model_testing/all_data/all_models/regular_80_border/data/3lag/val_3lag.h5'
# utils.print_h5_keys(h5)

"""
################################################################################################
################################################################################################
make the majority labels and the individual labels
################################################################################################
################################################################################################
################################################################################################
"""

border = 80
second_border = 3
split_ratio = [7, 2, 1]
label_dir = '/Volumes/GoogleDrive-114825029448473821206/My Drive/LIGHT_GBM/H5_data/3lag_numpy_aug_for_final_LGBM/labels'
regular_dir = '/Users/phil/Dropbox/Colab data/H5_data/regular/'

bd_good_vids = '/Volumes/GoogleDrive-114825029448473821206/My Drive/LIGHT_GBM/H5_data/3lag_numpy_aug_for_final_LGBM/keep_inds_no_pole_hair_no_skip_frames/'
bd_good_vids = '/Volumes/GoogleDrive-114825029448473821206/My Drive/LIGHT_GBM/H5_data/3lag_numpy_aug_for_final_LGBM/keep_inds_no_pole_hair_no_skip_frames_for_CNN_compare/'
# bd_good_vids = '/Volumes/GoogleDrive-114825029448473821206/My Drive/LIGHT_GBM/H5_data/3lag_numpy_aug_for_final_LGBM/keep_inds_no_skip_frames/'
# bd_good_vids = '/Volumes/GoogleDrive-114825029448473821206/My Drive/LIGHT_GBM/H5_data/3lag_numpy_aug_for_final_LGBM/keep_inds_no_pole_hair_no_skip_frames_cnn_compare/'

bd_80 = bd_good_vids+'/80_border/'
bd_3 = bd_good_vids+'/3_border/'
# utils.rmtree(bd_3)
# utils.rmtree(bd_80)
"""
get split ratio to copy it 
use it for the first 4 videos and then done 

full set multiply by the 80 border for the train and Val 
"""
split_ratio_list = [[.7, .3], [.7, .3], [.7, .3], [.7, .3], [0,0,1], [0,0,1], [0,0,1], [0,0,1]]
label_files = natsorted(utils.get_files(label_dir, '*.npy'), alg=ns.REAL)
h5_meta_data_files = natsorted(utils.get_files(regular_dir, '*.h5'), alg=ns.REAL)

for i, (label_f, h5_meta_data) in enumerate(zip(label_files, h5_meta_data_files)):
    split_ratio = split_ratio_list[i]
    good_vid_inds = np.load(bd_good_vids+os.path.basename(label_f), allow_pickle=True)
    base_name = os.path.basename(label_f)
    labels = np.load(label_f, allow_pickle=True)
    labels = good_vid_inds*labels # this will remove all the bad videos by making the labels == 0

    if not np.all(labels==0):
        """
        label_f had continious variable, need to source the human data directly and stor ein the folders under the names
        then make a final npy ile with all labels 
        """
        b = utils.inds_around_inds(labels, border * 2 + 1)
        group_inds, _ = utils.group_consecutives(b)
        new_frame_nums = []
        for tmp2 in group_inds:
            new_frame_nums.append(len(tmp2))

        OG_frame_nums = image_tools.get_h5_key_and_concatenate(h5_meta_data, 'frame_nums')
        OG_frame_nums_cumulative = np.cumsum(OG_frame_nums)

        trial_ind_1 = []
        trial_ind_2 = []
        for k in group_inds:
            trial_ind_1.append(np.sum(k[0]>=OG_frame_nums_cumulative))
            trial_ind_2.append(np.sum(k[0]>=OG_frame_nums_cumulative))
        assert np.all(trial_ind_2 == trial_ind_1), 'there are overlapping images from one video to the next, which should be ' \
                                                   'impossible unless the pole stays up between trials '

        np.random.seed(0)
        tmp_sets = utils.split_list(group_inds, split_ratio)
        if len(tmp_sets)==2:
            tmp_sets.append([])

        T_V_TS_sets = []
        frame_nums_set = []
        labels_80 = []
        # labels = np.asarray(labels)
        for k in tmp_sets:
            if len(k) == 0:
                T_V_TS_sets.append(sorted(k))
            else:
                T_V_TS_sets.append(sorted(np.concatenate(k)))
            frame_nums_set.append(len(k))
            labels_80.append(labels[T_V_TS_sets[-1]])
        foo_save(bd_80 + '/T_V_TS_set_inds_CNN_COMPARE/'+base_name, list(T_V_TS_sets))
        # foo_save(bd_80 + '/labels/'+ base_name, labels_80)

        # T_V_TS_sets_3_border = []
        # labels_3 = []
        # for k in T_V_TS_sets:
        #     tmp_labels = labels[k]
        #     b = utils.inds_around_inds(tmp_labels, second_border * 2 + 1)
        #     group_inds, _ = utils.group_consecutives(b)
        #     border_3_inds = np.asarray(k)[np.concatenate(group_inds)]
        #     T_V_TS_sets_3_border.append(border_3_inds)
        #     labels_3.append(labels[T_V_TS_sets_3_border[-1]])
        #
        # # foo_save(bd_3 + '/T_V_TS_set_inds_cnn_compare/'+ base_name, T_V_TS_sets_3_border)
        # foo_save(bd_3 + '/T_V_TS_set_inds/'+ base_name, T_V_TS_sets_3_border)
        # foo_save(bd_3 + '/labels/'+ base_name, labels_3)
bd = '/Volumes/GoogleDrive-114825029448473821206/My Drive/LIGHT_GBM/H5_data/3lag_numpy_aug_for_final_LGBM/keep_inds_no_pole_hair_no_skip_frames_for_CNN_compare/80_border/T_V_TS_set_inds_CNN_COMPARE'

for k in utils.get_files(bd, '*.npy'):
    tmp1 = np.load(k, allow_pickle=True)
    print(len(tmp1))
    asdf


bd = '/Volumes/GoogleDrive-114825029448473821206/My Drive/LIGHT_GBM/H5_data/3lag_numpy_aug_for_final_LGBM/keep_inds_no_pole_hair_no_skip_frames/80_border/'
ind_dir = bd+'/T_V_TS_set_inds/'
save_data_dir = bd + '/final_2105/'
feature_dir = '/Volumes/GoogleDrive-114825029448473821206/My Drive/LIGHT_GBM/H5_data/3lag_numpy_aug_for_final_LGBM/final_2105/'
feature_files = utils.sort(utils.get_files(feature_dir, '*.npy'))
feature_files_base_names = np.asarray([os.path.basename(k) for k in feature_files])
for k in tqdm(utils.sort(utils.get_files(ind_dir, '*.npy'))):
    tmp1 = np.load(k, allow_pickle=True)

    basename_inds = os.path.basename(k)
    iii = np.where(basename_inds == feature_files_base_names)[0][0]
    data_file = feature_files[iii]


    # label_file = utils.norm_path(save_data_dir+os.path.basename(data_file), '/').split('/')
    # label_file[-2] = 'labels'
    # label_file = '/' + '/'.join(label_file)
    # labels = np.load(label_file, allow_pickle=True)

    base_name = '_'+os.path.basename(data_file)
    run_it = False
    for (inds, save_name) in zip(tmp1, ['train', 'val', 'test']):
        fn = save_data_dir+save_name+base_name
        # labels_name = os.path.dirname(fn)+'_labels/'+os.path.basename(fn)
        # x = labels[inds]
        # foo_save(labels_name, x)
        if os.path.isfile(fn):
            run_it = True
    if run_it:
        final_2105 = np.load(data_file, allow_pickle=True)
        for (inds, save_name) in zip(tmp1, ['train', 'val', 'test']):
            x = final_2105[inds, :]
            foo_save(save_data_dir+save_name+base_name, x)
            #make new folder

"""
need to add the labels here too

"""



bd = '/Volumes/GoogleDrive-114825029448473821206/My Drive/LIGHT_GBM/H5_data/3lag_numpy_aug_for_final_LGBM/keep_inds_no_pole_hair_no_skip_frames/3_border/'
ind_dir = bd+'/T_V_TS_set_inds/'

for folder_num in range(10):
    feature_dir = '/Volumes/GoogleDrive-114825029448473821206/My Drive/LIGHT_GBM/H5_data/3lag_numpy_aug_for_final_LGBM/final_2105_AUG_'+str(folder_num)+os.sep
    save_data_dir = bd + '/final_2105'+'_AUG_'+str(folder_num)+os.sep
    feature_files = utils.sort(utils.get_files(feature_dir, '*.npy'))
    feature_files_base_names = np.asarray([os.path.basename(k) for k in feature_files])
    for k in tqdm(utils.sort(utils.get_files(ind_dir, '*.npy'))):
        basename_inds = os.path.basename(k)
        iii = np.where(basename_inds == feature_files_base_names)[0][0]
        data_file = feature_files[iii]
        base_name = '_'+os.path.basename(data_file)
        run_it = False

        for save_name in ['train', 'val', 'test']:
            fn = save_data_dir+save_name+base_name
            if not os.path.isfile(fn):
                run_it = True

        if run_it:
            tmp1 = np.load(k, allow_pickle=True)
            final_2105 = np.load(data_file, allow_pickle=True)
            for (inds, save_name) in zip(tmp1, ['train', 'val', 'test']):
                x = final_2105[inds, :]
                foo_save(save_data_dir+save_name+base_name, x)


        #
        # base_name = '_'+os.path.basename(data_file)
        # for (inds, save_name) in zip(tmp1, ['train', 'val', 'test']):
        #     x = final_2105[inds, :]
        #     foo_save(save_data_dir+save_name+base_name, x)
        # if run_it:
        #     final_2105 = np.load(data_file, allow_pickle=True)
        #


"""
################################################################################################
################################################################################################
################################################################################################
################################################################################################
generate the final datasets 
need to account for missing frame datasets and samsons dataset 

shit I realized i need to remove the bad ones and then chose the final indexes otherwise it can reduce the 
total number of in any particular set 


ok so to re
"""
h5 = '/Volumes/GoogleDrive-114825029448473821206/My Drive/LIGHT_GBM/H5_data/3lag_numpy_aug_for_final_LGBM/keep_inds_no_pole_hair_no_skip_frames/80_border/T_V_TS_set_inds/AH0407_160613_JC1003_AAAC_3lag.npy'
h5 = '/Volumes/GoogleDrive-114825029448473821206/My Drive/LIGHT_GBM/H5_data/3lag_numpy_aug_for_final_LGBM/keep_inds_no_pole_hair_no_skip_frames/80_border/T_V_TS_set_inds/AH0407_160613_JC1003_AAAC_3lag.npy'
h5_list = utils.get_h5s('/Volumes/GoogleDrive-114825029448473821206/My Drive/LIGHT_GBM/H5_data/3lag_numpy_aug_for_final_LGBM/keep_inds_no_pole_hair_no_skip_frames/80_border/T_V_TS_set_inds')
utils.print_h5_keys(h5)
np_in = '/Volumes/GoogleDrive-114825029448473821206/My Drive/LIGHT_GBM/H5_data/3lag_numpy_aug_for_final_LGBM/keep_inds_no_pole_hair_no_skip_frames/80_border/T_V_TS_set_inds/AH0407_160613_JC1003_AAAC_3lag.npy'
tmp1 = np.load(np_in, allow_pickle=True)

tmp1[0]


################################################################################################
################################################################################################
################################################################################################
################################################################################################
################################################################################################
################################################################################################
################################################################################################
################################################################################################
################################################################################################
################################################################################################
################################################################################################
################################################################################################
################################################################################################
################################################################################################
################################################################################################
################################################################################################
################################################################################################
################################################################################################
################################################################################################
################################################################################################
################################################################################################
################################################################################################
################################################################################################
################################################################################################
################################################################################################
################################################################################################
################################################################################################

def foo_save(name_in, data):
        tmp1 = os.path.dirname(name_in)
        Path(tmp1).mkdir(parents=True, exist_ok=True)
        np.save(name_in, data)
# h5_meta_data = '/Users/phil/Dropbox/Colab data/H5_data/regular/AH0407_160613_JC1003_AAAC_regular.h5'
# h5_frames = '/Users/phil/Dropbox/Colab data/H5_data/3lag/AH0407_160613_JC1003_AAAC_3lag.h5'
# h5_frames = '/Users/phil/Dropbox/Colab data/H5_data/ALT_LABELS_FINAL_PRED/AH0407_160613_JC1003_AAAC_ALT_LABELS.h5'

border = 80
d_list = ['/Users/phil/Dropbox/Colab data/H5_data/regular/',
          '/Users/phil/Dropbox/Colab data/H5_data/3lag/',
          '/Users/phil/Dropbox/Colab data/H5_data/ALT_LABELS_FINAL_PRED/',
          '/Users/phil/Dropbox/Colab data/H5_data/ALT_LABELS']

h5_meta_images_labels = []
for k in d_list:
    sorted_files = natsorted(utils.get_h5s(k), alg=ns.REAL)
    h5_meta_images_labels.append(sorted_files)

for h5_meta_data, h5_frames, h5_labels2, h5_labels in tqdm(np.asarray(h5_meta_images_labels).T):
    # for k in [h5_meta_data, h5_frames, h5_labels2, h5_labels]:
    #     print(os.path.basename(k))
    # print('______')
    h5_meta_data, h5_frames, h5_labels2, h5_labels = str(h5_meta_data), str(h5_frames), str(h5_labels), str(h5_labels2)

    # get the 80 border indices and the 3 border indices
    y = image_tools.get_h5_key_and_concatenate(h5_labels, '[0, 1]- (no touch, touch)')


    # y = np.zeros(4001)
    # y[2000] = 1
    OG_frame_nums = image_tools.get_h5_key_and_concatenate(h5_meta_data, 'frame_nums')
    b = utils.inds_around_inds(y, border * 2 + 1)
    group_inds, result_ind = utils.group_consecutives(b)
    new_frame_nums = []
    for tmp2 in group_inds:
        new_frame_nums.append(len(tmp2))

    OG_frame_nums_cumulative = np.cumsum(OG_frame_nums)
    trial_ind_1 = []
    trial_ind_2 = []
    for k in group_inds:
        trial_ind_1.append(np.sum(k[0]>=OG_frame_nums_cumulative))
        trial_ind_2.append(np.sum(k[0]>=OG_frame_nums_cumulative))
    assert np.all(trial_ind_2 == trial_ind_1), 'there are overlapping images from one video to the next'

    images = image_tools.get_h5_key_and_concatenate(h5_frames, 'images')
    extracted_images = images[np.concatenate(group_inds), :, :, :]

    del images
    labels = np.asarray(y)[np.concatenate(group_inds)]
    end_name = os.path.basename(h5_frames)[:-3]
    name = '/Users/phil/Dropbox/Colab data/H5_data/3lag_80_border_numpy/images/' + end_name
    foo_save(name, extracted_images)
    name = '/Users/phil/Dropbox/Colab data/H5_data/3lag_80_border_numpy/80_border_inds/' + end_name
    foo_save(name, group_inds)
    name = '/Users/phil/Dropbox/Colab data/H5_data/3lag_80_border_numpy/frame_nums/' + end_name
    foo_save(name, new_frame_nums)
    # name = '/Users/phil/Dropbox/Colab data/H5_data/3lag_80_border_numpy/labels/' + end_name # WRONGGGGGG
    # foo_save(name, labels)
    del extracted_images

    #
    # for aug_num in range(10):
    #     datagen = ImageDataGenerator(rotation_range=360,  #
    #                                     width_shift_range=.1,  #
    #                                     height_shift_range=.1,  #
    #                                     shear_range=.00,  #
    #                                     zoom_range=.25,
    #                                     brightness_range=[0.2, 1.2])  #
    #     gaussian_noise = iaa.AdditiveGaussianNoise(loc = 0, scale=3)
    #     num_aug = 1
    #
    #
    #     aug_img_stack = []
    #     # labels_stack = []
    #     for image, label in tzip(zip(images, labels)):
    #         aug_img, label_copy = image_tools.augment_helper(datagen, num_aug, 0, image, label)
    #         aug_img = gaussian_noise.augment_images(aug_img) # optional
    #         aug_img_stack.append(aug_img)
    #         # labels_stack.append(label_copy)
    #     name = '/Users/phil/Dropbox/Colab data/H5_data/3lag_80_border_numpy/images_AUG_'+ str(aug_num) +'/' + end_name
    #
    #     np.squeeze(np.asarray(aug_img_stack))
    #     foo_save(name, extracted_images)




################################################################################################
################################################################################################
################################################################################################
################################################################################################
################################################################################################

new_keys = 'src_file'  # ull
# src_file - full directory of all source files


ID_keys = ['file_name_nums',
           'frame_nums',
           'in_range',
           'labels',
           'trial_nums_and_frame_nums',
           'full_file_names',]
for key in ID_keys:
    value = image_tools.get_h5_key_and_concatenate(h5_meta_data, key)

    print(key)
    utils.info(value)
    print('________')
    # for k in trial_ind_1:
################################################################################################
################################################################################################
################################################################################################
################################################################################################
################################################################################################
# for k in utils.get_files(bd, '*.npy'):
#     os.rename(k, k.replace('.h5', ''))


bd = '/Users/phil/Dropbox/Colab data/H5_data/3lag_80_border_numpy/'
fold_list = sorted(next(os.walk(bd))[1])

borderINDS_frame_NUMS_images_labels = []
for k in fold_list:
    sorted_files = natsorted(utils.get_files(bd+k, '*.npy'), alg=ns.REAL)
    borderINDS_frame_NUMS_images_labels.append(sorted_files)

for border_inds, frame_nums, images, labels in tqdm(np.asarray(borderINDS_frame_NUMS_images_labels).T):
    # for k in [border_inds, frame_nums, images, labels]:
    #     print(os.path.basename(k))
    # print('______')
    border_inds, frame_nums, images, labels = str(border_inds), str(frame_nums), str(images), str(labels)
    border_inds, frame_nums, images, labels = np.load(border_inds, allow_pickle=True), np.load(frame_nums, allow_pickle=True), np.load(images, allow_pickle=True), np.load(labels, allow_pickle=True)


datagen = ImageDataGenerator(rotation_range=360,  #
                                width_shift_range=.1,  #
                                height_shift_range=.1,  #
                                shear_range=.00,  #
                                zoom_range=.25,
                                brightness_range=[0.2, 1.2])  #
gaussian_noise = iaa.AdditiveGaussianNoise(loc = 0, scale=3)
num_aug = 1

ind = 80
aug_img_stack = []
labels_stack = []
for image, label in tqdm(zip(images, labels)):
    aug_img, label_copy = image_tools.augment_helper(datagen, num_aug, 0, image, label)
    aug_img = gaussian_noise.augment_images(aug_img) # optional
    aug_img_stack.append(aug_img)
    labels_stack.append(label_copy)





h5creator.add_to_h5(aug_img_stack[:, :, :, :], labels_stack)
utils.copy_h5_key_to_another_h5(each_h5, new_H5_file, 'frame_nums', 'frame_nums') # copy the frame nums to the sug files
# combine all the
image_tools.split_h5_loop_segments(combine_list,
                                     [1],
                                     each_h5.split('.h5')[0]+'_AUG.h5',
                                     add_numbers_to_name = False,
                                     set_seed=0,
                                     color_channel=True)


"""
#### add frame nums 
"""

bd = '/Volumes/GoogleDrive-114825029448473821206/My Drive/LIGHT_GBM/H5_data/3lag_numpy_aug_for_final_LGBM/keep_inds_no_pole_hair_no_skip_frames/80_border/T_V_TS_set_inds'
bd = '/Volumes/GoogleDrive-114825029448473821206/My Drive/LIGHT_GBM/H5_data/3lag_numpy_aug_for_final_LGBM/keep_inds_no_pole_hair_no_skip_frames/3_border/T_V_TS_set_inds'
bd = '/Volumes/GoogleDrive-114825029448473821206/My Drive/LIGHT_GBM/H5_data/3lag_numpy_aug_for_final_LGBM/keep_inds_no_pole_hair_no_skip_frames_for_CNN_compare/80_border/T_V_TS_set_inds_CNN_COMPARE/'
replace_string = 'T_V_TS_set_inds'
for f in tqdm(utils.sort(utils.get_files(bd, '*.npy'))):
    data_list = np.load(f, allow_pickle=True)
    frame_nums_list = []
    for k in data_list:
        result, result_ind = utils.group_consecutives(k)
        fn = [len(kk) for kk in result]
        frame_nums_list.append(fn)
    f2 = f.replace(replace_string, 'frame_nums')
    utils.make_path(os.path.dirname(f2))
    np.save(f2, frame_nums_list)



"""
everything about indexing can be done later
just get the images for now 
that mean just get the images for 3 and 80 
upload and start running the 80 through colab
then augment the 3 
then run the 3 augmented 
worry about the labels later tonight  
"""



"""
loop through group inds 
assert they are between some value of the loop segments

"""




"""
##########################################################################################
##########################################################################################
MAKE THE REGULAR IMAGES FROM THE 3LAG IMAGES FOR THE CNN DIRECT COMPARISONS
##########################################################################################
##########################################################################################
"""

bd = '/Volumes/GoogleDrive-114825029448473821206/My Drive/LIGHT_GBM/H5_data/3lag_numpy_aug_for_final_LGBM/images'
replace_string = 'regular_numpy_for_final_CNN_comparison_to_LGBM'
for k in tqdm(utils.get_files(bd, '*.npy')):
    images = np.load(k, allow_pickle=True)
    reg_images = images[:, :, :, 2]
    reg_images = np.repeat(reg_images[:, :, :, None], 3, axis=3)
    foo_save(k.replace('3lag_numpy_aug_for_final_LGBM', replace_string), reg_images)





########



















"""
################################################################################################
################################################################################################
SPLIT BY TRIAL 
SPLIT BY TRIAL 
SPLIT BY TRIAL 
SPLIT BY TRIAL 
SPLIT BY TRIAL 
SPLIT BY TRIAL 
SPLIT BY TRIAL 
SPLIT BY TRIAL 
SPLIT BY TRIAL 
SPLIT BY TRIAL 
################################################################################################
################################################################################################
################################################################################################
"""


split_ratio = [7, 2, 1]
from scipy import stats
ind_naming = '/keep_inds_no_skip_frames/'
ind_naming = 'keep_inds_no_pole_hair_no_skip_frames_for_SPLIT_BY_TRIAL'
bd = '/Volumes/GoogleDrive-114825029448473821206/My Drive/LIGHT_GBM/H5_data/3lag_numpy_aug_for_final_LGBM/frame_nums/'
bd2 = '/Volumes/GoogleDrive-114825029448473821206/My Drive/LIGHT_GBM/H5_data/3lag_numpy_aug_for_final_LGBM/'
all_fn = []
sorted_files = natsorted(utils.get_files(bd, '*.npy'), alg=ns.REAL)
split_trail_frame_nums = []
for k in sorted_files:
    fn = np.load(k, allow_pickle=True)
    all_fn.append(fn)
    mode = stats.mode(fn)[0][0]
    good_vids = fn==mode

    label_multiply_by_all = []
    np.random.seed(1)
    fn_inds = utils.split_list(range(len(fn)), split_ratio)
    split_trail_frame_nums.append([fn[k] for k in fn_inds])
    for fn_ind in fn_inds:
        label_multiply_by = []
        for ii, num_frames in enumerate(fn):
            if ii in fn_ind and good_vids[ii]:
                label_multiply_by.append([1] * num_frames)
            else:
                label_multiply_by.append([0] * num_frames)
        label_multiply_by = np.concatenate(label_multiply_by)
        label_multiply_by_all.append(label_multiply_by)
    save_name = bd2 +ind_naming+ '/' + os.path.basename(k)
    if 'AH1120_200322' in os.path.basename(k): # remove samsons bad data

        print('AH1120_200322    AH1120_200322    AH1120_200322    AH1120_200322    AH1120_200322    ')
        tmp1 = []
        for kk in label_multiply_by_all:
            tmp1.append(kk*0)
        tmp1 = []

        for kk in split_trail_frame_nums[-1]:
            tmp1.append([])
        split_trail_frame_nums[-1] = tmp1

    foo_save(save_name, label_multiply_by_all)
utils.save_obj(split_trail_frame_nums,  bd2 +ind_naming+ '/split_trail_frame_nums')












#
#
# split_ratio = [7, 2, 1]
# from scipy import stats
# ind_naming = '/keep_inds_no_skip_frames/'
# ind_naming = 'INDS'
# bd = '/Volumes/GoogleDrive-114825029448473821206/My Drive/LIGHT_GBM/H5_data/3lag_numpy_aug_for_final_LGBM/frame_nums'
# bd2 = '/Volumes/GoogleDrive-114825029448473821206/My Drive/LIGHT_GBM/H5_data/3lag_numpy_aug_for_final_LGBM/'
# all_fn = []
# sorted_files = natsorted(utils.get_files(bd, '*.npy'), alg=ns.REAL)
# for k in sorted_files:
#     save_name = bd2 +ind_naming+ '/' + os.path.basename(k)
#     if os.path.isfile(save_name):
#         read_write = 'r+'
#     else:
#         read_write = 'w'
#     with h5py.File(save_name, read_write) as h:
#         fn = np.load(k, allow_pickle=True)
#         h['frame_nums'] = fn ####
#         all_fn.append(fn)
#         mode = stats.mode(fn)[0][0]
#         good_vids = fn==mode
#         h['good_vids'] = good_vids
#         """########### GOOD VIDEOS ##########"""
#         label_multiply_by = []
#             for ii, num_frames in enumerate(fn):
#                 if ii in fn_ind and good_vids[ii]:
#                     label_multiply_by.append([1] * num_frames)
#                 else:
#                     label_multiply_by.append([0] * num_frames)
#             label_multiply_by = np.concatenate(label_multiply_by)
#         if 'AH1120_200322' in os.path.basename(k): # remove samsons bad data
#             print('AH1120_200322    AH1120_200322    AH1120_200322    AH1120_200322    AH1120_200322    ')
#             label_multiply_by = label_multiply_by_all*0
#         h[''] = label_multiply_by
#         """########### SPLIT BY TRIAL ##########"""
#
#
#
#         """########### 80 BORDER  ##########"""
#
#


split_trail_frame_nums = utils.load_obj('/Volumes/GoogleDrive-114825029448473821206/My Drive/LIGHT_GBM/H5_data/3lag_numpy_aug_for_final_LGBM/keep_inds_no_pole_hair_no_skip_frames_for_SPLIT_BY_TRIAL/split_trail_frame_nums')

def foo_rename(instr):
    if isinstance(instr, list):
        for i, k in enumerate(instr):
            instr[i] = foo_rename(k)
        return instr
    else:
        return '/Volumes/GoogleDrive-114825029448473821206/My Drive' + instr.split('My Drive')[-1]


def foo_border_extraction(y, border):
    b = utils.inds_around_inds(y, border * 2 + 1)
    group_inds, result_ind = utils.group_consecutives(b)
    return group_inds, [len(k) for k in group_inds]

all_h5s = utils.get_h5s(foo_rename('/content/gdrive/My Drive/Colab data/curation_for_auto_curator/finished_contacts/'),
                        print_h5_list=False)
h_cont, h_names = utils._get_human_contacts_(all_h5s)
labels = []
for k in h_cont:
    labels.append(1*(np.nanmean(k, axis=0)>.5))

d_list = ['/Users/phil/Dropbox/Colab data/H5_data/regular/',
          '/Users/phil/Dropbox/Colab data/H5_data/3lag/',
          '/Users/phil/Dropbox/Colab data/H5_data/ALT_LABELS_FINAL_PRED/',
          '/Users/phil/Dropbox/Colab data/H5_data/ALT_LABELS']

h5_meta_images_labels = []
for k in d_list: # just save all the dat to numpy in different folders
    sorted_files = natsorted(utils.get_h5s(k), alg=ns.REAL)
    h5_meta_images_labels.append(sorted_files)



ind_naming = 'keep_inds_no_pole_hair_no_skip_frames_for_SPLIT_BY_TRIAL'
ind_naming2 = 'keep_inds_no_pole_hair_no_skip_frames_for_SPLIT_BY_TRIAL_80_border'

bd2 = '/Volumes/GoogleDrive-114825029448473821206/My Drive/LIGHT_GBM/H5_data/3lag_numpy_aug_for_final_LGBM/'
save_name = bd2 +ind_naming+ '/'
files = utils.sort(utils.get_files(save_name, '*'))
border = 80
# with h5py.File(bd2 +ind_naming2+'.h5', 'w') as h:
h = dict()
for iii, (f, h5_meta_data, y) in enumerate(zip(files, h5_meta_images_labels[0], labels)):
    bn = os.path.basename(f)

    OG_frame_nums = image_tools.get_h5_key_and_concatenate(h5_meta_data, 'frame_nums')

    group_inds, new_frame_nums = foo_border_extraction(y, border)
    TVt_good_frames = np.load(f, allow_pickle=1)


    border_inds_80 = np.zeros_like(y)
    border_inds_80[np.concatenate(group_inds).astype(int)] = 1

    TVt_good_frames_80_border = [tvt*border_inds_80 for tvt in TVt_good_frames]

    new_fn = []
    for k in TVt_good_frames_80_border:
        k = np.where(k==1)[0]
        group_inds, result_ind = utils.group_consecutives(k)
        new_fn.append([len(kk) for kk in group_inds])

    h[bn] = dict()
    # h[bn]['OG_frame_nums'] = OG_frame_nums

    h[bn]['new_frame_nums'] = new_fn
    h[bn]['TVt_good_frames_80_border'] = TVt_good_frames_80_border
    h[bn]['full_test_set_inds'] = TVt_good_frames[-1]
    h[bn]['full_test_set_frame_nums'] = split_trail_frame_nums[iii][-1]

final_save_name = bd2 + ind_naming2
utils.save_obj(h, final_save_name)



final_save_name = bd2 +ind_naming2
d = utils.load_obj(final_save_name)



split_trail_frame_nums = utils.load_obj('/Volumes/GoogleDrive-114825029448473821206/My Drive/LIGHT_GBM/H5_data/3lag_numpy_aug_for_final_LGBM/keep_inds_no_pole_hair_no_skip_frames_for_SPLIT_BY_TRIAL/split_trail_frame_nums')

replace_data = r'final_2105'
replace_labels = r'labels'
replace_frame_nums = r'frame_nums'

bd = '/Volumes/GoogleDrive-114825029448473821206/My Drive/LIGHT_GBM/H5_data/3lag_numpy_aug_for_final_LGBM/'
bd_data = bd + replace_data

data_files = utils.sort(utils.get_files(bd_data, '*.npy'))

tvt_x = [[],[],[]]
tvt_y = [[],[],[]]
tvt_fn = [[],[],[]]

'/Volumes/GoogleDrive-114825029448473821206/My Drive/LIGHT_GBM/H5_data/3lag_numpy_aug_for_final_LGBM/final_2105'
bd = '/Volumes/GoogleDrive-114825029448473821206/My Drive/LIGHT_GBM/H5_data/'
for f_data in tqdm(data_files):
    bn = os.path.basename(f_data)
    d2 = d[bn]

    f_label = f_data.replace(replace_data, replace_labels)
    f_fn = f_data.replace(replace_data, replace_frame_nums)


    f_data = np.load(f_data, allow_pickle=True)
    f_label = np.load(f_label, allow_pickle=True)
    f_fn = np.load(f_fn, allow_pickle=True)


    for set_i in range(3):
        inds = d2['TVt_good_frames_80_border'][set_i]==1
        tvt_x[set_i].append(f_data[inds, :])
        tvt_y[set_i].append(f_label[inds])
        tvt_fn[set_i].append(d2['new_frame_nums'][set_i])
    del f_data

bd3 = '/Volumes/GoogleDrive-114825029448473821206/My Drive/LIGHT_GBM/H5_data/3lag_numpy_aug_for_final_LGBM/keep_inds_no_pole_hair_no_skip_frames_for_SPLIT_BY_TRIAL/'
for i, k in enumerate(tvt_x):
    tvt_x[i] = np.vstack(k)
for i, k in enumerate(tvt_y):
    tvt_y[i] = np.concatenate(k).astype(int)
for i, k in enumerate(tvt_fn):
    tvt_fn[i] = np.concatenate(k).astype(int)

utils.save_obj(tvt_x, bd3+'/tvt_x')
utils.save_obj(tvt_y, bd3+'/tvt_y')
utils.save_obj(tvt_fn, bd3+'/tvt_fn')



"""
MAKE THE FULL TEST DATA (NOT 80 BORDER) 
SPLIT BY TRIAL 
"""

split_trail_frame_nums = utils.load_obj('/Volumes/GoogleDrive-114825029448473821206/My Drive/LIGHT_GBM/H5_data/3lag_numpy_aug_for_final_LGBM/keep_inds_no_pole_hair_no_skip_frames_for_SPLIT_BY_TRIAL/split_trail_frame_nums')

replace_data = r'final_2105'
replace_labels = r'labels'
replace_frame_nums = r'frame_nums'

bd = '/Volumes/GoogleDrive-114825029448473821206/My Drive/LIGHT_GBM/H5_data/3lag_numpy_aug_for_final_LGBM/'
bd_data = bd + replace_data

data_files = utils.sort(utils.get_files(bd_data, '*.npy'))
'/Volumes/GoogleDrive-114825029448473821206/My Drive/LIGHT_GBM/H5_data/3lag_numpy_aug_for_final_LGBM/final_2105'
bd = '/Volumes/GoogleDrive-114825029448473821206/My Drive/LIGHT_GBM/H5_data/'
full_test_data = []
full_test_fn = []
full_test_labels = []
full_test_inds = []
full_test_files_names = []
for f_data in tqdm(data_files):
    bn = os.path.basename(f_data)
    d2 = d[bn]
    # print(d2['full_test_set_inds']))

    f_label = f_data.replace(replace_data, replace_labels)
    f_fn = f_data.replace(replace_data, replace_frame_nums)

    f_data = np.load(f_data, allow_pickle=True)
    f_label = np.load(f_label, allow_pickle=True)
    # f_fn = np.load(f_fn, allow_pickle=True)

    full_test_set_frame_nums = d2['full_test_set_frame_nums']
    inds = d2['full_test_set_inds'] == 1

    full_test_data.append(f_data[inds, :])
    full_test_labels.append(f_label[inds])
    full_test_fn.append(full_test_set_frame_nums)

    full_test_inds.append(inds)
    full_test_files_names.append(bn)
    del f_data
"""last minute add in ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓ """
each_file_len = []
for f_data in tqdm(data_files):
    bn = os.path.basename(f_data)
    d2 = d[bn]
    each_file_len.append(np.sum(d2['full_test_set_inds']))
"""last minute add in ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑ """


bd3 = '/Volumes/GoogleDrive-114825029448473821206/My Drive/LIGHT_GBM/H5_data/3lag_numpy_aug_for_final_LGBM/keep_inds_no_pole_hair_no_skip_frames_for_SPLIT_BY_TRIAL/'
"""##### save the files as pickles #####"""
utils.save_obj(full_test_data, bd3+'/full_test_data')
utils.save_obj(full_test_labels, bd3+'/full_test_labels')
utils.save_obj(full_test_fn, bd3+'/full_test_fn')


full_test_data = np.vstack(full_test_data).astype(np.float64)
full_test_labels = np.concatenate(full_test_labels).astype(np.float32)
full_test_fn = np.concatenate(full_test_fn).astype(np.int32)
full_test_inds = [np.asarray(k).astype(np.int32) for k in full_test_inds]
h5_file_name = bd3+'FINAL_TEST_SPLIT_BY_TRIAL_FULL_TRIALS' + '.h5'
with h5py.File(h5_file_name, 'w') as h:
    # h['full_test_inds'] = full_test_inds
    h['full_test_data'] = full_test_data
    h['full_test_labels'] = full_test_labels
    h['full_test_fn'] = full_test_fn
    for i, k in enumerate(full_test_files_names):
        h[k] = full_test_inds[i]

"""
 ADD THE IMAGE FILES TO MATCH THE FINAL TEST SET
"""
image_dir = '/Volumes/GoogleDrive-114825029448473821206/My Drive/LIGHT_GBM/H5_data/3lag_numpy_aug_for_final_LGBM//images/'
image_files = natsorted(utils.get_files(image_dir, '*.npy'), alg=ns.REAL)
all_images = []
for f, inds in zip(image_files, full_test_inds):
    print(np.sum(inds))
    x = np.load(f, allow_pickle=1)
    all_images.append(x[inds.astype(bool)])
del x
all_images = np.vstack(all_images)

utils.overwrite_h5_key(h5_file_name, 'images', all_images)


no_hair_inds

utils.overwrite_h5_key(h5_file_name, 'each_file_len', each_file_len)

file_frame_counts = np.concatenate([np.asarray([0]), np.cumsum(each_file_len)])
no_hair_inds = np.ones(np.sum(each_file_len)).astype(bool)
no_hair_inds[file_frame_counts[4]:file_frame_counts[5]] = False

utils.overwrite_h5_key(h5_file_name, 'no_hair_inds', no_hair_inds)




"""
now I can tak the video frames and add them and scan through them for pole down mistakes 
"""
# from whacc.touch_curation_GUI import touch_gui
# touch_gui(h5_file_name, 'full_test_labels', label_write_key='XXXXXXXXXXXXXXXXXXXXXXXXpole_in_rangeXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')


pole_in_range = image_tools.get_h5_key_and_concatenate('/Volumes/GoogleDrive-114825029448473821206/My Drive/LIGHT_GBM/H5_data/3lag_numpy_aug_for_final_LGBM/keep_inds_no_pole_hair_no_skip_frames_for_SPLIT_BY_TRIAL/FINAL_TEST_SPLIT_BY_TRIAL_FULL_TRIALS.h5', 'pole_in_range')
full_test_fn = image_tools.get_h5_key_and_concatenate('/Volumes/GoogleDrive-114825029448473821206/My Drive/LIGHT_GBM/H5_data/3lag_numpy_aug_for_final_LGBM/keep_inds_no_pole_hair_no_skip_frames_for_SPLIT_BY_TRIAL/FINAL_TEST_SPLIT_BY_TRIAL_FULL_TRIALS.h5', 'full_test_fn')
fn_192000 = image_tools.get_h5_key_and_concatenate(h5_file_name, 'fn_192000')

in_range_by_hand = []
in_range_by_hand_frame_nums = []
for ii, (i1, i2) in enumerate(utils.loop_segments(fn_192000)):
    i3 = (i2-i1)/2
    in_range_labels = pole_in_range[i1:i2]
    oor_inds = np.where(in_range_labels==-1)[0]

    pole_in_range_start = np.max(oor_inds[oor_inds<i3])+1
    pole_in_range_end = np.min(oor_inds[oor_inds>i3])-1
    in_range = np.zeros_like(in_range_labels)
    in_range[pole_in_range_start:pole_in_range_end] = 1
    in_range_by_hand.append(in_range)
    in_range_by_hand_frame_nums.append(int(np.sum(in_range)))

in_range_by_hand = np.concatenate(in_range_by_hand)
# utils.overwrite_h5_key(h5_file_name, 'in_range_by_hand', None)
utils.overwrite_h5_key(h5_file_name, 'in_range_by_hand_192000', in_range_by_hand)
utils.overwrite_h5_key(h5_file_name, 'in_range_by_hand_frame_nums', in_range_by_hand_frame_nums)

mod_path = '/Users/phil/Desktop/by_trial_temp_model.pkl'
mod_path = '/Users/phil/Desktop/by_trial_temp_model_with_nans.pkl'
mod = utils.load_obj(mod_path)
full_test_fn = image_tools.get_h5_key_and_concatenate(h5_file_name, 'full_test_fn')
each_file_len = image_tools.get_h5_key_and_concatenate(h5_file_name, 'each_file_len')



fn_192000 = np.concatenate([full_test_fn[:-12], [3000]*6, full_test_fn[-12:]])
utils.overwrite_h5_key(h5_file_name, 'fn_192000', fn_192000)


no_hair_inds = image_tools.get_h5_key_and_concatenate(h5_file_name, 'no_hair_inds')
full_test_fn = image_tools.get_h5_key_and_concatenate(h5_file_name, 'full_test_fn')
fd = image_tools.get_h5_key_and_concatenate(h5_file_name, 'full_test_data')
in_range_by_hand_FULL_192000 = image_tools.get_h5_key_and_concatenate(h5_file_name, 'in_range_by_hand_192000')
labels = image_tools.get_h5_key_and_concatenate(h5_file_name, 'full_test_labels')

# in_range_by_hand_FULL_192000 = np.zeros_like(no_hair_inds)
# in_range_by_hand_FULL_192000[no_hair_inds] = in_range_by_hand

"""
get unique nan feature data 
"""
tmp1 = [np.isnan(k) for k in copy.deepcopy(fd)]
tmp1 = np.asarray(tmp1)
tmp2 = np.unique(tmp1, axis=0)
tmp2.shape

plt.figure(figsize = (20,2))
plt.imshow(tmp2, interpolation='nearest', aspect='auto')

tmp3 = tmp1[:50,:]
plt.figure(figsize = (20,2))
plt.imshow(tmp3, interpolation='nearest', aspect='auto')

start_end_nan_locations = tmp1[4000-50:4000+50,:]
plt.figure(figsize = (20,2))
plt.imshow(start_end_nan_locations, interpolation='nearest', aspect='auto')

utils.save_obj(start_end_nan_locations, '/Users/phil/Dropbox/HIRES_LAB/GitHub/whacc/whacc/whacc_data/feature_data/'+'start_end_nan_locations'+'.pkl')

# """
# remove the noise images
# """
# corrected_images = []
# for ii, (i1, i2) in enumerate(utils.loop_segments(fn_192000)):
#     with h5py.File(h5_file_name, 'r') as h:
#         x = h['images'][i1:i2]
#         asdf
#
#         corrected_images.append(x)

"""
########################
"""

fd = fd[no_hair_inds]
yhat = mod.predict(fd)
utils.overwrite_h5_key(h5_file_name, 'TEMP_yhat', yhat)
x = 1*(yhat>.5)
x = x*in_range_by_hand_FULL_192000

segments, _ = utils.group_consecutives(np.where(x!=labels)[0])
# utils.overwrite_h5_key(h5_file_name, 'TEMP_yhat_full_192000', x)
utils.overwrite_h5_key(h5_file_name, 'TEMP_yhat_full_192000_nan', x)

"""
########################
"""
from scipy.signal import medfilt
yhat = mod.predict(fd)
thresh = .5
yhat_med_5 = []
for i1, i2 in utils.loop_segments(fn_192000):
    x = medfilt(yhat[i1:i2], 5)
    x = 1*(x>thresh)
    yhat_med_5.append(x)
yhat_med_5 = np.concatenate(yhat_med_5)
tmp1 = copy.deepcopy(yhat_med_5)
yhat_med_5 = yhat_med_5*in_range_by_hand_FULL_192000
yhat_med_5 = yhat_med_5*no_hair_inds

utils.overwrite_h5_key(h5_file_name, 'TEMP_yhat_full_192000_nan', yhat_med_5)

plt.plot(tmp1+.2)
plt.plot(TEMP_yhat_full_192000+.1)
plt.plot(labels*no_hair_inds)


"""
########################
"""


plt.plot(in_range_by_hand_FULL_192000)
plt.plot(labels)


# fd2 = []
# for ii, (i1, i2) in enumerate(utils.loop_segments(fn_192000)):
#     x = fd[i1:i2]
#     asdf
#     fd2.append(x)


f2 = np.vstack(f2)


for k in np.asarray(segments)[np.where([len(k)>2 for k in segments])[0]]:
    print(k[0])

from scipy.signal import medfilt
thresh = .5
yhat_med_5 = []
for i1, i2 in utils.loop_segments(full_test_fn):
    x = medfilt(yhat[i1:i2], 5)
    x = 1*(x>thresh)
    yhat_med_5.append(x)
yhat_med_5 = np.concatenate(yhat_med_5)


utils.overwrite_h5_key(h5_file_name, 'TEMP_yhat_med_5', yhat_med_5)
"""
each_file_len
"""


x = yhat_med_5[in_range_by_hand.astype(bool)]
x2 = labels[no_hair_inds][in_range_by_hand.astype(bool)]
plt.plot(x+.2)
plt.plot(x2)
np.sum(no_hair_inds)






# :96000 and 114000:
x = yhat_med_5*in_range_by_hand
plt.plot(x[10*-4000:])




def h5_string_switcher(list_in):
    list_in = utils.make_list(list_in)
    if type(list_in[0]) == bytes:
        print('DECODE switching from bytes to string')
        out = [k.decode("ascii", "ignore") for k in list_in]
    elif type(list_in[0]) == str:
        print('ENCODE switching from string to bytes')
        out = [k.encode("ascii", "ignore") for k in list_in]
    else:
        print('not bytes or string format, returning input')
        return list_in
    return out
utils.h5_string_switcher = h5_string_switcher





for i, A in enumerate(TVt_good_frames_80_border):
    plt.plot(i*.1 + A)
plt.plot(y-1)
for i1, i2 in utils.loop_segments(OG_frame_nums):
    plt.vlines(i1, -1, 1, 'k')


b = utils.inds_around_inds(y, border * 2 + 1)
group_inds, result_ind = utils.group_consecutives(b)

group_inds, [len(k) for k in group_inds]

# b = utils.inds_around_inds(y, border * 2 + 1)
# group_inds, result_ind = utils.group_consecutives(b)
# new_frame_nums = []
# for tmp2 in group_inds:
#     new_frame_nums.append(len(tmp2))

# OG_frame_nums_cumulative = np.cumsum(OG_frame_nums)


