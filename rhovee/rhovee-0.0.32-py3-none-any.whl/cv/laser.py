import numpy as np
import cv2
import matplotlib.pyplot as plt


def draw_centered_line(img_size, angle, line_width):
    # draw a line that goes through the center of the image
    img = np.zeros(img_size)
    center = np.array(img_size) / 2
    x1 = 0
    y1 = int(center[1] - np.tan(angle) * center[0])
    x2 = img.shape[1]
    y2 = int(center[1] + np.tan(angle) * (img.shape[1] - center[0]))
    cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 5)
    return img

def weighted_mean_row_index(img, threshold=20, verbose=0):
    assert img.ndim == 2
    img = img.copy()
    img = np.where(img > threshold, img, 0).astype(np.uint8)
    if verbose:
        cv2.imshow('img', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    # find index weighted mean
    indeces = np.arange(img.shape[1])
    mean = np.sum(indeces * img, axis=1) / np.sum(img, axis=1)
    return mean

def row_list_to_points(row_list):
    ys = np.arange(len(row_list))
    xs = row_list
    return np.vstack([xs, ys, np.ones(len(xs))]).T

def draw_homg_line(img, l):
    assert l.shape[0] == 3
    if np.isnan(l).any():
        return img
    out = img.copy()
    x1 = 0
    y1 = int(-l[2] / l[1])
    x2 = img.shape[1]
    y2 = int(-(l[2] + l[0] * x2) / l[1])
    cv2.line(out, (x1, y1), (x2, y2), (255, 0, 0), 1)
    return out

def fit_homogenous_line(points):
   assert points.shape[1] == 3
   # find m,c using least squares
   points = np.asarray(points)
   n, _ = points.shape
   mean_x = np.mean(points[:,0])
   mean_y = np.mean(points[:,1])
   sum_xy = sum([points[i,0]*points[i,1] for i in range(n)])
   sum_x = sum([points[i,0] for i in range(n)])
   sum_y = sum([points[i,1] for i in range(n)])
   sum_x2 = sum([points[i,0]**2 for i in range(n)])
   slope = (n*sum_xy - sum_x*sum_y) / (n*sum_x2 - sum_x**2)
   intercept = mean_y - slope*mean_x
   return np.array([-slope, 1, -intercept])

def overlap_gray_imgs_rgb(img1, img2):
    assert img1.shape == img2.shape
    rgb_img = np.zeros(img1.shape + (3,))
    rgb_img[..., 0] = img1
    rgb_img[..., 2] = img2
    return rgb_img.astype(np.uint8)





def get_laser_line_as_homg(img, threshold, verbose=0):
    if img.ndim == 3:
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    mean = weighted_mean_row_index(img, threshold, verbose)
    points = row_list_to_points(mean)
    if len(points) < 2:
        print("Not enough points to fit line")
        raise ValueError
    l = fit_homogenous_line(points)
    if verbose:
        zero_img = np.zeros(img.shape)
        homg_line_img = draw_homg_line(zero_img, l)
        overlap = overlap_gray_imgs_rgb(img, homg_line_img)
        cv2.imshow('overlap', overlap)
        cv2.waitKey(0)
    return l

def get_essential_matrix(R_12, t_12):
    T = np.eye(4)
    T[:3,:3] = R_12
    T[:3,3] = t_12
    T_inv = np.linalg.inv(T)
    R_21 = T_inv[:3,:3]
    t_21 = T_inv[:3,3]
    E = cross_prod_mat(t_21)@(R_21)
    return E

def homg_points_to_plucker_line(pt1, pt2):
    pt1 = pt1.squeeze()
    pt2 = pt2.squeeze()
    if pt1.shape[0] == 3:
        pt1 = np.append(pt1, 1)
    if pt2.shape[0] == 3:
        pt2 = np.append(pt2, 1)
    l = pt1[3]*pt2[:3] - pt2[3]*pt1[:3]
    l_dash = np.cross(pt1[:3],pt2[:3])
    return l, l_dash

def intersect_plucker_lines(l1, l1_dash, l2, l2_dash):
    n = np.cross(l1, l2)
    v = np.zeros(4)
    v[:3] = np.cross(n, l1)
    v[3] = np.dot(n, l1_dash)
    x = np.zeros(4)
    x[:3] = -v[3]*l2+np.cross(v[:3], l2_dash)
    x[3] = np.dot(v[:3], l2)
    x = x / x[3]
    return x[:3]

def cross_prod_mat(v):
    return np.array([[0, -v[2], v[1]],
                     [v[2], 0, -v[0]],
                     [-v[1], v[0], 0]])

def triangulate_laser_lines(l_img, r_img, thresh, R12, t12, lK, ldc, rK, rdc, verbose=0):
    print("Triangulating laser lines")
    if l_img.ndim == 3:
        l_img = cv2.cvtColor(l_img, cv2.COLOR_RGB2GRAY)
    if r_img.ndim == 3:
        r_img = cv2.cvtColor(r_img, cv2.COLOR_RGB2GRAY)
    l_img = cv2.undistort(l_img, lK, ldc)
    r_img = cv2.undistort(r_img, rK, rdc)
    l_homg = get_laser_line_as_homg(l_img, thresh, verbose)
    r_homg = get_laser_line_as_homg(r_img, thresh, verbose)
    l_mean_rows = weighted_mean_row_index(l_img, thresh)
    l_points = row_list_to_points(l_mean_rows)
    E = get_essential_matrix(R12, t12)
    F = np.linalg.inv(rK).T @ E @ np.linalg.inv(lK)
    all_pts = []
    for idx,point in enumerate(l_points):
        line = F @ point
        intersect_r = np.cross(r_homg, line)
        intersect_r = intersect_r / intersect_r[2]
        norm_r = np.linalg.inv(rK) @ intersect_r
        norm_r = norm_r / norm_r[2]
        norm_l = R12@norm_r + t12
        line_r, line_r_dash = homg_points_to_plucker_line(norm_l, t12)
        line_l = np.linalg.inv(lK) @ point
        line_l_dash = np.zeros(3)
        intersect = intersect_plucker_lines(line_l, line_l_dash, line_r, line_r_dash)
        if np.isnan(intersect).any() or np.isinf(intersect).any():
            print("Found nan or inf in triangulation, continuing")
            continue
        all_pts.append(intersect)
    return np.array(all_pts)

def get_proj_planar_homography(R12, t12, u1, K1, K2):
    d = u1[-1]
    n = u1[:3]
    T = np.eye(4)
    T[:3,:3] = R12
    T[:3,3] = t12
    T_inv = np.linalg.inv(T)
    R_inv = T_inv[:3,:3]
    t_inv = T_inv[:3,3]
    H = R_inv - (1/d)*np.outer(t_inv,n)
    H = K2@H@np.linalg.inv(K1)
    H12 = np.linalg.inv(H)
    return H12

def apply_planar_homography(H12, undist_right_img):
    undist_right_img = cv2.warpPerspective(undist_right_img, H12, (undist_right_img.shape[1], undist_right_img.shape[0]))
    return undist_right_img







if __name__ == '__main__':
    img_path = "/Users/olaals/projects/laser-charuco-calib/stereo-cam-laser-calib/laser-images/test-images/left/img00.png"
    #img = draw_centered_line((500, 500), np.pi / 2.1, 5)
    img = cv2.imread(img_path)
    # blur img
    # cam mat with focal len 500 and center 250,250
    K = np.array([[500, 0, 250], [0, 500, 250], [0, 0, 1]])
    dc = np.array([0, 0, 0, 0])
    # rot mat with -20 deg rot around y axis
    R = np.array([[np.cos(-np.pi/9), 0, np.sin(-np.pi/9)], [0, 1, 0], [-np.sin(-np.pi/9), 0, np.cos(-np.pi/9)]])
    t = np.array([0.5, 0, 0.2])
    pts = triangulate_laser_lines(img, img, 50, R, t, K, dc, K, dc, 1)





