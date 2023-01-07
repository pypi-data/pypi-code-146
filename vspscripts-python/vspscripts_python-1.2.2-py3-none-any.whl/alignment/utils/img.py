import cv2
import warnings
import numpy as np
from PIL import Image
from vspscripts.alignment.utils import gol

def scaling_imgcam(img, cam, size_max):
    if isinstance(img, str) and isinstance(cam, str):
        img = cv2.imread(img)
        cam = cv2.imread(cam)
    elif type(img) is np.ndarray:
        h_img, w_img = img.shape[:2]
        if size_max < max(h_img, w_img):
            scale = size_max/max(h_img, w_img)
            img_scaled = cv2.resize(img, (int(scale*w_img), int(scale*h_img)), interpolation=cv2.INTER_NEAREST)
            # print(img_scaled.shape, cam_scaled.shape, scale)
            # raise ValueError
        else:
            scale = 1
    else:
        w_img, h_img = img.size[:2]
        if size_max < max(h_img, w_img):
            scale = size_max/max(h_img, w_img)
            img_scaled = img.resize((int(scale*w_img), int(scale*h_img)), Image.NEAREST)
        else:
            scale = 1
    h_cam, w_cam = cam.shape[:2]
    cam_scaled = cv2.resize(cam, (int(scale*w_cam), int(scale*h_cam)), interpolation=cv2.INTER_NEAREST)
    return img_scaled, cam_scaled, scale

def binarize_imgcam(img, cam, method):
    if isinstance(img, str) and isinstance(cam, str):
        img = cv2.imread(img)
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # cv2.imread(img, cv2.IMREAD_GRAYSCALE)
        cam = cv2.imread(cam)
        cam_r = cam[:, :, 2]
    else:
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if img.shape[2]==3 else img
        cam_r = cam[:, :, 2] if cam.shape[2]==3 else cam

    if method == 'ONLY_GRAY':
        return img_gray, None, cam_r, None

    _, thresh_cam = cv2.threshold(cam_r, 150, 255, cv2.THRESH_BINARY)

    if cam_r.shape[0]<img_gray.shape[0] or cam_r.shape[1]<img_gray.shape[1]:
        scale = min(img_gray.shape[0]/cam_r.shape[0], img_gray.shape[1]/cam_r.shape[1])
        thresh_cam = cv2.resize(thresh_cam, (int(scale*thresh_cam.shape[1]), int(scale*thresh_cam.shape[0])), interpolation=cv2.INTER_NEAREST)
        cam_r = cv2.resize(cam_r, (int(scale*cam_r.shape[1]), int(scale*cam_r.shape[0])), interpolation=cv2.INTER_NEAREST)

        height_expand = img_gray.shape[0]-cam_r.shape[0]
        width_expand = img_gray.shape[1]-cam_r.shape[1]
        thresh_cam = cv2.copyMakeBorder(thresh_cam, int(height_expand/2), height_expand-int(height_expand/2), int(width_expand/2), width_expand-int(width_expand/2), cv2.BORDER_CONSTANT,value=127)
        cam_r = cv2.copyMakeBorder(cam_r, int(height_expand/2), height_expand-int(height_expand/2), int(width_expand/2), width_expand-int(width_expand/2), cv2.BORDER_CONSTANT,value=0)
    # try:
    #     cam_expand
    # except NameError:
    #     cam_expand_r = thresh_cam

    if np.sum(thresh_cam==255) <= 10:
        method = 'HSV_BINARY'
        thresh_cam = False
    elif np.sum(thresh_cam==0) <= 10:
        # method = 'HSV_BINARY'
        thresh_cam = True

    # ret,thresh1 = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
    # Otsu's thresholding after Gaussian filtering
    # blur = cv2.GaussianBlur(img, (5, 5), 0)
    # ret,thresh2 = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    if method == 'RGB_OTSU':
        # Otsu's thresholding
        ret2, thresh_img = cv2.threshold(img_gray, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

        # ret, thresh_cam = cv2.threshold(cam,10,255,cv2.THRESH_BINARY)

        # Otsu's thresholding
        # ret, thresh_cam = cv2.threshold(cam, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        # _, thresh_cam = cv2.threshold(cam_r, 150, 255, cv2.THRESH_BINARY)
    elif method == 'RGB_BINARY':
        _, thresh_img = cv2.threshold(img_gray, 127, 255, cv2.THRESH_BINARY)
    elif method == 'HSV_OTSU':
        # img = cv2.imread(img)
        img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        img_v = img_hsv[:, :, 2]
        # img_v = cv2.GaussianBlur(img_v, (5, 5), 0)
        _, thresh_img = cv2.threshold(img_v, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        # thresh_img = cv2.bitwise_and(img_gray, img_gray, mask=mask)
        # _, thresh_img = cv2.threshold(img_gray, 127, 255, cv2.THRESH_BINARY)
    elif method == 'HSV_BINARY':
        # img = cv2.imread(img)
        img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        # TODO
        lower_hsv = np.array([10,0,0])
        upper_hsv = np.array([20,255,255])
        mask = cv2.inRange(img_hsv, lower_hsv, upper_hsv)
        thresh_img = mask
        
        # thresh_img = cv2.bitwise_and(img_gray, img_gray, mask=mask)
        # _, thresh_img = cv2.threshold(img_gray, 127, 255, cv2.THRESH_BINARY)
        
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (int(img.shape[0]/100), int(img.shape[1]/100)))
    thresh_img = cv2.morphologyEx(thresh_img, cv2.MORPH_OPEN, kernel)
    thresh_img = cv2.morphologyEx(thresh_img, cv2.MORPH_CLOSE, kernel)

    return img_gray, thresh_img, cam_r, thresh_cam

def crop_imgcam(img, cam, size=300):
    # assert img.shape==cam.shape
    # print(img.shape, cam.shape)
    Height_img, Width_img = img.shape[:2]
    Height_cam, Width_cam = cam.shape[:2]

    if Height_img < size or Width_img < size or Height_cam < size or Width_cam < size:
        size = min(Height_img, Width_img, Height_cam, Width_cam)
        warnings.warn('The min size is {}!'.format(size), UserWarning)

    img_crop = img[int(Height_img/2-size/2): int(Height_img/2-size/2)+size, int(Width_img/2-size/2): int(Width_img/2-size/2)+size]
    cam_crop = cam[int(Height_cam/2-size/2): int(Height_cam/2-size/2)+size, int(Width_cam/2-size/2): int(Width_cam/2-size/2)+size]
    return img_crop, cam_crop, size

def crop_cam(cam=None, size=300):
    Height_cam, Width_cam = cam.shape[:2]

    if Height_cam < size or Width_cam < size:
        size = min(Height_cam, Width_cam)
        warnings.warn('The min size is {}!'.format(size), UserWarning)

    cam_crop = cam[int(Height_cam/2-size/2): int(Height_cam/2-size/2)+size, int(Width_cam/2-size/2): int(Width_cam/2-size/2)+size]
    return cam_crop, size

def crop_imgcam_ori(mask, img, cam, size=300, is_expand=True):
    # assert img.shape==cam.shape
    # print(img.shape, cam.shape)
    Extd_value = gol.get_value('EXTEND_VALUE')
    Height_img, Width_img = img.shape[:2]
    Height_cam, Width_cam = cam.shape[:2]
    if Height_img < size or Width_img < size or Height_cam < size or Width_cam < size:
        if is_expand:
            height_img_expand = max(size-Height_img, 0)
            width_img_expand = max(size-Width_img, 0)
            height_cam_expand = max(size-Height_cam, 0)
            width_cam_expand = max(size-Width_cam, 0)
            mask = cv2.copyMakeBorder(mask, int(height_img_expand/2), height_img_expand-int(height_img_expand/2), int(width_img_expand/2), width_img_expand-int(width_img_expand/2), cv2.BORDER_CONSTANT,value=[0, 0, 0])
            img = cv2.copyMakeBorder(img, int(height_img_expand/2), height_img_expand-int(height_img_expand/2), int(width_img_expand/2), width_img_expand-int(width_img_expand/2), cv2.BORDER_CONSTANT,value=[Extd_value, Extd_value, Extd_value])
            cam = cv2.copyMakeBorder(cam, int(height_cam_expand/2), height_cam_expand-int(height_cam_expand/2), int(width_cam_expand/2), width_cam_expand-int(width_cam_expand/2), cv2.BORDER_CONSTANT,value=[Extd_value, Extd_value, Extd_value])
            Height_img, Width_img = img.shape[:2]
            Height_cam, Width_cam = cam.shape[:2]
        else:
            size = min(Height_img, Width_img, Height_cam, Width_cam)
            warnings.warn('The min size is {}!'.format(size), UserWarning)

    mask_crop = mask[int(Height_img/2-size/2): int(Height_img/2-size/2)+size, int(Width_img/2-size/2): int(Width_img/2-size/2)+size]
    img_crop = img[int(Height_img/2-size/2): int(Height_img/2-size/2)+size, int(Width_img/2-size/2): int(Width_img/2-size/2)+size]
    cam_crop = cam[int(Height_cam/2-size/2): int(Height_cam/2-size/2)+size, int(Width_cam/2-size/2): int(Width_cam/2-size/2)+size]
    return mask_crop, img_crop, cam_crop, size

def Get_Mask_ROI(img, cam, mask_value, Extd_value):
    masked_cam = cam.copy()
    if len(img.shape) == len(cam.shape) == 2:
        # rows, cols = img.shape
        roi = np.zeros(img.shape, np.uint8)
        roi.fill(mask_value)

        roi_img = np.zeros(img.shape, np.uint8)
        roi_cam = np.zeros(cam.shape, np.uint8)
        roi_img = img != roi
        roi_cam = cam != roi
        roi = cv2.bitwise_and(roi_img*255, roi_cam*255).astype(np.bool)
        # cv2.imwrite('test4.jpg', roi.astype("int")*255)
        roi_Reverse = ~roi
        # cv2.imwrite('test3.jpg', roi_Reverse.astype("int")*255)
        # print(masked_cam.shape, roi_Reverse.shape)
        masked_cam[roi_Reverse]=Extd_value
        # print(cam)
        # for r in range(rows):
        #     for c in range(cols):
        #         if img[r, c] == mask_value:
        #             roi[r, c] = 0
        #             cam_mask[r, c] = img[r, c]
    elif len(img.shape) == len(cam.shape) == 3:
        rows, cols, channels = img.shape
        roi = np.zeros((rows, cols), np.uint8)
        roi.fill(mask_value)
        roi = img[:,:,2] != roi
        # cv2.imwrite('test4.jpg', roi.astype("int")*255)
        roi_Reverse = ~roi
        # cv2.imwrite('test3.jpg', roi_Reverse.astype("int")*255)
        # print(masked_cam.shape, roi_Reverse.shape)
        masked_cam[roi_Reverse]=(Extd_value, Extd_value, Extd_value)
    return masked_cam, roi*255
