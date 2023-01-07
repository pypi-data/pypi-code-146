import os
import cv2
import argparse
from PIL import Image
from functools import partial
from vspscripts.alignment.utils import gol
from vspscripts.alignment.utils.utils import Sim_Trans, Crop_Trans, findAllFile
from vspscripts.alignment.utils.mat import Matrix_Sim_Generation, Matrix_Sim_Scaled
from vspscripts.alignment.matching.matching import copper_centered, Pixel_matching_multi
from vspscripts.alignment.utils.img import binarize_imgcam, Get_Mask_ROI, crop_imgcam_ori, scaling_imgcam

gol._init()
gol.set_value('IS_PRINT', False)
gol.set_value('EXTEND_VALUE', 127)
gol.set_value('IS_MULTI_PROC', True)
gol.set_value('PROC_NUM', 9)

def parse_args():
    parser = argparse.ArgumentParser('parser for alignment')
    parser.add_argument("--data_path", type=str, default='../samples/gp4s___7670_14_11_-1.jpg')
    parser.add_argument("--output_dir", type=str, default='../outputs')
    parser.add_argument("--out_size", type=int, default=600)
    return parser.parse_args()

def ICpair_Aligning(img_path, cam_path, output_dir=None, out_size=600, is_masked=True):
    img_ori = cv2.imread(img_path)
    cam_ori = cv2.imread(cam_path)
    img, img_bin, cam, cam_bin = binarize_imgcam(img_ori, cam_ori, 'HSV_OTSU') # HSV_BINARY, HSV_OTSU

    Extd_value = gol.get_value('EXTEND_VALUE')
    if cam_ori.shape[0]<img_ori.shape[0] or cam_ori.shape[1]<img_ori.shape[1]:
        scale = min(img_ori.shape[0]/cam_ori.shape[0], img_ori.shape[1]/cam_ori.shape[1])
        cam_ori = cv2.resize(cam_ori, (int(scale*cam_ori.shape[1]), int(scale*cam_ori.shape[0])), interpolation=cv2.INTER_LINEAR)

        height_expand = img_ori.shape[0]-cam_ori.shape[0]
        width_expand = img_ori.shape[1]-cam_ori.shape[1]
        cam_ori = cv2.copyMakeBorder(cam_ori, int(height_expand/2), height_expand-int(height_expand/2), int(width_expand/2), width_expand-int(width_expand/2), cv2.BORDER_CONSTANT,value=[Extd_value, Extd_value, Extd_value])

    h, w = img_ori.shape[:2]
    if type(cam_bin) == bool:
        if cam_bin:
            if gol.get_value('IS_PRINT'):
                print("This case is full copper!")
            _, M_Sim, score = copper_centered(cv2.bitwise_not(img_bin, img_bin), method = 'max')
        else:
            if gol.get_value('IS_PRINT'):
                print("This case is no copper!")
            _, M_Sim, score = copper_centered(img_bin, method = 'max')
    else:
        if gol.get_value('IS_MULTI_PROC'):
            Pixel_matching = Pixel_matching_multi
            img_bin = Image.fromarray(img_bin)

        M_Sim = Matrix_Sim_Generation(0, 1, 0, 0)
        img_scaled_1, cam_scaled_1, scale_1 = scaling_imgcam(img_bin, cam_bin, 100)
        M_Sim_p1, score = Pixel_matching(img_scaled_1, cam_scaled_1, M_Sim, shift_max = 50, match_step = 5, threshold_err = 0, is_Scaling=True)
        img_scaled_2, cam_scaled_2, scale = scaling_imgcam(img_bin, cam_bin, 300)
        M_Sim, score = Pixel_matching(img_scaled_2, cam_scaled_2, Matrix_Sim_Scaled(M_Sim_p1, scale_1/scale), shift_max = 5, match_step = 1, threshold_err = 0)

        if gol.get_value('IS_PRINT'):
            print('The matching accuracy is {}'.format(1-score))
    M_Sim = Matrix_Sim_Scaled(M_Sim, scale)
    warped_img = cv2.warpAffine(img_ori, M_Sim, (w, h), flags=cv2.INTER_NEAREST, borderValue=(Extd_value, Extd_value, Extd_value))
    warped_mask = cv2.warpAffine(img_ori, M_Sim, (w, h), flags=cv2.INTER_NEAREST, borderValue=(0, 0, 0))
    masked_img, out_img, out_cam, out_size = crop_imgcam_ori(warped_mask, warped_img, cam_ori, size=out_size, is_expand = True)
    
    if is_masked:
        out_cam, _ = Get_Mask_ROI(masked_img, out_cam, 0, Extd_value)
    if output_dir:
        if not os.path.exists(output_dir):
                os.makedirs(output_dir)
    else:
        output_dir = os.path.dirname(img_path)
    img_new_name = os.path.basename(img_path).replace('.jpg', '_aligned.jpg')
    cam_new_name = os.path.basename(cam_path).replace('.png', '_aligned.png')
    cv2.imwrite(os.path.join(output_dir, img_new_name), out_img)
    cv2.imwrite(os.path.join(output_dir, cam_new_name), out_cam)

    return out_img, out_cam, out_size, M_Sim, 1-score


if __name__ == "__main__":
    args = parse_args()
    img_path = args.data_path
    cam_path = img_path.replace('.jpg', '.png')
    # ICpair_Aligning(img_path, cam_path, args.output_dir, args.out_size, is_masked=True)
    if gol.get_value('IS_PRINT'):
        from timeit import timeit
        func = partial(ICpair_Aligning, img_path, cam_path, args.output_dir, args.out_size)
        print('time Usage {} s'.format(timeit(func, number = 1)))
    else:
        _, _, _, M_Sim, _ = ICpair_Aligning(img_path, cam_path, args.output_dir, args.out_size)
        print(M_Sim)
