import os
import cv2
import argparse
from utils import gol
from utils.utils import findAllFile
from utils.ann import Modification_ann
from PyAlignment import ICpair_Aligning

def parse_args():
    parser = argparse.ArgumentParser('parser for alignment')
    parser.add_argument("--data_path", type=str, default='/data/AIVS_2021_06_17')
    parser.add_argument("--output_dir", type=str, default='../outputs')
    parser.add_argument("--out_size", type=int, default=600)

    return parser.parse_args()
    

if __name__ == "__main__":
    img_format = '.jpg'
    cam_format = '.png'
    ann_format = '.json'
    args = parse_args()
    if os.path.isdir(args.data_path):
        for img in findAllFile(args.data_path, img_format):
            cam = img.replace(img_format, cam_format)
            ann = img.replace(img_format, ann_format)
            if not os.path.isfile(img):
                print('{} does not exist!'.format(img))
            elif not os.path.isfile(cam):
                print('{} does not exist!'.format(cam))
            else:
                output_dir = os.path.split(img.replace(os.path.dirname(args.data_path), args.output_dir))[0]
                _, _, out_size, M_Sim, matching_acc = ICpair_Aligning(img, cam, output_dir, out_size=args.out_size)

                Modification_ann(ann, M_Sim, matching_acc, output_dir, out_size)
                # try:
                #     Modification_ann(ann, M_Sim, matching_acc, output_dir, out_size)
                # except NameError:
                #     print('{} does not exist!'.format(ann))
    else:
        img = args.data_path
        cam = img.replace(img_format, cam_format)
        ann = img.replace(img_format, ann_format)
        output_dir = args.output_dir
        _, _, out_size, M_Sim, matching_acc = ICpair_Aligning(img, cam, output_dir, out_size=args.out_size)
        Modification_ann(ann, M_Sim, matching_acc, output_dir, out_size)
        