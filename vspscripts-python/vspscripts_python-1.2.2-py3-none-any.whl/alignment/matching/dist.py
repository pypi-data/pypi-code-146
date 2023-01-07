import cv2
import numpy as np

def pixel_dist(imageA, imageB, *args, is_highlights=False):
    assert (imageA.shape == imageB.shape)
    pixel = imageA != imageB
    # cv2.imwrite('imageA.jpg', imageA)
    # cv2.imwrite('imageB.jpg', imageB)
    # cv2.imwrite('pixel.jpg', pixel.astype("int")*255)
    if is_highlights:
        dif_num = np.sum(pixel.astype("float")*(imageB/255).astype("int"))
        roi_num = np.sum((imageB/255).astype("int"))
        # cv2.imwrite('imageB_highlights.jpg', pixel.astype("float")*(imageB/255).astype("int")*255)
        # print(dif_num)
        # raise ValueError('test')
        if roi_num <= 10*10:
            return 1.0
        else:
            return dif_num/roi_num
    else:
        if args == ():
            dif_num = np.sum(pixel)
            return dif_num/float(pixel.shape[0] * pixel.shape[1])
        else:
            roi = args[0]
            dif_num = np.sum(cv2.bitwise_and(pixel*255, roi).astype(np.bool))
            pixel_roi = roi != 0
            # cv2.imwrite('test.png', pixel.astype("int")*255)
            # cv2.imwrite('test1.png', pixel_roi.astype("int")*255)
            roi_num = np.sum(pixel_roi)
            # print(dif_num, roi_num)
            if roi_num <= 50*50:
                return 1.0
            else:
                total_num = float(pixel.shape[0] * pixel.shape[1])
                return dif_num/roi_num + 0.2*(total_num-roi_num)/total_num

def mse_dist(imageA, imageB):
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])
    return err
