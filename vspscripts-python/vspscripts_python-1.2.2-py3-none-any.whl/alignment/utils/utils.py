import os
import cv2
import warnings
import numpy as np
from math import cos, sin, acos

def findAllFile(base, format=None):
    for root, ds, fs in os.walk(base):
        for f in fs:
            if format:
                if f.endswith(format):
                    fullname = os.path.join(root, f)
                    yield fullname
            else:
                fullname = os.path.join(root, f)
                yield fullname

def Sim_Trans(points, M_Sim):
    points_exp = np.c_[points, np.ones((points.shape[0], 1))]
    points_sim_exp = (M_Sim.dot(points_exp.T)).T
    # return np.delete(points_sim_exp, -1, axis=1)
    return points_sim_exp

def is_deleted(points, img_size):
    for i in range(len(points)):
        if points[i][0] > 0 and points[i][0] < img_size and points[i][1] > 0 and points[i][1] < img_size:
            return False
    return True

def points_check(points, img_size):
    if is_deleted(points, img_size):
        return np.array([])
    else:
        return np.clip(points, 0, img_size)

def Crop_Trans(points_sim, ori_shape, img_size):
    crop_deta = ((ori_shape[0]-img_size)/2, (ori_shape[1]-img_size)/2)
    return points_check(points_sim - crop_deta, img_size)
