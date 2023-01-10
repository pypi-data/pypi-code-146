import os
import glob
import shutil

import cv2

def gen_sub_img(img, num_slice):
    if isinstance(img, str):
        img = cv2.imread(img)
    sub_imgs = []
    h, w = img.shape[:2]
    sub_h, sub_w = h // num_slice[0], w // num_slice[1]
    for r in range(num_slice[0]):
        for c in range(num_slice[1]):
            sub_img = img[r * sub_h : (r+1) * sub_h, c * sub_w : (c+1) * sub_w]
            sub_imgs.append(sub_img)
    return sub_imgs


def save_sub_img(save_dir, save_name, images):
    for i, image in enumerate(images):
        save_path = os.path.join(save_dir[i], save_name.replace('.jpg', f'_{i}.jpg'))
        cv2.imwrite(save_path, image)

def get_subdata(data_root, scene, num_slice = [2, 2]):
    scene_dir = os.path.join(data_root, scene)

    # tmp_path = os.path.join(data_root, 'tmp_' + scene)
    slice_raw = num_slice[0]
    slice_col = num_slice[1]

    for i in range(0, slice_raw):
        for j in range(0, slice_col):
            new_dir = os.path.join(data_root, scene + '_' + str(i) + '_' + str(j))
            if os.path.exists(new_dir):
                shutil.rmtree(new_dir)

    new_train_dirs = []
    for i in range(0, slice_raw):
        for j in range(0, slice_col):
            new_dir = os.path.join(data_root, scene + '_' + str(i) + '_' + str(j))
            new_train_dir = os.path.join(new_dir, 'train', 'good')
            os.makedirs(new_train_dir, exist_ok=True)
            new_train_dirs.append(new_train_dir)

    print('On train folder')
    train_dir = os.path.join(scene_dir, 'train', 'good')
    train_img_list = glob.glob(os.path.join(train_dir, '*.jpg'))
    for img_path in train_img_list:
        sub_imgs = gen_sub_img(img_path, num_slice)
        save_sub_img(new_train_dirs, os.path.basename(img_path), sub_imgs)

    # test and ground-truth

    print('On test and ground-truth folder')
    test_dir = os.path.join(scene_dir, 'test')
    gt_dir = os.path.join(scene_dir, 'ground_truth')
    for bad_name in os.listdir(test_dir):
        bad_dir = os.path.join(test_dir, bad_name)
        bad_gt_dir = os.path.join(gt_dir, bad_name)

        new_bad_dirs = []
        new_gt_dirs = []
        for i in range(0, slice_raw):
            for j in range(0, slice_col):
                new_dir = os.path.join(data_root, scene + '_' + str(i) + '_' + str(j))

                new_bad_dir = os.path.join(new_dir, 'test', bad_name)
                os.makedirs(new_bad_dir, exist_ok=True)
                new_bad_dirs.append(new_bad_dir)

                new_gt_dir = os.path.join(new_dir, 'ground_truth', bad_name)
                os.makedirs(new_gt_dir, exist_ok=True)
                new_gt_dirs.append(new_gt_dir)

        for img_path in glob.glob(os.path.join(bad_dir, '*.jpg')):
            print(img_path)
            img_name = os.path.basename(img_path)
            xml_path = os.path.join(bad_gt_dir, img_name.replace('.jpg', '.xml'))
            # if os.path.exists(xml_path):
            #     sub_img, sub_xml_writer = gen_sub_img_and_xml(img_path, xml_path, points)
            #     save_sub_img_and_xml(new_bad_dir, new_gt_dir, sub_img, sub_xml_writer)
            # else:
            sub_imgs = gen_sub_img(img_path, num_slice)
            save_sub_img(new_bad_dirs, img_name, sub_imgs)
    
