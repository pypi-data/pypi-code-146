import pandas as pd
from numba import jit, prange
from scipy import spatial
import numpy as np
import math
from simba.rw_dfs import read_df
from simba.drop_bp_cords import getBpNames, create_body_part_dictionary, get_fn_ext
from simba.misc_tools import check_multi_animal_status
from simba.read_config_unit_tests import read_config_file, check_float
import time
import sys
sys.frozen = True


def convex_hull_area(data: pd.DataFrame,
                     animal_name: str,
                     animal_bp_lk: dict,
                     pix_per_mm: float):

    """
    Calculates the hull of an animal in each frame.

    Parameters
    ----------
    data: pd.DataFrame
        df with features.
    animal_name: str
        Name of animal to calculate hull area for
    animal_bp_lk: dict
        Dict containing animal body-part names
    pix_per_mm: float
        Pixels per millimeter in the video

    Returns
    -------
    results: np.array
    """

    bp_lst = [x for xs in zip(animal_bp_lk[animal_name]['X_bps'], animal_bp_lk[animal_name]['Y_bps']) for x in xs]
    data_array = data[bp_lst].values
    results = np.full((data_array.shape[0], 1), -1)
    for frm_cnt in range(data_array.shape[0]):
        frm_data = np.reshape(data_array[frm_cnt], (-1, 2))
        results[frm_cnt] = (spatial.ConvexHull(points=frm_data).area / pix_per_mm)

    return results

@jit(nopython=True, parallel=True)
def euclid_distance_between_two_bodyparts(data: np.array,
                                          pix_per_mm: float):
    """
    Calculates the euclidean distance between two body parts in a series.

    Parameters
    ----------
    data: np.array
        2d numpy array where each row is a frame and 4 column [bp1_x, bp1_y, bp2_x, bp2_y]
    pix_per_mm: float
        Pixels per millimeter in the video

    Returns
    -------
    results: np.array
    """


    results = np.full((data.shape[0], 1), -1.0)
    for i in prange(results.shape[0]):
        results[i] = np.sqrt((data[i][0] - data[i][2]) ** 2 + (data[i][1] - data[i][3]) ** 2) / pix_per_mm
    return results


def aggregate_statistics_of_hull_area(data: np.array,
                                      agg_type: str,
                                      pix_per_mm: float):

    """
    Calculates aggregate statistics of points in a hull (i.e., largest, smallest, mean, or median distances
    between points).

    Parameters
    ----------
    data: np.array
        2d numpy array where each row is a frame and each
    agg_type: str
        Type of aggregation (min, max, mean, or median)
    pix_per_mm: float
        Pixels per millimeter in the video

    Returns
    -------
    results: np.array
    """

    distances = spatial.distance.cdist(data, data, metric='euclidean')
    distances[distances == 0] = np.nan
    if agg_type == 'mean':
        results = np.nanmean(distances, axis=1) / pix_per_mm
    elif agg_type == 'median':
        results = np.nanmedian(distances, axis=1) / pix_per_mm
    elif agg_type == 'max':
        results = np.nanmax(distances, axis=1) / pix_per_mm
    elif agg_type == 'min':
        results = np.nanmin(distances, axis=1) / pix_per_mm
    else:
        print('SIMBA ERROR: {} is not recofnized (OPTIONS: min, max, mean, median)'.format(str(agg_type)))
        raise ValueError()

    return results

@jit(nopython=True, parallel=True)
def rolling_window_aggregation(data: np.array,
                               window_size: int,
                               agg_type: str,
                               pix_per_mm: float):
    """
    Calculates time-window rolling aggregate statistics for a vector

    Parameters
    ----------
    data: np.array
        Vector of data (e.g., the size of the animal in each frame of the video)
    agg_type: str
        Type of aggregation (mean median, or sum)
    pix_per_mm: float
        Pixels per millimeter in the video

    Returns
    -------
    results: np.array
    """

    results = np.full((data.shape[0], 1), -1.0)
    for end_frame in prange(data.shape[0]):
        start_frame = end_frame-window_size
        if start_frame < 0: start_frame = 0
        window_data = data[start_frame: end_frame]
        if agg_type == 'mean':
            results[end_frame] = np.nanmean(window_data) / pix_per_mm
        if agg_type == 'median':
            results[end_frame] = np.nanmedian(window_data) / pix_per_mm
        if agg_type == 'sum':
            results[end_frame] = np.nansum(window_data) / pix_per_mm

    return results

@jit(nopython=True, parallel=True, cache=True)
def three_point_angle(data: np.array):
    results = np.full((data.shape[0], 1), -1.0)
    for i in prange(data.shape[0]):
        angle = np.degrees(np.arctan2(data[i][5] - data[i][3], data[i][4] - data[i][2]) - np.arctan2(data[i][1] - data[i][3], data[i][1] - data[i][1]))
        if angle < 0:
            results[i] = angle + 360
        else:
            results[i] = angle
    return results










in_data = read_df('/Users/simon/Desktop/troubleshooting/train_model_project/project_folder/csv/outlier_corrected_movement_location/Together_1.csv', 'csv')
no_animals = 2
config_path = r'/Users/simon/Desktop/troubleshooting/train_model_project/project_folder/project_config.ini'
config = read_config_file(config_path)
multi_animal_status, multi_animal_id_lst = check_multi_animal_status(config, no_animals)
x_cols, y_cols, p_cols = getBpNames(config_path)
animal_bp_dict = create_body_part_dictionary(multi_animal_status, multi_animal_id_lst, no_animals, x_cols, y_cols, p_cols, [])
mouse_1_headers = [x for xs in zip(animal_bp_dict['Animal_1']['X_bps'], animal_bp_dict['Animal_1']['Y_bps']) for x in xs]


angle_data = in_data[['Nose_2_x', 'Nose_2_y', 'Center_2_x', 'Center_2_y', 'Tail_base_2_x', 'Tail_base_2_y']].values




_ = convex_hull_area(data=in_data, animal_name='Animal_1', animal_bp_lk=animal_bp_dict, pix_per_mm=4.75)
_ = euclid_distance_between_two_bodyparts(data=in_data[['Nose_1_x', 'Nose_1_y', 'Tail_base_1_x', 'Tail_base_1_y']].values, pix_per_mm=4.75)
_ = aggregate_statistics_of_hull_area(data=in_data[mouse_1_headers].values, agg_type='median', pix_per_mm=4.75)
_ = rolling_window_aggregation(data=in_data['Nose_1_x'].values, window_size=15, agg_type='mean', pix_per_mm=4.75)
_ = three_point_angle(data=angle_data)


#rolling_window_aggregation.parallel_diagnostics(level=4)
#euclid_distance_between_two_bodyparts.parallel_diagnostics(level=4)