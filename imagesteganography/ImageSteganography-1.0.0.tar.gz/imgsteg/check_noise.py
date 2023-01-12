import math, time
import cv2
import numpy as np

original = cv2.imread(input('Enter src image address:\n'))
contrast = cv2.imread(input("Enter encrypted image address:\n"))

def psnr(img1, img2):
    mse = np.mean((img1 - img2) ** 2)
    if mse == 0:
        return 100
    PIXEL_MAX = 255.0
    return 20 * math.log10(PIXEL_MAX / math.sqrt(mse))

d = psnr(original, contrast)
print(d)

time.sleep(10)
