from whacc import utils
import h5py
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches


def foo_rename(instr):#keep
    if isinstance(instr, list):
        for i, k in enumerate(instr):
            instr[i] = foo_rename(k)
        return instr
    else:
        return '/Volumes/GoogleDrive-114825029448473821206/My Drive' + instr.split('My Drive')[-1]
wedgeprops={'linewidth': 3.0, 'edgecolor': 'white'}

all_data = utils.load_obj(foo_rename('/content/gdrive/My Drive/colab_data2/all_data'))
main_mod = all_data[45]['info']
#
# for k2 in ['train', 'val', 'test']:
#     k = foo_rename(main_mod['h5_'+k2])
#     exec(k2 + ' = "' + k + '"')
#     print(k)
#
# # training
# 383810 # aug - 3 border X 10
# 292217 # reg - 80 border (676027 - 383810)
# # validation
# 163120 # aug - 3 border X 10
# 118734 # regular - 80 border (281854 - 163120)
# # test
# 0      # aug
# 38884  #regular
#
#
# inds = [383810, 163120, 0]
# d = {'Training': [], 'Validation': [], 'Test': []}
# d_len = {'Training': [], 'Validation': [], 'Test': []}
# keys = list(d.keys())
# count = []
# for i, k2 in enumerate(['train', 'val']):#, 'test']):
#     k = foo_rename(main_mod['h5_'+k2])
#     print(k)
#     with h5py.File(k, 'r') as h:
#         L = len(h['labels'][:])
#         count.append(L)
#         d[keys[i]].append(np.sum(h['labels'][inds[i]:] != 0) / L) # reg touch
#         d[keys[i]].append(np.sum(h['labels'][:inds[i]] != 0) / L) # aug touch
#         d[keys[i]].append(np.sum(h['labels'][:inds[i]] == 0) / L) # aug no-touch
#         d[keys[i]].append(np.sum(h['labels'][inds[i]:] == 0) / L) # reg no-touch
#
# print(np.round(count, -3)) #array([676000, 282000,  39000])
#
import seaborn as sns
colors = np.asarray(sns.color_palette("Paired")[:4])
colors = colors[[1, 0, 2, 3,], :]
labels = ['regular\ntouch', 'augmented\ntouch', 'augmented\nno-touch', 'regular\nno-touch']
# pie, ax = plt.subplots(figsize=[10,6])
# plt.pie(x=d['Training'], autopct="%.1f%%", explode=[0.02]*4, labels=labels, pctdistance=0.5, colors= colors)
# plt.title("Training Data\n676k frames", fontsize=14)
#
# pie, ax = plt.subplots(figsize=[10,6])
# plt.pie(x=d['Validation'], autopct="%.1f%%", explode=[0.02]*4, labels=labels, pctdistance=0.5, colors= colors)
# plt.title("Validation Data\n282k frames", fontsize=14)
#
#
# # doing this the old way I would only get the 10% holy set because that is what the data is evaled on originally
# # this is all the test data without the hair data with samsons 1 session (no hair session) and andrews 2 sessions
# fn2 = '/Volumes/GoogleDrive-114825029448473821206/My Drive/Colab data/curation_for_auto_curator/DATA_FULL/full_in_range_16_and_whacc_pred_no_hair.pkl'
# yhat_d = utils.load_obj(fn2)
# yhat_d['frame_nums'], yhat_d['in_range']
# test_lab= yhat_d['labels'] * yhat_d['in_range']
# print(len(test_lab))
# d['Test'] = [np.mean(test_lab==1), np.mean(test_lab!=1)]
#
#
# pie, ax = plt.subplots(figsize=[10,6])
# plt.pie(x=d['Test'], autopct="%.1f%%", explode=[0.02]*2, labels=labels[::3], pctdistance=0.5, colors= colors[::3, :])
# plt.title("Testing Data\n780k frames", fontsize=14)
#
#
#








tvt = '/Volumes/GoogleDrive-114825029448473821206/My Drive/LIGHT_GBM/H5_data/3lag_numpy_aug_for_final_LGBM/keep_inds_no_pole_hair_no_skip_frames_for_SPLIT_BY_TRIAL/tvt_y.pkl'
tvt = utils.load_obj(tvt)
# arrange data
d = {'Training': [], 'Validation': [], 'Test': []}
d_len = {'Training': [], 'Validation': [], 'Test': []}
for i, k in enumerate(d):
    x = np.mean(tvt[i]==1)
    d[k] = [x, 1-x]
    d_len[k] = int(np.round(len(tvt[i]), -3)/1000)
# make plot
pie, ax = plt.subplots(1, 3, figsize=[10,6])
ax = ax.flatten()
for i, key in enumerate(d):
    ax[i].pie(x=d[key], autopct="%.1f%%", pctdistance=0.5, colors=colors[::3, :], wedgeprops=wedgeprops)
    ax[i].title.set_text(key+" Data\n"+str(d_len[key])+"k frames")
# make legend and its data
patches = []
for c, l in zip(colors[::3], labels[::3]):
    patches.append(mpatches.Patch(color=c, label=l))
plt.legend(handles=patches, bbox_to_anchor=(0.9, 1), loc=2, borderaxespad=0, fontsize=10)












inds = [383810, 163120, 0]
d = {'Training': [], 'Validation': [], 'Test': []}
d_len = {'Training': [], 'Validation': [], 'Test': []}
keys = list(d.keys())
count = []
for i, k2 in enumerate(['train', 'val']):#, 'test']):
    k = foo_rename(main_mod['h5_'+k2])
    print(k)
    with h5py.File(k, 'r') as h:
        L = len(h['labels'][:])
        count.append(L)
        d[keys[i]].append(np.sum(h['labels'][inds[i]:] != 0) / L) # reg touch
        d[keys[i]].append(np.sum(h['labels'][:inds[i]] != 0) / L) # aug touch
        d[keys[i]].append(np.sum(h['labels'][:inds[i]] == 0) / L) # aug no-touch
        d[keys[i]].append(np.sum(h['labels'][inds[i]:] == 0) / L) # reg no-touch
        d_len[keys[i]] = int(np.round(L, -3)/1000)

fn2 = '/Volumes/GoogleDrive-114825029448473821206/My Drive/Colab data/curation_for_auto_curator/DATA_FULL/full_in_range_16_and_whacc_pred_no_hair.pkl'
yhat_d = utils.load_obj(fn2)
test_lab= yhat_d['labels'] * yhat_d['in_range']
d['Test'] = [np.mean(test_lab==1), np.mean(test_lab!=1)]
d_len['Test']= int(np.round(len(test_lab), -3)/1000)


pie, ax = plt.subplots(1, 3, figsize=[10,6])
ax = ax.flatten()
for i, key in enumerate(['Training', 'Validation']):
    ax[i].pie(x=d[key], autopct="%.1f%%", pctdistance=0.5, colors=colors, wedgeprops=wedgeprops)
    ax[i].title.set_text(key+" Data\n"+str(d_len[key])+"k frames")
for i, key in enumerate(['Test']):
    ax[2].pie(x=d[key], autopct="%.1f%%", pctdistance=0.5, colors=colors[::3, :], wedgeprops=wedgeprops)
    ax[2].title.set_text(key+" Data\n"+str(d_len[key])+"k frames")

# make legend and its data
patches = []
for c, l in zip(colors, labels):
    patches.append(mpatches.Patch(color=c, label=l))
plt.legend(handles=patches, bbox_to_anchor=(0.95, 1), loc=2, borderaxespad=0, fontsize=10)







#
# key = 'Training'
# pie, ax = plt.subplots(figsize=[10,6])
# plt.pie(x=d[key], autopct="%.1f%%", explode=[0.02]*2, labels=labels[::3], pctdistance=0.5, colors= colors[::3, :])
# plt.title(key+" Data\n"+str(d_len[key])+"k frames", fontsize=14)
#
# key = 'Validation'
# pie, ax = plt.subplots(figsize=[10,6])
# plt.pie(x=d[key], autopct="%.1f%%", explode=[0.02]*2, labels=labels[::3], pctdistance=0.5, colors= colors[::3, :])
# plt.title(key+" Data\n"+str(d_len[key])+"k frames", fontsize=14)
#
# key = 'Test'
# pie, ax = plt.subplots(figsize=[10,6])
# plt.pie(x=d[key], autopct="%.1f%%", explode=[0.02]*2, labels=labels[::3], pctdistance=0.5, colors= colors[::3, :])
# plt.title(key+" Data\n"+str(d_len[key])+"k frames", fontsize=14)






# ax[0].legend(handles=patches, bbox_to_anchor=(1.02, 1), loc=2, borderaxespad=0, fontsize=10)
# # ax[i].legend(patches, loc="best")
# plt.legend(handles=patches, bbox_to_anchor=(1.02, 1), loc=2, borderaxespad=0, fontsize=50)

#
# patches, texts = plt.pie(sizes, colors=colors, startangle=90)
# plt.legend(colors[::3, :], labels, loc="best")
#
#     # ax1.title.set_text
#
#


#
# k = test
# utils.print_h5_keys(k)
#
#
# a1 = 0
# with h5py.File(k, 'r') as h:
#     print(h['labels'].shape)
#     imgs = h['images'][a1:a1+20]
# fig, ax = plt.subplots(5, 4)
# for i, a in enumerate(ax.flatten()):
#     a.imshow(imgs[i])


# # ind = int(281854//1.1)
# # a1 = 234878
# # a2 = 281854
# # a3 = int((a2-a1)/20)
# # with h5py.File(k, 'r') as h:
# #     print(h['labels'].shape)
# #     imgs = h['images'][a1:a2:a3]
# # fig, ax = plt.subplots(5, 4)
# # for i, a in enumerate(ax.flatten()):
# #     a.imshow(imgs[i])
# #
#
# #
# #
# # with h5py.File(k, 'r') as h:
# #     print(h['labels'].shape)
# #     imgs = h['images'][163120:163120+20]
# #     print(len(h['labels'][163120:]))
# # fig, ax = plt.subplots(5, 4)
# # for i, a in enumerate(ax.flatten()):
# #     a.imshow(imgs[i])
# #
# #
# #
# #
# #
# #
# #
# # utils.get_dict_info(main_mod)
# #
# #
# # utils.open_folder(foo_rename('/content/gdrive/My Drive/colab_data2/model_testing/all_data'))
