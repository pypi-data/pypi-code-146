import cv2
import os
import numpy as np
from cv2 import aruco
import json
import matplotlib.pyplot as plt

def calibrate_camera(image_paths, board, req_markers=10, verbose=0):
    all_corners = []
    all_ids = []
    for im_path in image_paths:
        im_col = cv2.imread(im_path)
        if len(im_col.shape) == 3:
            gray = cv2.cvtColor(im_col, cv2.COLOR_BGR2GRAY)
        else:
            gray = im_col
        corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, board.dictionary)
        if len(corners) > 0 and len(corners) >= req_markers:
            ret, charuco_corners, charuco_ids = aruco.interpolateCornersCharuco(corners, ids, gray, board)
            if verbose > 0:
                im_col = aruco.drawDetectedCornersCharuco(im_col, charuco_corners, charuco_ids)
                cv2.imshow('calibrate_camera: corners', im_col)
                cv2.waitKey(0)
            if ret is not None:
                all_corners.append(charuco_corners)
                all_ids.append(charuco_ids)
    print("Found {} images with at least {} markers".format(len(all_corners), req_markers))
    if len(all_corners) > 0:
        print("Calibrating camera...")
        rms, camera_matrix, dist_coeffs, rvecs, tvecs = aruco.calibrateCameraCharuco(all_corners, all_ids, board, gray.shape, None, None)
        print("Camera calibration complete.")
        return camera_matrix, dist_coeffs, rms
    else:
        print("No images with enough markers found.")
        return None, None, None


def rvec_tvec_to_transf(rvec,tvec):
    R = cv2.Rodrigues(rvec)
    T = np.eye(4)
    T[:3,:3] = R[0]
    T[:3,3] = tvec.squeeze()
    return T

def transf_to_rvec_tvec(T):
    rvec = cv2.Rodrigues(T[:3,:3])[0]
    tvec = T[:3,3]
    return rvec, tvec

def draw_frame_axes(img, K, dist_coeffs, T, size=0.05):
    img = img.copy()
    rvec, tvec = transf_to_rvec_tvec(T)
    cv2.drawFrameAxes(img, K, dist_coeffs, rvec, tvec, size)
    return img

def get_charuco_cb_pose(img, board, K, dist_coeffs, req_det_markers=6):
    corners, ids, rejectedImgPoints = aruco.detectMarkers(img, board.dictionary)
    if ids is not None and len(ids) >= req_det_markers:
        ret, charuco_corners, charuco_ids = aruco.interpolateCornersCharuco(corners, ids, img, board)
        if ret and charuco_corners is not None:
            retval, rvec, tvec = aruco.estimatePoseCharucoBoard(charuco_corners, charuco_ids, board, K, dist_coeffs, np.array([]), np.array([]))
            if retval:
                # convert to transformation matrix
                T = rvec_tvec_to_transf(rvec,tvec)
                return T
    return None

def average_rotation_matrices_svd(Rs):
    avg_R = np.zeros((3,3))
    for R in Rs:
        avg_R = avg_R + R
    avg_R = avg_R / len(Rs)
    U, S, V = np.linalg.svd(avg_R)
    avg_R = U.dot(V)
    return avg_R

def calculate_average_R_dev_angle(avg_R, Rs):
    avg_R_inv = np.linalg.inv(avg_R)
    R_devs = []
    for R in Rs:
        R_dev = avg_R_inv.dot(R)
        # calculate angle
        R_dev_angle = np.arccos((np.trace(R_dev) - 1) / 2)
        R_dev_angle = R_dev_angle * 180 / np.pi
        R_devs.append(R_dev_angle)
    return R_devs


def average_translation_vectors(ts):
    avg_t = np.zeros(3)
    for t in ts:
        avg_t = avg_t + t
    avg_t = avg_t / len(ts)
    return avg_t

def average_transformation_matrices(Ts):
    Rs = []
    ts = []
    for T in Ts:
        Rs.append(T[:3,:3])
        ts.append(T[:3,3])
    avg_R = average_rotation_matrices_svd(Rs)
    avg_t = average_translation_vectors(ts)
    avg_T = np.eye(4)
    avg_T[:3,:3] = avg_R
    avg_T[:3,3] = avg_t
    return avg_T

def calibrate_stereo_charuco(left_image_paths, right_image_paths, lK, ldc, rK, rdc, board, verbose=0):
    left_image_paths.sort()
    right_image_paths.sort()
    l_to_rs = []
    for l_img_path, r_img_path in zip(left_image_paths, right_image_paths):
        l_img = cv2.imread(l_img_path)
        r_img = cv2.imread(r_img_path)
        lT = get_charuco_cb_pose(l_img, board, lK, ldc)
        rT = get_charuco_cb_pose(r_img, board, rK, rdc)
        if lT is not None and rT is not None:
            l_to_r = lT@np.linalg.inv(rT)
            l_to_rs.append(l_to_r)
            if verbose > 0:
                l_img = draw_frame_axes(l_img, lK, ldc, lT)
                r_img = draw_frame_axes(r_img, rK, rdc, rT)
                #cv2.imshow('calibrate_stereo_charuco: left', l_img)
                #cv2.imshow('calibrate_stereo_charuco: right', r_img)
                #cv2.waitKey(0)
    l_to_r_avg = average_transformation_matrices(l_to_rs)
    l_to_r_avg_dev_angle = calculate_average_R_dev_angle(l_to_r_avg[:3,:3], [l_to_r[:3,:3] for l_to_r in l_to_rs])
    print("Average deviation angle: {} deg".format(np.mean(l_to_r_avg_dev_angle)))
    if verbose > 0:
        plt.plot(l_to_r_avg_dev_angle)
        plt.show()
    return l_to_r_avg, np.mean(l_to_r_avg_dev_angle)


def create_board(squares_x, squares_y, cb_sq_width, aruco_sq_width, aruco_dict_str, start_id):
    aruco_dict = aruco.Dictionary_get(getattr(aruco, aruco_dict_str))
    aruco_dict.bytesList=aruco_dict.bytesList[start_id:,:,:]
    board = aruco.CharucoBoard_create(squares_x,squares_y,cb_sq_width,aruco_sq_width,aruco_dict)
    return board

def fit_plane_svd(points):
    assert points.shape[0] >= 3
    assert points.shape[1] == 3
    mean = np.mean(points, axis=0)
    U, S, Vt = np.linalg.svd(points - mean)
    normal = Vt[-1]
    d = -normal.dot(mean)
    if d < 0:
        normal = -normal
        d = -d
    return np.concatenate((normal, [d]))


def read_json(path):
    with open(path, 'r') as f:
        return json.load(f)

def load_charuco_board(json_path):
    board_dict = read_json(json_path)
    squares_x = board_dict['square_x']
    squares_y = board_dict['square_y']
    cb_sq_width = board_dict['cb_sq_width']
    aruco_sq_width = board_dict['aruco_sq_width']
    aruco_dict_str = board_dict['aruco_dict_str']
    start_id = board_dict['start_id']
    return create_board(squares_x, squares_y, cb_sq_width, aruco_sq_width, aruco_dict_str, start_id)

