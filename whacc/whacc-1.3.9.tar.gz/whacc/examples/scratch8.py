# # # # from whacc import utils, image_tools
# # # #
# # # # import copy
# # # # import numpy as np
# # # # import pandas as pd
# # # # import h5py
# # # #
# # # # from tqdm.autonotebook import tqdm
# # # #
# # # #
# # # # class feature_maker():
# # # #     def __init__(self, h5_in, frame_num_ind=None, frame_nums=None, operational_key='FD__original', disable_tqdm=False,
# # # #                  delete_if_exists=False, index_features_delete_the_rest=None):
# # # #         """
# # # #
# # # #         Parameters
# # # #         ----------
# # # #         h5_in : h5 string pointing to the h4 file with the data to transform
# # # #         frame_num_ind : int referencing the frame num  ind to transform, note: if save_it is one ALL data is converted
# # # #         automatically and saved in h5. frame_num_ind only works when you call with
# # # #         frame_nums : default None, auto looks for key 'frame_nums' in h5 file or you can insert your own
# # # #         operational_key : the data array key to be transformed
# # # #         disable_tqdm : default False, when save_it is True it will show a loading bar with the progress unless set to true
# # # #         delete_if_exists : default False, when calling a function with save_it as True, you can choose to overwrite that
# # # #         data by setting this value to True
# # # #
# # # #         Returns
# # # #         -------
# # # #         feature maker class
# # # #
# # # #         Examples
# # # #         ________
# # # #
# # # #         h5_in = '/Users/phil/Desktop/AH0407_160613_JC1003_AAAC_3lag.h5'
# # # #
# # # #         FM = feature_maker(h5_in, frame_num_ind=2, delete_if_exists = True) #set frame_num_ind to an int so that we can quickly look at the transformation
# # # #         data, data_name = FM.shift(5, save_it=False) # shift it 5 to the right, fills in with nan as needed, look at just the 5th frame num set (5th video)
# # # #         # to see how it looks
# # # #         print('the below name will be used to save the data in the the h5 when calling functions with save_it=True')
# # # #         print(data_name)
# # # #         FM.shift(5, save_it=True) # now lets save it
# # # #
# # # #         data, data_name_rolling_mean_100 = FM.rolling(100, 'mean', save_it=True)  #lets do the rolling mean and save it
# # # #
# # # #         data, data_name = FM.operate('diff', kwargs={'periods': 1}, save_it=False) # lets perform a diff operation
# # # #         print(data_name)
# # # #         print(data)
# # # #         FM.operate('diff', kwargs={'periods': -1}, save_it=True) # now lets save it and save it
# # # #
# # # #         # now lets change the operational key so we can transform some data we just transformed, specifically the rolling mean 10
# # # #         FM.set_operation_key(data_name_rolling_mean_100)
# # # #
# # # #         data, data_name_diff_100_mean = FM.operate('diff', kwargs={'periods': -50}, save_it=False) # lets check how the name will change
# # # #         print(data_name_diff_100_mean)
# # # #         print("notice the FD__ twice, this means the data has been transformed twice")
# # # #         print('also notice that how the data was transformed can be seen because it is split up by ____ (4 underscores)')
# # # #
# # # #         data, data_name_diff_100_mean = FM.operate('diff', kwargs={'periods': -50}, save_it=True) # save it
# # # #
# # # #         a = utils.print_h5_keys(h5_in, 1, 1)
# # # #         key_name_list = ['FD__original', 'FD__FD__FD__original_rolling_mean_W_100_SFC_0_MP_100_____diff_periods_-50____', 'FD__FD__original_rolling_mean_W_100_SFC_0_MP_100____']
# # # #         with h5py.File(h5_in, 'r+') as h:
# # # #             for k in key_name_list:
# # # #                 plt.plot(h[k][:8000, 0])
# # # #         """
# # # #         if utils.h5_key_exists(h5_in, 'has_data_been_randomized'):
# # # #             assert image_tools.get_h5_key_and_concatenate(h5_in,
# # # #                                                           'has_data_been_randomized').tolist() is False, """this data has been randomized, it is not fit to perform temporal operations on, search for key 'has_data_been_randomized' for more info"""
# # # #
# # # #         self._frame_num_ind_save_ = None
# # # #         self.disable_tqdm = disable_tqdm
# # # #         self.h5_in = h5_in
# # # #         self.frame_num_ind = frame_num_ind
# # # #         self.delete_if_exists = delete_if_exists
# # # #         self.operational_key = operational_key
# # # #         if frame_nums is None:
# # # #             print('extracting frame_nums from h5 file, ideally you should just put that in yourself though')
# # # #             frame_nums = image_tools.get_h5_key_and_concatenate(h5_in, 'frame_nums')
# # # #         self.all_frame_nums = frame_nums
# # # #         self.len_frame_nums = len(self.all_frame_nums)
# # # #         self.set_data_and_frame(frame_num_ind)
# # # #         index_features_delete_the_rest
# # # #
# # # #     def set_data_inds(self, ind):  # frame nums used ot extract below in 'set_operation_key'
# # # #         tmp_inds = np.asarray(utils.loop_segments(self.all_frame_nums, returnaslist=True))
# # # #         if ind is None:
# # # #             self.data_inds = [tmp_inds[0][0], tmp_inds[-1][-1]]
# # # #         else:
# # # #             self.data_inds = tmp_inds[:, ind]
# # # #
# # # #     def set_operation_key(self, key_name=None):
# # # #         if key_name is not None:
# # # #             self.operational_key = key_name
# # # #         with h5py.File(self.h5_in, 'r') as h:
# # # #             self.full_data_shape = np.asarray(h[self.operational_key].shape)
# # # #             if self.frame_num_ind is None:
# # # #                 self.data = pd.DataFrame(copy.deepcopy(h[self.operational_key][:]))
# # # #             else:
# # # #                 a = self.data_inds  # just the current frame numbers
# # # #                 self.data = pd.DataFrame(copy.deepcopy(h[self.operational_key][a[0]:a[1]]))
# # # #
# # # #     def init_h5_data_key(self, data_key, delete_if_exists=False):
# # # #         key_exists = utils.h5_key_exists(self.h5_in, data_key)
# # # #         assert not (
# # # #                 key_exists and not delete_if_exists), "key exists, if you want to overwrite set 'delete_if_exists' = True"
# # # #         with h5py.File(self.h5_in, 'r+') as x:
# # # #             if key_exists and delete_if_exists:
# # # #                 print('deleting key to overwrite it')
# # # #                 del x[data_key]
# # # #             x.create_dataset_like(data_key, x[self.operational_key])
# # # #
# # # #     def rolling(self, window, operation, shift_from_center=0, min_periods=None, save_it=False, kwargs={}):
# # # #         """
# # # #
# # # #         Parameters
# # # #         ----------
# # # #         window : window size int
# # # #         operation : a string with the operation e.g. 'mean' or 'std' see pandas docs for rolling
# # # #         shift_from_center : default 0 but can shift as needed
# # # #         min_periods : default is equal to win length, only allows operation when we have this many data points. so deals with
# # # #         the edges
# # # #         save_it : bool, False, loop through frame nums and save to h5 file
# # # #         kwargs : dict of args that can be applied to 'operation' function
# # # #
# # # #         Returns
# # # #         -------
# # # #
# # # #         """
# # # #         if min_periods is None:
# # # #             min_periods = window
# # # #         add_name_list = ['FD__' + self.operational_key + '_rolling_',
# # # #                          '_W_' + str(window) + '_SFC_' + str(shift_from_center) + '_MP_' + str(min_periods) + '____']
# # # #         add_name_str = operation.join(add_name_list)
# # # #         if save_it:
# # # #             self._save_it_(self.rolling, window, operation, shift_from_center, min_periods, False, kwargs)
# # # #             return None, add_name_str
# # # #         data_frame = self.data.copy()
# # # #         for i1, i2 in utils.loop_segments(self.frame_nums):
# # # #             df_rolling = self.data[i1:i2].rolling(window=window, min_periods=min_periods, center=True)
# # # #             tmp_func = eval('df_rolling.' + operation)
# # # #             data_frame[i1:i2] = tmp_func(**kwargs).shift(shift_from_center).astype(np.float32)
# # # #         return data_frame, add_name_str
# # # #
# # # #     def shift(self, shift_by, save_it=False):
# # # #         """
# # # #
# # # #         Parameters
# # # #         ----------
# # # #         shift_by : amount to shift by
# # # #         save_it :  bool, False, loop through frame nums and save to h5 file
# # # #
# # # #         Returns
# # # #         -------
# # # #
# # # #         """
# # # #         add_name_str = 'FD__' + self.operational_key + '_shift_' + str(shift_by) + '____'
# # # #         if save_it:
# # # #             self._save_it_(self.shift, shift_by)
# # # #             return None, add_name_str
# # # #
# # # #         data_frame = self.data.copy()
# # # #         for i1, i2 in utils.loop_segments(self.frame_nums):
# # # #             data_frame[i1:i2] = self.data[i1:i2].shift(shift_by).astype(np.float32)
# # # #         return data_frame, add_name_str
# # # #
# # # #     def operate(self, operation, save_it=False, extra_name_str='', kwargs={}):
# # # #         """
# # # #
# # # #         Parameters
# # # #         ----------
# # # #         operation : a string with the operation e.g. 'mean' or 'std' or 'diff' see pandas operation on  dataframes
# # # #         save_it :  bool, False, loop through frame nums and save to h5 file
# # # #         extra_name_str : add to key name string if desired
# # # #         kwargs : dict of args that can be applied to 'operation' function see pandas operation on  dataframes
# # # #
# # # #         Returns
# # # #         -------
# # # #
# # # #         """
# # # #         add_name_str_tmp = self.dict_to_string_name(kwargs)
# # # #         add_name_str = 'FD__' + self.operational_key + '_' + operation + '_' + add_name_str_tmp + extra_name_str + '____'
# # # #         if save_it:
# # # #             self._save_it_(self.operate, operation, False, extra_name_str, kwargs)
# # # #             return None, add_name_str
# # # #         data_frame = self.data.copy()
# # # #         for i1, i2 in utils.loop_segments(self.frame_nums):
# # # #             data_frame[i1:i2] = eval('self.data[i1:i2].' + operation + '(**kwargs).astype(np.float32)')
# # # #         return data_frame, add_name_str
# # # #
# # # #     @staticmethod
# # # #     def dict_to_string_name(in_dict):
# # # #         """
# # # #         used to transform dict into a string name for naming h5 keys
# # # #         Parameters
# # # #         ----------
# # # #         in_dict : dict
# # # #
# # # #         Returns
# # # #         -------
# # # #         string
# # # #         """
# # # #         str_list = []
# # # #         for k in in_dict:
# # # #             str_list.append(k)
# # # #             str_list.append(str(in_dict[k]))
# # # #         return '_'.join(str_list)
# # # #
# # # #     def set_data_and_frame(self, ind):
# # # #         self.frame_num_ind = ind
# # # #         if ind is None:
# # # #             self.frame_nums = copy.deepcopy(self.all_frame_nums)
# # # #         else:
# # # #             self.frame_nums = [self.all_frame_nums[ind]]
# # # #         self.set_data_inds(ind)
# # # #         self.set_operation_key()
# # # #
# # # #     # tqdm(sorted(random_frame_inds[i]), disable=disable_TQDM, total=total_frames, initial=cnt1)
# # # #     def _save_it_(self, temp_funct, *args):
# # # #         self._frame_num_ind_save_ = copy.deepcopy(self.frame_num_ind)
# # # #         with h5py.File(self.h5_in, 'r+') as h:
# # # #             for k in tqdm(range(self.len_frame_nums), disable=self.disable_tqdm):
# # # #                 self.set_data_and_frame(k)
# # # #                 data, key_name = temp_funct(*args)
# # # #                 if k == 0:
# # # #                     self.init_h5_data_key(key_name, delete_if_exists=self.delete_if_exists)
# # # #                     print('making key, ' + key_name)
# # # #                 a = self.data_inds
# # # #                 h[key_name][a[0]:a[1]] = data
# # # #         self.set_data_and_frame(self._frame_num_ind_save_)  # set data back to what it was when user set it
# # # #
# # # #     def total_rolling_operation(self, data_in, win, operation_function, shift_from_center=0):
# # # #         """
# # # #         NOTE: for making feature data proper key names for saving is 'FD_TOTAL_' folowed by operation e.g. 'FD_TOTAL_nanstd'
# # # #         Parameters
# # # #         ----------
# # # #         data_in : 2D matrix
# # # #         win : window size
# # # #         operation_function : function to be applies to each window e.g. np.nanmean, note DON'T include parentheses
# # # #         shift_from_center : num units shift from center
# # # #
# # # #         Returns
# # # #         -------
# # # #         data_out: output data
# # # #         is_nan_inds: bool array indexing where nans were
# # # #         """
# # # #         assert win % 2 == 1, 'window must be odd'
# # # #         mid = win // 2
# # # #         pad = np.zeros([win, data_in.shape[1]]) * np.nan
# # # #
# # # #         L_pad = pad[:mid - shift_from_center]
# # # #         R_pad = pad[:mid + shift_from_center]
# # # #
# # # #         data_in = np.vstack([L_pad, data_in, R_pad])
# # # #
# # # #         is_nan_inds = []
# # # #         data_out = []
# # # #         for k in range(data_in.shape[0] - win + 1):
# # # #             x = data_in[k:(k + win)]
# # # #             data_out.append(operation_function(x))
# # # #             is_nan_inds.append(np.any(np.isnan(x)))
# # # #         return np.asarray(data_out), np.asarray(is_nan_inds)
# # # #
# # # #     def total_rolling_operation_h5_wrapper(self, window, operation, key_to_operate_on, mod_key_name=None,
# # # #                                            save_it=False,
# # # #                                            shift_from_center=0):
# # # #         if save_it:
# # # #             assert mod_key_name is not None, """if save_it is True, 'mod_key_name' must not be None e.g. 'FD_TOTAL_std_1_of_'"""
# # # #         all_data = []
# # # #         with h5py.File(self.h5_in, 'r') as h:
# # # #             frame_nums = h['frame_nums'][:]
# # # #             for i, (i1, i2) in enumerate(utils.loop_segments(frame_nums)):
# # # #                 data_out, is_nan_inds = self.total_rolling_operation(h[key_to_operate_on][i1:i2, :], window, operation,
# # # #                                                                      shift_from_center=shift_from_center)
# # # #                 all_data.append(data_out)
# # # #         all_data = np.hstack(all_data)
# # # #         mod_key_name = mod_key_name + key_to_operate_on
# # # #         if save_it:
# # # #             utils.overwrite_h5_key(self.h5_in, mod_key_name, all_data)
# # # #         return all_data
# # # #
# # # #
# # # # from tqdm.auto import tqdm
# # # # import numpy as np
# # # #
# # # # ########################################################################################################################
# # # # ########################################################################################################################
# # # # h5_feature_data = '/Users/phil/Desktop/pipeline_test/AH0407x160609_3lag_feature_data.h5'
# # # # FM = feature_maker(h5_feature_data, operational_key='FD__original', delete_if_exists=True)
# # # #
# # # # for periods in tqdm([-5]):
# # # #     data, key_name = FM.shift(periods, save_it=True)
# # # # ########################################################################################################################
# # # # ########################################################################################################################
# # # # ########################################################################################################################
# # # # # from whacc.feature_maker import feature_maker, total_rolling_operation_h5_wrapper
# # # #
# # # #
# # # # for periods in tqdm([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5]):
# # # #     data, key_name = FM.shift(periods, save_it=True)
# # # #
# # # # for smooth_it_by in tqdm([3, 7, 11, 15, 21, 41, 61]):
# # # #     data, key_name = FM.rolling(smooth_it_by, 'mean', save_it=True)
# # # #
# # # # for periods in tqdm([-50, -20, -10, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 10, 20, 50]):
# # # #     data, key_name = FM.operate('diff', kwargs={'periods': periods}, save_it=True)
# # # #
# # # # for smooth_it_by in tqdm([3, 7, 11, 15, 21, 41, 61]):
# # # #     data, key_name = FM.rolling(smooth_it_by, 'std', save_it=True)
# # # #
# # # # win = 1
# # # # # key_to_operate_on = 'FD__original'
# # # # op = np.std
# # # # mod_key_name = 'FD_TOTAL_std_' + str(win) + '_of_'
# # # # all_keys = utils.lister_it(utils.print_h5_keys(FM.h5_in, 1, 0), 'FD__', 'FD_TOTAL')
# # # # for key_to_operate_on in tqdm(all_keys):
# # # #     data_out = FM.total_rolling_operation_h5_wrapper(win, op, key_to_operate_on, mod_key_name=mod_key_name,
# # # #                                                      save_it=True)
# # # #
# # # # utils.get_selected_features(greater_than_or_equal_to=4)
# # # #
# # # # inds = fd_dict['features_used_of_10'] >= 4
# # # # tmp1 = fd_dict['full_feature_names_and_neuron_nums'][inds]
# # # # import numpy as np
# # # #
# # # # tmp2 = np.unique(fd_dict['full_neuron_nums'][inds])
# # # #
# # # # for k in tmp1:
# # # #     print(k)
# # # #
# # # # """
# # # # 'FD_TOTAL_std_1_of_original_diff_periods_3',
# # # # 'FD_TOTAL_std_1_of_original_rolling_mean_W_3_SFC_0_MP_3',
# # # # 'FD_TOTAL_std_1_of_original_rolling_mean_W_7_SFC_0_MP_7',
# # # # 'FD_TOTAL_std_1_of_original_rolling_mean_W_11_SFC_0_MP_11',
# # # # 'FD_TOTAL_std_1_of_original_shift_3', 'FD_TOTAL_std_1_of_original'],
# # # #
# # # # do those first then take any of the completed data from them that are used as single features
# # # #
# # # # then save the TOTAL operations and singles,
# # # #
# # # # then go through all the singles
# # # #
# # # # """
# # # #
# # # # len(utils.lister_it(tmp1, '_diff_'))
# # # #
# # # # h52 = '/Users/phil/Desktop/pipeline_test/AH0407x160609_3lag_feature_data.h5'
# # # # utils.print
# # # #
# # # #
# # # # def total_rolling_sliding_window_view(data_in, win, operation_function, shift_from_center=0):
# # # #     assert win % 2 == 1, 'window must be odd'
# # # #     mid = win // 2
# # # #     pad = np.zeros([win, data_in.shape[1]]) * np.nan
# # # #
# # # #     L_pad = pad[:mid - shift_from_center]
# # # #     R_pad = pad[:mid + shift_from_center]
# # # #
# # # #     data_in = np.vstack([L_pad, data_in, R_pad])
# # # #     w = data_in.shape[1]
# # # #     data_in = np.lib.stride_tricks.sliding_window_view(data_in, (win, w))
# # # #     data_in = np.reshape(data_in, [-1, win * w])
# # # #     data_out = operation_function(data_in, axis=1)
# # # #     return np.asarray(data_out)
# # #
# # #
# # # from whacc import utils, image_tools
# # # import matplotlib.pyplot as plt
# # # import h5py
# # # import numpy as np
# # # h5 = '/Users/phil/Dropbox/HIRES_LAB/GitHub/Phillip_AC/model_testing/all_data/test_data/10_percent_holy_set/regular/holy_test_set_10_percent_regular.h5'
# # # h5 = '/Users/phil/Dropbox/HIRES_LAB/GitHub/Phillip_AC/model_testing/all_data/test_data/10_percent_holy_set/3lag/holy_test_set_10_percent_3lag.h5'
# # # count = 19
# # # start = 24850 - 1000
# # # end = 24850 + 1000
# # # # start = 0
# # #
# # #
# # # # L = 40000
# # # #  32736
# # #
# # # with h5py.File(h5, 'r') as h:
# # #     L = len(h['labels'][:])
# # #     print(L)
# # #     L = end - start
# # #     imgs = h['images'][start:end:L//count]
# # #     # L = len(h['labels'][:])
# # #     titles = np.arange(L)[start:end:L//count]
# # #
# # # fig, ax = plt.subplots(5, 4)
# # # for ind, ax2 in enumerate(ax.flatten()):
# # #     ax2.imshow(imgs[ind])
# # #     # ax2.title.set_text(titles[ind])
# # #
# # #
# # #
# # # import matplotlib.pyplot as plt
# # # import h5py
# # # import numpy as np
# # # h5 = '/Users/phil/Dropbox/HIRES_LAB/GitHub/Phillip_AC/model_testing/all_data/test_data/10_percent_holy_set/regular/holy_test_set_10_percent_regular.h5'
# # # h5 = '/Users/phil/Dropbox/HIRES_LAB/GitHub/Phillip_AC/model_testing/all_data/test_data/10_percent_holy_set/3lag/holy_test_set_10_percent_3lag.h5'
# # # h5 =  '/Users/phil/Dropbox/HIRES_LAB/GitHub/Phillip_AC/model_testing/all_data/test_data/full_holy_set/3lag/holy_set_80_border_single_frame_3lag.h5'
# # #
# # # # start = 0
# # #
# # #
# # # # L = 40000
# # # #  32736
# # #
# # # with h5py.File(h5, 'r') as h:
# # #     imgs = []
# # #     for k1, k2 in utils.loop_segments(h['frame_nums'][:]):
# # #         i = np.where(h['labels'][k1:k2]==1)[0]
# # #         i = i[int(len(i)/2)]
# # #         # i = int(np.mean([k1, k2])) # center ind
# # #         imgs.append(h['images'][k1+i])
# # # imgs = np.asarray(imgs)
# # #
# # # for ind, img_in in enumerate(imgs):
# # #     if ind%20 == 0:
# # #         fig, ax = plt.subplots(5, 4)
# # #         ax = ax.flatten()
# # #     ax[ind%20].imshow(img_in)
# # #     ax[ind%20].title.set_text(str(ind))
# # #     # ax2.title.set_text(titles[ind])
# # #
# # # """
# # # ##################################################################################################
# # # ##################################################################################################
# # # ##################use to compare unfinished trained data #########################################
# # # ##################################################################################################
# # # """
# # # test_set_to = 10
# # # from natsort import natsorted, ns
# # #
# # # mod_dir = '/Volumes/GoogleDrive-114825029448473821206/My Drive/LIGHT_GBM/models/10_sets_frame_nums_split_then_random_split_method_numpy_feature_selection_V1/'
# # # mods = utils.get_files(mod_dir, '*')
# # # mods = natsorted(mods, alg=ns.REAL)[:test_set_to]
# # # # from natsort import natsorted
# # # # mods = natsorted(mods)[:-1]
# # # features_out_of_10 = []
# # # for k in mods:
# # #     lgbm = utils.load_obj(k)
# # #     features_out_of_10.append(lgbm.feature_importance()>0)
# # # features_out_of_10 = np.sum(np.asarray(features_out_of_10), axis = 0)
# # #
# # # for k in range(test_set_to):
# # #     print(np.round(100 * np.mean(features_out_of_10 > k), 2), '% have ', k+1, ' or more')
# # #     print('count ', np.sum(features_out_of_10 > k))
# # # count_importance = np.where(features_out_of_10>=3)[0]
# # # print('____________________')
# # # mod_dir = '/Volumes/GoogleDrive-114825029448473821206/My Drive/LIGHT_GBM/models/10_sets_frame_nums_split_then_random_split_method/'
# # # mods = utils.get_files(mod_dir, '*')
# # # mods = natsorted(mods, alg=ns.REAL)[:test_set_to]
# # # # from natsort import natsorted
# # # # mods = natsorted(mods)[:-1]
# # # features_out_of_10 = []
# # # for k in mods:
# # #     lgbm = utils.load_obj(k)
# # #     features_out_of_10.append(lgbm.feature_importance()>0)
# # # features_out_of_10 = np.sum(np.asarray(features_out_of_10), axis = 0)
# # #
# # # for k in range(test_set_to):
# # #     print(np.round(100 * np.mean(features_out_of_10 > k), 2), '% have ', k+1, ' or more')
# # #     print('count ', np.sum(features_out_of_10 > k))
# # # count_importance = np.where(features_out_of_10>=3)[0]
# # #
# # #
# # #
# # # """
# # # CHOOSING THE BEST FEATURES, I SHOULD TRAIN AND TEST THIS FOR MY SHIT BEFORE CONFIRMING IT IS ALL GOOD.
# # # I have times used and gain importance
# # # each conveys something different and I can choose whichever I want. or I can do a combination of both because they are
# # # not perfectly overlapping
# # # I can also use SD as a decider as it can show variables that would be useful like outliers that catch something
# # #
# # # I could also train data on like the top 15k or something or maybe even 32k?? if i do all at least one will i get the
# # # same results?
# # #
# # # so after looking at https://simility.com/wp-content/uploads/2020/07/WP-Feature-Selection.pdf
# # # I think it is totally appropriate to take the union of the models and train again and see how they do
# # # or I could do some voting
# # #
# # # """
# # # import os
# # # """ times used metric  """
# # # mod_dir = '/Volumes/GoogleDrive-114825029448473821206/My Drive/LIGHT_GBM/models/10_sets_frame_nums_split_then_random_split_method/'
# # # mods = utils.get_files(mod_dir, '*')
# # # # from natsort import natsorted
# # # # mods = natsorted(mods)[:-1]
# # # features_out_of_10 = []
# # # for k in mods:
# # #     lgbm = utils.load_obj(k)
# # #     features_out_of_10.append(lgbm.feature_importance()>0)
# # # features_out_of_10 = np.sum(np.asarray(features_out_of_10), axis = 0)
# # #
# # # for k in range(10):
# # #     print(np.round(100 * np.mean(features_out_of_10 > k), 2), '% have ', k+1, ' or more')
# # #     print('count ', np.sum(features_out_of_10 > k))
# # # count_importance = np.where(features_out_of_10>=3)[0]
# # #
# # # non_zero_features = np.where(features_out_of_10>0)[0]
# # #
# # # non_zero_features_bool = [k>0 for k in features_out_of_10]
# # #
# # # bd = '/Volumes/GoogleDrive-114825029448473821206/My Drive/LIGHT_GBM/feature_index_for_feature_selection'
# # # np.save(bd+os.sep+'non_zero_features_bool_29913_features.npy', non_zero_features_bool)
# # #
# # # """ gain importance mean  """
# # # features_out_of_10 = []
# # # #3063
# # # for k in mods:
# # #     lgbm = utils.load_obj(k)
# # #     features_out_of_10.append(lgbm.feature_importance(importance_type='gain'))
# # # x = np.asarray(features_out_of_10)
# # # features_out_of_10 = np.mean(np.asarray(features_out_of_10), axis = 0)
# # #
# # # for k in np.linspace(0, 4, 30):
# # #     print(np.round(100 * np.mean(features_out_of_10 > k), 2), '% have more than', k)
# # #     print('count ', np.sum(features_out_of_10 > k))
# # # gain_importance = np.where(features_out_of_10>1.793103448275862)[0]
# # #
# # # tmp1 = np.unique(np.concatenate([gain_importance, count_importance]))
# # # len(tmp1), len(count_importance), len(gain_importance)
# # #
# # #
# # # """ gain importance max  """
# # # features_out_of_10 = []
# # # #3063
# # # for k in mods:
# # #     lgbm = utils.load_obj(k)
# # #     features_out_of_10.append(lgbm.feature_importance(importance_type='gain'))
# # # features_out_of_10 = np.asarray(features_out_of_10)
# # # features_out_of_10 = np.max(features_out_of_10, axis = 0)
# # #
# # # for k in np.linspace(1, 40, 30):
# # #     print(np.round(100 * np.mean(features_out_of_10 > k), 2), '% have more than', k)
# # #     print('count ', np.sum(features_out_of_10 > k))
# # #
# # # tmp1 = []
# # # for k in np.linspace(0, 100, 100):
# # #     tmp1.append(np.sum(features_out_of_10 > k))
# # # plt.plot(tmp1, '.')
# # #
# # #
# # #
# # # """ gain importance mean  """
# # # features_out_of_10 = []
# # # #3063
# # # for k in mods:
# # #     lgbm = utils.load_obj(k)
# # #     features_out_of_10.append(lgbm.feature_importance(importance_type='gain'))
# # # x = np.asarray(features_out_of_10)
# # # features_out_of_10 = np.mean(np.asarray(features_out_of_10), axis = 0)
# # #
# # # for k in np.linspace(0, 4, 30):
# # #     print(np.round(100 * np.mean(features_out_of_10 > k), 2), '% have more than', k)
# # #     print('count ', np.sum(features_out_of_10 > k))
# # #
# # #
# # #
# # # bins = np.linspace(0.00001, 1, 1000)
# # # plt.hist(features_out_of_10, bins = bins)
# # # np.mean(features_out_of_10<=0.002)
# # #
# # # tmp8 = features_out_of_10>=0.004
# # #
# # # tmp9 = features_out_of_10>=2
# # #
# # # tmp10 = np.mean(np.vstack((tmp8, tmp9))*1, axis = 0)>0
# # #
# # # np.sum(tmp8), np.sum(tmp9), np.sum(tmp10), len(tmp8)
# # #
# # # """
# # # so the rules are, include all the data that is 2 or higher and that is greater than 0.002 (for now) that result sin 87.7%
# # # for the new set
# # # """
# # #
# # #
# # # utils.np_stats(features_out_of_10)
# # # xu = np.unique(features_out_of_10)
# # # a = xu[1]/2
# # # bins = list(xu-a)
# # # bins.append(xu[-1]+a)
# # # import matplotlib.pyplot as plt
# # # count = []
# # # for k in xu[1:]:
# # #     count.append(np.sum(k==features_out_of_10))
# # #
# # # plt.bar(range(len(count)), count)
# # # """
# # # want to plot to see if there is a clear gain features that have a mean for the first bump i can remove for feature selection
# # # """
# # # win = 1001
# # # x = np.convolve(count, np.ones(win)/win, mode='valid')
# # # plt.plot(xu[1:], x)
# # # x2 = np.cumsum(count)
# # # x2 = x2/np.max(x2)
# # # plt.plot(x2)
# # #
# # #
# # # tmp1 = np.unique(np.concatenate([gain_importance, count_importance]))
# # # len(tmp1), len(count_importance), len(gain_importance)
# # #
# # #
# # #
# # #
# # #
# # #
# # #
# # #
# # #
# # #
# # # """ gain importance SD to see if there are certain predictors that are used in one but not other sub models  """
# # # features_out_of_10 = []
# # # #3063
# # # for k in mods:
# # #     lgbm = utils.load_obj(k)
# # #     features_out_of_10.append(lgbm.feature_importance(importance_type='gain'))
# # # features_out_of_10 = np.asarray(features_out_of_10)
# # # features_out_of_10 = np.std(features_out_of_10, axis = 0)
# # #
# # # # for k in np.linspace(1, 40, 30):
# # # #     print(np.round(100 * np.mean(features_out_of_10 > k), 2), '% have more than', k)
# # # #     print('count ', np.sum(features_out_of_10 > k))
# # #
# # # tmp1 = []
# # # for k in np.linspace(0, 1000, 100):
# # #     tmp1.append(np.sum(features_out_of_10 > k))
# # # plt.plot(tmp1, '.')
# # # plt.xlabel('SD of each set of 10 ')
# # # plt.ylabel('count greater than ...')
# # #
# # #
# # #
# # #
# # #
# # #
# # #
# # # plt.hist(x.flatten(), bins=np.arange(0, 200))
# # #
# # #
# # # tmp1 = '/Users/phil/Dropbox/HIRES_LAB/GitHub/whacc/whacc/whacc_data/feature_data/feature_data_dict.pkl'
# # # tmp1 = utils.load_obj(tmp1) # ok this needs to change
# # #
# # #
# # # tmp1 = '/Volumes/GoogleDrive-114825029448473821206/My Drive/final_features_window_version_corrected_v2/'
# # # tmp1 = utils.get_files(tmp1, '*')
# # #
# # #
# # # """
# # # #####################################################################################################################
# # # #####################################################################################################################
# # # #####################################################################################################################
# # # ##################################### LOAD AND PREDICT WITH THE GBM MODEL############################################
# # # #####################################################################################################################
# # # #####################################################################################################################
# # # """
# # # import lightgbm as lgb
# # # from whacc import utils
# # # import numpy as np
# # # import matplotlib.pyplot as plt
# # # fn = '/Volumes/GoogleDrive-114825029448473821206/My Drive/LIGHT_GBM/OPTUNA_mod_saves/V1/67.pkl'
# # # mod = utils.load_obj(fn)
# # #
# # # x = np.random.rand(100, 2105)
# # # testy = x[:, 0]>.5
# # # yhat = mod.predict(x)
# # #
# # # plt.plot(yhat)
# # #
# # #
# # # #  precition recal curve
# # # from sklearn.metrics import precision_recall_curve
# # # precision, recall, thresholds = precision_recall_curve(testy, yhat)
# # #
# # #
# # # # from whacc import utils, image_tools
# # # #
# # # # import copy
# # # # import numpy as np
# # # # import pandas as pd
# # # # import h5py
# # # #
# # # # from tqdm.autonotebook import tqdm
# # # #
# # # #
# # # # class feature_maker():
# # # #     def __init__(self, h5_in, frame_num_ind=None, frame_nums=None, operational_key='FD__original', disable_tqdm=False,
# # # #                  delete_if_exists=False, index_features_delete_the_rest=None):
# # # #         """
# # # #
# # # #         Parameters
# # # #         ----------
# # # #         h5_in : h5 string pointing to the h4 file with the data to transform
# # # #         frame_num_ind : int referencing the frame num  ind to transform, note: if save_it is one ALL data is converted
# # # #         automatically and saved in h5. frame_num_ind only works when you call with
# # # #         frame_nums : default None, auto looks for key 'frame_nums' in h5 file or you can insert your own
# # # #         operational_key : the data array key to be transformed
# # # #         disable_tqdm : default False, when save_it is True it will show a loading bar with the progress unless set to true
# # # #         delete_if_exists : default False, when calling a function with save_it as True, you can choose to overwrite that
# # # #         data by setting this value to True
# # # #
# # # #         Returns
# # # #         -------
# # # #         feature maker class
# # # #
# # # #         Examples
# # # #         ________
# # # #
# # # #         h5_in = '/Users/phil/Desktop/AH0407_160613_JC1003_AAAC_3lag.h5'
# # # #
# # # #         FM = feature_maker(h5_in, frame_num_ind=2, delete_if_exists = True) #set frame_num_ind to an int so that we can quickly look at the transformation
# # # #         data, data_name = FM.shift(5, save_it=False) # shift it 5 to the right, fills in with nan as needed, look at just the 5th frame num set (5th video)
# # # #         # to see how it looks
# # # #         print('the below name will be used to save the data in the the h5 when calling functions with save_it=True')
# # # #         print(data_name)
# # # #         FM.shift(5, save_it=True) # now lets save it
# # # #
# # # #         data, data_name_rolling_mean_100 = FM.rolling(100, 'mean', save_it=True)  #lets do the rolling mean and save it
# # # #
# # # #         data, data_name = FM.operate('diff', kwargs={'periods': 1}, save_it=False) # lets perform a diff operation
# # # #         print(data_name)
# # # #         print(data)
# # # #         FM.operate('diff', kwargs={'periods': -1}, save_it=True) # now lets save it and save it
# # # #
# # # #         # now lets change the operational key so we can transform some data we just transformed, specifically the rolling mean 10
# # # #         FM.set_operation_key(data_name_rolling_mean_100)
# # # #
# # # #         data, data_name_diff_100_mean = FM.operate('diff', kwargs={'periods': -50}, save_it=False) # lets check how the name will change
# # # #         print(data_name_diff_100_mean)
# # # #         print("notice the FD__ twice, this means the data has been transformed twice")
# # # #         print('also notice that how the data was transformed can be seen because it is split up by ____ (4 underscores)')
# # # #
# # # #         data, data_name_diff_100_mean = FM.operate('diff', kwargs={'periods': -50}, save_it=True) # save it
# # # #
# # # #         a = utils.print_h5_keys(h5_in, 1, 1)
# # # #         key_name_list = ['FD__original', 'FD__FD__FD__original_rolling_mean_W_100_SFC_0_MP_100_____diff_periods_-50____', 'FD__FD__original_rolling_mean_W_100_SFC_0_MP_100____']
# # # #         with h5py.File(h5_in, 'r+') as h:
# # # #             for k in key_name_list:
# # # #                 plt.plot(h[k][:8000, 0])
# # # #         """
# # # #         if utils.h5_key_exists(h5_in, 'has_data_been_randomized'):
# # # #             assert image_tools.get_h5_key_and_concatenate(h5_in,
# # # #                                                           'has_data_been_randomized').tolist() is False, """this data has been randomized, it is not fit to perform temporal operations on, search for key 'has_data_been_randomized' for more info"""
# # # #
# # # #         self._frame_num_ind_save_ = None
# # # #         self.disable_tqdm = disable_tqdm
# # # #         self.h5_in = h5_in
# # # #         self.frame_num_ind = frame_num_ind
# # # #         self.delete_if_exists = delete_if_exists
# # # #         self.operational_key = operational_key
# # # #         if frame_nums is None:
# # # #             print('extracting frame_nums from h5 file, ideally you should just put that in yourself though')
# # # #             frame_nums = image_tools.get_h5_key_and_concatenate(h5_in, 'frame_nums')
# # # #         self.all_frame_nums = frame_nums
# # # #         self.len_frame_nums = len(self.all_frame_nums)
# # # #         self.set_data_and_frame(frame_num_ind)
# # # #         index_features_delete_the_rest
# # # #
# # # #     def set_data_inds(self, ind):  # frame nums used ot extract below in 'set_operation_key'
# # # #         tmp_inds = np.asarray(utils.loop_segments(self.all_frame_nums, returnaslist=True))
# # # #         if ind is None:
# # # #             self.data_inds = [tmp_inds[0][0], tmp_inds[-1][-1]]
# # # #         else:
# # # #             self.data_inds = tmp_inds[:, ind]
# # # #
# # # #     def set_operation_key(self, key_name=None):
# # # #         if key_name is not None:
# # # #             self.operational_key = key_name
# # # #         with h5py.File(self.h5_in, 'r') as h:
# # # #             self.full_data_shape = np.asarray(h[self.operational_key].shape)
# # # #             if self.frame_num_ind is None:
# # # #                 self.data = pd.DataFrame(copy.deepcopy(h[self.operational_key][:]))
# # # #             else:
# # # #                 a = self.data_inds  # just the current frame numbers
# # # #                 self.data = pd.DataFrame(copy.deepcopy(h[self.operational_key][a[0]:a[1]]))
# # # #
# # # #     def init_h5_data_key(self, data_key, delete_if_exists=False):
# # # #         key_exists = utils.h5_key_exists(self.h5_in, data_key)
# # # #         assert not (
# # # #                 key_exists and not delete_if_exists), "key exists, if you want to overwrite set 'delete_if_exists' = True"
# # # #         with h5py.File(self.h5_in, 'r+') as x:
# # # #             if key_exists and delete_if_exists:
# # # #                 print('deleting key to overwrite it')
# # # #                 del x[data_key]
# # # #             x.create_dataset_like(data_key, x[self.operational_key])
# # # #
# # # #     def rolling(self, window, operation, shift_from_center=0, min_periods=None, save_it=False, kwargs={}):
# # # #         """
# # # #
# # # #         Parameters
# # # #         ----------
# # # #         window : window size int
# # # #         operation : a string with the operation e.g. 'mean' or 'std' see pandas docs for rolling
# # # #         shift_from_center : default 0 but can shift as needed
# # # #         min_periods : default is equal to win length, only allows operation when we have this many data points. so deals with
# # # #         the edges
# # # #         save_it : bool, False, loop through frame nums and save to h5 file
# # # #         kwargs : dict of args that can be applied to 'operation' function
# # # #
# # # #         Returns
# # # #         -------
# # # #
# # # #         """
# # # #         if min_periods is None:
# # # #             min_periods = window
# # # #         add_name_list = ['FD__' + self.operational_key + '_rolling_',
# # # #                          '_W_' + str(window) + '_SFC_' + str(shift_from_center) + '_MP_' + str(min_periods) + '____']
# # # #         add_name_str = operation.join(add_name_list)
# # # #         if save_it:
# # # #             self._save_it_(self.rolling, window, operation, shift_from_center, min_periods, False, kwargs)
# # # #             return None, add_name_str
# # # #         data_frame = self.data.copy()
# # # #         for i1, i2 in utils.loop_segments(self.frame_nums):
# # # #             df_rolling = self.data[i1:i2].rolling(window=window, min_periods=min_periods, center=True)
# # # #             tmp_func = eval('df_rolling.' + operation)
# # # #             data_frame[i1:i2] = tmp_func(**kwargs).shift(shift_from_center).astype(np.float32)
# # # #         return data_frame, add_name_str
# # # #
# # # #     def shift(self, shift_by, save_it=False):
# # # #         """
# # # #
# # # #         Parameters
# # # #         ----------
# # # #         shift_by : amount to shift by
# # # #         save_it :  bool, False, loop through frame nums and save to h5 file
# # # #
# # # #         Returns
# # # #         -------
# # # #
# # # #         """
# # # #         add_name_str = 'FD__' + self.operational_key + '_shift_' + str(shift_by) + '____'
# # # #         if save_it:
# # # #             self._save_it_(self.shift, shift_by)
# # # #             return None, add_name_str
# # # #
# # # #         data_frame = self.data.copy()
# # # #         for i1, i2 in utils.loop_segments(self.frame_nums):
# # # #             data_frame[i1:i2] = self.data[i1:i2].shift(shift_by).astype(np.float32)
# # # #         return data_frame, add_name_str
# # # #
# # # #     def operate(self, operation, save_it=False, extra_name_str='', kwargs={}):
# # # #         """
# # # #
# # # #         Parameters
# # # #         ----------
# # # #         operation : a string with the operation e.g. 'mean' or 'std' or 'diff' see pandas operation on  dataframes
# # # #         save_it :  bool, False, loop through frame nums and save to h5 file
# # # #         extra_name_str : add to key name string if desired
# # # #         kwargs : dict of args that can be applied to 'operation' function see pandas operation on  dataframes
# # # #
# # # #         Returns
# # # #         -------
# # # #
# # # #         """
# # # #         add_name_str_tmp = self.dict_to_string_name(kwargs)
# # # #         add_name_str = 'FD__' + self.operational_key + '_' + operation + '_' + add_name_str_tmp + extra_name_str + '____'
# # # #         if save_it:
# # # #             self._save_it_(self.operate, operation, False, extra_name_str, kwargs)
# # # #             return None, add_name_str
# # # #         data_frame = self.data.copy()
# # # #         for i1, i2 in utils.loop_segments(self.frame_nums):
# # # #             data_frame[i1:i2] = eval('self.data[i1:i2].' + operation + '(**kwargs).astype(np.float32)')
# # # #         return data_frame, add_name_str
# # # #
# # # #     @staticmethod
# # # #     def dict_to_string_name(in_dict):
# # # #         """
# # # #         used to transform dict into a string name for naming h5 keys
# # # #         Parameters
# # # #         ----------
# # # #         in_dict : dict
# # # #
# # # #         Returns
# # # #         -------
# # # #         string
# # # #         """
# # # #         str_list = []
# # # #         for k in in_dict:
# # # #             str_list.append(k)
# # # #             str_list.append(str(in_dict[k]))
# # # #         return '_'.join(str_list)
# # # #
# # # #     def set_data_and_frame(self, ind):
# # # #         self.frame_num_ind = ind
# # # #         if ind is None:
# # # #             self.frame_nums = copy.deepcopy(self.all_frame_nums)
# # # #         else:
# # # #             self.frame_nums = [self.all_frame_nums[ind]]
# # # #         self.set_data_inds(ind)
# # # #         self.set_operation_key()
# # # #
# # # #     # tqdm(sorted(random_frame_inds[i]), disable=disable_TQDM, total=total_frames, initial=cnt1)
# # # #     def _save_it_(self, temp_funct, *args):
# # # #         self._frame_num_ind_save_ = copy.deepcopy(self.frame_num_ind)
# # # #         with h5py.File(self.h5_in, 'r+') as h:
# # # #             for k in tqdm(range(self.len_frame_nums), disable=self.disable_tqdm):
# # # #                 self.set_data_and_frame(k)
# # # #                 data, key_name = temp_funct(*args)
# # # #                 if k == 0:
# # # #                     self.init_h5_data_key(key_name, delete_if_exists=self.delete_if_exists)
# # # #                     print('making key, ' + key_name)
# # # #                 a = self.data_inds
# # # #                 h[key_name][a[0]:a[1]] = data
# # # #         self.set_data_and_frame(self._frame_num_ind_save_)  # set data back to what it was when user set it
# # # #
# # # #     def total_rolling_operation(self, data_in, win, operation_function, shift_from_center=0):
# # # #         """
# # # #         NOTE: for making feature data proper key names for saving is 'FD_TOTAL_' folowed by operation e.g. 'FD_TOTAL_nanstd'
# # # #         Parameters
# # # #         ----------
# # # #         data_in : 2D matrix
# # # #         win : window size
# # # #         operation_function : function to be applies to each window e.g. np.nanmean, note DON'T include parentheses
# # # #         shift_from_center : num units shift from center
# # # #
# # # #         Returns
# # # #         -------
# # # #         data_out: output data
# # # #         is_nan_inds: bool array indexing where nans were
# # # #         """
# # # #         assert win % 2 == 1, 'window must be odd'
# # # #         mid = win // 2
# # # #         pad = np.zeros([win, data_in.shape[1]]) * np.nan
# # # #
# # # #         L_pad = pad[:mid - shift_from_center]
# # # #         R_pad = pad[:mid + shift_from_center]
# # # #
# # # #         data_in = np.vstack([L_pad, data_in, R_pad])
# # # #
# # # #         is_nan_inds = []
# # # #         data_out = []
# # # #         for k in range(data_in.shape[0] - win + 1):
# # # #             x = data_in[k:(k + win)]
# # # #             data_out.append(operation_function(x))
# # # #             is_nan_inds.append(np.any(np.isnan(x)))
# # # #         return np.asarray(data_out), np.asarray(is_nan_inds)
# # # #
# # # #     def total_rolling_operation_h5_wrapper(self, window, operation, key_to_operate_on, mod_key_name=None,
# # # #                                            save_it=False,
# # # #                                            shift_from_center=0):
# # # #         if save_it:
# # # #             assert mod_key_name is not None, """if save_it is True, 'mod_key_name' must not be None e.g. 'FD_TOTAL_std_1_of_'"""
# # # #         all_data = []
# # # #         with h5py.File(self.h5_in, 'r') as h:
# # # #             frame_nums = h['frame_nums'][:]
# # # #             for i, (i1, i2) in enumerate(utils.loop_segments(frame_nums)):
# # # #                 data_out, is_nan_inds = self.total_rolling_operation(h[key_to_operate_on][i1:i2, :], window, operation,
# # # #                                                                      shift_from_center=shift_from_center)
# # # #                 all_data.append(data_out)
# # # #         all_data = np.hstack(all_data)
# # # #         mod_key_name = mod_key_name + key_to_operate_on
# # # #         if save_it:
# # # #             utils.overwrite_h5_key(self.h5_in, mod_key_name, all_data)
# # # #         return all_data
# # # #
# # # #
# # # # from tqdm.auto import tqdm
# # # # import numpy as np
# # # #
# # # # ########################################################################################################################
# # # # ########################################################################################################################
# # # # h5_feature_data = '/Users/phil/Desktop/pipeline_test/AH0407x160609_3lag_feature_data.h5'
# # # # FM = feature_maker(h5_feature_data, operational_key='FD__original', delete_if_exists=True)
# # # #
# # # # for periods in tqdm([-5]):
# # # #     data, key_name = FM.shift(periods, save_it=True)
# # # # ########################################################################################################################
# # # # ########################################################################################################################
# # # # ########################################################################################################################
# # # # # from whacc.feature_maker import feature_maker, total_rolling_operation_h5_wrapper
# # # #
# # # #
# # # # for periods in tqdm([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5]):
# # # #     data, key_name = FM.shift(periods, save_it=True)
# # # #
# # # # for smooth_it_by in tqdm([3, 7, 11, 15, 21, 41, 61]):
# # # #     data, key_name = FM.rolling(smooth_it_by, 'mean', save_it=True)
# # # #
# # # # for periods in tqdm([-50, -20, -10, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 10, 20, 50]):
# # # #     data, key_name = FM.operate('diff', kwargs={'periods': periods}, save_it=True)
# # # #
# # # # for smooth_it_by in tqdm([3, 7, 11, 15, 21, 41, 61]):
# # # #     data, key_name = FM.rolling(smooth_it_by, 'std', save_it=True)
# # # #
# # # # win = 1
# # # # # key_to_operate_on = 'FD__original'
# # # # op = np.std
# # # # mod_key_name = 'FD_TOTAL_std_' + str(win) + '_of_'
# # # # all_keys = utils.lister_it(utils.print_h5_keys(FM.h5_in, 1, 0), 'FD__', 'FD_TOTAL')
# # # # for key_to_operate_on in tqdm(all_keys):
# # # #     data_out = FM.total_rolling_operation_h5_wrapper(win, op, key_to_operate_on, mod_key_name=mod_key_name,
# # # #                                                      save_it=True)
# # # #
# # # # utils.get_selected_features(greater_than_or_equal_to=4)
# # # #
# # # # inds = fd_dict['features_used_of_10'] >= 4
# # # # tmp1 = fd_dict['full_feature_names_and_neuron_nums'][inds]
# # # # import numpy as np
# # # #
# # # # tmp2 = np.unique(fd_dict['full_neuron_nums'][inds])
# # # #
# # # # for k in tmp1:
# # # #     print(k)
# # # #
# # # # """
# # # # 'FD_TOTAL_std_1_of_original_diff_periods_3',
# # # # 'FD_TOTAL_std_1_of_original_rolling_mean_W_3_SFC_0_MP_3',
# # # # 'FD_TOTAL_std_1_of_original_rolling_mean_W_7_SFC_0_MP_7',
# # # # 'FD_TOTAL_std_1_of_original_rolling_mean_W_11_SFC_0_MP_11',
# # # # 'FD_TOTAL_std_1_of_original_shift_3', 'FD_TOTAL_std_1_of_original'],
# # # #
# # # # do those first then take any of the completed data from them that are used as single features
# # # #
# # # # then save the TOTAL operations and singles,
# # # #
# # # # then go through all the singles
# # # #
# # # # """
# # # #
# # # # len(utils.lister_it(tmp1, '_diff_'))
# # # #
# # # # h52 = '/Users/phil/Desktop/pipeline_test/AH0407x160609_3lag_feature_data.h5'
# # # # utils.print
# # # #
# # # #
# # # # def total_rolling_sliding_window_view(data_in, win, operation_function, shift_from_center=0):
# # # #     assert win % 2 == 1, 'window must be odd'
# # # #     mid = win // 2
# # # #     pad = np.zeros([win, data_in.shape[1]]) * np.nan
# # # #
# # # #     L_pad = pad[:mid - shift_from_center]
# # # #     R_pad = pad[:mid + shift_from_center]
# # # #
# # # #     data_in = np.vstack([L_pad, data_in, R_pad])
# # # #     w = data_in.shape[1]
# # # #     data_in = np.lib.stride_tricks.sliding_window_view(data_in, (win, w))
# # # #     data_in = np.reshape(data_in, [-1, win * w])
# # # #     data_out = operation_function(data_in, axis=1)
# # # #     return np.asarray(data_out)
# # #
# # #
# # # from whacc import utils, image_tools
# # # import matplotlib.pyplot as plt
# # # import h5py
# # # import numpy as np
# # # h5 = '/Users/phil/Dropbox/HIRES_LAB/GitHub/Phillip_AC/model_testing/all_data/test_data/10_percent_holy_set/regular/holy_test_set_10_percent_regular.h5'
# # # h5 = '/Users/phil/Dropbox/HIRES_LAB/GitHub/Phillip_AC/model_testing/all_data/test_data/10_percent_holy_set/3lag/holy_test_set_10_percent_3lag.h5'
# # # count = 19
# # # start = 24850 - 1000
# # # end = 24850 + 1000
# # # # start = 0
# # #
# # #
# # # # L = 40000
# # # #  32736
# # #
# # # with h5py.File(h5, 'r') as h:
# # #     L = len(h['labels'][:])
# # #     print(L)
# # #     L = end - start
# # #     imgs = h['images'][start:end:L//count]
# # #     # L = len(h['labels'][:])
# # #     titles = np.arange(L)[start:end:L//count]
# # #
# # # fig, ax = plt.subplots(5, 4)
# # # for ind, ax2 in enumerate(ax.flatten()):
# # #     ax2.imshow(imgs[ind])
# # #     # ax2.title.set_text(titles[ind])
# # #
# # #
# # #
# # # import matplotlib.pyplot as plt
# # # import h5py
# # # import numpy as np
# # # h5 = '/Users/phil/Dropbox/HIRES_LAB/GitHub/Phillip_AC/model_testing/all_data/test_data/10_percent_holy_set/regular/holy_test_set_10_percent_regular.h5'
# # # h5 = '/Users/phil/Dropbox/HIRES_LAB/GitHub/Phillip_AC/model_testing/all_data/test_data/10_percent_holy_set/3lag/holy_test_set_10_percent_3lag.h5'
# # # h5 =  '/Users/phil/Dropbox/HIRES_LAB/GitHub/Phillip_AC/model_testing/all_data/test_data/full_holy_set/3lag/holy_set_80_border_single_frame_3lag.h5'
# # #
# # # # start = 0
# # #
# # #
# # # # L = 40000
# # # #  32736
# # #
# # # with h5py.File(h5, 'r') as h:
# # #     imgs = []
# # #     for k1, k2 in utils.loop_segments(h['frame_nums'][:]):
# # #         i = np.where(h['labels'][k1:k2]==1)[0]
# # #         i = i[int(len(i)/2)]
# # #         # i = int(np.mean([k1, k2])) # center ind
# # #         imgs.append(h['images'][k1+i])
# # # imgs = np.asarray(imgs)
# # #
# # # for ind, img_in in enumerate(imgs):
# # #     if ind%20 == 0:
# # #         fig, ax = plt.subplots(5, 4)
# # #         ax = ax.flatten()
# # #     ax[ind%20].imshow(img_in)
# # #     ax[ind%20].title.set_text(str(ind))
# # #     # ax2.title.set_text(titles[ind])
# # #
# # # """
# # # ##################################################################################################
# # # ##################################################################################################
# # # ##################use to compare unfinished trained data #########################################
# # # ##################################################################################################
# # # """
# # # test_set_to = 10
# # # from natsort import natsorted, ns
# # #
# # # mod_dir = '/Volumes/GoogleDrive-114825029448473821206/My Drive/LIGHT_GBM/models/10_sets_frame_nums_split_then_random_split_method_numpy_feature_selection_V1/'
# # # mods = utils.get_files(mod_dir, '*')
# # # mods = natsorted(mods, alg=ns.REAL)[:test_set_to]
# # # # from natsort import natsorted
# # # # mods = natsorted(mods)[:-1]
# # # features_out_of_10 = []
# # # for k in mods:
# # #     lgbm = utils.load_obj(k)
# # #     features_out_of_10.append(lgbm.feature_importance()>0)
# # # features_out_of_10 = np.sum(np.asarray(features_out_of_10), axis = 0)
# # #
# # # for k in range(test_set_to):
# # #     print(np.round(100 * np.mean(features_out_of_10 > k), 2), '% have ', k+1, ' or more')
# # #     print('count ', np.sum(features_out_of_10 > k))
# # # count_importance = np.where(features_out_of_10>=3)[0]
# # # print('____________________')
# # # mod_dir = '/Volumes/GoogleDrive-114825029448473821206/My Drive/LIGHT_GBM/models/10_sets_frame_nums_split_then_random_split_method/'
# # # mods = utils.get_files(mod_dir, '*')
# # # mods = natsorted(mods, alg=ns.REAL)[:test_set_to]
# # # # from natsort import natsorted
# # # # mods = natsorted(mods)[:-1]
# # # features_out_of_10 = []
# # # for k in mods:
# # #     lgbm = utils.load_obj(k)
# # #     features_out_of_10.append(lgbm.feature_importance()>0)
# # # features_out_of_10 = np.sum(np.asarray(features_out_of_10), axis = 0)
# # #
# # # for k in range(test_set_to):
# # #     print(np.round(100 * np.mean(features_out_of_10 > k), 2), '% have ', k+1, ' or more')
# # #     print('count ', np.sum(features_out_of_10 > k))
# # # count_importance = np.where(features_out_of_10>=3)[0]
# # #
# # #
# # #
# # # """
# # # CHOOSING THE BEST FEATURES, I SHOULD TRAIN AND TEST THIS FOR MY SHIT BEFORE CONFIRMING IT IS ALL GOOD.
# # # I have times used and gain importance
# # # each conveys something different and I can choose whichever I want. or I can do a combination of both because they are
# # # not perfectly overlapping
# # # I can also use SD as a decider as it can show variables that would be useful like outliers that catch something
# # #
# # # I could also train data on like the top 15k or something or maybe even 32k?? if i do all at least one will i get the
# # # same results?
# # #
# # # so after looking at https://simility.com/wp-content/uploads/2020/07/WP-Feature-Selection.pdf
# # # I think it is totally appropriate to take the union of the models and train again and see how they do
# # # or I could do some voting
# # #
# # # """
# # # import os
# # # """ times used metric  """
# # # mod_dir = '/Volumes/GoogleDrive-114825029448473821206/My Drive/LIGHT_GBM/models/10_sets_frame_nums_split_then_random_split_method/'
# # # mods = utils.get_files(mod_dir, '*')
# # # # from natsort import natsorted
# # # # mods = natsorted(mods)[:-1]
# # # features_out_of_10 = []
# # # for k in mods:
# # #     lgbm = utils.load_obj(k)
# # #     features_out_of_10.append(lgbm.feature_importance()>0)
# # # features_out_of_10 = np.sum(np.asarray(features_out_of_10), axis = 0)
# # #
# # # for k in range(10):
# # #     print(np.round(100 * np.mean(features_out_of_10 > k), 2), '% have ', k+1, ' or more')
# # #     print('count ', np.sum(features_out_of_10 > k))
# # # count_importance = np.where(features_out_of_10>=3)[0]
# # #
# # # non_zero_features = np.where(features_out_of_10>0)[0]
# # #
# # # non_zero_features_bool = [k>0 for k in features_out_of_10]
# # #
# # # bd = '/Volumes/GoogleDrive-114825029448473821206/My Drive/LIGHT_GBM/feature_index_for_feature_selection'
# # # np.save(bd+os.sep+'non_zero_features_bool_29913_features.npy', non_zero_features_bool)
# # #
# # # """ gain importance mean  """
# # # features_out_of_10 = []
# # # #3063
# # # for k in mods:
# # #     lgbm = utils.load_obj(k)
# # #     features_out_of_10.append(lgbm.feature_importance(importance_type='gain'))
# # # x = np.asarray(features_out_of_10)
# # # features_out_of_10 = np.mean(np.asarray(features_out_of_10), axis = 0)
# # #
# # # for k in np.linspace(0, 4, 30):
# # #     print(np.round(100 * np.mean(features_out_of_10 > k), 2), '% have more than', k)
# # #     print('count ', np.sum(features_out_of_10 > k))
# # # gain_importance = np.where(features_out_of_10>1.793103448275862)[0]
# # #
# # # tmp1 = np.unique(np.concatenate([gain_importance, count_importance]))
# # # len(tmp1), len(count_importance), len(gain_importance)
# # #
# # #
# # # """ gain importance max  """
# # # features_out_of_10 = []
# # # #3063
# # # for k in mods:
# # #     lgbm = utils.load_obj(k)
# # #     features_out_of_10.append(lgbm.feature_importance(importance_type='gain'))
# # # features_out_of_10 = np.asarray(features_out_of_10)
# # # features_out_of_10 = np.max(features_out_of_10, axis = 0)
# # #
# # # for k in np.linspace(1, 40, 30):
# # #     print(np.round(100 * np.mean(features_out_of_10 > k), 2), '% have more than', k)
# # #     print('count ', np.sum(features_out_of_10 > k))
# # #
# # # tmp1 = []
# # # for k in np.linspace(0, 100, 100):
# # #     tmp1.append(np.sum(features_out_of_10 > k))
# # # plt.plot(tmp1, '.')
# # #
# # #
# # #
# # # """ gain importance mean  """
# # # features_out_of_10 = []
# # # #3063
# # # for k in mods:
# # #     lgbm = utils.load_obj(k)
# # #     features_out_of_10.append(lgbm.feature_importance(importance_type='gain'))
# # # x = np.asarray(features_out_of_10)
# # # features_out_of_10 = np.mean(np.asarray(features_out_of_10), axis = 0)
# # #
# # # for k in np.linspace(0, 4, 30):
# # #     print(np.round(100 * np.mean(features_out_of_10 > k), 2), '% have more than', k)
# # #     print('count ', np.sum(features_out_of_10 > k))
# # #
# # #
# # #
# # # bins = np.linspace(0.00001, 1, 1000)
# # # plt.hist(features_out_of_10, bins = bins)
# # # np.mean(features_out_of_10<=0.002)
# # #
# # # tmp8 = features_out_of_10>=0.004
# # #
# # # tmp9 = features_out_of_10>=2
# # #
# # # tmp10 = np.mean(np.vstack((tmp8, tmp9))*1, axis = 0)>0
# # #
# # # np.sum(tmp8), np.sum(tmp9), np.sum(tmp10), len(tmp8)
# # #
# # # """
# # # so the rules are, include all the data that is 2 or higher and that is greater than 0.002 (for now) that result sin 87.7%
# # # for the new set
# # # """
# # #
# # #
# # # utils.np_stats(features_out_of_10)
# # # xu = np.unique(features_out_of_10)
# # # a = xu[1]/2
# # # bins = list(xu-a)
# # # bins.append(xu[-1]+a)
# # # import matplotlib.pyplot as plt
# # # count = []
# # # for k in xu[1:]:
# # #     count.append(np.sum(k==features_out_of_10))
# # #
# # # plt.bar(range(len(count)), count)
# # # """
# # # want to plot to see if there is a clear gain features that have a mean for the first bump i can remove for feature selection
# # # """
# # # win = 1001
# # # x = np.convolve(count, np.ones(win)/win, mode='valid')
# # # plt.plot(xu[1:], x)
# # # x2 = np.cumsum(count)
# # # x2 = x2/np.max(x2)
# # # plt.plot(x2)
# # #
# # #
# # # tmp1 = np.unique(np.concatenate([gain_importance, count_importance]))
# # # len(tmp1), len(count_importance), len(gain_importance)
# # #
# # #
# # #
# # #
# # #
# # #
# # #
# # #
# # #
# # #
# # # """ gain importance SD to see if there are certain predictors that are used in one but not other sub models  """
# # # features_out_of_10 = []
# # # #3063
# # # for k in mods:
# # #     lgbm = utils.load_obj(k)
# # #     features_out_of_10.append(lgbm.feature_importance(importance_type='gain'))
# # # features_out_of_10 = np.asarray(features_out_of_10)
# # # features_out_of_10 = np.std(features_out_of_10, axis = 0)
# # #
# # # # for k in np.linspace(1, 40, 30):
# # # #     print(np.round(100 * np.mean(features_out_of_10 > k), 2), '% have more than', k)
# # # #     print('count ', np.sum(features_out_of_10 > k))
# # #
# # # tmp1 = []
# # # for k in np.linspace(0, 1000, 100):
# # #     tmp1.append(np.sum(features_out_of_10 > k))
# # # plt.plot(tmp1, '.')
# # # plt.xlabel('SD of each set of 10 ')
# # # plt.ylabel('count greater than ...')
# # #
# # #
# # #
# # #
# # #
# # #
# # #
# # # plt.hist(x.flatten(), bins=np.arange(0, 200))
# # #
# # #
# # # tmp1 = '/Users/phil/Dropbox/HIRES_LAB/GitHub/whacc/whacc/whacc_data/feature_data/feature_data_dict.pkl'
# # # tmp1 = utils.load_obj(tmp1) # ok this needs to change
# # #
# # #
# # # tmp1 = '/Volumes/GoogleDrive-114825029448473821206/My Drive/final_features_window_version_corrected_v2/'
# # # tmp1 = utils.get_files(tmp1, '*')
# # #
# # #
# # # """
# # # #####################################################################################################################
# # # #####################################################################################################################
# # # #####################################################################################################################
# # # ##################################### LOAD AND PREDICT WITH THE GBM MODEL############################################
# # # #####################################################################################################################
# # # #####################################################################################################################
# # # """
# # # import lightgbm as lgb
# # # from whacc import utils
# # # import numpy as np
# # # import matplotlib.pyplot as plt
# # # fn = '/Volumes/GoogleDrive-114825029448473821206/My Drive/LIGHT_GBM/OPTUNA_mod_saves/V1/67.pkl'
# # # mod = utils.load_obj(fn)
# # #
# # # x = np.random.rand(100, 2105)
# # # testy = x[:, 0]>.93
# # # yhat = mod.predict(x)
# # #
# # # plt.plot(yhat)
# # #
# # #
# # # #  precition recal curve
# # # from sklearn.metrics import precision_recall_curve
# # # precision, recall, thresholds = precision_recall_curve(testy, yhat)
# # #
# # #
# # # # plot the roc curve for the model
# # # no_skill = len(testy[testy==1]) / len(testy)
# # # plt.plot([0,1], [no_skill,no_skill], linestyle='--', label='No Skill')# # from whacc import utils, image_tools
# # # # #
# # # # # import copy
# # # # # import numpy as np
# # # # # import pandas as pd
# # # # # import h5py
# # # # #
# # # # # from tqdm.autonotebook import tqdm
# # # # #
# # # # #
# # # # # class feature_maker():
# # # # #     def __init__(self, h5_in, frame_num_ind=None, frame_nums=None, operational_key='FD__original', disable_tqdm=False,
# # # # #                  delete_if_exists=False, index_features_delete_the_rest=None):
# # # # #         """
# # # # #
# # # # #         Parameters
# # # # #         ----------
# # # # #         h5_in : h5 string pointing to the h4 file with the data to transform
# # # # #         frame_num_ind : int referencing the frame num  ind to transform, note: if save_it is one ALL data is converted
# # # # #         automatically and saved in h5. frame_num_ind only works when you call with
# # # # #         frame_nums : default None, auto looks for key 'frame_nums' in h5 file or you can insert your own
# # # # #         operational_key : the data array key to be transformed
# # # # #         disable_tqdm : default False, when save_it is True it will show a loading bar with the progress unless set to true
# # # # #         delete_if_exists : default False, when calling a function with save_it as True, you can choose to overwrite that
# # # # #         data by setting this value to True
# # # # #
# # # # #         Returns
# # # # #         -------
# # # # #         feature maker class
# # # # #
# # # # #         Examples
# # # # #         ________
# # # # #
# # # # #         h5_in = '/Users/phil/Desktop/AH0407_160613_JC1003_AAAC_3lag.h5'
# # # # #
# # # # #         FM = feature_maker(h5_in, frame_num_ind=2, delete_if_exists = True) #set frame_num_ind to an int so that we can quickly look at the transformation
# # # # #         data, data_name = FM.shift(5, save_it=False) # shift it 5 to the right, fills in with nan as needed, look at just the 5th frame num set (5th video)
# # # # #         # to see how it looks
# # # # #         print('the below name will be used to save the data in the the h5 when calling functions with save_it=True')
# # # # #         print(data_name)
# # # # #         FM.shift(5, save_it=True) # now lets save it
# # # # #
# # # # #         data, data_name_rolling_mean_100 = FM.rolling(100, 'mean', save_it=True)  #lets do the rolling mean and save it
# # # # #
# # # # #         data, data_name = FM.operate('diff', kwargs={'periods': 1}, save_it=False) # lets perform a diff operation
# # # # #         print(data_name)
# # # # #         print(data)
# # # # #         FM.operate('diff', kwargs={'periods': -1}, save_it=True) # now lets save it and save it
# # # # #
# # # # #         # now lets change the operational key so we can transform some data we just transformed, specifically the rolling mean 10
# # # # #         FM.set_operation_key(data_name_rolling_mean_100)
# # # # #
# # # # #         data, data_name_diff_100_mean = FM.operate('diff', kwargs={'periods': -50}, save_it=False) # lets check how the name will change
# # # # #         print(data_name_diff_100_mean)
# # # # #         print("notice the FD__ twice, this means the data has been transformed twice")
# # # # #         print('also notice that how the data was transformed can be seen because it is split up by ____ (4 underscores)')
# # # # #
# # # # #         data, data_name_diff_100_mean = FM.operate('diff', kwargs={'periods': -50}, save_it=True) # save it
# # # # #
# # # # #         a = utils.print_h5_keys(h5_in, 1, 1)
# # # # #         key_name_list = ['FD__original', 'FD__FD__FD__original_rolling_mean_W_100_SFC_0_MP_100_____diff_periods_-50____', 'FD__FD__original_rolling_mean_W_100_SFC_0_MP_100____']
# # # # #         with h5py.File(h5_in, 'r+') as h:
# # # # #             for k in key_name_list:
# # # # #                 plt.plot(h[k][:8000, 0])
# # # # #         """
# # # # #         if utils.h5_key_exists(h5_in, 'has_data_been_randomized'):
# # # # #             assert image_tools.get_h5_key_and_concatenate(h5_in,
# # # # #                                                           'has_data_been_randomized').tolist() is False, """this data has been randomized, it is not fit to perform temporal operations on, search for key 'has_data_been_randomized' for more info"""
# # # # #
# # # # #         self._frame_num_ind_save_ = None
# # # # #         self.disable_tqdm = disable_tqdm
# # # # #         self.h5_in = h5_in
# # # # #         self.frame_num_ind = frame_num_ind
# # # # #         self.delete_if_exists = delete_if_exists
# # # # #         self.operational_key = operational_key
# # # # #         if frame_nums is None:
# # # # #             print('extracting frame_nums from h5 file, ideally you should just put that in yourself though')
# # # # #             frame_nums = image_tools.get_h5_key_and_concatenate(h5_in, 'frame_nums')
# # # # #         self.all_frame_nums = frame_nums
# # # # #         self.len_frame_nums = len(self.all_frame_nums)
# # # # #         self.set_data_and_frame(frame_num_ind)
# # # # #         index_features_delete_the_rest
# # # # #
# # # # #     def set_data_inds(self, ind):  # frame nums used ot extract below in 'set_operation_key'
# # # # #         tmp_inds = np.asarray(utils.loop_segments(self.all_frame_nums, returnaslist=True))
# # # # #         if ind is None:
# # # # #             self.data_inds = [tmp_inds[0][0], tmp_inds[-1][-1]]
# # # # #         else:
# # # # #             self.data_inds = tmp_inds[:, ind]
# # # # #
# # # # #     def set_operation_key(self, key_name=None):
# # # # #         if key_name is not None:
# # # # #             self.operational_key = key_name
# # # # #         with h5py.File(self.h5_in, 'r') as h:
# # # # #             self.full_data_shape = np.asarray(h[self.operational_key].shape)
# # # # #             if self.frame_num_ind is None:
# # # # #                 self.data = pd.DataFrame(copy.deepcopy(h[self.operational_key][:]))
# # # # #             else:
# # # # #                 a = self.data_inds  # just the current frame numbers
# # # # #                 self.data = pd.DataFrame(copy.deepcopy(h[self.operational_key][a[0]:a[1]]))
# # # # #
# # # # #     def init_h5_data_key(self, data_key, delete_if_exists=False):
# # # # #         key_exists = utils.h5_key_exists(self.h5_in, data_key)
# # # # #         assert not (
# # # # #                 key_exists and not delete_if_exists), "key exists, if you want to overwrite set 'delete_if_exists' = True"
# # # # #         with h5py.File(self.h5_in, 'r+') as x:
# # # # #             if key_exists and delete_if_exists:
# # # # #                 print('deleting key to overwrite it')
# # # # #                 del x[data_key]
# # # # #             x.create_dataset_like(data_key, x[self.operational_key])
# # # # #
# # # # #     def rolling(self, window, operation, shift_from_center=0, min_periods=None, save_it=False, kwargs={}):
# # # # #         """
# # # # #
# # # # #         Parameters
# # # # #         ----------
# # # # #         window : window size int
# # # # #         operation : a string with the operation e.g. 'mean' or 'std' see pandas docs for rolling
# # # # #         shift_from_center : default 0 but can shift as needed
# # # # #         min_periods : default is equal to win length, only allows operation when we have this many data points. so deals with
# # # # #         the edges
# # # # #         save_it : bool, False, loop through frame nums and save to h5 file
# # # # #         kwargs : dict of args that can be applied to 'operation' function
# # # # #
# # # # #         Returns
# # # # #         -------
# # # # #
# # # # #         """
# # # # #         if min_periods is None:
# # # # #             min_periods = window
# # # # #         add_name_list = ['FD__' + self.operational_key + '_rolling_',
# # # # #                          '_W_' + str(window) + '_SFC_' + str(shift_from_center) + '_MP_' + str(min_periods) + '____']
# # # # #         add_name_str = operation.join(add_name_list)
# # # # #         if save_it:
# # # # #             self._save_it_(self.rolling, window, operation, shift_from_center, min_periods, False, kwargs)
# # # # #             return None, add_name_str
# # # # #         data_frame = self.data.copy()
# # # # #         for i1, i2 in utils.loop_segments(self.frame_nums):
# # # # #             df_rolling = self.data[i1:i2].rolling(window=window, min_periods=min_periods, center=True)
# # # # #             tmp_func = eval('df_rolling.' + operation)
# # # # #             data_frame[i1:i2] = tmp_func(**kwargs).shift(shift_from_center).astype(np.float32)
# # # # #         return data_frame, add_name_str
# # # # #
# # # # #     def shift(self, shift_by, save_it=False):
# # # # #         """
# # # # #
# # # # #         Parameters
# # # # #         ----------
# # # # #         shift_by : amount to shift by
# # # # #         save_it :  bool, False, loop through frame nums and save to h5 file
# # # # #
# # # # #         Returns
# # # # #         -------
# # # # #
# # # # #         """
# # # # #         add_name_str = 'FD__' + self.operational_key + '_shift_' + str(shift_by) + '____'
# # # # #         if save_it:
# # # # #             self._save_it_(self.shift, shift_by)
# # # # #             return None, add_name_str
# # # # #
# # # # #         data_frame = self.data.copy()
# # # # #         for i1, i2 in utils.loop_segments(self.frame_nums):
# # # # #             data_frame[i1:i2] = self.data[i1:i2].shift(shift_by).astype(np.float32)
# # # # #         return data_frame, add_name_str
# # # # #
# # # # #     def operate(self, operation, save_it=False, extra_name_str='', kwargs={}):
# # # # #         """
# # # # #
# # # # #         Parameters
# # # # #         ----------
# # # # #         operation : a string with the operation e.g. 'mean' or 'std' or 'diff' see pandas operation on  dataframes
# # # # #         save_it :  bool, False, loop through frame nums and save to h5 file
# # # # #         extra_name_str : add to key name string if desired
# # # # #         kwargs : dict of args that can be applied to 'operation' function see pandas operation on  dataframes
# # # # #
# # # # #         Returns
# # # # #         -------
# # # # #
# # # # #         """
# # # # #         add_name_str_tmp = self.dict_to_string_name(kwargs)
# # # # #         add_name_str = 'FD__' + self.operational_key + '_' + operation + '_' + add_name_str_tmp + extra_name_str + '____'
# # # # #         if save_it:
# # # # #             self._save_it_(self.operate, operation, False, extra_name_str, kwargs)
# # # # #             return None, add_name_str
# # # # #         data_frame = self.data.copy()
# # # # #         for i1, i2 in utils.loop_segments(self.frame_nums):
# # # # #             data_frame[i1:i2] = eval('self.data[i1:i2].' + operation + '(**kwargs).astype(np.float32)')
# # # # #         return data_frame, add_name_str
# # # # #
# # # # #     @staticmethod
# # # # #     def dict_to_string_name(in_dict):
# # # # #         """
# # # # #         used to transform dict into a string name for naming h5 keys
# # # # #         Parameters
# # # # #         ----------
# # # # #         in_dict : dict
# # # # #
# # # # #         Returns
# # # # #         -------
# # # # #         string
# # # # #         """
# # # # #         str_list = []
# # # # #         for k in in_dict:
# # # # #             str_list.append(k)
# # # # #             str_list.append(str(in_dict[k]))
# # # # #         return '_'.join(str_list)
# # # # #
# # # # #     def set_data_and_frame(self, ind):
# # # # #         self.frame_num_ind = ind
# # # # #         if ind is None:
# # # # #             self.frame_nums = copy.deepcopy(self.all_frame_nums)
# # # # #         else:
# # # # #             self.frame_nums = [self.all_frame_nums[ind]]
# # # # #         self.set_data_inds(ind)
# # # # #         self.set_operation_key()
# # # # #
# # # # #     # tqdm(sorted(random_frame_inds[i]), disable=disable_TQDM, total=total_frames, initial=cnt1)
# # # # #     def _save_it_(self, temp_funct, *args):
# # # # #         self._frame_num_ind_save_ = copy.deepcopy(self.frame_num_ind)
# # # # #         with h5py.File(self.h5_in, 'r+') as h:
# # # # #             for k in tqdm(range(self.len_frame_nums), disable=self.disable_tqdm):
# # # # #                 self.set_data_and_frame(k)
# # # # #                 data, key_name = temp_funct(*args)
# # # # #                 if k == 0:
# # # # #                     self.init_h5_data_key(key_name, delete_if_exists=self.delete_if_exists)
# # # # #                     print('making key, ' + key_name)
# # # # #                 a = self.data_inds
# # # # #                 h[key_name][a[0]:a[1]] = data
# # # # #         self.set_data_and_frame(self._frame_num_ind_save_)  # set data back to what it was when user set it
# # # # #
# # # # #     def total_rolling_operation(self, data_in, win, operation_function, shift_from_center=0):
# # # # #         """
# # # # #         NOTE: for making feature data proper key names for saving is 'FD_TOTAL_' folowed by operation e.g. 'FD_TOTAL_nanstd'
# # # # #         Parameters
# # # # #         ----------
# # # # #         data_in : 2D matrix
# # # # #         win : window size
# # # # #         operation_function : function to be applies to each window e.g. np.nanmean, note DON'T include parentheses
# # # # #         shift_from_center : num units shift from center
# # # # #
# # # # #         Returns
# # # # #         -------
# # # # #         data_out: output data
# # # # #         is_nan_inds: bool array indexing where nans were
# # # # #         """
# # # # #         assert win % 2 == 1, 'window must be odd'
# # # # #         mid = win // 2
# # # # #         pad = np.zeros([win, data_in.shape[1]]) * np.nan
# # # # #
# # # # #         L_pad = pad[:mid - shift_from_center]
# # # # #         R_pad = pad[:mid + shift_from_center]
# # # # #
# # # # #         data_in = np.vstack([L_pad, data_in, R_pad])
# # # # #
# # # # #         is_nan_inds = []
# # # # #         data_out = []
# # # # #         for k in range(data_in.shape[0] - win + 1):
# # # # #             x = data_in[k:(k + win)]
# # # # #             data_out.append(operation_function(x))
# # # # #             is_nan_inds.append(np.any(np.isnan(x)))
# # # # #         return np.asarray(data_out), np.asarray(is_nan_inds)
# # # # #
# # # # #     def total_rolling_operation_h5_wrapper(self, window, operation, key_to_operate_on, mod_key_name=None,
# # # # #                                            save_it=False,
# # # # #                                            shift_from_center=0):
# # # # #         if save_it:
# # # # #             assert mod_key_name is not None, """if save_it is True, 'mod_key_name' must not be None e.g. 'FD_TOTAL_std_1_of_'"""
# # # # #         all_data = []
# # # # #         with h5py.File(self.h5_in, 'r') as h:
# # # # #             frame_nums = h['frame_nums'][:]
# # # # #             for i, (i1, i2) in enumerate(utils.loop_segments(frame_nums)):
# # # # #                 data_out, is_nan_inds = self.total_rolling_operation(h[key_to_operate_on][i1:i2, :], window, operation,
# # # # #                                                                      shift_from_center=shift_from_center)
# # # # #                 all_data.append(data_out)
# # # # #         all_data = np.hstack(all_data)
# # # # #         mod_key_name = mod_key_name + key_to_operate_on
# # # # #         if save_it:
# # # # #             utils.overwrite_h5_key(self.h5_in, mod_key_name, all_data)
# # # # #         return all_data
# # # # #
# # # # #
# # # # # from tqdm.auto import tqdm
# # # # # import numpy as np
# # # # #
# # # # # ########################################################################################################################
# # # # # ########################################################################################################################
# # # # # h5_feature_data = '/Users/phil/Desktop/pipeline_test/AH0407x160609_3lag_feature_data.h5'
# # # # # FM = feature_maker(h5_feature_data, operational_key='FD__original', delete_if_exists=True)
# # # # #
# # # # # for periods in tqdm([-5]):
# # # # #     data, key_name = FM.shift(periods, save_it=True)
# # # # # ########################################################################################################################
# # # # # ########################################################################################################################
# # # # # ########################################################################################################################
# # # # # # from whacc.feature_maker import feature_maker, total_rolling_operation_h5_wrapper
# # # # #
# # # # #
# # # # # for periods in tqdm([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5]):
# # # # #     data, key_name = FM.shift(periods, save_it=True)
# # # # #
# # # # # for smooth_it_by in tqdm([3, 7, 11, 15, 21, 41, 61]):
# # # # #     data, key_name = FM.rolling(smooth_it_by, 'mean', save_it=True)
# # # # #
# # # # # for periods in tqdm([-50, -20, -10, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 10, 20, 50]):
# # # # #     data, key_name = FM.operate('diff', kwargs={'periods': periods}, save_it=True)
# # # # #
# # # # # for smooth_it_by in tqdm([3, 7, 11, 15, 21, 41, 61]):
# # # # #     data, key_name = FM.rolling(smooth_it_by, 'std', save_it=True)
# # # # #
# # # # # win = 1
# # # # # # key_to_operate_on = 'FD__original'
# # # # # op = np.std
# # # # # mod_key_name = 'FD_TOTAL_std_' + str(win) + '_of_'
# # # # # all_keys = utils.lister_it(utils.print_h5_keys(FM.h5_in, 1, 0), 'FD__', 'FD_TOTAL')
# # # # # for key_to_operate_on in tqdm(all_keys):
# # # # #     data_out = FM.total_rolling_operation_h5_wrapper(win, op, key_to_operate_on, mod_key_name=mod_key_name,
# # # # #                                                      save_it=True)
# # # # #
# # # # # utils.get_selected_features(greater_than_or_equal_to=4)
# # # # #
# # # # # inds = fd_dict['features_used_of_10'] >= 4
# # # # # tmp1 = fd_dict['full_feature_names_and_neuron_nums'][inds]
# # # # # import numpy as np
# # # # #
# # # # # tmp2 = np.unique(fd_dict['full_neuron_nums'][inds])
# # # # #
# # # # # for k in tmp1:
# # # # #     print(k)
# # # # #
# # # # # """
# # # # # 'FD_TOTAL_std_1_of_original_diff_periods_3',
# # # # # 'FD_TOTAL_std_1_of_original_rolling_mean_W_3_SFC_0_MP_3',
# # # # # 'FD_TOTAL_std_1_of_original_rolling_mean_W_7_SFC_0_MP_7',
# # # # # 'FD_TOTAL_std_1_of_original_rolling_mean_W_11_SFC_0_MP_11',
# # # # # 'FD_TOTAL_std_1_of_original_shift_3', 'FD_TOTAL_std_1_of_original'],
# # # # #
# # # # # do those first then take any of the completed data from them that are used as single features
# # # # #
# # # # # then save the TOTAL operations and singles,
# # # # #
# # # # # then go through all the singles
# # # # #
# # # # # """
# # # # #
# # # # # len(utils.lister_it(tmp1, '_diff_'))
# # # # #
# # # # # h52 = '/Users/phil/Desktop/pipeline_test/AH0407x160609_3lag_feature_data.h5'
# # # # # utils.print
# # # # #
# # # # #
# # # # # def total_rolling_sliding_window_view(data_in, win, operation_function, shift_from_center=0):
# # # # #     assert win % 2 == 1, 'window must be odd'
# # # # #     mid = win // 2
# # # # #     pad = np.zeros([win, data_in.shape[1]]) * np.nan
# # # # #
# # # # #     L_pad = pad[:mid - shift_from_center]
# # # # #     R_pad = pad[:mid + shift_from_center]
# # # # #
# # # # #     data_in = np.vstack([L_pad, data_in, R_pad])
# # # # #     w = data_in.shape[1]
# # # # #     data_in = np.lib.stride_tricks.sliding_window_view(data_in, (win, w))
# # # # #     data_in = np.reshape(data_in, [-1, win * w])
# # # # #     data_out = operation_function(data_in, axis=1)
# # # # #     return np.asarray(data_out)
# # # #
# # # #
# # # # from whacc import utils, image_tools
# # # # import matplotlib.pyplot as plt
# # # # import h5py
# # # # import numpy as np
# # # # h5 = '/Users/phil/Dropbox/HIRES_LAB/GitHub/Phillip_AC/model_testing/all_data/test_data/10_percent_holy_set/regular/holy_test_set_10_percent_regular.h5'
# # # # h5 = '/Users/phil/Dropbox/HIRES_LAB/GitHub/Phillip_AC/model_testing/all_data/test_data/10_percent_holy_set/3lag/holy_test_set_10_percent_3lag.h5'
# # # # count = 19
# # # # start = 24850 - 1000
# # # # end = 24850 + 1000
# # # # # start = 0
# # # #
# # # #
# # # # # L = 40000
# # # # #  32736
# # # #
# # # # with h5py.File(h5, 'r') as h:
# # # #     L = len(h['labels'][:])
# # # #     print(L)
# # # #     L = end - start
# # # #     imgs = h['images'][start:end:L//count]
# # # #     # L = len(h['labels'][:])
# # # #     titles = np.arange(L)[start:end:L//count]
# # # #
# # # # fig, ax = plt.subplots(5, 4)
# # # # for ind, ax2 in enumerate(ax.flatten()):
# # # #     ax2.imshow(imgs[ind])
# # # #     # ax2.title.set_text(titles[ind])
# # # #
# # # #
# # # #
# # # # import matplotlib.pyplot as plt
# # # # import h5py
# # # # import numpy as np
# # # # h5 = '/Users/phil/Dropbox/HIRES_LAB/GitHub/Phillip_AC/model_testing/all_data/test_data/10_percent_holy_set/regular/holy_test_set_10_percent_regular.h5'
# # # # h5 = '/Users/phil/Dropbox/HIRES_LAB/GitHub/Phillip_AC/model_testing/all_data/test_data/10_percent_holy_set/3lag/holy_test_set_10_percent_3lag.h5'
# # # # h5 =  '/Users/phil/Dropbox/HIRES_LAB/GitHub/Phillip_AC/model_testing/all_data/test_data/full_holy_set/3lag/holy_set_80_border_single_frame_3lag.h5'
# # # #
# # # # # start = 0
# # # #
# # # #
# # # # # L = 40000
# # # # #  32736
# # # #
# # # # with h5py.File(h5, 'r') as h:
# # # #     imgs = []
# # # #     for k1, k2 in utils.loop_segments(h['frame_nums'][:]):
# # # #         i = np.where(h['labels'][k1:k2]==1)[0]
# # # #         i = i[int(len(i)/2)]
# # # #         # i = int(np.mean([k1, k2])) # center ind
# # # #         imgs.append(h['images'][k1+i])
# # # # imgs = np.asarray(imgs)
# # # #
# # # # for ind, img_in in enumerate(imgs):
# # # #     if ind%20 == 0:
# # # #         fig, ax = plt.subplots(5, 4)
# # # #         ax = ax.flatten()
# # # #     ax[ind%20].imshow(img_in)
# # # #     ax[ind%20].title.set_text(str(ind))
# # # #     # ax2.title.set_text(titles[ind])
# # # #
# # # # """
# # # # ##################################################################################################
# # # # ##################################################################################################
# # # # ##################use to compare unfinished trained data #########################################
# # # # ##################################################################################################
# # # # """
# # # # test_set_to = 10
# # # # from natsort import natsorted, ns
# # # #
# # # # mod_dir = '/Volumes/GoogleDrive-114825029448473821206/My Drive/LIGHT_GBM/models/10_sets_frame_nums_split_then_random_split_method_numpy_feature_selection_V1/'
# # # # mods = utils.get_files(mod_dir, '*')
# # # # mods = natsorted(mods, alg=ns.REAL)[:test_set_to]
# # # # # from natsort import natsorted
# # # # # mods = natsorted(mods)[:-1]
# # # # features_out_of_10 = []
# # # # for k in mods:
# # # #     lgbm = utils.load_obj(k)
# # # #     features_out_of_10.append(lgbm.feature_importance()>0)
# # # # features_out_of_10 = np.sum(np.asarray(features_out_of_10), axis = 0)
# # # #
# # # # for k in range(test_set_to):
# # # #     print(np.round(100 * np.mean(features_out_of_10 > k), 2), '% have ', k+1, ' or more')
# # # #     print('count ', np.sum(features_out_of_10 > k))
# # # # count_importance = np.where(features_out_of_10>=3)[0]
# # # # print('____________________')
# # # # mod_dir = '/Volumes/GoogleDrive-114825029448473821206/My Drive/LIGHT_GBM/models/10_sets_frame_nums_split_then_random_split_method/'
# # # # mods = utils.get_files(mod_dir, '*')
# # # # mods = natsorted(mods, alg=ns.REAL)[:test_set_to]
# # # # # from natsort import natsorted
# # # # # mods = natsorted(mods)[:-1]
# # # # features_out_of_10 = []
# # # # for k in mods:
# # # #     lgbm = utils.load_obj(k)
# # # #     features_out_of_10.append(lgbm.feature_importance()>0)
# # # # features_out_of_10 = np.sum(np.asarray(features_out_of_10), axis = 0)
# # # #
# # # # for k in range(test_set_to):
# # # #     print(np.round(100 * np.mean(features_out_of_10 > k), 2), '% have ', k+1, ' or more')
# # # #     print('count ', np.sum(features_out_of_10 > k))
# # # # count_importance = np.where(features_out_of_10>=3)[0]
# # # #
# # # #
# # # #
# # # # """
# # # # CHOOSING THE BEST FEATURES, I SHOULD TRAIN AND TEST THIS FOR MY SHIT BEFORE CONFIRMING IT IS ALL GOOD.
# # # # I have times used and gain importance
# # # # each conveys something different and I can choose whichever I want. or I can do a combination of both because they are
# # # # not perfectly overlapping
# # # # I can also use SD as a decider as it can show variables that would be useful like outliers that catch something
# # # #
# # # # I could also train data on like the top 15k or something or maybe even 32k?? if i do all at least one will i get the
# # # # same results?
# # # #
# # # # so after looking at https://simility.com/wp-content/uploads/2020/07/WP-Feature-Selection.pdf
# # # # I think it is totally appropriate to take the union of the models and train again and see how they do
# # # # or I could do some voting
# # # #
# # # # """
# # # # import os
# # # # """ times used metric  """
# # # # mod_dir = '/Volumes/GoogleDrive-114825029448473821206/My Drive/LIGHT_GBM/models/10_sets_frame_nums_split_then_random_split_method/'
# # # # mods = utils.get_files(mod_dir, '*')
# # # # # from natsort import natsorted
# # # # # mods = natsorted(mods)[:-1]
# # # # features_out_of_10 = []
# # # # for k in mods:
# # # #     lgbm = utils.load_obj(k)
# # # #     features_out_of_10.append(lgbm.feature_importance()>0)
# # # # features_out_of_10 = np.sum(np.asarray(features_out_of_10), axis = 0)
# # # #
# # # # for k in range(10):
# # # #     print(np.round(100 * np.mean(features_out_of_10 > k), 2), '% have ', k+1, ' or more')
# # # #     print('count ', np.sum(features_out_of_10 > k))
# # # # count_importance = np.where(features_out_of_10>=3)[0]
# # # #
# # # # non_zero_features = np.where(features_out_of_10>0)[0]
# # # #
# # # # non_zero_features_bool = [k>0 for k in features_out_of_10]
# # # #
# # # # bd = '/Volumes/GoogleDrive-114825029448473821206/My Drive/LIGHT_GBM/feature_index_for_feature_selection'
# # # # np.save(bd+os.sep+'non_zero_features_bool_29913_features.npy', non_zero_features_bool)
# # # #
# # # # """ gain importance mean  """
# # # # features_out_of_10 = []
# # # # #3063
# # # # for k in mods:
# # # #     lgbm = utils.load_obj(k)
# # # #     features_out_of_10.append(lgbm.feature_importance(importance_type='gain'))
# # # # x = np.asarray(features_out_of_10)
# # # # features_out_of_10 = np.mean(np.asarray(features_out_of_10), axis = 0)
# # # #
# # # # for k in np.linspace(0, 4, 30):
# # # #     print(np.round(100 * np.mean(features_out_of_10 > k), 2), '% have more than', k)
# # # #     print('count ', np.sum(features_out_of_10 > k))
# # # # gain_importance = np.where(features_out_of_10>1.793103448275862)[0]
# # # #
# # # # tmp1 = np.unique(np.concatenate([gain_importance, count_importance]))
# # # # len(tmp1), len(count_importance), len(gain_importance)
# # # #
# # # #
# # # # """ gain importance max  """
# # # # features_out_of_10 = []
# # # # #3063
# # # # for k in mods:
# # # #     lgbm = utils.load_obj(k)
# # # #     features_out_of_10.append(lgbm.feature_importance(importance_type='gain'))
# # # # features_out_of_10 = np.asarray(features_out_of_10)
# # # # features_out_of_10 = np.max(features_out_of_10, axis = 0)
# # # #
# # # # for k in np.linspace(1, 40, 30):
# # # #     print(np.round(100 * np.mean(features_out_of_10 > k), 2), '% have more than', k)
# # # #     print('count ', np.sum(features_out_of_10 > k))
# # # #
# # # # tmp1 = []
# # # # for k in np.linspace(0, 100, 100):
# # # #     tmp1.append(np.sum(features_out_of_10 > k))
# # # # plt.plot(tmp1, '.')
# # # #
# # # #
# # # #
# # # # """ gain importance mean  """
# # # # features_out_of_10 = []
# # # # #3063
# # # # for k in mods:
# # # #     lgbm = utils.load_obj(k)
# # # #     features_out_of_10.append(lgbm.feature_importance(importance_type='gain'))
# # # # x = np.asarray(features_out_of_10)
# # # # features_out_of_10 = np.mean(np.asarray(features_out_of_10), axis = 0)
# # # #
# # # # for k in np.linspace(0, 4, 30):
# # # #     print(np.round(100 * np.mean(features_out_of_10 > k), 2), '% have more than', k)
# # # #     print('count ', np.sum(features_out_of_10 > k))
# # # #
# # # #
# # # #
# # # # bins = np.linspace(0.00001, 1, 1000)
# # # # plt.hist(features_out_of_10, bins = bins)
# # # # np.mean(features_out_of_10<=0.002)
# # # #
# # # # tmp8 = features_out_of_10>=0.004
# # # #
# # # # tmp9 = features_out_of_10>=2
# # # #
# # # # tmp10 = np.mean(np.vstack((tmp8, tmp9))*1, axis = 0)>0
# # # #
# # # # np.sum(tmp8), np.sum(tmp9), np.sum(tmp10), len(tmp8)
# # # #
# # # # """
# # # # so the rules are, include all the data that is 2 or higher and that is greater than 0.002 (for now) that result sin 87.7%
# # # # for the new set
# # # # """
# # # #
# # # #
# # # # utils.np_stats(features_out_of_10)
# # # # xu = np.unique(features_out_of_10)
# # # # a = xu[1]/2
# # # # bins = list(xu-a)
# # # # bins.append(xu[-1]+a)
# # # # import matplotlib.pyplot as plt
# # # # count = []
# # # # for k in xu[1:]:
# # # #     count.append(np.sum(k==features_out_of_10))
# # # #
# # # # plt.bar(range(len(count)), count)
# # # # """
# # # # want to plot to see if there is a clear gain features that have a mean for the first bump i can remove for feature selection
# # # # """
# # # # win = 1001
# # # # x = np.convolve(count, np.ones(win)/win, mode='valid')
# # # # plt.plot(xu[1:], x)
# # # # x2 = np.cumsum(count)
# # # # x2 = x2/np.max(x2)
# # # # plt.plot(x2)
# # # #
# # # #
# # # # tmp1 = np.unique(np.concatenate([gain_importance, count_importance]))
# # # # len(tmp1), len(count_importance), len(gain_importance)
# # # #
# # # #
# # # #
# # # #
# # # #
# # # #
# # # #
# # # #
# # # #
# # # #
# # # # """ gain importance SD to see if there are certain predictors that are used in one but not other sub models  """
# # # # features_out_of_10 = []
# # # # #3063
# # # # for k in mods:
# # # #     lgbm = utils.load_obj(k)
# # # #     features_out_of_10.append(lgbm.feature_importance(importance_type='gain'))
# # # # features_out_of_10 = np.asarray(features_out_of_10)
# # # # features_out_of_10 = np.std(features_out_of_10, axis = 0)
# # # #
# # # # # for k in np.linspace(1, 40, 30):
# # # # #     print(np.round(100 * np.mean(features_out_of_10 > k), 2), '% have more than', k)
# # # # #     print('count ', np.sum(features_out_of_10 > k))
# # # #
# # # # tmp1 = []
# # # # for k in np.linspace(0, 1000, 100):
# # # #     tmp1.append(np.sum(features_out_of_10 > k))
# # # # plt.plot(tmp1, '.')
# # # # plt.xlabel('SD of each set of 10 ')
# # # # plt.ylabel('count greater than ...')
# # # #
# # # #
# # # #
# # # #
# # # #
# # # #
# # # #
# # # # plt.hist(x.flatten(), bins=np.arange(0, 200))
# # # #
# # # #
# # # # tmp1 = '/Users/phil/Dropbox/HIRES_LAB/GitHub/whacc/whacc/whacc_data/feature_data/feature_data_dict.pkl'
# # # # tmp1 = utils.load_obj(tmp1) # ok this needs to change
# # # #
# # # #
# # # # tmp1 = '/Volumes/GoogleDrive-114825029448473821206/My Drive/final_features_window_version_corrected_v2/'
# # # # tmp1 = utils.get_files(tmp1, '*')
# # # #
# # # #
# # # # """
# # # # #####################################################################################################################
# # # # #####################################################################################################################
# # # # #####################################################################################################################
# # # # ##################################### LOAD AND PREDICT WITH THE GBM MODEL############################################
# # # # #####################################################################################################################
# # # # #####################################################################################################################
# # # # """
# # # # import lightgbm as lgb
# # # # from whacc import utils
# # # # import numpy as np
# # # # import matplotlib.pyplot as plt
# # # # fn = '/Volumes/GoogleDrive-114825029448473821206/My Drive/LIGHT_GBM/OPTUNA_mod_saves/V1/67.pkl'
# # # # mod = utils.load_obj(fn)
# # # #
# # # # x = np.random.rand(100, 2105)
# # # # testy = x[:, 0]>.5
# # # # yhat = mod.predict(x)
# # # #
# # # # plt.plot(yhat)
# # # #
# # # #
# # # # #  precition recal curve
# # # # from sklearn.metrics import precision_recall_curve
# # # # precision, recall, thresholds = precision_recall_curve(testy, yhat)
# # # #
# # # #
# # # # # from whacc import utils, image_tools
# # # # #
# # # # # import copy
# # # # # import numpy as np
# # # # # import pandas as pd
# # # # # import h5py
# # # # #
# # # # # from tqdm.autonotebook import tqdm
# # # # #
# # # # #
# # # # # class feature_maker():
# # # # #     def __init__(self, h5_in, frame_num_ind=None, frame_nums=None, operational_key='FD__original', disable_tqdm=False,
# # # # #                  delete_if_exists=False, index_features_delete_the_rest=None):
# # # # #         """
# # # # #
# # # # #         Parameters
# # # # #         ----------
# # # # #         h5_in : h5 string pointing to the h4 file with the data to transform
# # # # #         frame_num_ind : int referencing the frame num  ind to transform, note: if save_it is one ALL data is converted
# # # # #         automatically and saved in h5. frame_num_ind only works when you call with
# # # # #         frame_nums : default None, auto looks for key 'frame_nums' in h5 file or you can insert your own
# # # # #         operational_key : the data array key to be transformed
# # # # #         disable_tqdm : default False, when save_it is True it will show a loading bar with the progress unless set to true
# # # # #         delete_if_exists : default False, when calling a function with save_it as True, you can choose to overwrite that
# # # # #         data by setting this value to True
# # # # #
# # # # #         Returns
# # # # #         -------
# # # # #         feature maker class
# # # # #
# # # # #         Examples
# # # # #         ________
# # # # #
# # # # #         h5_in = '/Users/phil/Desktop/AH0407_160613_JC1003_AAAC_3lag.h5'
# # # # #
# # # # #         FM = feature_maker(h5_in, frame_num_ind=2, delete_if_exists = True) #set frame_num_ind to an int so that we can quickly look at the transformation
# # # # #         data, data_name = FM.shift(5, save_it=False) # shift it 5 to the right, fills in with nan as needed, look at just the 5th frame num set (5th video)
# # # # #         # to see how it looks
# # # # #         print('the below name will be used to save the data in the the h5 when calling functions with save_it=True')
# # # # #         print(data_name)
# # # # #         FM.shift(5, save_it=True) # now lets save it
# # # # #
# # # # #         data, data_name_rolling_mean_100 = FM.rolling(100, 'mean', save_it=True)  #lets do the rolling mean and save it
# # # # #
# # # # #         data, data_name = FM.operate('diff', kwargs={'periods': 1}, save_it=False) # lets perform a diff operation
# # # # #         print(data_name)
# # # # #         print(data)
# # # # #         FM.operate('diff', kwargs={'periods': -1}, save_it=True) # now lets save it and save it
# # # # #
# # # # #         # now lets change the operational key so we can transform some data we just transformed, specifically the rolling mean 10
# # # # #         FM.set_operation_key(data_name_rolling_mean_100)
# # # # #
# # # # #         data, data_name_diff_100_mean = FM.operate('diff', kwargs={'periods': -50}, save_it=False) # lets check how the name will change
# # # # #         print(data_name_diff_100_mean)
# # # # #         print("notice the FD__ twice, this means the data has been transformed twice")
# # # # #         print('also notice that how the data was transformed can be seen because it is split up by ____ (4 underscores)')
# # # # #
# # # # #         data, data_name_diff_100_mean = FM.operate('diff', kwargs={'periods': -50}, save_it=True) # save it
# # # # #
# # # # #         a = utils.print_h5_keys(h5_in, 1, 1)
# # # # #         key_name_list = ['FD__original', 'FD__FD__FD__original_rolling_mean_W_100_SFC_0_MP_100_____diff_periods_-50____', 'FD__FD__original_rolling_mean_W_100_SFC_0_MP_100____']
# # # # #         with h5py.File(h5_in, 'r+') as h:
# # # # #             for k in key_name_list:
# # # # #                 plt.plot(h[k][:8000, 0])
# # # # #         """
# # # # #         if utils.h5_key_exists(h5_in, 'has_data_been_randomized'):
# # # # #             assert image_tools.get_h5_key_and_concatenate(h5_in,
# # # # #                                                           'has_data_been_randomized').tolist() is False, """this data has been randomized, it is not fit to perform temporal operations on, search for key 'has_data_been_randomized' for more info"""
# # # # #
# # # # #         self._frame_num_ind_save_ = None
# # # # #         self.disable_tqdm = disable_tqdm
# # # # #         self.h5_in = h5_in
# # # # #         self.frame_num_ind = frame_num_ind
# # # # #         self.delete_if_exists = delete_if_exists
# # # # #         self.operational_key = operational_key
# # # # #         if frame_nums is None:
# # # # #             print('extracting frame_nums from h5 file, ideally you should just put that in yourself though')
# # # # #             frame_nums = image_tools.get_h5_key_and_concatenate(h5_in, 'frame_nums')
# # # # #         self.all_frame_nums = frame_nums
# # # # #         self.len_frame_nums = len(self.all_frame_nums)
# # # # #         self.set_data_and_frame(frame_num_ind)
# # # # #         index_features_delete_the_rest
# # # # #
# # # # #     def set_data_inds(self, ind):  # frame nums used ot extract below in 'set_operation_key'
# # # # #         tmp_inds = np.asarray(utils.loop_segments(self.all_frame_nums, returnaslist=True))
# # # # #         if ind is None:
# # # # #             self.data_inds = [tmp_inds[0][0], tmp_inds[-1][-1]]
# # # # #         else:
# # # # #             self.data_inds = tmp_inds[:, ind]
# # # # #
# # # # #     def set_operation_key(self, key_name=None):
# # # # #         if key_name is not None:
# # # # #             self.operational_key = key_name
# # # # #         with h5py.File(self.h5_in, 'r') as h:
# # # # #             self.full_data_shape = np.asarray(h[self.operational_key].shape)
# # # # #             if self.frame_num_ind is None:
# # # # #                 self.data = pd.DataFrame(copy.deepcopy(h[self.operational_key][:]))
# # # # #             else:
# # # # #                 a = self.data_inds  # just the current frame numbers
# # # # #                 self.data = pd.DataFrame(copy.deepcopy(h[self.operational_key][a[0]:a[1]]))
# # # # #
# # # # #     def init_h5_data_key(self, data_key, delete_if_exists=False):
# # # # #         key_exists = utils.h5_key_exists(self.h5_in, data_key)
# # # # #         assert not (
# # # # #                 key_exists and not delete_if_exists), "key exists, if you want to overwrite set 'delete_if_exists' = True"
# # # # #         with h5py.File(self.h5_in, 'r+') as x:
# # # # #             if key_exists and delete_if_exists:
# # # # #                 print('deleting key to overwrite it')
# # # # #                 del x[data_key]
# # # # #             x.create_dataset_like(data_key, x[self.operational_key])
# # # # #
# # # # #     def rolling(self, window, operation, shift_from_center=0, min_periods=None, save_it=False, kwargs={}):
# # # # #         """
# # # # #
# # # # #         Parameters
# # # # #         ----------
# # # # #         window : window size int
# # # # #         operation : a string with the operation e.g. 'mean' or 'std' see pandas docs for rolling
# # # # #         shift_from_center : default 0 but can shift as needed
# # # # #         min_periods : default is equal to win length, only allows operation when we have this many data points. so deals with
# # # # #         the edges
# # # # #         save_it : bool, False, loop through frame nums and save to h5 file
# # # # #         kwargs : dict of args that can be applied to 'operation' function
# # # # #
# # # # #         Returns
# # # # #         -------
# # # # #
# # # # #         """
# # # # #         if min_periods is None:
# # # # #             min_periods = window
# # # # #         add_name_list = ['FD__' + self.operational_key + '_rolling_',
# # # # #                          '_W_' + str(window) + '_SFC_' + str(shift_from_center) + '_MP_' + str(min_periods) + '____']
# # # # #         add_name_str = operation.join(add_name_list)
# # # # #         if save_it:
# # # # #             self._save_it_(self.rolling, window, operation, shift_from_center, min_periods, False, kwargs)
# # # # #             return None, add_name_str
# # # # #         data_frame = self.data.copy()
# # # # #         for i1, i2 in utils.loop_segments(self.frame_nums):
# # # # #             df_rolling = self.data[i1:i2].rolling(window=window, min_periods=min_periods, center=True)
# # # # #             tmp_func = eval('df_rolling.' + operation)
# # # # #             data_frame[i1:i2] = tmp_func(**kwargs).shift(shift_from_center).astype(np.float32)
# # # # #         return data_frame, add_name_str
# # # # #
# # # # #     def shift(self, shift_by, save_it=False):
# # # # #         """
# # # # #
# # # # #         Parameters
# # # # #         ----------
# # # # #         shift_by : amount to shift by
# # # # #         save_it :  bool, False, loop through frame nums and save to h5 file
# # # # #
# # # # #         Returns
# # # # #         -------
# # # # #
# # # # #         """
# # # # #         add_name_str = 'FD__' + self.operational_key + '_shift_' + str(shift_by) + '____'
# # # # #         if save_it:
# # # # #             self._save_it_(self.shift, shift_by)
# # # # #             return None, add_name_str
# # # # #
# # # # #         data_frame = self.data.copy()
# # # # #         for i1, i2 in utils.loop_segments(self.frame_nums):
# # # # #             data_frame[i1:i2] = self.data[i1:i2].shift(shift_by).astype(np.float32)
# # # # #         return data_frame, add_name_str
# # # # #
# # # # #     def operate(self, operation, save_it=False, extra_name_str='', kwargs={}):
# # # # #         """
# # # # #
# # # # #         Parameters
# # # # #         ----------
# # # # #         operation : a string with the operation e.g. 'mean' or 'std' or 'diff' see pandas operation on  dataframes
# # # # #         save_it :  bool, False, loop through frame nums and save to h5 file
# # # # #         extra_name_str : add to key name string if desired
# # # # #         kwargs : dict of args that can be applied to 'operation' function see pandas operation on  dataframes
# # # # #
# # # # #         Returns
# # # # #         -------
# # # # #
# # # # #         """
# # # # #         add_name_str_tmp = self.dict_to_string_name(kwargs)
# # # # #         add_name_str = 'FD__' + self.operational_key + '_' + operation + '_' + add_name_str_tmp + extra_name_str + '____'
# # # # #         if save_it:
# # # # #             self._save_it_(self.operate, operation, False, extra_name_str, kwargs)
# # # # #             return None, add_name_str
# # # # #         data_frame = self.data.copy()
# # # # #         for i1, i2 in utils.loop_segments(self.frame_nums):
# # # # #             data_frame[i1:i2] = eval('self.data[i1:i2].' + operation + '(**kwargs).astype(np.float32)')
# # # # #         return data_frame, add_name_str
# # # # #
# # # # #     @staticmethod
# # # # #     def dict_to_string_name(in_dict):
# # # # #         """
# # # # #         used to transform dict into a string name for naming h5 keys
# # # # #         Parameters
# # # # #         ----------
# # # # #         in_dict : dict
# # # # #
# # # # #         Returns
# # # # #         -------
# # # # #         string
# # # # #         """
# # # # #         str_list = []
# # # # #         for k in in_dict:
# # # # #             str_list.append(k)
# # # # #             str_list.append(str(in_dict[k]))
# # # # #         return '_'.join(str_list)
# # # # #
# # # # #     def set_data_and_frame(self, ind):
# # # # #         self.frame_num_ind = ind
# # # # #         if ind is None:
# # # # #             self.frame_nums = copy.deepcopy(self.all_frame_nums)
# # # # #         else:
# # # # #             self.frame_nums = [self.all_frame_nums[ind]]
# # # # #         self.set_data_inds(ind)
# # # # #         self.set_operation_key()
# # # # #
# # # # #     # tqdm(sorted(random_frame_inds[i]), disable=disable_TQDM, total=total_frames, initial=cnt1)
# # # # #     def _save_it_(self, temp_funct, *args):
# # # # #         self._frame_num_ind_save_ = copy.deepcopy(self.frame_num_ind)
# # # # #         with h5py.File(self.h5_in, 'r+') as h:
# # # # #             for k in tqdm(range(self.len_frame_nums), disable=self.disable_tqdm):
# # # # #                 self.set_data_and_frame(k)
# # # # #                 data, key_name = temp_funct(*args)
# # # # #                 if k == 0:
# # # # #                     self.init_h5_data_key(key_name, delete_if_exists=self.delete_if_exists)
# # # # #                     print('making key, ' + key_name)
# # # # #                 a = self.data_inds
# # # # #                 h[key_name][a[0]:a[1]] = data
# # # # #         self.set_data_and_frame(self._frame_num_ind_save_)  # set data back to what it was when user set it
# # # # #
# # # # #     def total_rolling_operation(self, data_in, win, operation_function, shift_from_center=0):
# # # # #         """
# # # # #         NOTE: for making feature data proper key names for saving is 'FD_TOTAL_' folowed by operation e.g. 'FD_TOTAL_nanstd'
# # # # #         Parameters
# # # # #         ----------
# # # # #         data_in : 2D matrix
# # # # #         win : window size
# # # # #         operation_function : function to be applies to each window e.g. np.nanmean, note DON'T include parentheses
# # # # #         shift_from_center : num units shift from center
# # # # #
# # # # #         Returns
# # # # #         -------
# # # # #         data_out: output data
# # # # #         is_nan_inds: bool array indexing where nans were
# # # # #         """
# # # # #         assert win % 2 == 1, 'window must be odd'
# # # # #         mid = win // 2
# # # # #         pad = np.zeros([win, data_in.shape[1]]) * np.nan
# # # # #
# # # # #         L_pad = pad[:mid - shift_from_center]
# # # # #         R_pad = pad[:mid + shift_from_center]
# # # # #
# # # # #         data_in = np.vstack([L_pad, data_in, R_pad])
# # # # #
# # # # #         is_nan_inds = []
# # # # #         data_out = []
# # # # #         for k in range(data_in.shape[0] - win + 1):
# # # # #             x = data_in[k:(k + win)]
# # # # #             data_out.append(operation_function(x))
# # # # #             is_nan_inds.append(np.any(np.isnan(x)))
# # # # #         return np.asarray(data_out), np.asarray(is_nan_inds)
# # # # #
# # # # #     def total_rolling_operation_h5_wrapper(self, window, operation, key_to_operate_on, mod_key_name=None,
# # # # #                                            save_it=False,
# # # # #                                            shift_from_center=0):
# # # # #         if save_it:
# # # # #             assert mod_key_name is not None, """if save_it is True, 'mod_key_name' must not be None e.g. 'FD_TOTAL_std_1_of_'"""
# # # # #         all_data = []
# # # # #         with h5py.File(self.h5_in, 'r') as h:
# # # # #             frame_nums = h['frame_nums'][:]
# # # # #             for i, (i1, i2) in enumerate(utils.loop_segments(frame_nums)):
# # # # #                 data_out, is_nan_inds = self.total_rolling_operation(h[key_to_operate_on][i1:i2, :], window, operation,
# # # # #                                                                      shift_from_center=shift_from_center)
# # # # #                 all_data.append(data_out)
# # # # #         all_data = np.hstack(all_data)
# # # # #         mod_key_name = mod_key_name + key_to_operate_on
# # # # #         if save_it:
# # # # #             utils.overwrite_h5_key(self.h5_in, mod_key_name, all_data)
# # # # #         return all_data
# # # # #
# # # # #
# # # # # from tqdm.auto import tqdm
# # # # # import numpy as np
# # # # #
# # # # # ########################################################################################################################
# # # # # ########################################################################################################################
# # # # # h5_feature_data = '/Users/phil/Desktop/pipeline_test/AH0407x160609_3lag_feature_data.h5'
# # # # # FM = feature_maker(h5_feature_data, operational_key='FD__original', delete_if_exists=True)
# # # # #
# # # # # for periods in tqdm([-5]):
# # # # #     data, key_name = FM.shift(periods, save_it=True)
# # # # # ########################################################################################################################
# # # # # ########################################################################################################################
# # # # # ########################################################################################################################
# # # # # # from whacc.feature_maker import feature_maker, total_rolling_operation_h5_wrapper
# # # # #
# # # # #
# # # # # for periods in tqdm([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5]):
# # # # #     data, key_name = FM.shift(periods, save_it=True)
# # # # #
# # # # # for smooth_it_by in tqdm([3, 7, 11, 15, 21, 41, 61]):
# # # # #     data, key_name = FM.rolling(smooth_it_by, 'mean', save_it=True)
# # # # #
# # # # # for periods in tqdm([-50, -20, -10, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 10, 20, 50]):
# # # # #     data, key_name = FM.operate('diff', kwargs={'periods': periods}, save_it=True)
# # # # #
# # # # # for smooth_it_by in tqdm([3, 7, 11, 15, 21, 41, 61]):
# # # # #     data, key_name = FM.rolling(smooth_it_by, 'std', save_it=True)
# # # # #
# # # # # win = 1
# # # # # # key_to_operate_on = 'FD__original'
# # # # # op = np.std
# # # # # mod_key_name = 'FD_TOTAL_std_' + str(win) + '_of_'
# # # # # all_keys = utils.lister_it(utils.print_h5_keys(FM.h5_in, 1, 0), 'FD__', 'FD_TOTAL')
# # # # # for key_to_operate_on in tqdm(all_keys):
# # # # #     data_out = FM.total_rolling_operation_h5_wrapper(win, op, key_to_operate_on, mod_key_name=mod_key_name,
# # # # #                                                      save_it=True)
# # # # #
# # # # # utils.get_selected_features(greater_than_or_equal_to=4)
# # # # #
# # # # # inds = fd_dict['features_used_of_10'] >= 4
# # # # # tmp1 = fd_dict['full_feature_names_and_neuron_nums'][inds]
# # # # # import numpy as np
# # # # #
# # # # # tmp2 = np.unique(fd_dict['full_neuron_nums'][inds])
# # # # #
# # # # # for k in tmp1:
# # # # #     print(k)
# # # # #
# # # # # """
# # # # # 'FD_TOTAL_std_1_of_original_diff_periods_3',
# # # # # 'FD_TOTAL_std_1_of_original_rolling_mean_W_3_SFC_0_MP_3',
# # # # # 'FD_TOTAL_std_1_of_original_rolling_mean_W_7_SFC_0_MP_7',
# # # # # 'FD_TOTAL_std_1_of_original_rolling_mean_W_11_SFC_0_MP_11',
# # # # # 'FD_TOTAL_std_1_of_original_shift_3', 'FD_TOTAL_std_1_of_original'],
# # # # #
# # # # # do those first then take any of the completed data from them that are used as single features
# # # # #
# # # # # then save the TOTAL operations and singles,
# # # # #
# # # # # then go through all the singles
# # # # #
# # # # # """
# # # # #
# # # # # len(utils.lister_it(tmp1, '_diff_'))
# # # # #
# # # # # h52 = '/Users/phil/Desktop/pipeline_test/AH0407x160609_3lag_feature_data.h5'
# # # # # utils.print
# # # # #
# # # # #
# # # # # def total_rolling_sliding_window_view(data_in, win, operation_function, shift_from_center=0):
# # # # #     assert win % 2 == 1, 'window must be odd'
# # # # #     mid = win // 2
# # # # #     pad = np.zeros([win, data_in.shape[1]]) * np.nan
# # # # #
# # # # #     L_pad = pad[:mid - shift_from_center]
# # # # #     R_pad = pad[:mid + shift_from_center]
# # # # #
# # # # #     data_in = np.vstack([L_pad, data_in, R_pad])
# # # # #     w = data_in.shape[1]
# # # # #     data_in = np.lib.stride_tricks.sliding_window_view(data_in, (win, w))
# # # # #     data_in = np.reshape(data_in, [-1, win * w])
# # # # #     data_out = operation_function(data_in, axis=1)
# # # # #     return np.asarray(data_out)
# # # #
# # # #
# # # # from whacc import utils, image_tools
# # # # import matplotlib.pyplot as plt
# # # # import h5py
# # # # import numpy as np
# # # # h5 = '/Users/phil/Dropbox/HIRES_LAB/GitHub/Phillip_AC/model_testing/all_data/test_data/10_percent_holy_set/regular/holy_test_set_10_percent_regular.h5'
# # # # h5 = '/Users/phil/Dropbox/HIRES_LAB/GitHub/Phillip_AC/model_testing/all_data/test_data/10_percent_holy_set/3lag/holy_test_set_10_percent_3lag.h5'
# # # # count = 19
# # # # start = 24850 - 1000
# # # # end = 24850 + 1000
# # # # # start = 0
# # # #
# # # #
# # # # # L = 40000
# # # # #  32736
# # # #
# # # # with h5py.File(h5, 'r') as h:
# # # #     L = len(h['labels'][:])
# # # #     print(L)
# # # #     L = end - start
# # # #     imgs = h['images'][start:end:L//count]
# # # #     # L = len(h['labels'][:])
# # # #     titles = np.arange(L)[start:end:L//count]
# # # #
# # # # fig, ax = plt.subplots(5, 4)
# # # # for ind, ax2 in enumerate(ax.flatten()):
# # # #     ax2.imshow(imgs[ind])
# # # #     # ax2.title.set_text(titles[ind])
# # # #
# # # #
# # # #
# # # # import matplotlib.pyplot as plt
# # # # import h5py
# # # # import numpy as np
# # # # h5 = '/Users/phil/Dropbox/HIRES_LAB/GitHub/Phillip_AC/model_testing/all_data/test_data/10_percent_holy_set/regular/holy_test_set_10_percent_regular.h5'
# # # # h5 = '/Users/phil/Dropbox/HIRES_LAB/GitHub/Phillip_AC/model_testing/all_data/test_data/10_percent_holy_set/3lag/holy_test_set_10_percent_3lag.h5'
# # # # h5 =  '/Users/phil/Dropbox/HIRES_LAB/GitHub/Phillip_AC/model_testing/all_data/test_data/full_holy_set/3lag/holy_set_80_border_single_frame_3lag.h5'
# # # #
# # # # # start = 0
# # # #
# # # #
# # # # # L = 40000
# # # # #  32736
# # # #
# # # # with h5py.File(h5, 'r') as h:
# # # #     imgs = []
# # # #     for k1, k2 in utils.loop_segments(h['frame_nums'][:]):
# # # #         i = np.where(h['labels'][k1:k2]==1)[0]
# # # #         i = i[int(len(i)/2)]
# # # #         # i = int(np.mean([k1, k2])) # center ind
# # # #         imgs.append(h['images'][k1+i])
# # # # imgs = np.asarray(imgs)
# # # #
# # # # for ind, img_in in enumerate(imgs):
# # # #     if ind%20 == 0:
# # # #         fig, ax = plt.subplots(5, 4)
# # # #         ax = ax.flatten()
# # # #     ax[ind%20].imshow(img_in)
# # # #     ax[ind%20].title.set_text(str(ind))
# # # #     # ax2.title.set_text(titles[ind])
# # # #
# # # # """
# # # # ##################################################################################################
# # # # ##################################################################################################
# # # # ##################use to compare unfinished trained data #########################################
# # # # ##################################################################################################
# # # # """
# # # # test_set_to = 10
# # # # from natsort import natsorted, ns
# # # #
# # # # mod_dir = '/Volumes/GoogleDrive-114825029448473821206/My Drive/LIGHT_GBM/models/10_sets_frame_nums_split_then_random_split_method_numpy_feature_selection_V1/'
# # # # mods = utils.get_files(mod_dir, '*')
# # # # mods = natsorted(mods, alg=ns.REAL)[:test_set_to]
# # # # # from natsort import natsorted
# # # # # mods = natsorted(mods)[:-1]
# # # # features_out_of_10 = []
# # # # for k in mods:
# # # #     lgbm = utils.load_obj(k)
# # # #     features_out_of_10.append(lgbm.feature_importance()>0)
# # # # features_out_of_10 = np.sum(np.asarray(features_out_of_10), axis = 0)
# # # #
# # # # for k in range(test_set_to):
# # # #     print(np.round(100 * np.mean(features_out_of_10 > k), 2), '% have ', k+1, ' or more')
# # # #     print('count ', np.sum(features_out_of_10 > k))
# # # # count_importance = np.where(features_out_of_10>=3)[0]
# # # # print('____________________')
# # # # mod_dir = '/Volumes/GoogleDrive-114825029448473821206/My Drive/LIGHT_GBM/models/10_sets_frame_nums_split_then_random_split_method/'
# # # # mods = utils.get_files(mod_dir, '*')
# # # # mods = natsorted(mods, alg=ns.REAL)[:test_set_to]
# # # # # from natsort import natsorted
# # # # # mods = natsorted(mods)[:-1]
# # # # features_out_of_10 = []
# # # # for k in mods:
# # # #     lgbm = utils.load_obj(k)
# # # #     features_out_of_10.append(lgbm.feature_importance()>0)
# # # # features_out_of_10 = np.sum(np.asarray(features_out_of_10), axis = 0)
# # # #
# # # # for k in range(test_set_to):
# # # #     print(np.round(100 * np.mean(features_out_of_10 > k), 2), '% have ', k+1, ' or more')
# # # #     print('count ', np.sum(features_out_of_10 > k))
# # # # count_importance = np.where(features_out_of_10>=3)[0]
# # # #
# # # #
# # # #
# # # # """
# # # # CHOOSING THE BEST FEATURES, I SHOULD TRAIN AND TEST THIS FOR MY SHIT BEFORE CONFIRMING IT IS ALL GOOD.
# # # # I have times used and gain importance
# # # # each conveys something different and I can choose whichever I want. or I can do a combination of both because they are
# # # # not perfectly overlapping
# # # # I can also use SD as a decider as it can show variables that would be useful like outliers that catch something
# # # #
# # # # I could also train data on like the top 15k or something or maybe even 32k?? if i do all at least one will i get the
# # # # same results?
# # # #
# # # # so after looking at https://simility.com/wp-content/uploads/2020/07/WP-Feature-Selection.pdf
# # # # I think it is totally appropriate to take the union of the models and train again and see how they do
# # # # or I could do some voting
# # # #
# # # # """
# # # # import os
# # # # """ times used metric  """
# # # # mod_dir = '/Volumes/GoogleDrive-114825029448473821206/My Drive/LIGHT_GBM/models/10_sets_frame_nums_split_then_random_split_method/'
# # # # mods = utils.get_files(mod_dir, '*')
# # # # # from natsort import natsorted
# # # # # mods = natsorted(mods)[:-1]
# # # # features_out_of_10 = []
# # # # for k in mods:
# # # #     lgbm = utils.load_obj(k)
# # # #     features_out_of_10.append(lgbm.feature_importance()>0)
# # # # features_out_of_10 = np.sum(np.asarray(features_out_of_10), axis = 0)
# # # #
# # # # for k in range(10):
# # # #     print(np.round(100 * np.mean(features_out_of_10 > k), 2), '% have ', k+1, ' or more')
# # # #     print('count ', np.sum(features_out_of_10 > k))
# # # # count_importance = np.where(features_out_of_10>=3)[0]
# # # #
# # # # non_zero_features = np.where(features_out_of_10>0)[0]
# # # #
# # # # non_zero_features_bool = [k>0 for k in features_out_of_10]
# # # #
# # # # bd = '/Volumes/GoogleDrive-114825029448473821206/My Drive/LIGHT_GBM/feature_index_for_feature_selection'
# # # # np.save(bd+os.sep+'non_zero_features_bool_29913_features.npy', non_zero_features_bool)
# # # #
# # # # """ gain importance mean  """
# # # # features_out_of_10 = []
# # # # #3063
# # # # for k in mods:
# # # #     lgbm = utils.load_obj(k)
# # # #     features_out_of_10.append(lgbm.feature_importance(importance_type='gain'))
# # # # x = np.asarray(features_out_of_10)
# # # # features_out_of_10 = np.mean(np.asarray(features_out_of_10), axis = 0)
# # # #
# # # # for k in np.linspace(0, 4, 30):
# # # #     print(np.round(100 * np.mean(features_out_of_10 > k), 2), '% have more than', k)
# # # #     print('count ', np.sum(features_out_of_10 > k))
# # # # gain_importance = np.where(features_out_of_10>1.793103448275862)[0]
# # # #
# # # # tmp1 = np.unique(np.concatenate([gain_importance, count_importance]))
# # # # len(tmp1), len(count_importance), len(gain_importance)
# # # #
# # # #
# # # # """ gain importance max  """
# # # # features_out_of_10 = []
# # # # #3063
# # # # for k in mods:
# # # #     lgbm = utils.load_obj(k)
# # # #     features_out_of_10.append(lgbm.feature_importance(importance_type='gain'))
# # # # features_out_of_10 = np.asarray(features_out_of_10)
# # # # features_out_of_10 = np.max(features_out_of_10, axis = 0)
# # # #
# # # # for k in np.linspace(1, 40, 30):
# # # #     print(np.round(100 * np.mean(features_out_of_10 > k), 2), '% have more than', k)
# # # #     print('count ', np.sum(features_out_of_10 > k))
# # # #
# # # # tmp1 = []
# # # # for k in np.linspace(0, 100, 100):
# # # #     tmp1.append(np.sum(features_out_of_10 > k))
# # # # plt.plot(tmp1, '.')
# # # #
# # # #
# # # #
# # # # """ gain importance mean  """
# # # # features_out_of_10 = []
# # # # #3063
# # # # for k in mods:
# # # #     lgbm = utils.load_obj(k)
# # # #     features_out_of_10.append(lgbm.feature_importance(importance_type='gain'))
# # # # x = np.asarray(features_out_of_10)
# # # # features_out_of_10 = np.mean(np.asarray(features_out_of_10), axis = 0)
# # # #
# # # # for k in np.linspace(0, 4, 30):
# # # #     print(np.round(100 * np.mean(features_out_of_10 > k), 2), '% have more than', k)
# # # #     print('count ', np.sum(features_out_of_10 > k))
# # # #
# # # #
# # # #
# # # # bins = np.linspace(0.00001, 1, 1000)
# # # # plt.hist(features_out_of_10, bins = bins)
# # # # np.mean(features_out_of_10<=0.002)
# # # #
# # # # tmp8 = features_out_of_10>=0.004
# # # #
# # # # tmp9 = features_out_of_10>=2
# # # #
# # # # tmp10 = np.mean(np.vstack((tmp8, tmp9))*1, axis = 0)>0
# # # #
# # # # np.sum(tmp8), np.sum(tmp9), np.sum(tmp10), len(tmp8)
# # # #
# # # # """
# # # # so the rules are, include all the data that is 2 or higher and that is greater than 0.002 (for now) that result sin 87.7%
# # # # for the new set
# # # # """
# # # #
# # # #
# # # # utils.np_stats(features_out_of_10)
# # # # xu = np.unique(features_out_of_10)
# # # # a = xu[1]/2
# # # # bins = list(xu-a)
# # # # bins.append(xu[-1]+a)
# # # # import matplotlib.pyplot as plt
# # # # count = []
# # # # for k in xu[1:]:
# # # #     count.append(np.sum(k==features_out_of_10))
# # # #
# # # # plt.bar(range(len(count)), count)
# # # # """
# # # # want to plot to see if there is a clear gain features that have a mean for the first bump i can remove for feature selection
# # # # """
# # # # win = 1001
# # # # x = np.convolve(count, np.ones(win)/win, mode='valid')
# # # # plt.plot(xu[1:], x)
# # # # x2 = np.cumsum(count)
# # # # x2 = x2/np.max(x2)
# # # # plt.plot(x2)
# # # #
# # # #
# # # # tmp1 = np.unique(np.concatenate([gain_importance, count_importance]))
# # # # len(tmp1), len(count_importance), len(gain_importance)
# # # #
# # # #
# # # #
# # # #
# # # #
# # # #
# # # #
# # # #
# # # #
# # # #
# # # # """ gain importance SD to see if there are certain predictors that are used in one but not other sub models  """
# # # # features_out_of_10 = []
# # # # #3063
# # # # for k in mods:
# # # #     lgbm = utils.load_obj(k)
# # # #     features_out_of_10.append(lgbm.feature_importance(importance_type='gain'))
# # # # features_out_of_10 = np.asarray(features_out_of_10)
# # # # features_out_of_10 = np.std(features_out_of_10, axis = 0)
# # # #
# # # # # for k in np.linspace(1, 40, 30):
# # # # #     print(np.round(100 * np.mean(features_out_of_10 > k), 2), '% have more than', k)
# # # # #     print('count ', np.sum(features_out_of_10 > k))
# # # #
# # # # tmp1 = []
# # # # for k in np.linspace(0, 1000, 100):
# # # #     tmp1.append(np.sum(features_out_of_10 > k))
# # # # plt.plot(tmp1, '.')
# # # # plt.xlabel('SD of each set of 10 ')
# # # # plt.ylabel('count greater than ...')
# # # #
# # # #
# # # #
# # # #
# # # #
# # # #
# # # #
# # # # plt.hist(x.flatten(), bins=np.arange(0, 200))
# # # #
# # # #
# # # # tmp1 = '/Users/phil/Dropbox/HIRES_LAB/GitHub/whacc/whacc/whacc_data/feature_data/feature_data_dict.pkl'
# # # # tmp1 = utils.load_obj(tmp1) # ok this needs to change
# # # #
# # # #
# # # # tmp1 = '/Volumes/GoogleDrive-114825029448473821206/My Drive/final_features_window_version_corrected_v2/'
# # # # tmp1 = utils.get_files(tmp1, '*')
# # # #
# # # #
# # # # """
# # # # #####################################################################################################################
# # # # #####################################################################################################################
# # # # #####################################################################################################################
# # # # ##################################### LOAD AND PREDICT WITH THE GBM MODEL############################################
# # # # #####################################################################################################################
# # # # #####################################################################################################################
# # # # """
# # # # import lightgbm as lgb
# # # # from whacc import utils
# # # # import numpy as np
# # # # import matplotlib.pyplot as plt
# # # # fn = '/Volumes/GoogleDrive-114825029448473821206/My Drive/LIGHT_GBM/OPTUNA_mod_saves/V1/67.pkl'
# # # # mod = utils.load_obj(fn)
# # # #
# # # # x = np.random.rand(100, 2105)
# # # # testy = x[:, 0]>.93
# # # # yhat = mod.predict(x)
# # # #
# # # # plt.plot(yhat)
# # # #
# # # #
# # # # #  precition recal curve
# # # # from sklearn.metrics import precision_recall_curve
# # # # precision, recall, thresholds = precision_recall_curve(testy, yhat)
# # # #
# # # #
# # # # # plot the roc curve for the model
# # # # no_skill = len(testy[testy==1]) / len(testy)
# # # # plt.plot([0,1], [no_skill,no_skill], linestyle='--', label='No Skill')
# # # # plt.plot(recall, precision, marker='.', label='Logistic')
# # # #
# # # #
# # # # plt.xlabel('Recall')
# # # # plt.ylabel('Precision')
# # # # plt.legend()
# # # #
# # # #
# # # #
# # # #
# # # #
# # # # from whacc import utils
# # # # bd = ''
# # # # all_h5s = utils.get_h5s(bd)
# # # # for h5_feature_data in all_h5s:
# # # #     utils.standard_feature_generation2(h5_feature_data)
# # # plt.plot(recall, precision, marker='.', label='Logistic')
# # #
# # #
# # # plt.xlabel('Recall')
# # # plt.ylabel('Precision')
# # # plt.legend()
# # #
# # #
# # #
# # #
# # #
# # # from whacc import utils
# # # bd = ''
# # # all_h5s = utils.get_h5s(bd)
# # # for h5_feature_data in all_h5s:
# # #     utils.standard_feature_generation2(h5_feature_data)
# #
# #
# #
# #
# # # AH0688x170818
# #
# #
# #
# # video = cv2.VideoCapture(video_file)
# # # frame_number = 3768
# # # frame_number = 1
# # all_frames = []
# # for frame_number in range(4000):
# #     video.set(cv2.CAP_PROP_POS_FRAMES, frame_number-1)
# #     success, og_frame = video.read()
# #     all_frames.append(og_frame)
# #
# #
# # cap = cv2.VideoCapture(videopath)
# # cap.set(cv2.CV_CAP_PROP_POS_FRAMES, frame_number-1)
# # res, frame = cap.read()
# #
# #
# #
# #
# # h51 = '/Users/phil/Desktop/trashTMP_new_method/AH0688x170818.h5'
# # h52 = '/Users/phil/Desktop/trashTMP_old_method/AH0688x170818.h5'
# # from whacc import utils, image_tools
# # import numpy as np
# #
# # images1 = image_tools.get_h5_key_and_concatenate(h51, 'images')
# # images2 = image_tools.get_h5_key_and_concatenate(h52, 'images')
# # np.all(images2 == images1)
# #
# #
# #
#
# from whacc import utils
# import os
# bd = "/Volumes/GoogleDrive-114825029448473821206/My Drive/PHILLIP/processing/P18"
# utils.batch_process_videos_on_colab(bd, '/Users/phil/Desktop/TRASH_DIR/', video_batch_size=5)
#
#
# #
# # batch_file = '/Volumes/GoogleDrive-114825029448473821206/My Drive/PHILLIP/processing/P16/AH1047/190913/Camera 1/file_list_for_batch_processing.pkl'
# # d = utils.load_obj(batch_file)
# #
# # bd = os.path.basename(batch_file)
# # d.keys()
# #
# # def re_index_file_list(batch_file):
# #     bd = os.path.basename(batch_file)
# #     d = utils.load_obj(batch_file)
# #     utils.get_files(bd, '*.mp4')
# #     for k in d.mp4_names:
# #         f = os.path.basename(k)
#
#
# # def re_index_dir(batch_file, match_key, bd):
# #     utils.get_files(bd, match_key)
# #
#
#
#
# """
# #####################################################################################################################
# #####################################################################################################################
# #####################################################################################################################
# ##################################### looking at Samson's data for missed touches ###################################
# #####################################################################################################################
# #####################################################################################################################
# """
#
# from whacc import utils
# import h5py
# import matplotlib.pyplot as plt
# import numpy as np
# h5 = '/Users/phil/Downloads/AH1179X24052021x4_final_to_combine_1_to_5_of_310.h5'
# utils.print_h5_keys(h5)
# with h5py.File(h5) as h:
#     for i, (k1, k2) in enumerate(utils.loop_segments(h['frame_nums'])):
#         y = h['yhat_proba'][k1:k2]
#         plt.plot(range(k2-k1), y-i)
#
#
# with h5py.File(h5) as h:
#     for i, (k1, k2) in enumerate(utils.loop_segments(h['frame_nums'])):
#         y = h['locations_x_y'][k1:k2]
#         plt.plot(range(k2-k1), y-i)
#
# with h5py.File(h5) as h:
#     for i, (k1, k2) in enumerate(utils.loop_segments(h['frame_nums'])):
#         y = h['max_val_stack'][k1:k2]
#         plt.plot(range(k2-k1), y-i)
#
#
#
# from whacc import image_tools
#
# image_tools.get_h5_key_and_concatenate(h5, 'full_file_names')
# template_img = image_tools.get_h5_key_and_concatenate(h5, 'template_img')
# plt.imshow(template_img)
#
# final_features_2105 = image_tools.get_h5_key_and_concatenate(h5, 'final_features_2105')
# yhat_proba = image_tools.get_h5_key_and_concatenate(h5, 'yhat_proba')
#
# plt.imshow(final_features_2105[3000*3:3000*4, :].T)
#
#
#
#
#
#
#
# import scipy.cluster.hierarchy as sch
# import pandas as pd
# def cluster_corr(corr_array, max_div_by = 2):
#     pairwise_distances = sch.distance.pdist(corr_array)
#     linkage = sch.linkage(pairwise_distances, method='complete')
#     cluster_distance_threshold = pairwise_distances.max()/max_div_by
#     idx_to_cluster_array = sch.fcluster(linkage, cluster_distance_threshold, criterion='distance')
#     idx = np.argsort(idx_to_cluster_array)
#     if isinstance(corr_array, pd.DataFrame):
#         return corr_array.iloc[idx, :].T.iloc[idx, :]
#     return corr_array[idx, :][:, idx], idx
#
# import copy
# import seaborn as sns
# def foo_norm(x):################################################
#     x = x-np.nanmin(x)
#     x = x/np.nanmax(x)
#     return x
# # def foo_norm(x): ################################################
# #     return x
# FD = final_features_2105[3000*3:3000*4, :]
# FD2 = copy.deepcopy(FD)
# for i, k in enumerate(FD.T):
#     FD2[:, i] = foo_norm(k)
# #
# # for i, k in enumerate(FD):
# #     FD2[i,:] = foo_norm(k)
#
#
# FD = FD2
# FD[np.isnan(FD)] = 0.00000001
# FD[0, :] = FD[0, :]+0.00000001
# cc = np.corrcoef(FD, rowvar=False)
# cc, inds = cluster_corr(cc, .1)
#
# # sns.heatmap(cc)
# data = FD[:, inds].T
# ax_heat = sns.heatmap(data, cbar=False)
#
#
# plt.plot(100+-1*yhat_proba[3000*3:3000*4]*100,'w-', alpha=.5, linewidth = .3)
#
#
#
#
# """
# #####################################################################################################################
# #####################################################################################################################
# #####################################################################################################################
# ##################################### looking into the final triaing data ###################################
# #####################################################################################################################
# #####################################################################################################################
# """
# h5 = '/Volumes/GoogleDrive-114825029448473821206/My Drive/LIGHT_GBM/FEATURE_DATA/colab_data2/model_testing/all_data/all_models/small_h5s/data/3lag/small_train_3lag.h5'
# h5 = '/Volumes/GoogleDrive-114825029448473821206/My Drive/colab_data2/model_testing/all_data/all_models/small_h5s/data/3lag/small_train_3lag.h5'
# h5 = '/Volumes/GoogleDrive-114825029448473821206/My Drive/colab_data2/model_testing/all_data/all_models/regular_80_border/data/single_frame/val.h5'
#
# h5 = '/Volumes/GoogleDrive-114825029448473821206/My Drive/colab_data2/model_testing/all_data/all_models/regular_80_border/data/ALT_LABELS/val_ALT_LABELS.h5'
#
# h5 = '/Volumes/GoogleDrive-114825029448473821206/My Drive/colab_data2/model_testing/all_data/all_models/regular_80_border/data/regular/val_regular.h5'
# h5 = '/Users/phil/Dropbox/HIRES_LAB/GitHub/Phillip_AC/autoCuratorDiverseDataset/AH0000x000000/AH0000x000000_using_pole_tracker.h5'
# h5 = '/Volumes/GoogleDrive-114825029448473821206/My Drive/LIGHT_GBM/FEATURE_DATA/Colab data/curation_for_auto_curator/DATA_FULL_in_range_only/data_AH0407_160613_JC1003_AAAC/3lag/AH0407_160613_JC1003_AAAC_3lag.h5'
# h5 = '/Volumes/GoogleDrive-114825029448473821206/My Drive/LIGHT_GBM/FEATURE_DATA/colab_data2/model_testing/all_data/all_models_2105/regular_80_border/data/3lag/train_3lag.h5'
# h5 = '/Users/phil/Dropbox/Colab data/H5_data/3lag/ANM234232_140120_AH1030_AAAA_a_3lag.h5'
# h5 = '/Users/phil/Dropbox/Colab data/H5_data/OG/ANM234232_140118_AH1026_AAAA-008.h5'
# h5 = '/Users/phil/Dropbox/Colab data/H5_data/regular/ANM234232_140120_AH1030_AAAA_a_regular.h5'
#
# h5 = '/Users/phil/Dropbox/Colab data/H5_data/3lag/AH0407_160613_JC1003_AAAC_3lag.h5'
# utils.print_h5_keys(h5)
# trial_nums_and_frame_nums = image_tools.get_h5_key_and_concatenate(h5, 'trial_nums_and_frame_nums')
#
#
#
# h5 = '/Users/phil/Dropbox/Colab data/H5_data/regular/AH0407_160613_JC1003_AAAC_regular.h5'
# utils.print_h5_keys(h5)
# # frame_nums_3lag = image_tools.get_h5_key_and_concatenate(h5, 'frame_nums')
#
#
# # frame_nums_regular = image_tools.get_h5_key_and_concatenate(h5, 'frame_nums')
#
#
# trial_nums_and_frame_nums = image_tools.get_h5_key_and_concatenate(h5, 'trial_nums_and_frame_nums')
# trial_nums_and_frame_nums = image_tools.get_h5_key_and_concatenate(h5, 'trial_nums_and_frame_nums')
# trial_nums_and_frame_nums = image_tools.get_h5_key_and_concatenate(h5, 'trial_nums_and_frame_nums')
# trial_nums_and_frame_nums = image_tools.get_h5_key_and_concatenate(h5, 'trial_nums_and_frame_nums')
# trial_nums_and_frame_nums = image_tools.get_h5_key_and_concatenate(h5, 'trial_nums_and_frame_nums')
#
#
# h5 = '/Volumes/GoogleDrive-114825029448473821206/My Drive/LIGHT_GBM/FEATURE_DATA/colab_data2/model_testing/all_data/all_models/regular_80_border_aug_0_to_9/data/3lag/train_3lag.h5'
#
# # ofsets can only be found by taking the touch predition and actual and looking to see if ther eis an offset iguess
#
# """
#
# comapre 3lag and other to see if they match then I can use the meta data on the matching ones without re creating the 3lag ones
#
#
#
#
#
# the issue shtat I want to remove samsons data but the only way to do that that doesnt take a crazy amount of time
#
#
# to re do the data set I would have to do the following
# 1) select videos with correct frame count, remove samsons bad data
# 1.5) convert to 80 border
# 1.6) convert to 3 border
# 2) run through augmentation for 3 border
# 3) convert all to 2105
#
# """




from whacc import PoleTracking, utils
import whacc
import os
import glob
from whacc import utils
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.image as mpimg


bd = '/Users/phil/Desktop/untitled folder/'
search_term = '*.mp4'
folders_with_MP4s = whacc.utils.recursive_dir_finder(bd, search_term)
_ = [print(str(i) + ' ' + k) for i, k in enumerate(folders_with_MP4s)]

for video_directory in folders_with_MP4s:
    utils.make_mp4_list_dict(video_directory)



local_temp_dir = '/Users/phil/Desktop/untitled folder/untitled folder/'
utils.batch_process_videos_on_colab(bd, local_temp_dir, video_batch_size=5)

#
# bd = '/Users/phil/Desktop/'
# folders_with_MP4s = utils.recursive_dir_finder(bd, '*')
# folders_with_MP4s
#
# utils.get_files(bd, '*.mp4')
# import os
# utils.get_files('/Users/phil/Desktop/untitled folder/', '*')







































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

info = utils.info
of = utils.open_folder

'''##################################################################################################################'''
'''##################################################################################################################'''
'''##################################################################################################################'''
'''##################################################################################################################'''
'''##################################################################################################################'''

save_dir = '/Users/phil/Dropbox/HIRES_LAB/WhACC PAPER/figures/auc and TC errors smoothing test_V2 WITH_HAIR/'
utils.make_path(save_dir)
add_to_name = 'Optimal threshold 05 to 95'


fn = '/Volumes/GoogleDrive-114825029448473821206/My Drive/Colab data/curation_for_auto_curator/DATA_FULL/full_in_range_and_other_useful_data.pkl'
in_range_d = utils.load_obj(fn)

fn2 = '/Volumes/GoogleDrive-114825029448473821206/My Drive/Colab data/curation_for_auto_curator/DATA_FULL/full_in_range_16_and_whacc_pred_all_4.pkl'
# fn2 = '/Volumes/GoogleDrive-114825029448473821206/My Drive/Colab data/curation_for_auto_curator/DATA_FULL/full_in_range_16_and_whacc_pred_no_hair.pkl'

yhat_d = utils.load_obj(fn2)
for k in yhat_d:
    print(k)

# t2 = utils.load_obj('/Volumes/GoogleDrive-114825029448473821206/My Drive/LIGHT_GBM//final_16_and_whacc_yhat_for_plotting.pkl')
# for k in t2:
#     print(k)
# assert np.all(yhat_d['model_keys'] == t2['names']), 'model key names dont match'

['labels', 'frame_nums', 'yhat_all', 'names']

t3 = {'yhat_all': []}  # 'frame_nums':[], 'labels':[]
for k in yhat_d['model_keys']:
    t3['yhat_all'].append(yhat_d[k].flatten() * yhat_d['in_range'])
t3['frame_nums'] = yhat_d['frame_nums']
t3['labels'] = yhat_d['labels'] * yhat_d['in_range']

# t3['labels'][yhat_d['in_range']==0] = -1

t3['names'] = yhat_d['model_keys']
t3['yhat_all'] = [k.flatten() for k in t3['yhat_all']]
t2 = t3

from scipy.signal import medfilt

t2['inds'] = [13, 11, 9, 15, 5, 3, 1, 7, 4, 2, 0, 6, 16]

utils.print_list_with_inds(t2['names'])
for k in t2['inds']:
    print(t2['names'][k])

labels = t2['labels']

t2['total_touches'] = np.sum(np.diff(t2['labels']) == 1)

frame_nums = t2['frame_nums']
t2['analysis'] = dict()
t2['analysis']['name'] = ['ghost', 'miss', 'join', 'split', 'append_4+', 'deduct_4+', 'append', 'deduct', '1 - auc']
TC_err_all = []
for smooth_by in [1, 3, 5, 7, 9, 11]:
    tmp1 = []
    for yhat in tqdm(t2['yhat_all']):
        # yhat_smoothed = utils.smooth(copy.deepcopy(yhat), smooth_by)
        yhat_smoothed = medfilt(copy.deepcopy(yhat), smooth_by)
        a = analysis.thresholded_error_types(labels, yhat_smoothed, edge_threshold=4, frame_num_array=frame_nums,
                                             thresholds=np.linspace(.05, .95, 19*2-1))
        ind = np.argmin(np.sum(np.asarray(a), axis=1))
        a = np.asarray(a)[ind, :]
        x = list(np.asarray(a))
        # a = analysis.thresholded_error_types(labels, yhat_smoothed, edge_threshold=4, frame_num_array=frame_nums,
        #                                      thresholds=[.5])
        # x = list(np.asarray(a)[0])
        auc = 1 - metrics.roc_auc_score(labels, yhat_smoothed)
        x.append(auc)
        tmp1.append(x)
    t2['analysis']['smooth_by_' + str(smooth_by)] = tmp1

'''##################################################################################################################'''
'''##################################################################################################################'''
short_names = []
for k in t2['names'][:-1]:
    short_name = ''
    if '__3lag__' in k:
        short_name += 'lag'
    else:
        short_name += 'no-lag'
    if ' aug ' in k:
        short_name += '\naugmented'
    else:
        short_name += '\nnot-augmented'
    short_name += '____' + k.split('__')[1]
    short_names.append(short_name)
short_names.append('WhACC')
t2['short_names'] = short_names

'''##################################################################################################################'''
'''##################################################################################################################'''
'''##################################################################################################################'''

# x = t2['analysis']['smooth_by_11']

# add_to_name = 'fixed point_5 threshold'
for iii in [1, 3, 5, 7, 9, 11]:
    x = t2['analysis']['smooth_by_' + str(iii)]

    tc_err = []
    one_min_auc = []
    for x2 in x:
        # x2 = x[k]
        one_min_auc.append(x2[-1])
        TC_tmp = np.sum(x2[:-3]) / t2['total_touches']
        tc_err.append(TC_tmp)
        # print(t2['names'][k])
        # print(TC_tmp)
        # print('----')
    names = np.asarray(t2['names'])[t2['inds']]
    '''##################################################################################################################'''
    '''##################################################################################################################'''

    fig, ax = plt.subplots(figsize=[10, 6])
    color = ['r', 'b', 'g', 'y']
    tick_centers = []
    names = []
    for i, k in enumerate(t2['inds'][:]):
        print(i // 4)
        i2 = i % 4  # cycle 1 to 4
        i3 = (i // 4) * 5  # for each 4 goes up by 5
        i4 = i3 + i2  # proper spacing for bar fig
        i5 = i3 + 2  # center text for groups of 4 bars
        tick_centers.append(i5 - .5)
        names.append(t2['short_names'][k].split('____')[0])

        ax.bar(i4, tc_err[k], color=color[i2])

    ax.set_xticks(tick_centers[0::4])
    ax.set_xticklabels(names[0::4])
    plt.ylim([0, 1])
    plt.title('smooth_by_' + str(iii) + ' ' + 'TC-error' + add_to_name)
    plt.savefig(save_dir + 'TC-error_'+'smooth_by_' + str(iii) +'_'+ add_to_name)
    '''##################################################################################################################'''
    '''##################################################################################################################'''

    fig, ax = plt.subplots(figsize=[10, 6])
    color = ['r', 'b', 'g', 'y']
    tick_centers = []
    names = []
    for i, k in enumerate(t2['inds'][:]):
        print(i // 4)
        i2 = i % 4  # cycle 1 to 4
        i3 = (i // 4) * 5  # for each 4 goes up by 5
        i4 = i3 + i2  # proper spacing for bar fig
        i5 = i3 + 2  # center text for groups of 4 bars
        tick_centers.append(i5 - .5)
        names.append(t2['short_names'][k].split('____')[0])

        ax.bar(i4, one_min_auc[k], color=color[i2])

    ax.set_xticks(tick_centers[0::4])
    ax.set_xticklabels(names[0::4])
    plt.ylim([0, .1])
    plt.title('smooth_by_' + str(iii) + ' ' + '1 - AUC' + add_to_name)
    plt.savefig(save_dir + 'AUC_smooth_by_' + str(iii) + ' ' + '1 - AUC' + add_to_name)








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

info = utils.info
of = utils.open_folder

'''##################################################################################################################'''
'''##################################################################################################################'''
'''##################################################################################################################'''
'''##################################################################################################################'''
'''##################################################################################################################'''

save_dir = '/Users/phil/Dropbox/HIRES_LAB/WhACC PAPER/figures/auc and TC errors smoothing test_V2 WITH_HAIR/'
utils.make_path(save_dir)
add_to_name = 'fixed point_5 threshold'


fn = '/Volumes/GoogleDrive-114825029448473821206/My Drive/Colab data/curation_for_auto_curator/DATA_FULL/full_in_range_and_other_useful_data.pkl'
in_range_d = utils.load_obj(fn)

fn2 = '/Volumes/GoogleDrive-114825029448473821206/My Drive/Colab data/curation_for_auto_curator/DATA_FULL/full_in_range_16_and_whacc_pred_all_4.pkl'
# fn2 = '/Volumes/GoogleDrive-114825029448473821206/My Drive/Colab data/curation_for_auto_curator/DATA_FULL/full_in_range_16_and_whacc_pred_no_hair.pkl'

yhat_d = utils.load_obj(fn2)
for k in yhat_d:
    print(k)

# t2 = utils.load_obj('/Volumes/GoogleDrive-114825029448473821206/My Drive/LIGHT_GBM//final_16_and_whacc_yhat_for_plotting.pkl')
# for k in t2:
#     print(k)
# assert np.all(yhat_d['model_keys'] == t2['names']), 'model key names dont match'

['labels', 'frame_nums', 'yhat_all', 'names']

t3 = {'yhat_all': []}  # 'frame_nums':[], 'labels':[]
for k in yhat_d['model_keys']:
    t3['yhat_all'].append(yhat_d[k].flatten() * yhat_d['in_range'])
t3['frame_nums'] = yhat_d['frame_nums']
t3['labels'] = yhat_d['labels'] * yhat_d['in_range']

# t3['labels'][yhat_d['in_range']==0] = -1

t3['names'] = yhat_d['model_keys']
t3['yhat_all'] = [k.flatten() for k in t3['yhat_all']]
t2 = t3

from scipy.signal import medfilt

t2['inds'] = [13, 11, 9, 15, 5, 3, 1, 7, 4, 2, 0, 6, 16]

utils.print_list_with_inds(t2['names'])
for k in t2['inds']:
    print(t2['names'][k])

labels = t2['labels']

t2['total_touches'] = np.sum(np.diff(t2['labels']) == 1)

frame_nums = t2['frame_nums']
t2['analysis'] = dict()
t2['analysis']['name'] = ['ghost', 'miss', 'join', 'split', 'append_4+', 'deduct_4+', 'append', 'deduct', '1 - auc']
TC_err_all = []
for smooth_by in [1, 3, 5, 7, 9, 11]:
    tmp1 = []
    for yhat in tqdm(t2['yhat_all']):
        # yhat_smoothed = utils.smooth(copy.deepcopy(yhat), smooth_by)
        yhat_smoothed = medfilt(copy.deepcopy(yhat), smooth_by)
        # a = analysis.thresholded_error_types(labels, yhat_smoothed, edge_threshold=4, frame_num_array=frame_nums,
        #                                      thresholds=np.linspace(.05, .95, 19*2-1))
        # ind = np.argmin(np.sum(np.asarray(a), axis=1))
        # a = np.asarray(a)[ind, :]
        # x = list(np.asarray(a))
        a = analysis.thresholded_error_types(labels, yhat_smoothed, edge_threshold=4, frame_num_array=frame_nums,
                                             thresholds=[.5])
        x = list(np.asarray(a)[0])
        auc = 1 - metrics.roc_auc_score(labels, yhat_smoothed)
        x.append(auc)
        tmp1.append(x)
    t2['analysis']['smooth_by_' + str(smooth_by)] = tmp1

'''##################################################################################################################'''
'''##################################################################################################################'''
short_names = []
for k in t2['names'][:-1]:
    short_name = ''
    if '__3lag__' in k:
        short_name += 'lag'
    else:
        short_name += 'no-lag'
    if ' aug ' in k:
        short_name += '\naugmented'
    else:
        short_name += '\nnot-augmented'
    short_name += '____' + k.split('__')[1]
    short_names.append(short_name)
short_names.append('WhACC')
t2['short_names'] = short_names

'''##################################################################################################################'''
'''##################################################################################################################'''
'''##################################################################################################################'''

# x = t2['analysis']['smooth_by_11']

# add_to_name = 'fixed point_5 threshold'
for iii in [1, 3, 5, 7, 9, 11]:
    x = t2['analysis']['smooth_by_' + str(iii)]

    tc_err = []
    one_min_auc = []
    for x2 in x:
        # x2 = x[k]
        one_min_auc.append(x2[-1])
        TC_tmp = np.sum(x2[:-3]) / t2['total_touches']
        tc_err.append(TC_tmp)
        # print(t2['names'][k])
        # print(TC_tmp)
        # print('----')
    names = np.asarray(t2['names'])[t2['inds']]
    '''##################################################################################################################'''
    '''##################################################################################################################'''

    fig, ax = plt.subplots(figsize=[10, 6])
    color = ['r', 'b', 'g', 'y']
    tick_centers = []
    names = []
    for i, k in enumerate(t2['inds'][:]):
        print(i // 4)
        i2 = i % 4  # cycle 1 to 4
        i3 = (i // 4) * 5  # for each 4 goes up by 5
        i4 = i3 + i2  # proper spacing for bar fig
        i5 = i3 + 2  # center text for groups of 4 bars
        tick_centers.append(i5 - .5)
        names.append(t2['short_names'][k].split('____')[0])

        ax.bar(i4, tc_err[k], color=color[i2])

    ax.set_xticks(tick_centers[0::4])
    ax.set_xticklabels(names[0::4])
    plt.ylim([0, 1])
    plt.title('smooth_by_' + str(iii) + ' ' + 'TC-error' + add_to_name)
    plt.savefig(save_dir + 'TC-error_'+'smooth_by_' + str(iii) +'_'+ add_to_name)
    '''##################################################################################################################'''
    '''##################################################################################################################'''

    fig, ax = plt.subplots(figsize=[10, 6])
    color = ['r', 'b', 'g', 'y']
    tick_centers = []
    names = []
    for i, k in enumerate(t2['inds'][:]):
        print(i // 4)
        i2 = i % 4  # cycle 1 to 4
        i3 = (i // 4) * 5  # for each 4 goes up by 5
        i4 = i3 + i2  # proper spacing for bar fig
        i5 = i3 + 2  # center text for groups of 4 bars
        tick_centers.append(i5 - .5)
        names.append(t2['short_names'][k].split('____')[0])

        ax.bar(i4, one_min_auc[k], color=color[i2])

    ax.set_xticks(tick_centers[0::4])
    ax.set_xticklabels(names[0::4])
    plt.ylim([0, .1])
    plt.title('smooth_by_' + str(iii) + ' ' + '1 - AUC' + add_to_name)
    plt.savefig(save_dir + 'AUC_smooth_by_' + str(iii) + ' ' + '1 - AUC' + add_to_name)













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

info = utils.info
of = utils.open_folder

'''##################################################################################################################'''
'''##################################################################################################################'''
'''##################################################################################################################'''
'''##################################################################################################################'''
'''##################################################################################################################'''

save_dir = '/Users/phil/Dropbox/HIRES_LAB/WhACC PAPER/figures/auc and TC errors smoothing test_V2 WITH_HAIR/'
save_dir = '/Users/phil/Dropbox/HIRES_LAB/WhACC PAPER/figures/auc and TC errors smoothing test_V2 NO_HAIR/'

utils.make_path(save_dir)
add_to_name = 'fixed point_5 threshold'
# add_to_name = 'Optimal threshold 05 to 95'


fn = '/Volumes/GoogleDrive-114825029448473821206/My Drive/Colab data/curation_for_auto_curator/DATA_FULL/full_in_range_and_other_useful_data.pkl'
in_range_d = utils.load_obj(fn)

# fn2 = '/Volumes/GoogleDrive-114825029448473821206/My Drive/Colab data/curation_for_auto_curator/DATA_FULL/full_in_range_16_and_whacc_pred_all_4.pkl'
fn2 = '/Volumes/GoogleDrive-114825029448473821206/My Drive/Colab data/curation_for_auto_curator/DATA_FULL/full_in_range_16_and_whacc_pred_no_hair.pkl'

yhat_d = utils.load_obj(fn2)
for k in yhat_d:
    print(k)

# t2 = utils.load_obj('/Volumes/GoogleDrive-114825029448473821206/My Drive/LIGHT_GBM//final_16_and_whacc_yhat_for_plotting.pkl')
# for k in t2:
#     print(k)
# assert np.all(yhat_d['model_keys'] == t2['names']), 'model key names dont match'

['labels', 'frame_nums', 'yhat_all', 'names']

t3 = {'yhat_all': []}  # 'frame_nums':[], 'labels':[]
for k in yhat_d['model_keys']:
    t3['yhat_all'].append(yhat_d[k].flatten() * yhat_d['in_range'])
t3['frame_nums'] = yhat_d['frame_nums']
t3['labels'] = yhat_d['labels'] * yhat_d['in_range']

# t3['labels'][yhat_d['in_range']==0] = -1

t3['names'] = yhat_d['model_keys']
t3['yhat_all'] = [k.flatten() for k in t3['yhat_all']]
t2 = t3

from scipy.signal import medfilt

t2['inds'] = [13, 11, 9, 15, 5, 3, 1, 7, 4, 2, 0, 6, 16]

utils.print_list_with_inds(t2['names'])
for k in t2['inds']:
    print(t2['names'][k])

labels = t2['labels']

t2['total_touches'] = np.sum(np.diff(t2['labels']) == 1)

frame_nums = t2['frame_nums']
t2['analysis'] = dict()
t2['analysis']['name'] = ['ghost', 'miss', 'join', 'split', 'append_4+', 'deduct_4+', 'append', 'deduct', '1 - auc']
TC_err_all = []
for smooth_by in [1, 3, 5, 7, 9, 11]:
    tmp1 = []
    for yhat in tqdm(t2['yhat_all']):
        # yhat_smoothed = utils.smooth(copy.deepcopy(yhat), smooth_by)
        yhat_smoothed = medfilt(copy.deepcopy(yhat), smooth_by)
        # a = analysis.thresholded_error_types(labels, yhat_smoothed, edge_threshold=4, frame_num_array=frame_nums,
        #                                      thresholds=np.linspace(.05, .95, 19*2-1))
        # ind = np.argmin(np.sum(np.asarray(a), axis=1))
        # a = np.asarray(a)[ind, :]
        # x = list(np.asarray(a))
        a = analysis.thresholded_error_types(labels, yhat_smoothed, edge_threshold=4, frame_num_array=frame_nums,
                                             thresholds=[.5])
        x = list(np.asarray(a)[0])
        auc = 1 - metrics.roc_auc_score(labels, yhat_smoothed)
        x.append(auc)
        tmp1.append(x)
    t2['analysis']['smooth_by_' + str(smooth_by)] = tmp1

'''##################################################################################################################'''
'''##################################################################################################################'''
short_names = []
for k in t2['names'][:-1]:
    short_name = ''
    if '__3lag__' in k:
        short_name += 'lag'
    else:
        short_name += 'no-lag'
    if ' aug ' in k:
        short_name += '\naugmented'
    else:
        short_name += '\nnot-augmented'
    short_name += '____' + k.split('__')[1]
    short_names.append(short_name)
short_names.append('WhACC')
t2['short_names'] = short_names

'''##################################################################################################################'''
'''##################################################################################################################'''
'''##################################################################################################################'''

# x = t2['analysis']['smooth_by_11']

# add_to_name = 'fixed point_5 threshold'
for iii in [1, 3, 5, 7, 9, 11]:
    x = t2['analysis']['smooth_by_' + str(iii)]

    tc_err = []
    one_min_auc = []
    for x2 in x:
        # x2 = x[k]
        one_min_auc.append(x2[-1])
        TC_tmp = np.sum(x2[:-3]) / t2['total_touches']
        tc_err.append(TC_tmp)
        # print(t2['names'][k])
        # print(TC_tmp)
        # print('----')
    names = np.asarray(t2['names'])[t2['inds']]
    '''##################################################################################################################'''
    '''##################################################################################################################'''

    fig, ax = plt.subplots(figsize=[10, 6])
    color = ['r', 'b', 'g', 'y']
    tick_centers = []
    names = []
    for i, k in enumerate(t2['inds'][:]):
        print(i // 4)
        i2 = i % 4  # cycle 1 to 4
        i3 = (i // 4) * 5  # for each 4 goes up by 5
        i4 = i3 + i2  # proper spacing for bar fig
        i5 = i3 + 2  # center text for groups of 4 bars
        tick_centers.append(i5 - .5)
        names.append(t2['short_names'][k].split('____')[0])

        ax.bar(i4, tc_err[k], color=color[i2])

    ax.set_xticks(tick_centers[0::4])
    ax.set_xticklabels(names[0::4])
    plt.ylim([0, 1])
    plt.title('smooth_by_' + str(iii) + ' ' + 'TC-error' + add_to_name)
    plt.savefig(save_dir + 'TC-error_'+'smooth_by_' + str(iii) +'_'+ add_to_name)
    '''##################################################################################################################'''
    '''##################################################################################################################'''

    fig, ax = plt.subplots(figsize=[10, 6])
    color = ['r', 'b', 'g', 'y']
    tick_centers = []
    names = []
    for i, k in enumerate(t2['inds'][:]):
        print(i // 4)
        i2 = i % 4  # cycle 1 to 4
        i3 = (i // 4) * 5  # for each 4 goes up by 5
        i4 = i3 + i2  # proper spacing for bar fig
        i5 = i3 + 2  # center text for groups of 4 bars
        tick_centers.append(i5 - .5)
        names.append(t2['short_names'][k].split('____')[0])

        ax.bar(i4, one_min_auc[k], color=color[i2])

    ax.set_xticks(tick_centers[0::4])
    ax.set_xticklabels(names[0::4])
    plt.ylim([0, .1])
    plt.title('smooth_by_' + str(iii) + ' ' + '1 - AUC' + add_to_name)
    plt.savefig(save_dir + 'AUC_smooth_by_' + str(iii) + ' ' + '1 - AUC' + add_to_name)





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

info = utils.info
of = utils.open_folder

'''##################################################################################################################'''
'''##################################################################################################################'''
'''##################################################################################################################'''
'''##################################################################################################################'''
'''##################################################################################################################'''

save_dir = '/Users/phil/Dropbox/HIRES_LAB/WhACC PAPER/figures/auc and TC errors smoothing test_V2 WITH_HAIR/'
save_dir = '/Users/phil/Dropbox/HIRES_LAB/WhACC PAPER/figures/auc and TC errors smoothing test_V2 NO_HAIR/'

utils.make_path(save_dir)
add_to_name = 'fixed point_5 threshold'
# add_to_name = 'Optimal threshold 05 to 95'


fn = '/Volumes/GoogleDrive-114825029448473821206/My Drive/Colab data/curation_for_auto_curator/DATA_FULL/full_in_range_and_other_useful_data.pkl'
in_range_d = utils.load_obj(fn)

# fn2 = '/Volumes/GoogleDrive-114825029448473821206/My Drive/Colab data/curation_for_auto_curator/DATA_FULL/full_in_range_16_and_whacc_pred_all_4.pkl'
fn2 = '/Volumes/GoogleDrive-114825029448473821206/My Drive/Colab data/curation_for_auto_curator/DATA_FULL/full_in_range_16_and_whacc_pred_no_hair.pkl'

yhat_d = utils.load_obj(fn2)
for k in yhat_d:
    print(k)

# t2 = utils.load_obj('/Volumes/GoogleDrive-114825029448473821206/My Drive/LIGHT_GBM//final_16_and_whacc_yhat_for_plotting.pkl')
# for k in t2:
#     print(k)
# assert np.all(yhat_d['model_keys'] == t2['names']), 'model key names dont match'

['labels', 'frame_nums', 'yhat_all', 'names']

t3 = {'yhat_all': []}  # 'frame_nums':[], 'labels':[]
for k in yhat_d['model_keys']:
    t3['yhat_all'].append(yhat_d[k].flatten() * yhat_d['in_range'])
t3['frame_nums'] = yhat_d['frame_nums']
t3['labels'] = yhat_d['labels'] * yhat_d['in_range']

# t3['labels'][yhat_d['in_range']==0] = -1

t3['names'] = yhat_d['model_keys']
t3['yhat_all'] = [k.flatten() for k in t3['yhat_all']]
t2 = t3

from scipy.signal import medfilt

t2['inds'] = [13, 11, 9, 15, 5, 3, 1, 7, 4, 2, 0, 6, 16]

utils.print_list_with_inds(t2['names'])
for k in t2['inds']:
    print(t2['names'][k])

labels = t2['labels']

t2['total_touches'] = np.sum(np.diff(t2['labels']) == 1)

frame_nums = t2['frame_nums']
t2['analysis'] = dict()
t2['analysis']['name'] = ['ghost', 'miss', 'join', 'split', 'append_4+', 'deduct_4+', 'append', 'deduct', '1 - auc']
TC_err_all = []
for smooth_by in [1, 3, 5, 7, 9, 11]:
    tmp1 = []
    for yhat in tqdm(t2['yhat_all']):
        # yhat_smoothed = utils.smooth(copy.deepcopy(yhat), smooth_by)
        yhat_smoothed = medfilt(copy.deepcopy(yhat), smooth_by)
        # a = analysis.thresholded_error_types(labels, yhat_smoothed, edge_threshold=4, frame_num_array=frame_nums,
        #                                      thresholds=np.linspace(.05, .95, 19*2-1))
        # ind = np.argmin(np.sum(np.asarray(a), axis=1))
        # a = np.asarray(a)[ind, :]
        # x = list(np.asarray(a))
        a = analysis.thresholded_error_types(labels, yhat_smoothed, edge_threshold=4, frame_num_array=frame_nums,
                                             thresholds=[.5])
        x = list(np.asarray(a)[0])
        auc = 1 - metrics.roc_auc_score(labels, yhat_smoothed)
        x.append(auc)
        tmp1.append(x)
    t2['analysis']['smooth_by_' + str(smooth_by)] = tmp1

'''##################################################################################################################'''
'''##################################################################################################################'''
short_names = []
for k in t2['names'][:-1]:
    short_name = ''
    if '__3lag__' in k:
        short_name += 'lag'
    else:
        short_name += 'no-lag'
    if ' aug ' in k:
        short_name += '\naugmented'
    else:
        short_name += '\nnot-augmented'
    short_name += '____' + k.split('__')[1]
    short_names.append(short_name)
short_names.append('WhACC')
t2['short_names'] = short_names

'''##################################################################################################################'''
'''##################################################################################################################'''
'''##################################################################################################################'''

# x = t2['analysis']['smooth_by_11']

# add_to_name = 'fixed point_5 threshold'
for iii in [1, 3, 5, 7, 9, 11]:
    x = t2['analysis']['smooth_by_' + str(iii)]

    tc_err = []
    one_min_auc = []
    for x2 in x:
        # x2 = x[k]
        one_min_auc.append(x2[-1])
        TC_tmp = np.sum(x2[:-3]) / t2['total_touches']
        tc_err.append(TC_tmp)
        # print(t2['names'][k])
        # print(TC_tmp)
        # print('----')
    names = np.asarray(t2['names'])[t2['inds']]
    '''##################################################################################################################'''
    '''##################################################################################################################'''

    fig, ax = plt.subplots(figsize=[10, 6])
    color = ['r', 'b', 'g', 'y']
    tick_centers = []
    names = []
    for i, k in enumerate(t2['inds'][:]):
        print(i // 4)
        i2 = i % 4  # cycle 1 to 4
        i3 = (i // 4) * 5  # for each 4 goes up by 5
        i4 = i3 + i2  # proper spacing for bar fig
        i5 = i3 + 2  # center text for groups of 4 bars
        tick_centers.append(i5 - .5)
        names.append(t2['short_names'][k].split('____')[0])

        ax.bar(i4, tc_err[k], color=color[i2])

    ax.set_xticks(tick_centers[0::4])
    ax.set_xticklabels(names[0::4])
    plt.ylim([0, 1])
    plt.title('smooth_by_' + str(iii) + ' ' + 'TC-error' + add_to_name)
    plt.savefig(save_dir + 'TC-error_'+'smooth_by_' + str(iii) +'_'+ add_to_name)
    '''##################################################################################################################'''
    '''##################################################################################################################'''

    fig, ax = plt.subplots(figsize=[10, 6])
    color = ['r', 'b', 'g', 'y']
    tick_centers = []
    names = []
    for i, k in enumerate(t2['inds'][:]):
        print(i // 4)
        i2 = i % 4  # cycle 1 to 4
        i3 = (i // 4) * 5  # for each 4 goes up by 5
        i4 = i3 + i2  # proper spacing for bar fig
        i5 = i3 + 2  # center text for groups of 4 bars
        tick_centers.append(i5 - .5)
        names.append(t2['short_names'][k].split('____')[0])

        ax.bar(i4, one_min_auc[k], color=color[i2])

    ax.set_xticks(tick_centers[0::4])
    ax.set_xticklabels(names[0::4])
    plt.ylim([0, .1])
    plt.title('smooth_by_' + str(iii) + ' ' + '1 - AUC' + add_to_name)
    plt.savefig(save_dir + 'AUC_smooth_by_' + str(iii) + ' ' + '1 - AUC' + add_to_name)








#  temporally ordered but not sull trials by may be seperated by TIRAL???

f = '/Volumes/GoogleDrive-114825029448473821206/My Drive/LIGHT_GBM/FEATURE_DATA_2_just_2105_temporally_ordered/val_final_gbm_2105.h5'
utils.print_h5_keys(f)

with h5py.File(f, 'r') as h:
    h5_inds_each = h['h5_inds_each'][:]
    h5_inds_all = h['h5_inds_all'][:]
    h5_inds_each = h['h5_inds_each'][:]
    frame_nums = h['frame_nums'][:]

    all_combined_h5_names = h['all_combined_h5_names'][:]
    final_resorted_train_val_ins = h['final_resorted_train_val_ins'][:]
    frame_num_file_inds = h['frame_num_file_inds'][:]
    h5_lengths = h['h5_lengths'][:]




f = '/Volumes/GoogleDrive-114825029448473821206/My Drive/LIGHT_GBM/H5_data/3lag_numpy_aug_for_final_LGBM/keep_inds_no_pole_hair_no_skip_frames/80_border/T_V_TS_set_inds/AH0407_160613_JC1003_AAAC_3lag.npy'
tmp1 = np.load(f, allow_pickle=True)


for k in tmp1:
    # print(np.asarray(k).shape)
    print(np.unique(np.diff(k)))
    print(np.where(np.diff(k)!=1)[0])




















split_ratio = [7, 2, 1]
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

    label_multiply_by_all = []
    fn_inds = utils.split_list(range(len(fn)), split_ratio)
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
            tmp1.append(k*0)
        label_multiply_by_all = tmp1
    foo_save(save_name, label_multiply_by_all)



# for k in label_multiply_by_all:
#     plt.plot(.1+k[::3990])










"""
################################################################################################
################################################################################################
TESTING SPLIT BY TRIAL 
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
label_files = natsorted(utils.get_files(label_dir, '*.npy'), alg=ns.REAL)
h5_meta_data_files = natsorted(utils.get_files(regular_dir, '*.h5'), alg=ns.REAL)

for i, (label_f, h5_meta_data) in enumerate(zip(label_files, h5_meta_data_files)):
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

















