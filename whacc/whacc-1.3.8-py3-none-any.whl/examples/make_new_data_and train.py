import numpy as np
import pandas as pd

import os
from whacc import utils, image_tools, analysis
from pathlib import Path
from whacc import analysis, model_maker

import numpy as np
import optuna

import lightgbm as lgb
import numpy as np
from sklearn import metrics
import pdb
from tqdm.autonotebook import tqdm
from whacc import analysis
import shutil
import h5py
import warnings
import matplotlib.pyplot as plt
from matplotlib import cm
from whacc import utils
import numpy as np
import matplotlib.pyplot as plt
import copy

from whacc.pole_tracker import PoleTracking
from whacc.touch_curation_GUI import touch_gui

################################################################################################
################################################################################################
############################ MAKE THE NEW TRAINING DATA  #######################################
################################################################################################
################################################################################################
################################################################################################

h5 = '/Volumes/GoogleDrive-114825029448473821206/.shortcut-targets-by-id/1pUteMEgx37rAyqujJWxVN9-ywFAqaxhF/WhACC_PROCESSING_FOLDER/Finished_Sessions/Session1_FINISHED/Session1/AH1179X23052021x1_final_combined.h5'
h5 = '/Volumes/GoogleDrive-114825029448473821206/.shortcut-targets-by-id/1pUteMEgx37rAyqujJWxVN9-ywFAqaxhF/WhACC_PROCESSING_FOLDER/Finished_Sessions/Session1/AH1179X23052021x1_final_combined.h5'
frame_nums = utils.getkey(h5, 'frame_nums')
equal_x_trial_inds = utils.equal_distance_pole_sample(h5, num_videos=3, equal_x=True)

vid_dir = '/Volumes/GoogleDrive-114825029448473821206/.shortcut-targets-by-id/1pUteMEgx37rAyqujJWxVN9-ywFAqaxhF/WhACC_PROCESSING_FOLDER/Session1_FINISHED_MP4s/Session1/'
vid_dir = '/Volumes/GoogleDrive-114825029448473821206/.shortcut-targets-by-id/1pUteMEgx37rAyqujJWxVN9-ywFAqaxhF/WhACC_PROCESSING_FOLDER/Finished_mp4s/Session1_FINISHED_MP4s/Session1'
num_trials_per_session, start_frame, end_frame = 10, 1300, 1310
base_dir = '/Users/phil/Desktop/untitled folder'
mod_str = '/Volumes/GoogleDrive-114825029448473821206/My Drive/WhACC_DATA_FINAL_WITH_AUG/final_optuna_models/ALL_optuna_samson_all_sessions_100_trials_10_frames_each__weightedx10_V4__000_model.pkl'

utils.make_transfer_learning_data(h5, start_frame, end_frame, equal_x_trial_inds, vid_dir=vid_dir, base_dir=base_dir,
                                  final_trimmed_h5_name=None, overwrite=True, model_full_file_name=mod_str)

################################################################################################
################################################################################################
############################ CURATE THE DATA USING THE GUI TOOL,     ###########################
################################DON'T FORGET TO SAVE IT          ###############################
################################################################################################
################################################################################################
h5_ind_to_curate = 0  # go through all these curate and save
base_dir = '/Users/phil/Desktop/untitled folder'
h5_list = utils.get_files(base_dir, '*.h5')
label_read_key = 'labels'
label_write_key = 'human_labels'
touch_gui(h5_list[h5_ind_to_curate], label_read_key, image_read_key='images', label_write_key=label_write_key)

################################################################################################
################################################################################################
############################ FINAL LOADING AND APPENDING THE TL DATA ###########################
################################################################################################
################################################################################################
################################################################################################


bd = '/Users/phil/Desktop/untitled folder/'
labels_key = 'labels'
train_val_split = [7, 3]
h5_list = utils.get_files(bd, '*.h5')
tvt_x, tvt_y, tvt_fn, tvt_w = utils.load_training_and_curated_data(h5_list, labels_key, train_val_split=train_val_split,
                                                                   nan_ify_data=True, new_data_weight=2)

################################################################################################
################################################################################################
############################         TRAIN MODEL USING OPTUNA        ###########################
################################################################################################
################################################################################################
################################################################################################

import numpy as np
import pandas as pd

import os
from whacc import utils, image_tools, analysis
from pathlib import Path
from whacc import analysis

import numpy as np
import optuna

import lightgbm as lgb
import numpy as np
from sklearn import metrics
import pdb
from tqdm.autonotebook import tqdm
from whacc import analysis
import shutil
import h5py

import matplotlib.pyplot as plt
from whacc.utils import *


def reset_metrics():
    def callback(env):
        mod_dir = GLOBALS__________['mod_dir']
        edge_threshold = GLOBALS__________['edge_threshold']
        thresholds = GLOBALS__________['thresholds']
        smooth_by = GLOBALS__________['smooth_by']

        real = GLOBALS__________['tvt_y'][2]
        touch_count = np.sum(np.diff(real) == 1)
        frame_nums = GLOBALS__________['tvt_fn'][2]
        yhat = env.model.predict(GLOBALS__________['tvt_x'][2])
        yhat_proba = smooth(yhat, smooth_by)
        df = analysis.thresholded_error_types(real, yhat_proba, edge_threshold=edge_threshold,
                                              frame_num_array=frame_nums, thresholds=thresholds)
        df2 = df.iloc[:, :-2] / touch_count
        x = df2.sum(axis=1)
        err = x.min()

        GLOBALS__________['all_errors_test'].append(df)
        GLOBALS__________['metrics_test']['auc'].append(metrics.roc_auc_score(real, yhat))
        GLOBALS__________['metrics_test']['touch_count_errors_per_touch'].append(err)
        GLOBALS__________['metrics_test']['best_threshold'].append(thresholds[x.argmin()])

    return callback


def thresholded_error_types(yhat, dmat):
    ######################## SHOULDNT CHANGE
    frame_nums_val = GLOBALS__________['tvt_fn'][1]
    mod_dir = GLOBALS__________['mod_dir']
    higher_is_better = False
    edge_threshold = GLOBALS__________['edge_threshold']
    thresholds = GLOBALS__________['thresholds']
    smooth_by = GLOBALS__________['smooth_by']
    ######################## SHOULDNT CHANGE -- CALC TCerr
    yhat_proba = smooth(yhat, smooth_by)
    real = dmat.get_label() if isinstance(dmat, lgb.Dataset) else dmat
    touch_count = np.sum(np.diff(real) == 1)
    #     with HiddenPrints():
    df = analysis.thresholded_error_types(real, yhat_proba,
                                          edge_threshold=edge_threshold,
                                          frame_num_array=frame_nums_val,
                                          thresholds=thresholds)
    df2 = df.iloc[:, :-2] / touch_count
    x = df2.sum(axis=1)
    err = x.min()
    ######################## THE REST IS SAVING AND RETURN FOR LGBM EVAL
    GLOBALS__________['all_errors'].append(df)
    GLOBALS__________['metrics']['auc'].append(metrics.roc_auc_score(real, yhat))
    GLOBALS__________['metrics']['touch_count_errors_per_touch'].append(err)
    GLOBALS__________['metrics']['best_threshold'].append(thresholds[x.argmin()])
    if 'basic_info' not in list(GLOBALS__________.keys()):
        GLOBALS__________['basic_info'] = dict()
    GLOBALS__________['basic_info']['threshold'] = thresholds
    GLOBALS__________['basic_info']['higher_is_better'] = higher_is_better
    GLOBALS__________['basic_info']['edge_threshold'] = edge_threshold
    GLOBALS__________['basic_info']['touch_count'] = touch_count
    GLOBALS__________['basic_info']['real_human_predictions'] = real
    GLOBALS__________['basic_info']['smooth_by'] = smooth_by
    GLOBALS__________['basic_info']['num_optuna_trials'] = GLOBALS__________['num_optuna_trials']
    GLOBALS__________['basic_info']['early_stopping_rounds'] = GLOBALS__________['early_stopping_rounds']
    GLOBALS__________['basic_info']['num_iterations'] = GLOBALS__________['num_iterations']
    GLOBALS__________['basic_info']['num_optuna_trials'] = GLOBALS__________['num_optuna_trials']
    return "touch_count_errors", err, higher_is_better


def objective(trial):
    d = utils.load_feature_data()
    names = np.asarray(d['full_feature_names_and_neuron_nums'])
    final_feature_names_USE = list(names[d['final_selected_features_bool']])
    train_DATA = lgb.Dataset(GLOBALS__________['tvt_x'][0], label=GLOBALS__________['tvt_y'][0],
                             feature_name=final_feature_names_USE, weight=GLOBALS__________['tvt_w'][0])
    val_DATA = lgb.Dataset(GLOBALS__________['tvt_x'][1], label=GLOBALS__________['tvt_y'][1],
                           feature_name=final_feature_names_USE, reference=train_DATA,
                           weight=GLOBALS__________['tvt_w'][1])

    param = {
        "objective": "binary",
        "metric": "auc",
        "verbosity": -1,
        "boosting_type": "gbdt",
        "early_stopping_rounds": GLOBALS__________['early_stopping_rounds'],
        "num_iterations": GLOBALS__________['num_iterations'],
        "lambda_l1": trial.suggest_float("lambda_l1", 1e-8, 10.0, log=True),
        "lambda_l2": trial.suggest_float("lambda_l2", 1e-8, 10.0, log=True),
        "num_leaves": trial.suggest_int("num_leaves", 2, 256),
        "feature_fraction": trial.suggest_float("feature_fraction", 0.4, 1.0),
        "bagging_fraction": trial.suggest_float("bagging_fraction", 0.4, 1.0),
        "bagging_freq": trial.suggest_int("bagging_freq", 1, 7),
        "min_child_samples": trial.suggest_int("min_child_samples", 5, 100),
        #         'first_metric_only' : True,
    }

    ######################## INIT THE LISTS FOR SAVING LATER

    GLOBALS__________['metrics'] = dict()
    GLOBALS__________['metrics']['auc'] = []
    GLOBALS__________['metrics']['touch_count_errors_per_touch'] = []
    GLOBALS__________['metrics']['best_threshold'] = []
    GLOBALS__________['all_errors'] = []

    GLOBALS__________['metrics_test'] = dict()
    GLOBALS__________['metrics_test']['auc'] = []
    GLOBALS__________['metrics_test']['touch_count_errors_per_touch'] = []
    GLOBALS__________['metrics_test']['best_threshold'] = []
    GLOBALS__________['all_errors_test'] = []

    gbm = lgb.train(
        param,
        train_DATA,
        valid_sets=[val_DATA],
        feval=thresholded_error_types,
        callbacks=[reset_metrics()],
    )

    preds = gbm.predict(GLOBALS__________['tvt_x'][1])
    fpr, tpr, thresholds_auc = metrics.roc_curve(GLOBALS__________['tvt_y'][1], preds, pos_label=1)
    AUC_out = metrics.auc(fpr, tpr)

    # save the model
    mod_num = str(len(utils.get_files(GLOBALS__________['mod_dir'], '*_model.pkl'))).zfill(3)
    fn = GLOBALS__________['mod_dir'] + mod_num + '_model.pkl'
    utils.save_obj(gbm, fn)

    d = dict()
    d['metrics'] = GLOBALS__________['metrics']
    d['all_errors'] = GLOBALS__________['all_errors']
    d['metrics_test'] = GLOBALS__________['metrics_test']
    d['all_errors_test'] = GLOBALS__________['all_errors_test']

    fn = GLOBALS__________['mod_dir'] + mod_num + '_model_results.pkl'
    utils.save_obj(d, fn)

    if mod_num == '000':
        fn = GLOBALS__________['mod_dir'] + 'basic_info.pkl'
        utils.save_obj(GLOBALS__________['basic_info'], fn)

    return AUC_out


# bd = '/Users/phil/Desktop/untitled folder/'
# labels_key = 'labels'
# h5_list = utils.get_files(bd, '*.h5')
# tvt_x, tvt_y, tvt_fn, tvt_w = load_training_and_curated_data(h5_list, labels_key)


GLOBALS__________ = dict()
######################## model save directory
bd = '/Users/phil/Desktop/tmp_mod_test/'
study_name = 'my_custom_optuna_models'

GLOBALS__________['mod_dir'] = bd + os.sep + study_name + os.sep

GLOBALS__________['num_optuna_trials'] = 20  ########  20
GLOBALS__________['early_stopping_rounds'] = 10  ########  100
GLOBALS__________['num_iterations'] = 10000
######################## USER SETTING AFFECTING THE FINAL EVAL RESULTS
GLOBALS__________['edge_threshold'] = 5
GLOBALS__________['thresholds'] = np.linspace(0.4, .8, 5)
GLOBALS__________['smooth_by'] = 5
########################
GLOBALS__________['tvt_x'] = tvt_x
GLOBALS__________['tvt_y'] = tvt_y
GLOBALS__________['tvt_fn'] = tvt_fn

GLOBALS__________['tvt_w'] = tvt_w
########################
GLOBALS__________['study_name'] = study_name
GLOBALS__________['storage_dir'] = GLOBALS__________['mod_dir']
GLOBALS__________['basic_info'] = dict()

load_if_exists = True
mod_dir = GLOBALS__________['mod_dir']
if os.path.isdir(mod_dir):
    inp = input('directory exists already, type "delete" to delete existing training folder')
    if inp.lower() == 'delete':
        shutil.rmtree(mod_dir)
        print('directory was deleted and remade ready to run!')
    else:
        assert False, "directory already exists stopping training "

make_path(mod_dir)

if __name__ == "__main__":
    study_name = GLOBALS__________['study_name']
    storage_dir = GLOBALS__________['storage_dir']

    storage = f"sqlite:///{storage_dir}/OPTUNA_SAVE_{study_name}.db"

    study = optuna.create_study(study_name=study_name, storage=storage, direction="maximize",
                                load_if_exists=load_if_exists)

    study.optimize(objective, n_trials=GLOBALS__________['num_optuna_trials'], timeout=None, n_jobs=1,
                   show_progress_bar=True)

    print("Number of finished trials: {}".format(len(study.trials)))

    print("Best trial:")
    trial = study.best_trial

    print("  Value: {}".format(trial.value))

    print("  Params: ")
    for key, value in trial.params.items():
        print("    {}: {}".format(key, value))

################################################################################################
################################################################################################
############################         plot the best models        ###########################
################################################################################################
################################################################################################
################################################################################################
d2 = d_all
# make fig and axis
fig, ax1 = plt.subplots(figsize=[20, 5])
ax2 = ax1.twinx()
# setup colors
inds = np.linspace(.15, .95, len(loop_peaks))
Blues = cm.get_cmap('Blues')([inds])
Reds = cm.get_cmap('Reds')([inds])

color = Blues[0][i]
ax1.set_ylabel('1-auc', color=color)  # we already handled the x-label with ax1
ax1.plot(1 - d2['auc'], color=color)
ax1.tick_params(axis='y', labelcolor=color)

color = Reds[0][i]
ax2.set_xlabel('touch_count_errors_per_touch')
ax2.set_ylabel('touch_count_errors_per_touch', color=color)
ax2.plot(d2['touch_count_errors_per_touch'], color=color)
plt.text(len(d2['touch_count_errors_per_touch']), d2['touch_count_errors_per_touch'][-1], str(i))
ax2.tick_params(axis='y', labelcolor=color)


def foo_plot2(d, early_stopping_num, loop_peaks=None):
    x = np.diff(1 - d['auc'])
    peaks = np.where(x > 0.001)[0] + 1
    if loop_peaks is None:
        loop_peaks = np.diff([0] + list(peaks) + [len(d['auc'])])
    fig, ax1 = plt.subplots(figsize=[20, 5])
    ax2 = ax1.twinx()
    # tot = len(loop_peaks)

    inds = np.linspace(.15, .95, len(loop_peaks))
    Blues = cm.get_cmap('Blues')([inds])
    Reds = cm.get_cmap('Reds')([inds])

    for i, (k1, k2) in enumerate(utils.loop_segments(loop_peaks)):
        d2 = {'auc': d['auc'][k1:k2], 'touch_count_errors_per_touch': d['touch_count_errors_per_touch'][k1:k2]}
        color = Blues[0][i]
        ax1.set_ylabel('1-auc', color=color)  # we already handled the x-label with ax1
        ax1.plot(1 - d2['auc'], color=color)
        ax1.tick_params(axis='y', labelcolor=color)

        color = Reds[0][i]
        ax2.set_xlabel('touch_count_errors_per_touch')
        ax2.set_ylabel('touch_count_errors_per_touch', color=color)
        ax2.plot(d2['touch_count_errors_per_touch'], color=color)
        plt.text(len(d2['touch_count_errors_per_touch']), d2['touch_count_errors_per_touch'][-1], str(i))
        ax2.tick_params(axis='y', labelcolor=color)

        L = len(d2['auc'])

        b = np.argmin(1 - d2['auc'][-early_stopping_num:])
        b = np.arange(early_stopping_num)[b]
        a = b + L - early_stopping_num
        ax1.plot(a, 1 - d2['auc'][a], 'g.')

        b = np.argmin(d2['touch_count_errors_per_touch'][-early_stopping_num:])
        b = np.arange(early_stopping_num)[b]
        a = b + L - early_stopping_num
        ax2.plot(a, d2['touch_count_errors_per_touch'][a], 'g.')

        # b = np.argmin(np.flip(1-d2['auc'][-early_stopping_num:]))
        # b = np.flip(np.arange(early_stopping_num))[b]
        # a = b+L-early_stopping_num
        # ax1.plot(a, 1-d2['auc'][a], 'g.')
        #
        # b = np.argmin(np.flip(d2['touch_count_errors_per_touch'][-early_stopping_num:]))
        # b = np.flip(np.arange(early_stopping_num))[b]
        # a = b+L-early_stopping_num
        # ax2.plot(a, d2['touch_count_errors_per_touch'][a], 'g.')
    plt.grid()
    return ax1, ax2


def plot2(d, loop_peaks=None, early_stopping_num=None):
    from matplotlib import cm
    if early_stopping_num is None:
        early_stopping_num = 500
    x = np.diff(1 - d['auc'])
    peaks = np.where(x > 0.001)[0] + 1
    if loop_peaks is None:
        loop_peaks = np.diff([0] + list(peaks) + [len(d['auc'])])
    fig, ax1 = plt.subplots(figsize=[20, 5])
    ax2 = ax1.twinx()
    tot = len(loop_peaks)

    inds = np.linspace(.15, .95, len(loop_peaks))
    Blues = cm.get_cmap('Blues')([inds])
    Reds = cm.get_cmap('Reds')([inds])

    for i, (k1, k2) in enumerate(utils.loop_segments(loop_peaks)):
        # c1 = i+1/tot

        d2 = {'auc': d['auc'][k1:k2], 'touch_count_errors_per_touch': d['touch_count_errors_per_touch'][k1:k2]}
        color = Blues[0][i]
        ax1.set_ylabel('1-auc', color=color)  # we already handled the x-label with ax1
        ax1.plot(1 - d2['auc'], color=color)
        ax1.tick_params(axis='y', labelcolor=color)

        color = Reds[0][i]
        ax2.set_xlabel('touch_count_errors_per_touch')
        ax2.set_ylabel('touch_count_errors_per_touch', color=color)
        ax2.plot(d2['touch_count_errors_per_touch'], color=color)
        plt.text(len(d2['touch_count_errors_per_touch']), d2['touch_count_errors_per_touch'][-1], str(i))
        ax2.tick_params(axis='y', labelcolor=color)

        L = len(d2['auc'])

        b = np.argmin(np.flip(1 - d2['auc'][-early_stopping_num:]))
        b = np.flip(np.arange(early_stopping_num))[b]
        a = b + L - early_stopping_num
        ax1.plot(a, 1 - d2['auc'][a], 'g.')

        b = np.argmin(np.flip(d2['touch_count_errors_per_touch'][-early_stopping_num:]))
        b = np.flip(np.arange(early_stopping_num))[b]
        a = b + L - early_stopping_num
        ax2.plot(a, d2['touch_count_errors_per_touch'][a], 'g.')
    plt.grid()
    return ax1, ax2


def foo_best_ind(metric_in, min_or_max='min'):
    if min_or_max == 'min':
        return np.argmin([np.min(k) for k in metric_in])
    elif min_or_max == 'max':
        return np.argmax([np.max(k) for k in metric_in])
    else:
        assert False, 'oops'


def load_model_results(bd):
    results_list = []
    model_number = []
    for k in tqdm(utils.sort(utils.get_files(bd, '*_model_results.pkl'))):
        results_list.append(utils.load_obj(k))
        model_number.append(int(os.path.basename(k)[:3]))
    d_out = {}
    d_out['model_number'] = model_number
    d_out['validation'] = {}
    d_out['test'] = {}

    d_out['validation']['auc'] = np.asarray([np.asarray(k['metrics']['auc']) for k in results_list], dtype=object)
    d_out['test']['auc'] = np.asarray([np.asarray(k['metrics_test']['auc']) for k in results_list], dtype=object)
    d_out['validation']['TCE'] = np.asarray(
        [np.asarray(k['metrics']['touch_count_errors_per_touch']) for k in results_list], dtype=object)
    d_out['test']['TCE'] = np.asarray(
        [np.asarray(k['metrics_test']['touch_count_errors_per_touch']) for k in results_list], dtype=object)
    d_out['trial_lengths'] = [len(k) for k in d_out['validation']['auc']]

    d_out['validation']['best_auc_mod_ind'] = foo_best_ind(d_out['validation']['auc'], 'max')
    d_out['test']['best_auc_mod_ind'] = foo_best_ind(d_out['test']['auc'], 'max')
    d_out['validation']['best_TCE_mod_ind'] = foo_best_ind(d_out['validation']['TCE'], 'min')
    d_out['test']['best_TCE_mod_ind'] = foo_best_ind(d_out['test']['TCE'], 'min')
    d_out['best_mod_inds'] = [d_out['validation']['best_auc_mod_ind'], d_out['test']['best_auc_mod_ind'],
                              d_out['validation']['best_TCE_mod_ind'], d_out['test']['best_TCE_mod_ind']]

    d_out['best_iteration'] = []
    d_out['model_list_full_path'] = utils.sort(utils.get_files(bd, '*model.pkl'))
    for mod in tqdm(d_out['model_list_full_path']):
        mod = utils.load_obj(mod)
        d_out['best_iteration'].append(mod.best_iteration-1)
    d_out['basic_info'] = utils.load_obj(bd + '/basic_info.pkl')

    inds = np.linspace(.15, .95, len(d_out['validation']['auc']))

    d_out['colors'] = {}
    d_out['colors']['blues'] = cm.get_cmap('Blues')([inds])[0]
    d_out['colors']['reds'] = cm.get_cmap('Reds')([inds])[0]
    return d_out


bd = '/Users/phil/Desktop/tmp_mod_test/my_custom_optuna_models/'
d_all = load_model_results(bd)

utils.info(d_all)
utils.info(d_all['validation'])
utils.info(d_all['test'])
utils.info(d_all['basic_info'])

data_key = 'validation'
mod_inds_to_plot = None
plot_model_number_text = True
auto_set_y = True

def foo_plot_final(d_all, data_key='validation', mod_inds_to_plot=None, plot_model_number_text=True, auto_set_y=True):
    def best_mod_ind_location_plot(x, early_stopping_rounds):
        early_stopping_rounds+=1
        L = len(x)
        b = np.argmin(x[-early_stopping_rounds:])
        b = np.arange(early_stopping_rounds)[b]
        a = b + L - early_stopping_rounds
        return a, x[a]

    # make fig and axis
    early_stopping_rounds = d_all['basic_info']['early_stopping_rounds']
    fig, ax1 = plt.subplots(figsize=[20, 5])
    ax2 = ax1.twinx()
    d = d_all[data_key]
    if mod_inds_to_plot is None:
        mod_inds_to_plot = range(len(d['auc']))
    assert np.max(mod_inds_to_plot) <= len(
        d['auc']), """'mod_inds_to_plot' must not have inds larger than the number of models trained"""
    mod_inds_to_plot = np.sort(mod_inds_to_plot)
    color = d_all['colors']['blues']
    y_set = []
    for i in mod_inds_to_plot:
        x = 1 - d['auc'][i]
        ax1.plot(x, color=color[i])
        y_set.append(np.min(1 - d['auc'][i]))
        x1, y1 = best_mod_ind_location_plot(x, early_stopping_rounds)
        ax1.plot(x1, y1, 'g.')
        x2 = d_all['best_iteration'][i]
        if x2 == x1:
            ax1.plot(x2, y1, 'g*')
    ax1.set_ylabel('1-auc', color=color[-1])  # we already handled the x-label with ax1
    ax1.tick_params(axis='y', labelcolor=color[-1])
    if auto_set_y:
        ax1.set_ylim([np.min(y_set) * .75, np.max(y_set) * 1.05])

    color = d_all['colors']['reds']
    y_set = []
    for i in mod_inds_to_plot:
        x = d['TCE'][i]
        ax2.plot(x, color=color[i])
        y_set.append(np.min(d['TCE'][i]))
        x1, y1 = best_mod_ind_location_plot(x, early_stopping_rounds)
        ax2.plot(x1, y1, 'g.')
        x2 = d_all['best_iteration'][i]
        if x2 == x1:
            ax2.plot(x2, y1, 'g*')
        print(x1, y1)
        if plot_model_number_text:
            props = dict(boxstyle='round', facecolor='gray', alpha=0.5)

            plt.text(len(d['TCE'][i])-.9, d['TCE'][i][-1], str(d_all['model_number'][i]),  bbox=props)
    ax2.set_ylabel('touch count errors per touch', color=color[-1])
    ax2.tick_params(axis='y', labelcolor=color[-1])
    if auto_set_y:
        scale_by= 1.25
        ax2.set_ylim([np.min(y_set) * (1/scale_by), np.max(y_set) * scale_by])
    plt.xlabel('Boosting Iterations')

    return ax1, ax2


data_key = 'validation'
mod_inds_to_plot = [1, 10, 19]
plot_model_number_text = True
auto_set_y = True
ax1, ax2 = foo_plot_final(d_all, data_key=data_key, mod_inds_to_plot=mod_inds_to_plot,
               plot_model_number_text=plot_model_number_text, auto_set_y=auto_set_y)





d_all['best_iteration'][1]
np.asarray(d_all['best_iteration'])[mod_inds_to_plot]

mod = utils.load_obj(np.asarray(d_all['model_list_full_path'])[mod_inds_to_plot][0])
yhat = mod.predict(tvt_x[1])
y = tvt_y[1]


auc = metrics.roc_auc_score(y, yhat)
ax1.plot(35, 1-auc, 'r.')

# tvt_x, tvt_y, tvt_fn, tvt_w





"""
so i htink that the best model is correct which makes sense because its a pro package 
the ind is incorrect thought so I will have to plot a -1 form the best ind I THINK 
verify this...

also i need ot make the GLOBAL____ variable a class init self variable
"""









ax2.set_xlabel('touch_count_errors_per_touch')
ax2.set_ylabel('touch_count_errors_per_touch', color=color)
ax2.plot(d2['touch_count_errors_per_touch'], color=color)
plt.text(len(d2['touch_count_errors_per_touch']), d2['touch_count_errors_per_touch'][-1], str(i))
ax2.tick_params(axis='y', labelcolor=color)

select_mods_2_plot = [0, 1, 2]
d = dict()
d['auc'] = np.concatenate(np.asarray(d_all['val_auc'])[select_mods_2_plot])
d['touch_count_errors_per_touch'] = np.concatenate(np.asarray(d_all['val_TCE'])[select_mods_2_plot])
early_stopping = 20
"""

change the d['auc'] and d['touch_count_errors_per_touch']  to seperate inputs of just auc and touch_count_errors_per_touch
and then iterate over each set for val and test and done 
"""
d_all['auc'] = d_all['val_auc']

loop_peaks = d_all['trial_lengths']
early_stopping_num = basic_info['early_stopping_rounds']
# ax1, ax2 = foo_plot2(d)
ax1, ax2 = foo_plot2(d, early_stopping_num, loop_peaks=loop_peaks)

from whacc import utils

tmp1 = utils.load_obj('/Users/phil/Desktop/tmp_mod_test/my_custom_optuna_models/basic_info.pkl')
utils.info(tmp1)

################################################################################################
################################################################################################
############################         plot models actual performance        ###########################
################################## to see where it matches with the traces ########################
################################################################################################
################################################################################################
bd = '/Users/phil/Desktop/tmp_mod_test/my_custom_optuna_models/'
for mod in utils.sort(utils.get_files(bd, '*model.pkl')):
    print(mod)
    mod = utils.load_obj(mod)
    bi = mod.best_iteration
    print(bi)

mod = utils.load_obj(mod)

utils.info(mod)

mod.best_iteration
"""
fixed the matching now it aut finds the best model and I can plot the best model iteration in the final plot as well
seen above here 
"""
