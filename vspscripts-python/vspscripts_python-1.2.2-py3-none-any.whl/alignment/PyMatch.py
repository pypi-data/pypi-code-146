import os
import cv2
import argparse
import numpy as np
from PIL import Image
from logging import warning
from functools import partial
from vspscripts.alignment.utils import gol
from vspscripts.alignment.utils.mat import Matrix_Sim_Generation
from vspscripts.alignment.utils.img import binarize_imgcam, crop_cam

gol._init()
gol.set_value('IS_PRINT', False)
gol.set_value('DEBUG', False)

def parse_args():
    parser = argparse.ArgumentParser('parser for matching')
    parser.add_argument("--data_path", type=str, default='./samples/8365/3_4.jpg')
    parser.add_argument("--output_dir", type=str, default=None)
    parser.add_argument("--out_size", type=int, default=600)
    return parser.parse_args()

def ICpair_Matching(img,
                    cam,
                    output_dir=None,
                    out_size=600,
                    scaling=0.5,
                    is_bin=False,
                    method=cv2.TM_CCOEFF_NORMED):
    img_ori = cv2.imread(img) if isinstance(img, str) else cv2.cvtColor(np.array(img),cv2.COLOR_RGB2BGR)
    cam_ori = cv2.imread(cam) if isinstance(cam, str) else cv2.cvtColor(np.array(cam),cv2.COLOR_RGB2BGR)
    img_path = img if isinstance(img, str) else None
    cam_path = cam if isinstance(cam, str) else None
    
    if scaling != 1.0:
        img_resize = cv2.resize(img_ori, None, fx=scaling, fy=scaling)
        cam_resize = cv2.resize(cam_ori, None, fx=scaling, fy=scaling)
    else:
        img_resize = img_ori
        cam_resize = cam_ori
    tem_size = int(out_size * scaling)

    if cam_resize.shape[:2] < (tem_size,)*2 or img_resize.shape[:2] < (tem_size,)*2:
        raise ValueError('The size of the image is too small to be processed.')
    if is_bin:
        img_gray, img_bin, cam_r, cam_bin = binarize_imgcam(img_resize, cam_resize, 'HSV_OTSU') # HSV_BINARY, HSV_OTSU
        cam = cam_bin
        img = img_bin
    else:
        img_gray, _, cam_r, _ = binarize_imgcam(img_resize, cam_resize, 'ONLY_GRAY') # HSV_BINARY, HSV_OTSU
        cam = cam_r
        img = img_gray
    cam_gray = cv2.cvtColor(cam_ori, cv2.COLOR_BGR2GRAY)
    cam_cropped, _ = crop_cam(cam_ori, out_size)
    cam_gray_cropped, _ = crop_cam(cam_gray, out_size)
    cam_templ, _ = crop_cam(cam, tem_size)

    result = cv2.matchTemplate(img, cam_templ, method)
    if method==cv2.TM_CCOEFF_NORMED:
        result = np.absolute(result)
    threshold = np.max(result) - 0.01
    result_map = result>=threshold
    c = np.sum(result_map)
    if c > 200 and method==cv2.TM_CCOEFF_NORMED:
        if gol.get_value('IS_PRINT'):
            print('The number of pixels that meet the threshold is too large, please check the image and camera.')
        expand = int(out_size/2 * scaling)
        cam_templ, _ = crop_cam(cam, tem_size+2*expand)
        result = cv2.matchTemplate(img, cam_templ, method)
        result = np.absolute(result)
        max = np.max(result)
        threshold = max - 0.01
        result_map = result>=threshold
        c = np.sum(result_map)
        if c > 500 or max < 0.5:
            warning('Maybe the ICpair_Matching of {} and {} is fault!'.format('img:'+str(img_path), 'cam:'+str(cam_path)))
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        if method == cv2.TM_SQDIFF_NORMED:   # 如果是标准平方差匹配取最小值位置
            left_top = min_loc + np.array([expand, expand])
            score = min_val
        else:
            left_top = max_loc + np.array([expand, expand])
            score = max_val
    else:
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        if method == cv2.TM_SQDIFF_NORMED:   # 如果是标准平方差匹配取最小值位置
            left_top = min_loc
            score = min_val
        else:
            left_top = max_loc
            score = max_val
    left_top = tuple([int(x*(1.0/scaling)) for x in left_top])
    right_bottom = (left_top[0] + out_size, left_top[1] + out_size)  # 加上宽高
    img_cropped = img_ori[left_top[1]:right_bottom[1], left_top[0]:right_bottom[0]]
    if gol.get_value('DEBUG'):
        cv2.imwrite('./temp/cam_templ.jpg', cam_templ)
        cv2.imwrite('./temp/img_ori.jpg', img_ori)
        cv2.imwrite('./temp/cam_ori.jpg', cam_ori)
        cv2.imwrite('./temp/img_gray.jpg', img_gray)
        cv2.imwrite('./temp/cam_gray.jpg', cam_gray)
        if is_bin:
            cv2.imwrite('./temp/img_bin.jpg', img_bin)
            cv2.imwrite('./temp/cam_bin.jpg', cam_bin)
        cv2.imwrite('./temp/img_cropped.jpg', img_cropped)
        cv2.imwrite('./temp/cam_cropped.jpg', cam_cropped)
        # 匹配到最佳位置画小矩形
        cv2.rectangle(img=img_ori, pt1=left_top, pt2=right_bottom, color=(0, 0, 255), thickness=2)
        cv2.imwrite('./temp/match-{}.jpg'.format(str(method)), img_ori)

    M_Sim = Matrix_Sim_Generation(0, 1, (img_ori.shape[1]/2.0)-((right_bottom[0]+left_top[0])/2.0), \
        (img_ori.shape[0]/2.0)-((right_bottom[1]+left_top[1])/2.0))

    if gol.get_value('IS_PRINT'):
        print('The matching accuracy is {}'.format(score))

    if output_dir:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
    elif isinstance(img_path, str):
        output_dir = os.path.dirname(img_path)
    else:
        output_dir = None

    if isinstance(img_path, str) and isinstance(cam_path, str):
        img_new_name = os.path.basename(img_path).replace('.jpg', '_matched.jpg')
        cam_new_name = os.path.basename(cam_path).replace('.png', '_matched.png')
        cv2.imwrite(os.path.join(output_dir, img_new_name), img_cropped)
        cv2.imwrite(os.path.join(output_dir, cam_new_name), cam_cropped)
    return img_cropped, cam_gray_cropped, out_size, M_Sim, score, (left_top, right_bottom)
    # else:
    #     return Image.fromarray(cv2.cvtColor(img_cropped, cv2.COLOR_BGR2RGB)), Image.fromarray(cam_gray_cropped), out_size, M_Sim, score

if __name__ == "__main__":
    args = parse_args()
    img_path = args.data_path
    cam_path = img_path.replace('.jpg', '.png')
    # alignment_imgcam(img_path, cam_path, args.output_dir, args.out_size, is_masked=True)
    if gol.get_value('IS_PRINT'):
        from timeit import timeit
        func = partial(ICpair_Matching, img_path, cam_path, args.output_dir, args.out_size, scaling=0.5)
        print('time Usage {} s'.format(timeit(func, number = 1)))
    # TM_SQDIFF, TM_SQDIFF_NORMED, TM_CCORR, TM_CCORR_NORMED, TM_CCOEFF, TM_CCOEFF_NORMED
    else:
        _, _, _, M_Sim, score, _ = ICpair_Matching(img_path, cam_path, args.output_dir, args.out_size, scaling=0.5)
        print(M_Sim, score)
