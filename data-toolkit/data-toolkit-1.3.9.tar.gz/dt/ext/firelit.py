import streamlit as st
import pandas as pd
import numpy as np
import os    
import matplotlib.pyplot as plt
from PIL import Image
import random
import fire
    
try:
    import cv2
except ModuleNotFoundError:
    import os
    os.system('pip install streamlit pandas fire matplotlib numpy pillow')
    
IM_TYPE = ['fake_A','rec_B','real_B']


def get_full_img_path(file_path, image_name, image_type):
    # file_path = file_path.replace(IM_TYPE[0],f"{image_type}")
    # image_str = image_name.replace(IM_TYPE[1],f"{image_type}")
    if image_type.endswith(".png"):
        image_str = f"{image_name.split('_')[0]}_{image_type}"
    else:
        image_str = f"{image_name.split('_')[0]}_{image_type}.png"
    # file_path = f"{'/'.join(file_path.split('/')[:-1])}/{image_type}"
    # file_path = f"{'/'.join(file_path.split('/')[:-1])}"
    
    full_img_path = f"{file_path}/{image_str}" 
    return full_img_path


def process_one(image_type: str, image_name: str, percentage: float,
                image_root: str, adapted_root: str, im_type: str):
    # TODO: genericise. Currently assumes all file names are the same.
    # target_image = f'{image_root}/{image_type}/{"_".join(image_name.split("_"))}'
    target_image = get_full_img_path(image_root, image_name, im_type[-1])
                                    #  image_type.replace('A','B'))
    
    img = cv2.imread(target_image)[:,:,::-1]
    img = cv2.resize(img, (512,512))

    adapted_img = get_full_img_path(image_root, image_name, image_type)
    # adapted_img = f"{image_root}/{image_name}"
    adapted_img = np.array(Image.open(adapted_img).resize((512,512)))
    # adapted_img = cv2.imread(adapted_img)
    adapted_img.resize((512,512,3))
    # adapted_img = adapted_img[:,:,::-1]

    img_adj = int( img.shape[1] * percentage )
    reverse_adj = img.shape[1] - img_adj
    result_img = np.hstack(( img[:,:img_adj,:], adapted_img[:, img_adj:,:] ))
    # result_img = np.concat([img[:img_adj], adapted_img[img_adj:]])
    return result_img



def create_viz(
    images = '/efs/public_data/gta5/images',
    labels = 'labels',
    adapted = 'rec'):
    # adapted = '/efs/public_data/images'
    
    # labels_pth = '/'.join(images.split('/')[:-1]) + labels
    # adapted_pth = '/'.join(images.split('/')[:-1]) + adapted
    pth = '/'.join(images.split('/')[:-1])
    
    # parse images, labels and adapted into 3 seperate lists
    # labels and adapted are filepaths that contain "labels" and "adapted"
    label_paths = sorted([ f"{x}" for x in os.listdir(images) 
                          if labels in x ])[:1000][::-1]
    adapted_paths = sorted([ f"{x}" for x in os.listdir(images)
                            if adapted in x ])[2:1000][::-1]
    image_paths = sorted([ f"{x}" for x in os.listdir(images) ])[:1000][::-1]
    
    # set up ui
    # label_paths = sorted([ x for x in os.listdir(labels) ])[:1000][::-1]
    # adapted_paths = sorted([ x for x in os.listdir(adapted) ])[2:1000][::-1]
    
    direction = st.sidebar.selectbox('Direction', ['A to B', 'B to A'])
    IM_TYPE = {'A to B': ['fake_A','rec_B','real_B'],
               'B to A': ['fake_B','rec_A','real_A']}
    im_type = IM_TYPE[direction]

    tar_im_type = st.sidebar.selectbox("Which type of image?", im_type)

    file_selection = st.sidebar.selectbox("Which file?", adapted_paths)

    percentage = st.sidebar.slider("percentage", 0, 100) / 100

    col1, col2, col3 = st.columns(3)
    
    col1.header("Original")
    img = get_full_img_path(images, file_selection, im_type[1])
    
    st.code(img)
    
    img = np.array(Image.open(img).resize((512,512)))
    col1.image(img, use_column_width=True)
    
    col2.header("Mix")
    kpd_img = process_one(tar_im_type, file_selection, percentage,
                        images, adapted, im_type)
    col2.image(kpd_img, use_column_width=True)

    col3.header("Adapted")
    
    img = get_full_img_path(images, file_selection, tar_im_type)
    img = np.array(Image.open(img).resize((512,512)))
    col3.image(img, use_column_width=True)



if __name__ == "__main__":
    fire.Fire(create_viz)