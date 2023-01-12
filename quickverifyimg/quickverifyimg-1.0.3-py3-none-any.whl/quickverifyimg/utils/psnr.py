import cv2
import numpy as np

def psnr(img1, img2):
    # > 40，非常接近原始图像
    # 30 - 40，质量好，失真可接受
    # 20 - 30，质量差
    # < 20，不可接受

    mse = np.mean((img1-img2)**2)
    if mse == 0:
        return float('inf')
    else:
        return 20*np.log10(255/np.sqrt(mse))

def get_psnr_similar(img1, img2):
    img1 = np.array(img1).astype(np.float64)
    img2 = np.array(img2).astype(np.float64)
    result = psnr(img1, img2)
    if result > 40:
        return 0.999
    return 0
if __name__ == "__main__":
    # image_file1 = './downloads/1.png'
    # image_file2 = './downloads/background.png'
    # img1 = Image.open(image_file1)
    # img2 = Image.open(image_file2)

    img1 = cv2.imread('./downloads/1.png')
    img2 = cv2.imread('./downloads/background.png')
    print(get_psnr_similar(img1, img2))