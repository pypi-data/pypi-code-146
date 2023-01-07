import os
import cv2
import math
import time
import argparse
import numpy as np
from PIL import Image
import matplotlib.pylab as plt
import sys
# sys.path.append('../')
from vspscripts.alignment.utils import gol
from vspscripts.alignment.utils.img import binarize_imgcam, Get_Mask_ROI, crop_imgcam_ori, scaling_imgcam
from vspscripts.alignment.utils.mat import Matrix_Sim_Decomposition, Matrix_Sim_Generation, Matrix_Sim_Scaled
from vspscripts.alignment.matching.matching import Feature_matching, Pixel_matching, copper_centered, Pixel_matching_multi

def parse_args():
    parser = argparse.ArgumentParser('parser for alignment')
    parser.add_argument("--data_path", type=str, default='../samples/GP2S___977_11.jpg')
    parser.add_argument("--out_size", type=int, default=600)
    parser.add_argument("--reversal", '-r', action='store_true')
    return parser.parse_args()

if __name__ == "__main__":
    img_format = '.jpg' # '.png'
    cam_format = '.png' # '_1.png'
    # img_format = '.png' # '.png'
    # cam_format = '_1.png' # '_1.png'

    gol._init()
    gol.set_value('IS_PRINT', True)
    gol.set_value('EXTEND_VALUE', 127)
    gol.set_value('IS_MULTI_PROC', True)
    gol.set_value('PROC_NUM', 4) # 4 and 5 is perfect
    args = parse_args()

    T0 = time.time()
    Extd_value = gol.get_value('EXTEND_VALUE')
    img_path = args.data_path # gp4s___7663_18_16_5 l1___1992_10_521_-1
    cam_path = img_path.replace(img_format, cam_format) # GP2S___977_11

    img_ori = cv2.imread(img_path)
    cam_ori = cv2.imread(cam_path)
    
    img, img_bin, cam, cam_bin = binarize_imgcam(img_ori, cam_ori, 'HSV_OTSU') # HSV_BINARY, HSV_OTSU

    if cam_ori.shape[0]<img_ori.shape[0] or cam_ori.shape[1]<img_ori.shape[1]:
        scale = min(img_ori.shape[0]/cam_ori.shape[0], img_ori.shape[1]/cam_ori.shape[1])
        cam_ori = cv2.resize(cam_ori, (int(scale*cam_ori.shape[1]), int(scale*cam_ori.shape[0])), interpolation=cv2.INTER_CUBIC)

        height_expand = img_ori.shape[0]-cam_ori.shape[0]
        width_expand = img_ori.shape[1]-cam_ori.shape[1]
        cam_ori = cv2.copyMakeBorder(cam_ori, int(height_expand/2), height_expand-int(height_expand/2), int(width_expand/2), width_expand-int(width_expand/2), cv2.BORDER_CONSTANT,value=[Extd_value, Extd_value, Extd_value])
    # img = cv2.cvtColor(img_ori, cv2.COLOR_BGR2GRAY)
    # cam = cv2.cvtColor(cam_ori, cv2.COLOR_BGR2GRAY)

    if args.reversal:
        cv2.bitwise_not(cam_bin, cam_bin)
    h, w = img_ori.shape[:2]
    if type(cam_bin) == bool:
        if cam_bin:
            if gol.get_value('IS_PRINT'):
                print("This case is full copper!")
            thresh_img, M_Sim, _ = copper_centered(cv2.bitwise_not(img_bin, img_bin), method = 'max')
        else:
            if gol.get_value('IS_PRINT'):
                print("This case is no copper!")
            thresh_img, M_Sim, _ = copper_centered(img_bin, method = 'max')
        warped_img = cv2.warpAffine(img_ori, M_Sim, (w, h), flags=cv2.INTER_NEAREST, borderValue=(Extd_value, Extd_value, Extd_value))
        warped_mask = cv2.warpAffine(img_ori, M_Sim, (w, h), flags=cv2.INTER_NEAREST, borderValue=(0, 0, 0))
        masked_img, cropped_img, cropped_cam, out_size = crop_imgcam_ori(warped_mask, warped_img, cam_ori, size=args.out_size, is_expand=True)
        masked_cam, _ = Get_Mask_ROI(masked_img, cropped_cam, 0, Extd_value)
        if not os.path.exists('./tmp'):
            os.makedirs('./tmp')
        cv2.imwrite('./tmp/img.jpg', cropped_img)
        cv2.imwrite('./tmp/cam.png', cropped_cam)
        cv2.imwrite('./tmp/masked_cam.png', masked_cam)

        img_rgb = cv2.cvtColor(img_ori, cv2.COLOR_BGR2RGB)
        cam_rgb = cv2.cvtColor(cam_ori, cv2.COLOR_BGR2RGB)
        warped_img = cv2.cvtColor(warped_img, cv2.COLOR_BGR2RGB)
        cropped_img_rgb = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2RGB)
        cropped_cam_rgb = cv2.cvtColor(cropped_cam, cv2.COLOR_BGR2RGB)

        fig1=plt.figure('Alignment')
        plt.subplot(231),plt.imshow(img_rgb),plt.title("Original img")
        plt.subplot(232),plt.imshow(thresh_img, cmap ='gray'),plt.title("Binarize img")
        plt.subplot(233),plt.imshow(cropped_img_rgb),plt.title("Aligned img")
        plt.subplot(234),plt.imshow(cam_rgb),plt.title("Original cam")
        if cam_bin:
            plt.subplot(235),plt.imshow(cam_rgb, cmap ='gray'),plt.title("Binarize cam")
        else:
            plt.subplot(235),plt.imshow(np.zeros(cam_rgb.shape), cmap ='gray'),plt.title("Binarize cam")
        plt.subplot(236),plt.imshow(cropped_cam_rgb),plt.title("Cropped cam")
        plt.show()
    else:
        T1 = time.time()
        if gol.get_value('IS_MULTI_PROC'):
            Pixel_matching = Pixel_matching_multi
            img_bin = Image.fromarray(img_bin)
        # M_Sim_f = Feature_matching(img, cam, show_matches = True)
        if gol.get_value('IS_PRINT'):
            print("This case is difficult!")
        M_Sim = Matrix_Sim_Generation(0, 1, 0, 0)
        T2 = time.time()
        img_scaled_1, cam_scaled_1, scale_1 = scaling_imgcam(img_bin, cam_bin, 100)
        M_Sim_p1, score = Pixel_matching(img_scaled_1, cam_scaled_1, M_Sim, shift_max = 50, match_step = 5, threshold_err = 0, is_Scaling=True)
        T3 = time.time()
        img_scaled_2, cam_scaled_2, scale_2 = scaling_imgcam(img_bin, cam_bin, 300)
        M_Sim_p2, score = Pixel_matching(img_scaled_2, cam_scaled_2, Matrix_Sim_Scaled(M_Sim_p1, scale_1/scale_2), shift_max = 5, match_step = 1, threshold_err = 0)
        T4 = time.time()
        M_Sim_p3 = M_Sim_p2# score = Pixel_matching(img_bin, cam_bin, M_Sim_p2, shift_max = 5, match_step = 1, threshold_err = 0.05, is_Scaling=True)
        T8 = time.time()

        if gol.get_value('IS_PRINT'):
            print(Matrix_Sim_Scaled(M_Sim_p3, scale_2))
            print('The matching accuracy is {}'.format(1-score))

        T9 = time.time()
        # M_Sim = Matrix_Sim_Generation(-math.pi/6, 1, 100, 100)
        warped_img_f = warped_img_p1 = cv2.warpAffine(img_ori, Matrix_Sim_Scaled(M_Sim_p1, scale_1), (w, h), flags=cv2.INTER_NEAREST, borderValue=(Extd_value, Extd_value, Extd_value))
        warped_img_p2 = cv2.warpAffine(img_ori, Matrix_Sim_Scaled(M_Sim_p2, scale_2), (w, h), flags=cv2.INTER_NEAREST, borderValue=(Extd_value, Extd_value, Extd_value))
        warped_img_p3 = cv2.warpAffine(img_ori, Matrix_Sim_Scaled(M_Sim_p3, scale_2), (w, h), flags=cv2.INTER_NEAREST, borderValue=(Extd_value, Extd_value, Extd_value))
        warped_mask = cv2.warpAffine(img_ori, Matrix_Sim_Scaled(M_Sim_p3, scale_2), (w, h), flags=cv2.INTER_NEAREST, borderValue=(0, 0, 0))
        # cv2.imwrite('./tmp/warp.jpg', warped_img_p3)
        masked_img, cropped_img, cropped_cam, out_size = crop_imgcam_ori(warped_mask, warped_img_p3, cam_ori, size=args.out_size, is_expand=True)
        masked_cam, _ = Get_Mask_ROI(masked_img, cropped_cam, 0, Extd_value)

        if not os.path.exists('./tmp'):
            os.makedirs('./tmp')
        cv2.imwrite('./tmp/img.jpg', cropped_img)
        cv2.imwrite('./tmp/cam.png', cropped_cam)
        cv2.imwrite('./tmp/masked_cam.png', masked_cam)

        T10 = time.time()
        print('程序运行时间:%s毫秒' % ((T9 - T0)*1000))
        img_rgb = cv2.cvtColor(img_ori, cv2.COLOR_BGR2RGB)
        cam_rgb = cv2.cvtColor(cam_ori, cv2.COLOR_BGR2RGB)
        # img_scaled_rgb = cv2.cvtColor(img_scaled, cv2.COLOR_BGR2RGB)
        # cam_scaled_rgb = cv2.cvtColor(cam_scaled, cv2.COLOR_BGR2RGB)
        warped_img_f_rgb = cv2.cvtColor(warped_img_f, cv2.COLOR_BGR2RGB)
        warped_img_p1_rgb = cv2.cvtColor(warped_img_p1, cv2.COLOR_BGR2RGB)
        warped_img_p2_rgb = cv2.cvtColor(warped_img_p2, cv2.COLOR_BGR2RGB)
        warped_img_p3_rgb = cv2.cvtColor(warped_img_p3, cv2.COLOR_BGR2RGB)
        cropped_img_rgb = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2RGB)
        cropped_cam_rgb = cv2.cvtColor(cropped_cam, cv2.COLOR_BGR2RGB)

        # titles = ['Original img', 'Warped img', 'Original cam', 'Cropped cam']
        # images = [img, warped_img, cam, cropped_cam]

        fig1=plt.figure('Alignment')
        plt.subplot(241),plt.imshow(img_rgb),plt.title("Original img")
        plt.subplot(242),plt.imshow(img_scaled_1, cmap ='gray'),plt.title("Scaled_1 img")
        plt.subplot(243),plt.imshow(img_scaled_2, cmap ='gray'),plt.title("Scaled_2 img")
        plt.subplot(244),plt.imshow(cropped_img_rgb),plt.title("Aligned img")
        plt.subplot(245),plt.imshow(cam_rgb),plt.title("Original cam")
        plt.subplot(246),plt.imshow(cam_scaled_1, cmap ='gray'),plt.title("Scaled_1 cam")
        plt.subplot(247),plt.imshow(cam_scaled_2, cmap ='gray'),plt.title("Scaled_2 cam")
        plt.subplot(248),plt.imshow(cropped_cam_rgb),plt.title("Cropped cam")
        plt.savefig("./tmp/Alignment.jpg")
        # plt.show()

        fig2=plt.figure('Matching img')
        plt.subplot(231),plt.imshow(img_rgb),plt.title("Original img")
        plt.subplot(232),plt.imshow(warped_img_f_rgb),plt.title("Feature matching img")
        plt.subplot(233),plt.imshow(warped_img_p1_rgb),plt.title("Pixel matching img:1")
        plt.subplot(234),plt.imshow(cam_rgb),plt.title("Original cam")
        plt.subplot(235),plt.imshow(warped_img_p2_rgb),plt.title("Pixel matching img:2")
        plt.subplot(236),plt.imshow(warped_img_p3_rgb),plt.title("Pixel matching img:3")
        plt.savefig("./tmp/Matching_img.jpg")
        plt.show()
