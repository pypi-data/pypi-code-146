
from whacc import utils
import numpy as np
from whacc.retrain_LGBM import retrain_LGBM

bd = '/Users/phil/Desktop/untitled folder/'
labels_key = 'labels'
h5_list = utils.get_files(bd, '*.h5')
tvt_x, tvt_y, tvt_fn, tvt_w = utils.load_training_and_curated_data(h5_list, labels_key)


model_base_dir = '/Users/phil/Desktop/tmp_mod_test/'
study_name = 'my_custom_optuna_models_test_V2'

#VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV
load_optuna_if_exists = False # change to true if continuing training<<<<<<<<<<<<<<<<
#AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA

rm = retrain_LGBM(model_base_dir, study_name, tvt_x, tvt_y, tvt_fn, tvt_w, load_optuna_if_exists=load_optuna_if_exists)

rm.GLOBALS['num_optuna_trials'] = 3  ########  20  3
rm.GLOBALS['early_stopping_rounds'] = 10  ########  100 10
rm.GLOBALS['num_iterations'] = 5 ########  10000 5




rm.train_model()
