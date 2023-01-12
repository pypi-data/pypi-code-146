import cv2
import numpy

SSIM_DEFAULT_KERNEL = cv2.getGaussianKernel(11, 1.5)
SSIM_DEFAULT_WINDOW = SSIM_DEFAULT_KERNEL * SSIM_DEFAULT_KERNEL.T




def filter2valid(src, window):
    # https://cn.mathworks.com/help/matlab/ref/filter2.html#inputarg_shape
    ret = cv2.filter2D(src, -1, window, anchor=(1, 1),
                       delta=0, borderType=cv2.BORDER_CONSTANT)
    return ret[1:ret.shape[0] - window.shape[0] + 2, 1:ret.shape[1] - window.shape[1] + 2]


def ssim(img1, img2, K=(0.01, 0.03), window=SSIM_DEFAULT_WINDOW, L=255, downsample=True):
    # SSIM（structural similarity）是一种用来衡量图片相似度的指标，也可用来判断图片压缩后的质量。
    img1 = img1.astype(float)
    img2 = img2.astype(float)
    assert(img1.shape[0] == img2.shape[0] and img1.shape[1] == img2.shape[1])

    assert(len(K) == 2 and K[0] >= 0 and K[1] >= 0)

    M, N = img1.shape[0:2]
    H, W = window.shape[0:2]
    assert(H * W >= 4 and H <= M and W <= N)

    # automatic downsampling
    f = max(1, int(round(min(M, N) / 256.0)))
    # downsampling by f
    # use a simple low-pass filter
    if downsample and f > 1:
        lpf = numpy.ones((f, f))
        lpf = lpf / numpy.sum(lpf)

        # In opencv, filter2D use the center of kernel as the anchor,
        # according to http://docs.opencv.org/2.4.8/modules/imgproc/doc/filtering.html#void filter2D(InputArray src, OutputArray dst, int ddepth, InputArray kernel, Point anchor, double delta, int borderType)
        # but in matlab, imfilter use (2, 2) (matlab array starts with 1) as the anchor,
        # To ensure the results are the same with matlab's implementation, we
        # set filter2D's anchor to (1, 1) (python array starts with 0)
        img1 = cv2.filter2D(img1, -1, lpf, anchor=(1, 1),
                            borderType=cv2.BORDER_REFLECT)
        img2 = cv2.filter2D(img2, -1, lpf, anchor=(1, 1),
                            borderType=cv2.BORDER_REFLECT)

        img1 = img1[0::f, 0::f]
        img2 = img2[0::f, 0::f]

    C1, C2 = tuple((k * L) ** 2 for k in K)

    window = window / numpy.sum(window)

    mu1 = filter2valid(img1, window)
    mu2 = filter2valid(img2, window)

    mu1_sq = mu1 * mu1
    mu2_sq = mu2 * mu2

    mu1_mu2 = mu1 * mu2

    sigma1_sq = filter2valid(img1 * img1, window) - mu1_sq

    sigma2_sq = filter2valid(img2 * img2, window) - mu2_sq

    sigma12 = filter2valid(img1 * img2, window) - mu1_mu2

    ssim_map = ((2 * mu1_mu2 + C1) * (2 * sigma12 + C2)) / \
        ((mu1_sq + mu2_sq + C1) * (sigma1_sq + sigma2_sq + C2))

    ssim_scalar = cv2.mean(ssim_map)

    return ssim_scalar[0]


# hist直方图算法
def compare_hist(image_a, image_b):
    # Get the histogram data of image 1, then using normalize the picture for better compare
    img1_hist = cv2.calcHist([image_a], [1], None, [256], [0, 256])
    img1_hist = cv2.normalize(img1_hist, img1_hist, 0, 1, cv2.NORM_MINMAX, -1)

    img2_hist = cv2.calcHist([image_b], [1], None, [256], [0, 256])
    img2_hist = cv2.normalize(img2_hist, img2_hist, 0, 1, cv2.NORM_MINMAX, -1)
    similarity = cv2.compareHist(img1_hist, img2_hist, 0)

    return similarity


if __name__ == '__main__':
    image1 = cv2.imread('../downloads/screenshot/41.png')
    image2 = cv2.imread('../downloads/0_11403/793.png')
    print(ssim(image1, image2))