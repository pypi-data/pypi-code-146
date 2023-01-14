import copy
import matplotlib.pyplot as plt

import numpy as np
from scipy.signal import medfilt, medfilt2d

from whacc import image_tools
from whacc import utils
import pandas as pd
import seaborn as sns
from matplotlib.lines import Line2D

def foo_rename(instr):
    if isinstance(instr, list):
        for i, k in enumerate(instr):
            instr[i] = foo_rename(k)
        return instr
    else:
        return '/Volumes/GoogleDrive-114825029448473821206/My Drive' + instr.split('My Drive')[-1]


def medfilt_confidence_scores(pred_bool_in, kernel_size_in):
    if len(pred_bool_in.shape) == 1 or pred_bool_in.shape[1] == 1:
        pred_bool_out = medfilt(copy.deepcopy(pred_bool_in).flatten(), kernel_size=kernel_size_in)
    else:
        pred_bool_out = medfilt2d(copy.deepcopy(pred_bool_in), kernel_size=[kernel_size_in, 1])
    return pred_bool_out


def confidence_score_to_class(pred_bool_in, thresh_in):
    if len(pred_bool_in.shape) == 1 or pred_bool_in.shape[1] == 1:
        pred_bool_out = ((pred_bool_in > thresh_in) * 1).flatten()
    else:
        pred_bool_out = np.argmax(pred_bool_in, axis=1)
    #     NOTE: threshold is not used for the multi class models
    return pred_bool_out


def foo_arg_max_and_smooth(pred_bool_in, kernel_size_in, thresh_in, key_name_in, L_key_=None, L_type_split_ind=None):
    pred_bool_out = medfilt_confidence_scores(pred_bool_in, kernel_size_in)
    pred_bool_out = confidence_score_to_class(pred_bool_out, thresh_in)
    if L_key_ is None:
        L_key_ = '_'.join(key_name_in.split('__')[L_type_split_ind].split(' '))

    pred_bool_out = utils.convert_labels_back_to_binary(pred_bool_out, L_key_)
    return pred_bool_out


"""##################################################################################################################"""
"""##################################################################################################################"""
# key_name = 'model_5____3lag__regular_labels__MODEL_FULL_TRAIN_rollSTD_3_7_rollMEAN_3_7_shift_neg2_to_2_val_with_real_val_PM_JC_LIGHT_GBM'
# h5_file = '/Volumes/GoogleDrive-114825029448473821206/My Drive/colab_data2/model_testing/all_data/final_predictions/ALT_LABELS_FINAL_PRED/AH0407_160613_JC1003_AAAC_ALT_LABELS.h5'

"""
pred key 
TEMP_yhat_full_192000_nan

frame nums
fn_192000

~~other important keys~~ 
full_test_labels
no_hair_inds
in_range_by_hand_192000 ~~ has only 0's and 1's
pole_in_range ~~ has -1's 0's and 1's 
"""
# h5_file = '/Volumes/GoogleDrive-114825029448473821206/My Drive/LIGHT_GBM/H5_data/3lag_numpy_aug_for_final_LGBM/keep_inds_no_pole_hair_no_skip_frames_for_SPLIT_BY_TRIAL/FINAL_TEST_SPLIT_BY_TRIAL_FULL_TRIALS.h5'
# d = utils.h5_to_dict(h5_file)
# utils.info(d)
# utils.get_dict_info(d)


h5_file = '/Volumes/GoogleDrive-114825029448473821206/My Drive/LIGHT_GBM/H5_data/3lag_numpy_aug_for_final_LGBM/keep_inds_no_pole_hair_no_skip_frames_for_SPLIT_BY_TRIAL/FINAL_TEST_SPLIT_BY_TRIAL_FULL_TRIALS.h5'
# utils.print_h5_keys(h5_file)
# tmp1 = utils.getkey(h5_file, 'AH0407_160613_JC1003_AAAC_3lag.npy')

key_name = 'TEMP_yhat_full_192000_nan' # predictions
L_key_ = '[0, 1]- (no touch, touch)' # format of the predictions, wont change anything in this case but still needed
real_bool_key = 'full_test_labels'
kernel_size = 5
threshold = 0.5


# np.sum(utils.getkey(h5_file, 'pole_in_range')==1) # 14036
# np.sum(utils.getkey(h5_file, 'in_range_by_hand_192000')==1) # 114051
# np.sum(utils.getkey(h5_file, 'no_hair_inds')==1) # 174000

# L_key_ = None
fn_key = 'full_test_fn' #sum to 174000 becasue it removes one trial, use no_hair_inds on 192000 data to match it
in_range_key = 'in_range_by_hand_192000'
# in_range_key = 'in_range_by_hand_192000' # pole_in_range?????
#
# # tmp1 = utils.getkey(h5_file, 'pole_in_range')
# # plt.plot(tmp1)
"""##################################################################################################################"""
"""##################################################################################################################"""
pred_bool_temp = image_tools.get_h5_key_and_concatenate(h5_file, key_name)
pred_bool_temp = pred_bool_temp.astype(float)
pred_bool_smoothed = foo_arg_max_and_smooth(pred_bool_temp, kernel_size, threshold, key_name, L_key_=L_key_)

real_bool = image_tools.get_h5_key_and_concatenate(h5_file, real_bool_key)
# trial_nums_and_frame_nums = image_tools.get_h5_key_and_concatenate(h5_file, 'trial_nums_and_frame_nums')
# frame_nums = trial_nums_and_frame_nums[1, :].astype(int)
frame_nums = utils.getkey(h5_file, fn_key)

in_range = image_tools.get_h5_key_and_concatenate(h5_file, in_range_key)
"""##################################################################################################################"""
"""##################################################################################################################"""

all_h5s = utils.get_h5s(foo_rename('/content/gdrive/My Drive/Colab data/curation_for_auto_curator/finished_contacts/'),
                        print_h5_list=False)
tmp_h_cont, h_names = utils._get_human_contacts_(all_h5s)
"""##################################################################################################################"""
"""####################### correct 192000 dat to 17400 ##############################################################"""

"""##################################################################################################################"""
"""##################################################################################################################"""
data_key_inds = utils.lister_it(utils.print_h5_keys(h5_file, 1, 0), '.npy')
h_cont = []
for hi, key_i in zip(tmp_h_cont, data_key_inds):
    inds = utils.getkey(h5_file, key_i)==1
    x = hi[:, inds]
    h_cont.append(x)
human = np.hstack(h_cont)

no_hair_inds = utils.getkey(h5_file, 'no_hair_inds')

keep_inds = np.logical_and(no_hair_inds==1, in_range==1)==True

whacc = pred_bool_smoothed[keep_inds.astype(bool)]
human = human[:, keep_inds.astype(bool)]

human_mean = np.mean(human, axis=0)




def foo_agree_0_1(in1, in2):
    # full0agree = np.mean(1 * (in1 == 0) == 1 * (in2 == 0))
    # full1agree = np.mean(1 * (in1 == 1) == 1 * (in2 == 1))
    full0agree = np.mean((in1 == 0) == (in2 == 0))
    full1agree = np.mean((in1 == 1) == (in2 == 1))
    return full0agree, full1agree


# np.mean(full0agree)*100, np.mean(full1agree)*100
d = {'h0': [], 'h1': [],'w0': [], 'w1': []}
for i, a in enumerate(human):
    inds = np.ones(human.shape[0]).astype(bool)
    inds[i] = False
    tmp_mean = np.mean(human[inds], axis=0) # index out 2 human curator contacts
    full0agree, full1agree = foo_agree_0_1(a, tmp_mean) #comapre human to other 2 humans
    d['h0'].append(full0agree)
    d['h1'].append(full1agree)
    full0agree, full1agree = foo_agree_0_1(whacc, tmp_mean) #compare whac to other 2 humans
    d['w0'].append(full0agree)
    d['w1'].append(full1agree)

# df = pd.DataFrame(d)
# ax = sns.pointplot(x="h0", y="w0", data=df)
# ax = sns.pointplot(x="h1", y="w1", data=df)
#
# df = pd.DataFrame(d)
# ax = sns.scatterplot(x="h0", y="h1", data=df)
# ax = sns.scatterplot(x="w0", y="w1", data=df)
# plt.xlim([0.9930, .997])
# plt.ylim([0.9930, .997])


# np.mean(full0agree)*100, np.mean(full1agree)*100
d = {'percent correct':[], 'ind':[], 'label':[], 'class':[]}
for i, a in enumerate(human):
    inds = np.ones(human.shape[0]).astype(bool)
    inds[i] = False
    tmp_mean = np.mean(human[inds], axis=0)
    d['percent correct']+=list(foo_agree_0_1(a, tmp_mean))
    d['percent correct']+=list(foo_agree_0_1(whacc, tmp_mean))
    d['ind']+=[i]*4
    d['label']+=['human', 'human', 'WhACC', 'WhACC']
    d['class']+=['no touch', 'touch']*2

df = pd.DataFrame(d)
plt.figure(figsize=(7, 6))
ax = sns.pointplot(x="label", y="percent correct", hue="class", data=df, dodge=True)

plt.figure(figsize=(7, 6))
ax = sns.pointplot(x="label", y="percent correct", data=df, dodge=True)

plt.figure(figsize=(7, 6))
for k in range(3):
    ax = sns.pointplot(x="label", y="percent correct", data=df.loc[df['ind'] == k], dodge=True, ci=None)




def foo_agree_all(in1, in2):
    return np.mean(np.append([1 * (in1 == 0) == 1 * (in2 == 0)], [1 * (in1 == 1) == 1 * (in2 == 1)]))

d = {'percent correct':[], 'ind':[], 'label':[], 'class':[]}
for i, a in enumerate(human):
    inds = np.ones(human.shape[0]).astype(bool)
    inds[i] = False
    tmp_mean = np.mean(human[inds], axis=0)
    d['percent correct'].append(foo_agree_all(a, tmp_mean))
    d['percent correct'].append(foo_agree_all(whacc, tmp_mean))
    d['ind']+=[i]*2
    d['label']+=['human', 'WhACC']
    d['class']+=['all']*2


df = pd.DataFrame(d)
plt.figure(figsize=(7, 6))
ax = sns.pointplot(x="label", y="percent correct", data=df, dodge=True, ci = False, color='k', legend='sadf')

for k in range(3):
    ax = sns.pointplot(x="label", y="percent correct", data=df.loc[df['ind'] == k], dodge=True, ci=None, color='b')

custom_lines = [Line2D([0], [0], color='k', lw=4),
                Line2D([0], [0], color='b', lw=4)]
plt.legend(custom_lines, ['mean', 'individual'])



#######################################################################################################################
#######################################################################################################################
'''evaluate the total agree percentage of the touch count'''
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
d = dict()

""" touch count error version of the plot"""
from whacc import analysis
frame = frame_nums
human_performance = []
whacc_performance = []

human_temp = copy.deepcopy(list(human))

all_agree_inds = np.all(human[0] == human, axis = 0)
print('percent full agree ', np.mean(all_agree_inds))
d['percent humans full agree'] = np.mean(all_agree_inds)
d['humans full agree inds'] = all_agree_inds

human_temp2 = [k[all_agree_inds] for k in human_temp]
whacc2 = copy.deepcopy(whacc)[all_agree_inds]


d['percent whacc agree with human full agree'] = np.mean(whacc2==human_temp2[0])

utils.info(d)

#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
# # d = {'x' : [], 'and_or_labels':['human AND', 'human OR', 'WhACC AND', 'WhACC OR'],
# #                      'error_labels': ['ghost', 'miss', 'join', 'split', 'append++', 'deduct++', 'append', 'deduct']}
# d['error_type'] = []
# d['x'] = []
# for k in ['ghost', 'miss', 'join', 'split', 'append++', 'deduct++', 'append', 'deduct', 'pair_ind', 'human_or_whacc', 'and_or']:
#     d[k] = []
# """ touch count error version of the plot"""
# from whacc import analysis
# # frame = frame_nums
# human_performance = []
# whacc_performance = []
# for ind in range(3):
#     human_two = copy.deepcopy(list(human))
#     human_one = np.asarray(human_two.pop(ind))
#     human_two = np.asarray(human_two)
#
#     x_and = np.mean(human_two, axis = 0)
#     x_and[x_and<1] = 0
#
#     x_or = np.mean(human_two, axis = 0)
#     x_or[x_or>0] = 1
#
#     df_list = []
#     df_list.append(
#         analysis.thresholded_error_types(x_and, human_one, edge_threshold=4, frame_num_array=frame_nums, thresholds=[0.5]))
#     df_list.append(
#         analysis.thresholded_error_types(x_or, human_one, edge_threshold=4, frame_num_array=frame_nums, thresholds=[0.5]))
#     df_list.append(
#         analysis.thresholded_error_types(x_and, whacc, edge_threshold=4, frame_num_array=frame_nums, thresholds=[0.5]))
#     df_list.append(
#         analysis.thresholded_error_types(x_or, whacc, edge_threshold=4, frame_num_array=frame_nums, thresholds=[0.5]))
#
#     np.mean([df_list[0], df_list[1]], axis = 0)
#     np.mean([df_list[2], df_list[3]], axis = 0)
# # get TCerror for each and take the mean
#     plt.figure()
#     x = np.squeeze(np.asarray(df_list))
#     d['x'].append(x.T)
#     plt.plot(x.T, label = ['human AND', 'human OR', 'WhACC AND', 'WhACC OR'])
#     plt.xlabel(['ghost', 'miss', 'join', 'split', 'append++', 'deduct++', 'append', 'deduct'])
#     plt.legend()
#     print(np.max(np.max(x, axis = 0)[:-2]))
#     plt.ylim([0, 45])
#
# utils.info(d)
# type_compare = 'AND'
#
# and_or_inds = np.where([type_compare in k for k in d['and_or_labels']])[0]
# x2 = []
#
# for ii in range(3):
#     x = d['x'][ii][:, and_or_inds]
#     x2.append(x)
# for i, k in enumerate(d['error_labels']):
#     np.asarray(x2).T.shape # humans 1 to 3 , error type , human vs whacc



#######################################################################################################################
#######################################################################################################################
###########################$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$##########################################################

###########################$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$##########################################################

# d = {'x' : [], 'and_or_labels':['human AND', 'human OR', 'WhACC AND', 'WhACC OR'],
#                      'error_labels': ['ghost', 'miss', 'join', 'split', 'append++', 'deduct++', 'append', 'deduct']}
d = dict()
for k in ['ghost', 'miss', 'join', 'split', 'append++', 'deduct++', 'append', 'deduct', 'pair_ind', 'human_or_whacc', 'and_or']:
    d[k] = []
""" touch count error version of the plot"""
from whacc import analysis
# frame = frame_nums
human_performance = []
whacc_performance = []
for ind in range(3):
    human_two = copy.deepcopy(list(human))
    human_one = np.asarray(human_two.pop(ind))
    human_two = np.asarray(human_two)
    real_count = np.sum(np.diff(1*(np.mean(human, axis = 0)>.5))==1)
    x_and = np.mean(human_two, axis = 0)
    x_and[x_and<1] = 0
    and_count = np.sum(np.diff(x_and)==1)
    x_or = np.mean(human_two, axis = 0)
    x_or[x_or>0] = 1
    or_count = np.sum(np.diff(x_or)==1)
    print(real_count, and_count, or_count)

    df_list = []
    df_list.append(
        analysis.thresholded_error_types(x_and, human_one, edge_threshold=4, frame_num_array=frame_nums, thresholds=[0.5]))
    df_list.append(
        analysis.thresholded_error_types(x_or, human_one, edge_threshold=4, frame_num_array=frame_nums, thresholds=[0.5]))
    df_list.append(
        analysis.thresholded_error_types(x_and, whacc, edge_threshold=4, frame_num_array=frame_nums, thresholds=[0.5]))
    df_list.append(
        analysis.thresholded_error_types(x_or, whacc, edge_threshold=4, frame_num_array=frame_nums, thresholds=[0.5]))

    # np.mean([df_list[0], df_list[1]], axis = 0)
    # np.mean([df_list[2], df_list[3]], axis = 0)
    x = np.squeeze(np.asarray(df_list))
    x2 = []
    for kk, div_by in zip(x, [and_count, or_count, and_count, or_count]):
        x2.append(kk/div_by)
    x = np.asarray(x2)
    for ii, e_type in enumerate(['ghost', 'miss', 'join', 'split', 'append++', 'deduct++', 'append', 'deduct']):
        d[e_type].append(x[:, ii])
    d['human_or_whacc'].append(['human', 'human', 'WhACC', 'WhACC'])
    d['and_or'].append(['and', 'or', 'and', 'or'])
    d['pair_ind'].append([ind]*4)


for k in ['ghost', 'miss', 'join', 'split', 'append++', 'deduct++', 'append', 'deduct', 'pair_ind', 'human_or_whacc', 'and_or']:
    d[k] = np.concatenate(d[k])
df2 = pd.DataFrame(d)


plt.figure(figsize=(7, 6))
# ax = sns.pointplot(x="label", y="ghost", hue="class", data=df2, dodge=True)
ax = sns.pointplot(x="human_or_whacc", y="ghost", data=df2, dodge=True)

ax = sns.pointplot(x="human_or_whacc", y="ghost", data=df2, dodge=True)



plt.figure(figsize=(7, 6))
for k in range(3):
    x_in = df2.loc[np.logical_and(df2['pair_ind'] == k, df2['and_or'] == 'and')]
    ax = sns.pointplot(x='human_or_whacc', y='ghost', data=x_in, dodge=True, color = None, ci=None)


######
from matplotlib.pyplot import cm
n = 8
color = cm.tab10(np.linspace(0, 1, n))
# color = cm.jet(np.linspace(0, 1, n))

for i, c in zip(range(n), color):
   plt.scatter(i, i, c=c)

####

tmp1 = df2.iloc[:, :8].unstack().reset_index()
tmp2 = np.tile(np.asarray(df2.iloc[:, 8:]).T,8).T

for i, k in enumerate(['pair_ind', 'human_or_whacc', 'and_or']):
    tmp1[k] =tmp2[:, i]
tmp1['y'] = tmp1[0]
###########################$$$$$$$$$
plt.figure(figsize=(7, 6))
alpha = 0.3
for k in range(3):
    x_in = tmp1.loc[np.logical_and(tmp1['pair_ind'] == k, tmp1['and_or'] == 'and')]
    ax = sns.pointplot(x='human_or_whacc', y='y', data=x_in,  edgecolor=None, linewidth=0, markers='o', hue='level_0', dodge=True, palette=color, linestyles='', plot_kws=dict(alpha=alpha)) # plot_kws={'alpha':0.1}
plt.setp(ax.collections, alpha=alpha) #for the markers
plt.setp(ax.lines, alpha=alpha)       #for the lines
plt.legend('')


###
# ax = sns.scatterplot(x='human_or_whacc', y='y', data=x_in, hue='level_0', palette=color, dodge=True)
# plt.setp(ax.collections, alpha=alpha) #for the markers
# plt.setp(ax.lines, alpha=alpha)       #for the lines
# plt.legend('')
###########################$$$$$$$$$
# color[:, -1] = 1
hue_order = ['split', 'ghost', 'miss', 'join', 'deduct', 'append', 'deduct++', 'append++']
hue_order = ['split', 'ghost', 'miss', 'join', 'deduct++', 'append++', 'deduct', 'append']


x_in = tmp1.loc[tmp1['and_or'] == 'and']
ax = sns.pointplot(x='human_or_whacc', y='y', data=x_in, hue='level_0',hue_order=hue_order, dodge=False, ci=.95, palette=color)
plt.ylabel('Errors per touch'); plt.xlabel('');plt.ylim([0, .1])
###########################$$$$$$$$$

x2 = x_in.groupby(['human_or_whacc'])
sub_data = x2.get_group('WhACC').groupby('level_0').mean()['y'] - x2.get_group('human').groupby('level_0').mean()['y']

sub_data = pd.DataFrame(sub_data).reset_index()
# sub_data['index'] = [7, 4, 6, 5, 2, 0, 3, 1]
# sub_data = sub_data.set_index('index').sort()
#
# sub_data.sort_values(['index'])
sns.barplot(x = 'level_0', y = 'y', data=sub_data, palette=color, order=hue_order)
# plt.hlines(0, 0, 8, 'k')
plt.grid('on')
plt.ylabel('WhACC - Human (error rate)'); plt.xlabel('')

# plt.ylim([-.035, .035])

###########################$$$$$$$$$


# sub_data2 = np.asarray(x2.get_group('WhACC')['y']) - np.asarray(x2.get_group('human')['y'])
# plt.bar(range(len(sub_data2)), sub_data2)





x2 = x_in.groupby(['level_0', 'human_or_whacc'])
# x2.get_group()
x2.head(100)
x2.mean(['level_0'])

###########################$$$$$$$$$

###########################$$$$$$$$$


x_in = tmp1.loc[tmp1['and_or'] == 'and']
x_in = x_in.iloc[:36] # only TC errors

tmp3 = x_in.groupby(['pair_ind', 'human_or_whacc', 'level_0'])
tmp4 = tmp3['y'].mean()

tmp5 = tmp4.groupby(['pair_ind', 'human_or_whacc'])
tmp6 = tmp5.sum().reset_index()
tmp6 = pd.DataFrame(tmp6)
###########################$$$$$$$$$
ax = sns.pointplot(x='human_or_whacc', y='y', data=tmp6, dodge=True, ci=.95)
###########################$$$$$$$$$
for k in range(3):
    x_in = tmp6.loc[tmp6['pair_ind'] == k]
    ax = sns.pointplot(x='human_or_whacc', y='y', data=x_in, dodge=True, ci=None)

# ax = sns.pointplot(x='human_or_whacc', y='y', data=x_in, hue='level_0', dodge=True, ci=None)
###########################$$$$$$$$$

for k in range(3):
    x_in = tmp1.loc[np.logical_and(tmp1['pair_ind'] == k, tmp1['and_or'] == 'and')]
    ax = sns.pointplot(x='human_or_whacc', y='y', data=x_in, hue='level_0', dodge=True, ci=None)


ax = sns.pointplot(x='human_or_whacc', y='y', data=x_in, dodge=True)





tmp1 = df2.unstack().reset_index()
tmp1['data'] = tmp1[0]
ax = sns.pointplot(y='data', hue="level_0", data=tmp1, dodge=True)


###########################$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$##########################################################

###########################$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$##########################################################

#######################################################################################################################
#######################################################################################################################
#######################################################################################################################

""" touch count error version of the plot but with consensus rules and disagree touches are removed"""
from whacc import analysis

human_performance = []
whacc_performance = []
for ind in range(3):
    human_two = copy.deepcopy(list(human))
    human_one = np.asarray(human_two.pop(ind))
    human_two = list(np.asarray(human_two))

    inds = human_two[0] == human_two[1]

    human_two[0] = np.asarray(human_two[0])[inds]
    human_two[1] = np.asarray(human_two[1])[inds]
    human_one = human_one[inds]
    whacc_tmp = whacc[inds]


    x_conc = np.mean(human_two, axis = 0)
    x_conc[x_conc<1] = 0

    # x_or = np.mean(human_two, axis = 0)
    # x_or[x_or>0] = 1

    df_list = []
    df_list.append(
        analysis.thresholded_error_types(x_conc, human_one, edge_threshold=4, frame_num_array=frame, thresholds=[0.5]))
    # df_list.append(analysis.thresholded_error_types(x_or, human_one, edge_threshold=4, thresholds=[0.5]))
    df_list.append(
        analysis.thresholded_error_types(x_conc, whacc_tmp, edge_threshold=4, frame_num_array=frame, thresholds=[0.5]))
    # df_list.append(analysis.thresholded_error_types(x_or, whacc, edge_threshold=4, thresholds=[0.5]))

    np.mean([df_list[0], df_list[1]], axis = 0)
    # np.mean([df_list[2], df_list[3]], axis = 0)

# get TCerror for each and take the mean
    plt.figure()
    x = np.squeeze(np.asarray(df_list))
    plt.plot(x.T, label = ['human consensus', 'WhACC consensus'])
    plt.xlabel(['ghost', 'miss', 'join', 'split', 'append++', 'deduct++', 'append', 'deduct'])
    plt.legend()
    print(np.max(np.max(x, axis = 0)[:-2]))
    plt.ylim([0, 45])


