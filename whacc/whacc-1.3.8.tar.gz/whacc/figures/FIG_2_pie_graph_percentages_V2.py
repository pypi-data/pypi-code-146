from whacc import utils
import h5py
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches
import seaborn as sns


def foo_rename(instr):  # keep
    if isinstance(instr, list):
        for i, k in enumerate(instr):
            instr[i] = foo_rename(k)
        return instr
    else:
        return '/Volumes/GoogleDrive-114825029448473821206/My Drive' + instr.split('My Drive')[-1]


wedgeprops = {'linewidth': 2.0, 'edgecolor': 'white',  'antialiased': True}
pctdistance=.5

colors = np.asarray(sns.color_palette("Paired")[:4])
colors = colors[[1, 0, 2, 3, ], :]
labels = ['regular\ntouch', 'augmented\ntouch', 'augmented\nno-touch', 'regular\nno-touch']





""" data from the boosted model"""
tvt = '/Volumes/GoogleDrive-114825029448473821206/My Drive/LIGHT_GBM/H5_data/3lag_numpy_aug_for_final_LGBM/keep_inds_no_pole_hair_no_skip_frames_for_SPLIT_BY_TRIAL/tvt_y.pkl'
tvt = utils.load_obj(tvt)
# arrange data
d = {'Training': [], 'Validation': [], 'Test': []}
d_len = {'Training': [], 'Validation': [], 'Test': []}
for i, k in enumerate(d):
    x = np.mean(tvt[i] == 1)
    d[k] = [x, 1 - x]
    d_len[k] = int(np.round(len(tvt[i]), -3) / 1000)
# test data in the above file was for my ref only and not for plotting
# below file is used for paper
full_test_labels = '/Volumes/GoogleDrive-114825029448473821206/My Drive/LIGHT_GBM/H5_data/3lag_numpy_aug_for_final_LGBM/keep_inds_no_pole_hair_no_skip_frames_for_SPLIT_BY_TRIAL/full_test_labels.pkl'
full_test_labels = utils.load_obj(full_test_labels)

h5_file = '/Volumes/GoogleDrive-114825029448473821206/My Drive/LIGHT_GBM/H5_data/3lag_numpy_aug_for_final_LGBM/keep_inds_no_pole_hair_no_skip_frames_for_SPLIT_BY_TRIAL/FINAL_TEST_SPLIT_BY_TRIAL_FULL_TRIALS.h5'
in_range = utils.getkey(h5_file, 'in_range_by_hand_192000')
no_hair_inds = utils.getkey(h5_file, 'no_hair_inds')
keep_inds = np.logical_and(no_hair_inds==1, in_range==1)==True

full_test_labels = full_test_labels[keep_inds.astype(bool)]

d_len['Test'] = int(np.round(len(full_test_labels), -3) / 1000)
x = np.mean(full_test_labels == 1)
d['Test'] = [x, 1 - x]




# make plot
pie, ax = plt.subplots(1, 3, figsize=[10, 6])
ax = ax.flatten()
for i, key in enumerate(d):
    ax[i].pie(x=d[key], autopct="%.1f%%", pctdistance=pctdistance, colors=colors[::3, :], wedgeprops=wedgeprops)
    ax[i].title.set_text(key + " Data\n" + str(d_len[key]) + "k frames")
# make legend and its data
patches = []
for c, l in zip(colors[::3], labels[::3]):
    patches.append(mpatches.Patch(color=c, label=l))
plt.legend(handles=patches, bbox_to_anchor=(0.9, 1), loc=2, borderaxespad=0, fontsize=10)






""" data from the CNN model"""
all_data = utils.load_obj(foo_rename('/content/gdrive/My Drive/colab_data2/all_data'))
main_mod = all_data[45]['info']
inds = [383810, 163120, 0]
d = {'Training': [], 'Validation': [], 'Test': []}
d_len = {'Training': [], 'Validation': [], 'Test': []}
keys = list(d.keys())
count = []
for i, k2 in enumerate(['train', 'val']):  # , 'test']):
    k = foo_rename(main_mod['h5_' + k2])
    print(k)
    with h5py.File(k, 'r') as h:
        L = len(h['labels'][:])
        count.append(L)
        d[keys[i]].append(np.sum(h['labels'][inds[i]:] != 0) / L)  # reg touch
        d[keys[i]].append(np.sum(h['labels'][:inds[i]] != 0) / L)  # aug touch
        d[keys[i]].append(np.sum(h['labels'][:inds[i]] == 0) / L)  # aug no-touch
        d[keys[i]].append(np.sum(h['labels'][inds[i]:] == 0) / L)  # reg no-touch
        d_len[keys[i]] = int(np.round(L, -3) / 1000)

fn2 = '/Volumes/GoogleDrive-114825029448473821206/My Drive/Colab data/curation_for_auto_curator/DATA_FULL/full_in_range_16_and_whacc_pred_no_hair.pkl'
yhat_d = utils.load_obj(fn2)
test_lab = yhat_d['labels'] * yhat_d['in_range']
d['Test'] = [np.mean(test_lab == 1), np.mean(test_lab != 1)]
d_len['Test'] = int(np.round(len(test_lab), -3) / 1000)

pie, ax = plt.subplots(1, 3, figsize=[10, 6])
ax = ax.flatten()

for i, key in enumerate(['Training', 'Validation']):
    ax[i].pie(x=d[key], autopct="%.1f%%", pctdistance=pctdistance, colors=colors, wedgeprops=wedgeprops)
    ax[i].title.set_text(key + " Data\n" + str(d_len[key]) + "k frames")
for i, key in enumerate(['Test']):
    ax[2].pie(x=d[key], autopct="%.1f%%", pctdistance=pctdistance, colors=colors[::3, :], wedgeprops=wedgeprops)
    ax[2].title.set_text(key + " Data\n" + str(d_len[key]) + "k frames")

# make legend and its data
patches = []
for c, l in zip(colors, labels):
    patches.append(mpatches.Patch(color=c, label=l))
plt.legend(handles=patches, bbox_to_anchor=(0.95, 1), loc=2, borderaxespad=0, fontsize=10)
