import cv2
import numpy as np
import matplotlib.pylab as plt
from vspscripts.alignment.matching.dist import pixel_dist, mse_dist
from vspscripts.alignment.utils.img import binarize_imgcam, Get_Mask_ROI, crop_imgcam

def compare_imgcam(img_path, cam_path, method='pHash'):

    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    cam = cv2.imread(cam_path, cv2.IMREAD_GRAYSCALE)
    img, cam = crop_imgcam(img, cam, size=img.shape[0])
    masked_cam, roi = Get_Mask_ROI(img, cam, 0)

    _, thresh_img, _, thresh_cam = binarize_imgcam(img, masked_cam, 'RGB_BINARY')

    fig=plt.figure('Mask img&cam')
    plt.subplot(221),plt.imshow(img, cmap ='gray'),plt.title("Gray img")
    plt.subplot(222),plt.imshow(cam, cmap ='gray'),plt.title("Gray cam")
    plt.subplot(223),plt.imshow(thresh_img, cmap ='gray'),plt.title("Binarized img")
    plt.subplot(224),plt.imshow(thresh_cam, cmap ='gray'),plt.title("Binarized cam")
    plt.show()

    """
    Get the similarity of two pictures via pHash
        Generally, when:
            ham_dist == 0 -> particularly like
            ham_dist < 5  -> very like
            ham_dist > 10 -> different image

        Attention: this is not accurate compare_img_hist() method, so use hist() method to auxiliary comparision.
            This method is always used for graphical search applications, such as Google Image(Use photo to search photo)

    :param img1:
    :param img2:
    :return:
    """
    if method == 'aHash':
        hash_img = get_img_a_hash(thresh_img)
        hash_cam = get_img_a_hash(thresh_cam)
        return ham_dist(hash_img, hash_cam)
    elif method == 'pHash':
        hash_img = get_img_p_hash(thresh_img)
        hash_cam = get_img_p_hash(thresh_cam)
        return ham_dist(hash_img, hash_cam)
    elif method == 'dHash':
        hash_img = get_img_d_hash(thresh_img)
        hash_cam = get_img_d_hash(thresh_cam)
        return ham_dist(hash_img, hash_cam)
    elif method == 'mse':
        return mse_dist(thresh_img, thresh_cam, roi)
    elif method == 'pixel':
        return pixel_dist(thresh_img, thresh_cam, roi)

def get_img_p_hash(gray_img):
    """
    Get the pHash value of the image, pHash : Perceptual hash algorithm(感知哈希算法)
    
    :param img: img in MAT format(img = cv2.imread(image))
    :return: pHash value
    """
    hash_len = 32

    # GET Gray image
    # gray_img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    # Resize image, use the different way to get the best result
    resize_gray_img = cv2.resize(gray_img, (hash_len, hash_len), cv2.INTER_AREA)
    # resize_gray_img = cv.resize(gray_img, (hash_len, hash_len), cv.INTER_LANCZOS4)
    # resize_gray_img = cv.resize(gray_img, (hash_len, hash_len), cv.INTER_LINEAR)
    # resize_gray_img = cv.resize(gray_img, (hash_len, hash_len), cv.INTER_NEAREST)
    # resize_gray_img = cv.resize(gray_img, (hash_len, hash_len), cv.INTER_CUBIC)

    # Change the int of image to float, for better DCT
    h, w = resize_gray_img.shape[:2]
    vis0 = np.zeros((h, w), np.float32)
    vis0[:h, :w] = resize_gray_img

    # DCT: Discrete cosine transform(离散余弦变换)
    vis1 = cv2.dct(cv2.dct(vis0))
    vis1.resize(hash_len, hash_len)
    img_list = vis1.flatten()

    # Calculate the avg value
    avg = sum(img_list) * 1. / len(img_list)
    avg_list = []
    for i in img_list:
        if i < avg:
            tmp = '0'
        else:
            tmp = '1'
        avg_list.append(tmp)

    # Calculate the hash value
    p_hash_str = ''
    for x in range(0, hash_len * hash_len, 4):
        p_hash_str += '%x' % int(''.join(avg_list[x:x + 4]), 2)
    return p_hash_str

def get_img_a_hash(image):
    # 将图片缩放为8*8的
    gray = cv2.resize(image, (8, 8), interpolation=cv2.INTER_CUBIC)
    # 将图片转化为灰度图
    # gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    # s为像素和初始灰度值，hash_str为哈希值初始值
    s = 0
    # 遍历像素累加和
    for i in range(8):
        for j in range(8):
            s = s + gray[i, j]
    # 计算像素平均值
    avg = s / 64
    # 灰度大于平均值为1相反为0，得到图片的平均哈希值，此时得到的hash值为64位的01字符串
    ahash_str = ''
    for i in range(8):
        for j in range(8):
            if gray[i, j] > avg:
                ahash_str = ahash_str + '1'
            else:
                ahash_str = ahash_str + '0'
    result = ''
    for i in range(0, 64, 4):
        result += ''.join('%x' % int(ahash_str[i: i + 4], 2))
    # print("ahash值：",result)
    return result

def get_img_d_hash(image):
    # 将图片转化为8*8
    gray = cv2.resize(image, (9, 8), interpolation=cv2.INTER_CUBIC)
    # 将图片转化为灰度图
    # gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    dhash_str = ''
    for i in range(8):
        for j in range(8):
            if gray[i, j] > gray[i, j + 1]:
                dhash_str = dhash_str + '1'
            else:
                dhash_str = dhash_str + '0'
    result = ''
    for i in range(0, 64, 4):
        result += ''.join('%x' % int(dhash_str[i: i + 4], 2))
    # print("dhash值",result)
    return result

def ham_dist(x, y):
    """
    Get the hamming distance of two values.
        hamming distance(汉明距)
    :param x:
    :param y:
    :return: the hamming distance
    """
    assert len(x) == len(y)
    return sum([ch1 != ch2 for ch1, ch2 in zip(x, y)])


if __name__ == "__main__":
    img_path = 'test.jpg'
    cam_path = 'test.png'
    
    print(compare_imgcam(img_path, cam_path, method='pixel'))
