import pandas as pd

from simba.read_config_unit_tests import (read_config_entry, read_config_file)
from simba.features_scripts.unit_tests import read_video_info_csv, read_video_info
from simba.misc_tools import get_fn_ext
from simba.rw_dfs import read_df
import numpy as np
import os, glob
import cv2
from numba import jit
import matplotlib.pylab as plt
from scipy.ndimage.filters import gaussian_filter
import scipy.interpolate
import matplotlib.colors as colors

class HeatMapper(object):
    def __init__(self,
                 config_path: str=None,
                 final_img_setting: bool=None,
                 video_setting: bool=None,
                 frame_setting: bool=None,
                 bin_size: int=None,
                 palette: str=None,
                 bodypart: str=None,
                 clf_name: str=None,
                 max_scale: int=None):

        self.frame_setting, self.video_setting = frame_setting, video_setting
        self.final_img_setting, self.bp = final_img_setting, bodypart
        self.bin_size, self.max_scale = bin_size, max_scale
        self.clf_name, self.palette = clf_name, palette
        if (not self.frame_setting) and (not self.video_setting) and (not self.final_img_setting):
            raise ValueError('SIMBA ERROR: Please choose to select either videos, frames, and/or final image.')
        self.config = read_config_file(config_path)
        self.project_path = read_config_entry(self.config, 'General settings', 'project_path', data_type='folder_path')
        self.file_type = read_config_entry(self.config, 'General settings', 'workflow_file_type', 'str', 'csv')
        self.save_dir = os.path.join(self.project_path, 'frames', 'output', 'heatmaps_location')
        self.vid_info_df = read_video_info_csv(os.path.join(self.project_path, 'logs', 'video_info.csv'))
        if not os.path.exists(self.save_dir): os.makedirs(self.save_dir)
        self.dir_in = os.path.join(self.project_path, 'csv', 'machine_results')
        self.files_found = glob.glob(self.dir_in + "/*." + self.file_type)
        self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.bp_lst = [self.bp + '_x', self.bp + '_y']
        print('Processing {} video(s)...'.format(str(len(self.files_found))))

    @staticmethod
    @jit(nopython=True)
    def calculate_cum_array(cum_array=None, frames_in_window_array=None):
        for frame_no in range(frames_in_window_array.shape[2]):
            for row in range(frames_in_window_array.shape[0]):
                for col in range(frames_in_window_array.shape[1]):
                    cum_array[row, col] += frames_in_window_array[row, col, frame_no]
        return cum_array



    def create_heatmaps(self):
        for file_cnt, file_path in enumerate(self.files_found):
            _, self.video_name, _ = get_fn_ext(file_path)
            self.video_info, self.px_per_mm, self.fps = read_video_info(vidinfDf=self.vid_info_df, currVidName=self.video_name)
            self.width, self.height = int(self.video_info['Resolution_width'].values[0]), int(self.video_info['Resolution_height'].values[0])
            self.pixels_per_bin = int(self.px_per_mm * self.bin_size)
            self.hbins_cnt, self.vbins_cnt = int(self.width / self.pixels_per_bin), int(self.height / self.pixels_per_bin)
            hight_to_width = round((self.vbins_cnt / self.hbins_cnt), 3)
            plt.figure(figsize=(10, int(10*hight_to_width)))
            self.bin_dict = {}
            x_location, y_location = 0, 0
            self.data_df = read_df(file_path, self.file_type)
            self.clf_idx = self.data_df[self.bp_lst][self.data_df[self.clf_name] == 1].reset_index().to_numpy()
            for hbin in range(self.hbins_cnt):
                self.bin_dict[hbin] = {}
                for vbin in range(self.vbins_cnt):
                    self.bin_dict[hbin][vbin] = {'top_left_x': x_location,
                                                 'top_left_y': y_location,
                                                 'bottom_right_x': x_location + self.pixels_per_bin,
                                                 'bottom_right_y': y_location + self.pixels_per_bin}
                    y_location += self.pixels_per_bin
                y_location = 0
                x_location += self.pixels_per_bin
            self.clf_array = np.zeros((self.vbins_cnt, self.hbins_cnt, len(self.data_df)))
            for clf_frame in self.clf_idx:
                for h_bin_name, v_dict in self.bin_dict.items():
                    for v_bin_name, c in v_dict.items():
                        if (clf_frame[0] < c['bottom_right_x'] and clf_frame[0] > c['top_left_x']):
                            if (clf_frame[1] < c['bottom_right_y'] and clf_frame[1] < c['top_left_y']):
                                self.clf_array[v_bin_name][h_bin_name][clf_frame] = 1
            cum_array = np.zeros((self.clf_array.shape[0], self.clf_array.shape[1]))
            for frm_cnt, cumulative_frm in enumerate(range(self.clf_array.shape[2])):
                print(frm_cnt)
                frames_in_window = self.clf_array[:,:,:cumulative_frm]
                cum_array = self.calculate_cum_array(cum_array=cum_array, frames_in_window_array=frames_in_window)
                cum_array_s = cum_array / self.fps
                cum_df = pd.DataFrame(cum_array_s).reset_index()
                cum_df = cum_df.melt(id_vars='index', value_vars=None, var_name=None, value_name='seconds', col_level=None).rename(columns={'index':'vertical_idx', 'variable': 'horizontal_idx'})
                cum_df['color'] = (cum_df['seconds'] / self.max_scale).round(2).clip(upper=100)
                color_array = np.zeros((len(cum_df['vertical_idx'].unique()), len(cum_df['horizontal_idx'].unique())))
                for i in range(color_array.shape[0]):
                    for j in range(color_array.shape[1]):
                        value = cum_df["color"][(cum_df["horizontal_idx"] == j) & (cum_df["vertical_idx"] == i)].values[0]
                        value = round((value / 100) * self.max_scale, 2)
                        color_array[i,j] = value

                plt.pcolormesh(color_array, shading='gouraud', rasterized=True, alpha=1, vmin=0.0, vmax=float(self.max_scale))
                plt.xticks([])
                plt.yticks([])
                plt.axis('off')
                plt.tick_params(axis='both', which='both', length=0)
                cb = plt.colorbar(pad=0.0)
                cb.ax.tick_params(size=0)
                cb.outline.set_visible(False)
                cb.set_label('{} (seconds)'.format(self.clf_name), rotation=270, labelpad=25)
                plt.show()
                plt.close()




                #
                #
                #
                # spacing = 500
                # xi, yi = np.linspace(x.min(), x.max(), spacing), np.linspace(y.min(), y.max(), spacing)
                # XI, YI = np.meshgrid(xi, yi)
                # rbf = scipy.interpolate.Rbf(x, y, z, function='linear')
                # ZI = rbf(XI, YI)
                #
                # fig, ax = plt.subplots()
                #
                # sc = ax.imshow(ZI, vmin=z.min(), vmax=z.max(), origin='lower',
                #                extent=[x.min(), x.max(), y.min(),
                #                        y.max()], cmap="GnBu", norm=colors.LogNorm(vmin=ZI.min(),
                #                                                                   vmax=ZI.max()))
                #
                # fig.colorbar(sc, ax=ax, fraction=0.05, pad=0.01)
                # #
                # # plt.show()
                #




            #
            #     heatmap.tick_params(axis='both', which='both', length=0)
            #     heatmap.set(xticklabels=[], yticklabels=[])
            #     plt.close()
            #     print(frm_cnt, np.max(cum_array_s))
            # plt.show()















test = HeatMapper(config_path=r'/Users/simon/Desktop/troubleshooting/train_model_project/project_folder/project_config.ini',
                 final_img_setting=False,
                 video_setting=True,
                 frame_setting=False,
                 bin_size=100,
                 palette='jet',
                 bodypart='Nose_1',
                 clf_name='Attack',
                 max_scale=10)
test.create_heatmaps()






