import os
import cv2
import warnings
import numpy as np
from PIL import Image
from functools import partial
import matplotlib.pyplot as plt
from multiprocessing import Process, Manager, Pool
from sklearn.base import BaseEstimator, RegressorMixin
from sklearn.model_selection import RandomizedSearchCV
from vspscripts.alignment.utils import gol
from vspscripts.alignment.matching.dist import pixel_dist
from vspscripts.alignment.utils.img import crop_imgcam, Get_Mask_ROI
from vspscripts.alignment.utils.mat import Matrix_Sim_Modification, Matrix_Sim_Generation, Matrix_Sim_cv2image

def Feature_matching(img, cam, show_matches=False, method='AKAZE'):
    if method == 'KAZE':
        # Initiate KAZE detector
        operator = cv2.KAZE_create()
    elif method == 'AKAZE':
        # Initiate AKAZE detector
        operator = cv2.AKAZE_create()
    elif method == 'BRISK':
        # Initiate BRISK detector
        operator = cv2.BRISK_create()
    elif method == 'SIFT':
        # Initiate SIFT detector
        operator = cv2.xfeatures2d.SIFT_create()
    elif method == 'SURF':
        # Initiate SURF detector
        operator = cv2.xfeatures2d.SURF_create()
    elif method == 'ORB':
        # Initiate ORB detector
        operator = cv2.ORB_create()

    # Find the keypoints and descriptors
    kp1, des1 = operator.detectAndCompute(img, None)
    kp2, des2 = operator.detectAndCompute(cam, None)

    if type(des1) == type(None) or type(des2) == type(None):
        return
    # BFMatcher with default params
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1, des2, k=2)
    # Apply ratio test
    good_matches = []
    for m, n in matches:
        if m.distance < 0.75*n.distance:
            good_matches.append([m])

    # bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck = True)
    # matches = bf.match(des1, des2)
    # matches=sorted(matches, key=lambda x:x.distance)
    # good_matches = matches[:30]
    
    # Draw matches
    if show_matches:
        img_matches = cv2.drawMatchesKnn(img, kp1, cam, kp2, matches, None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
        img_good_matches = cv2.drawMatchesKnn(img, kp1, cam, kp2, good_matches, None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
        # img_matches = cv2.drawMatches(img, kp1, cam, kp2, matches, None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
        # img_good_matches = cv2.drawMatches(img, kp1, cam, kp2, good_matches, None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
        if not os.path.exists('./tmp'):
            os.makedirs('./tmp')
        cv2.imwrite('./tmp/Feature_matching.jpg', img_matches)
        cv2.imwrite('./tmp/Feature_good_matching.jpg', img_good_matches)

    # Select good matched keypoints
    ref_matched_kpts = np.float32([kp1[m[0].queryIdx].pt for m in good_matches]).reshape(-1,1,2)
    sensed_matched_kpts = np.float32([kp2[m[0].trainIdx].pt for m in good_matches]).reshape(-1,1,2)
    # ref_matched_kpts = np.float32([kp1[m.queryIdx].pt for m in good_matches]).reshape(-1,1,2)
    # sensed_matched_kpts = np.float32([kp2[m.trainIdx].pt for m in good_matches]).reshape(-1,1,2)

    ##############Implementation by OpenCV################
    assert len(ref_matched_kpts) == len(sensed_matched_kpts)
    if len(ref_matched_kpts) >= 2:
        M = cv2.estimateAffinePartial2D(ref_matched_kpts, sensed_matched_kpts, method=cv2.LMEDS) # 
        M_Sim = M[0]
        return M_Sim
    else:
        if gol.get_value('IS_PRINT'):
            print('The number of good matches is less than 2!')
        return
    ##############Implementation by skimage###############
    # from skimage import transform as trans
    # tform = trans.SimilarityTransform()
    # res =tform.estimate(np.squeeze(ref_matched_kpts), np.squeeze(sensed_matched_kpts))
    # M_Sim = tform.params[0:2,:]

    # warped_image = cv2.warpAffine(img_ori, M_Sim, img.shape, borderValue=(0, 0, 0))

def Pixel_matching(img, cam, M_Sim, shift_max = 50, match_step = 1, threshold_err = 0.1, is_difficult=False, is_Scaling=False):
    shift_x = np.arange(-shift_max, shift_max+1, step = match_step)
    shift_y = np.arange(-shift_max, shift_max+1, step = match_step)
    if is_Scaling:
        scale = np.arange(-0.05, 0.06, step = 0.01)
    else:
        scale = [0,]

    bad_score = 1.0
    best_parameters = {'shift_x':0, 'shift_y':0, 'scale_deta': 0}
    for x_deta in shift_x:
        for y_deta in shift_y:
            for scale_deta in scale:
                estimator = ImgCamRegression(M_Sim, x_deta, y_deta, scale_deta)
                # input_img = img.copy()
                # input_cam = cam.copy()
                score = estimator.predict_cv(img, cam, is_crop=not is_difficult)
                if score < bad_score:
                    bad_score = score
                    best_parameters = {'shift_x':x_deta, 'shift_y':y_deta, 'scale_deta': scale_deta}
                if bad_score <= threshold_err:
                    if gol.get_value('IS_PRINT'):
                        print('Achieve the preset error rate {}.'.format(bad_score))
                    return Matrix_Sim_Modification(M_Sim, 0, best_parameters['scale_deta'], best_parameters['shift_x'], best_parameters['shift_y']), bad_score
    if bad_score == 1.0:
        warnings.warn('Cannot find the best match!', UserWarning)
        return Matrix_Sim_Generation(), bad_score
    else:
        if gol.get_value('IS_PRINT'):
            print('The present error rate is {}'.format(bad_score))
        return Matrix_Sim_Modification(M_Sim, 0, best_parameters['scale_deta'], best_parameters['shift_x'], best_parameters['shift_y']), bad_score

def process_cell(img, cam, M_Sim, shift_y, scale, threshold_err, is_crop, x_deta):
    # global parameters # = gol.get_value("parameters")
    bad_score = 1.0
    best_parameters = {'shift_x':x_deta, 'shift_y':0, 'scale_deta': 0, 'error': bad_score}
    for y_deta in shift_y:
        for scale_deta in scale:
            estimator = ImgCamRegression(M_Sim, x_deta, y_deta, scale_deta)
            score = estimator.predict_Image(img, cam, is_crop=is_crop)
            # print(score, x_deta, y_deta, scale_deta)
            if score < best_parameters['error']:
                best_parameters = {'shift_x':x_deta, 'shift_y':y_deta, 'scale_deta':scale_deta, 'error': score}
            # print(x_deta, y_deta, scale_deta, score)
            if best_parameters['error'] <= threshold_err:
                if gol.get_value('IS_PRINT'):
                    print('Achieve the preset error rate {}.'.format(best_parameters['error']))
                return [best_parameters['shift_x'], best_parameters['shift_y'], best_parameters['scale_deta'], best_parameters['error']]
    return [best_parameters['shift_x'], best_parameters['shift_y'], best_parameters['scale_deta'], best_parameters['error']]

def Pixel_matching_multi(img, cam, M_Sim, shift_max = 50, match_step = 10, threshold_err = 0.1, is_Scaling=False):
    proc_num = gol.get_value('PROC_NUM')
    shift_x = np.arange(-shift_max, shift_max+1, step = match_step)
    shift_y = np.arange(-shift_max, shift_max+1, step = match_step)
    if is_Scaling:
        scale = np.arange(-0.1, 0.11, step = 0.01)
        # scale = [-0.01, -0.005, 0, 0.005, 0.01]
    else:
        scale = [0,]
    # print(M_Sim)
    func = partial(process_cell, img, cam, M_Sim, shift_y, scale, threshold_err, False)

    pool = Pool(proc_num)
    # parameters = pool.map(func, shift_x)
    results = pool.map_async(func, shift_x)
    pool.close()
    # pool.join()
    # raise ValueError
    while not results.ready():
        parameters = results.get()
        parameters = sorted(parameters, key = lambda e : e[3])
        best_parameters = parameters[0]
        if best_parameters[3] <= threshold_err:
            pool.terminate()
            # print(results.ready())
            break

    if gol.get_value('IS_PRINT'):
        print('The present error rate is {}'.format(best_parameters[3]))

    return Matrix_Sim_Modification(M_Sim, 0, best_parameters[2], best_parameters[0], best_parameters[1]), best_parameters[3]

class ImgCamRegression(BaseEstimator, RegressorMixin):
    def __init__(self, M_Sim, shift_x=0, shift_y=0, scale_deta=0):
        self.M_Sim = M_Sim
        self.shift_x = shift_x
        self.shift_y = shift_y
        self.scale_deta = scale_deta

    def fit(self, X, y=None):
        assert (type(self.shift_x) == int)
        assert (type(self.shift_y) == int)
        assert (type(self.scale_deta) == float)
        assert (y == 0)

        return self

    def predict_cv(self, img, cam, is_crop=True):
        # img and cam are both rriginal images after binarisation.
        M_Sim_new = Matrix_Sim_Modification(self.M_Sim, 0, self.scale_deta, self.shift_x, self.shift_y)
        h, w = img.shape[:2]
        warped_img = cv2.warpAffine(img, M_Sim_new, (w, h), flags=cv2.INTER_NEAREST, borderValue=127)
        if is_crop:
            cropped_img, cropped_cam, out_size = crop_imgcam(warped_img, cam, size=min(w, h))
            # print(img.shape, cam.shape)
        else:
            cropped_img, cropped_cam = warped_img, cam
        masked_cam, roi = Get_Mask_ROI(cropped_img, cropped_cam, 127, 127)

        return pixel_dist(cropped_img, masked_cam, roi, is_highlights=False)

    def predict_Image(self, img, cam, is_crop=True):
        # img and cam are both rriginal images after binarisation.
        M_Sim_new = Matrix_Sim_Modification(self.M_Sim, 0, self.scale_deta, self.shift_x, self.shift_y)
        warped_img = img.transform(img.size, Image.AFFINE, Matrix_Sim_cv2image(M_Sim_new), resample=Image.NEAREST, fillcolor=127)
        # warped_img = img.transform(img.size, Image.AFFINE, (1/2,0.866025404,0,-0.866025404,1/2,0), resample=Image.NEAREST, fillcolor=127)
        warped_img = np.asarray(warped_img)
        # if is_crop:
        #     w, h = img.size[:2]
        #     cropped_img, cropped_cam, _ = crop_imgcam(warped_img, cam, size=min(w, h))
        # else:
        #     cropped_img, cropped_cam = warped_img, cam
        w, h = img.size[:2]
        cropped_img, cropped_cam, _ = crop_imgcam(warped_img, cam, size=min(w, h))
        masked_cam, roi = Get_Mask_ROI(cropped_img, cropped_cam, 127, 127)

        return pixel_dist(cropped_img, masked_cam, roi, is_highlights=False)
    
def predict_Image(M_Sim, scale_deta, shift_x, shift_y, img, cam, is_crop=True):
    # img and cam are both rriginal images after binarisation.
    M_Sim_new = Matrix_Sim_Modification(M_Sim, 0, scale_deta, shift_x, shift_y)
    warped_img = img.transform(img.size, Image.AFFINE, Matrix_Sim_cv2image(M_Sim_new), resample=Image.NEAREST, fillcolor=127)
    # warped_img = img.transform(img.size, Image.AFFINE, (1/2,0.866025404,0,-0.866025404,1/2,0), resample=Image.NEAREST, fillcolor=127)
    warped_img = np.asarray(warped_img)
    if is_crop:
        cropped_img, cropped_cam, out_size = crop_imgcam(warped_img, cam, size=img.size[0]/2)
    else:
        cropped_img, cropped_cam, out_size = crop_imgcam(warped_img, cam, size=img.size[0])
    masked_cam, roi = Get_Mask_ROI(cropped_img, cropped_cam, 127, 127)

    return pixel_dist(cropped_img, masked_cam, roi, is_highlights=False)

def copper_centered(img_bin, method = 'max'):
    center_y = img_bin.shape[0]/2
    center_x = img_bin.shape[1]/2
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (50, 50))
    thresh_img = cv2.morphologyEx(img_bin, cv2.MORPH_CLOSE, kernel)
    contours, cnt = cv2.findContours(thresh_img.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) == 1:
        M = cv2.moments(contours[0])
        contour_x = int(M["m10"] / M["m00"])
        contour_y = int(M["m01"] / M["m00"])
    else:
        if gol.get_value('IS_PRINT'):
            print('More than one contour in the image!')
        if method == 'max':
            contours.sort(key=lambda c: cv2.contourArea(c), reverse=True)
            M = cv2.moments(contours[0])
            contour_x = int(M["m10"] / M["m00"])
            contour_y = int(M["m01"] / M["m00"])
        elif method == 'ave':
            contour_xs = []
            contour_ys = []
            for idx, contour in enumerate(contours):
                if cv2.contourArea(contour) > 50:
                    M = cv2.moments(contour)
                    contour_xs.append(int(M["m10"] / M["m00"]))
                    contour_ys.append(int(M["m01"] / M["m00"]))
            contour_x = np.mean(contour_xs)
            contour_y = np.mean(contour_ys)
    return thresh_img, Matrix_Sim_Generation(0, 1, center_x-contour_x, center_y-contour_y), 0
