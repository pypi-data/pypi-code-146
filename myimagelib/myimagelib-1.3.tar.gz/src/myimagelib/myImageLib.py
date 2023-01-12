# %% codecell
import os
import numpy as np
from scipy import fft
from scipy.signal import medfilt2d, convolve2d, fftconvolve
from scipy.optimize import curve_fit
import pandas as pd
import psutil
from skimage import io
import time
import shutil
from nd2reader import ND2Reader
# %% codecell

def dirrec(path, filename):
    """
    Recursively look for all the directories of files with name *filename*.

    :param path: the directory where you want to look for files.
    :type path: str
    :param filename: name of the files you want to look for.
    :type filename: str
    :return: a list of full directories of files with name *filename*
    :rtype: list[str]

    .. note::

       :code:`filename` can be partially specified, e.g. :code:`*.py` to search for all the files that end with *.py*. Similarly, setting :code:`filename` as :code:`*track*` will search for all files starting with *track*.

    .. rubric:: EDIT

    :11152022: Fix a bug, which falsely uses :py:func:`dirrec` within itself to iterate over subdirectories.
    """
    dirList = []
    for r, d, f in os.walk(path):
        # for dir in d:
        #     tmp = dirrec(dir, filename)
        #     if tmp:
        #         dirList.append(tmp)
        for file in f:
            if filename.startswith('*'):
                if file.endswith(filename[1:]):
                    dirList.append(os.path.join(r, file))
            elif filename.endswith('*'):
                if file.startswith(filename[:-1]):
                    dirList.append(os.path.join(r, file))
            elif file == filename:
                dirList.append(os.path.join(r, file))
    return dirList

def to8bit(img16):
    """
    Enhance contrast and convert to 8-bit.

    :param img: mono image of any dtype
    :type img: 2d array
    :return: 8-bit image
    :rtype: uint8 2d array
    """
    # if img16.dtype != 'uint16':
        # raise ValueError('16-bit grayscale image is expected')
    maxx = img16.max()
    minn = img16.min()
    img8 = (img16 - minn) / (maxx - minn) * 255
    return img8.astype('uint8')

def bpass(*args):
    """
    Apply bandpass filter on images. Useful when raw images have long wavelength intensity gradient.

    :param img: 8-bit image
    :type img: 2d array
    :param low: lower limit wavelength
    :type low: int
    :param high: upper limit wavelength
    :type high: int
    :return: processed image with low and high wavelength signals filtered
    :rtype: 2d array
    """
    img8 = args[0]
    low = args[1]
    high = args[2]
    def gen_filter(img, low, high):
        filt = np.zeros(img.shape)
        h, w = img.shape
        center = [int(w/2), int(h/2)]
        Y, X = np.ogrid[:h, :w]
        dist = ((X - center[0])**2 + (Y-center[1])**2)**.5

        filt[(dist>low)&(dist<=high)] = 1
        return filt
    filt = gen_filter(img8, low, high)
    filt = fft.ifftshift(filt)
    im_fft = fft.fft2(img8)
    im_fft_filt = im_fft * filt
    im_new = fft.ifft2(im_fft_filt).real
    im_new = im_new - im_new.min()
    im_new = np.floor_divide(im_new, (im_new.max()+1)/256)
    return im_new.astype('uint8')

def bestcolor(n):
    """
    Default plot color scheme of Matplotlib and Matlab. It is the same as `the "tab10" colormap of Matplotlib.colormaps <https://matplotlib.org/stable/tutorials/colors/colormaps.html#qualitative>`_.

    :param n: integer from 0 to 9, specifying the index of the color in the list
    :type n: int
    :return: the hex code of the specified color
    :rtype: str
    """
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
              '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
    return colors[n]

def wowcolor(n):
    """
    WOW class color scheme, used in my density fluctuations paper. I used to think these colors are aesthetically pleasing, but now I feel they are too saturated and cause eye fatigue easily. Therefore I would avoid using these colors in future publications.

    :param n: integer from 0 to 9, specifying the index of the color in the list
    :type n: int
    :return: the hex code of the specified color
    :rtype: str
    """
    colors = ['#C41F3B', '#A330C9', '#FF7D0A', '#A9D271', '#40C7EB',
              '#00FF96', '#F58CBA', '#FFF569', '#0070DE', '#8787ED',
              '#C79C6E', '#BBBBBB', '#1f77b4', '#ff7f0e', '#2ca02c',
              '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f',
              '#bcbd22', '#17becf']
    return colors[n]

def matlab_style_gauss2D(shape=(3,3),sigma=0.5):
    """
    Generate a 2D gaussian mask - should give the same result as MATLAB's :code:`fspecial('gaussian',[shape],[sigma])`.

    :param shape: shape of the mask, default to (3,3)
    :type shape: tuple
    :param simga: standard deviation of the mask, default to 0.5
    :type sigma: float
    :return: a gaussian mask
    :rtype: 2d array
    """
    m,n = [(ss-1.)/2. for ss in shape]
    y,x = np.ogrid[-m:m+1,-n:n+1]
    h = np.exp( -(x*x + y*y) / (2.*sigma*sigma) )
    h[ h < np.finfo(h.dtype).eps*h.max() ] = 0
    sumh = h.sum()
    if sumh != 0:
        h /= sumh
    return h

def FastPeakFind(data):
    """
    Detect peak in 2D images.

    I rewrote a `Matlab function <https://github.com/uw-cmg/MATLAB-loop-detection/blob/master/FastPeakFind.m>`_ with the same name in Python. The function, in my opinion, is unnecessarily complex, with thresholding, filtering, edge excluding etc. in the same function, making it very long and not easy to read. Moreover, it sometimes fails obviously simple tasks. Therefore, I would use :code:`skimage.feature.peak_local_max` for the same purpose, whenever possible.

    :param data: 2d images to find peaks in
    :type data: 2d array
    :return: coordinates of peaks in an Nx2 array
    :rtype: 2d array
    """
    if str(data.dtype) != 'float32':
        data = data.astype('float32')
    mf = medfilt2d(data, kernel_size=3)
    mf = mf.astype('float32')
    thres = max(min(np.amax(mf,axis=0)), min(np.amax(mf,axis=1)))
    filt = matlab_style_gauss2D()
    conv = convolve2d(mf, filt, mode='same')
    w_idx = conv > thres
    bw = conv.copy()
    bw[w_idx] = 1
    bw[~w_idx] = 0
    thresholded = np.multiply(bw, conv)
    edg = 3
    shape = data.shape
    idx = np.nonzero(thresholded[edg-1: shape[0]-edg-1, edg-1: shape[1]-edg-1])
    idx = np.transpose(idx)
    cent = []
    for xy in idx:
        x = xy[0]
        y = xy[1]
        if thresholded[x, y] >= thresholded[x-1, y-1] and \
            thresholded[x, y] > thresholded[x-1, y] and \
            thresholded[x, y] >= thresholded[x-1, y+1] and \
            thresholded[x, y] > thresholded[x, y-1] and \
            thresholded[x, y] > thresholded[x, y+1] and \
            thresholded[x, y] >= thresholded[x+1, y-1] and \
            thresholded[x, y] > thresholded[x+1, y] and \
            thresholded[x, y] >= thresholded[x+1, y+1]:
            cent.append(xy)
    cent = np.asarray(cent).transpose()
    return cent

def minimal_peakfind(img):
    """
    Minimal version of :py:func:`myImageLib.FastPeakFind`. Remove all the preprocessings, such as median filter, gauss filter and thresholding. Only keep the essential peak finding functionality.

    :param img: input image
    :type img: 2-d array
    :return: coordinates of peaks in an Nx2 array
    :rtype: 2d array
    """
    edg = 3
    shape = img.shape
    idx = np.nonzero(img[edg-1: shape[0]-edg-1, edg-1: shape[1]-edg-1])
    idx = np.transpose(idx)
    cent = []
    for xy in idx:
        x = xy[0]
        y = xy[1]
        if img[x, y] >= img[x-1, y-1] and \
            img[x, y] > img[x-1, y] and \
            img[x, y] >= img[x-1, y+1] and \
            img[x, y] > img[x, y-1] and \
            img[x, y] > img[x, y+1] and \
            img[x, y] >= img[x+1, y-1] and \
            img[x, y] > img[x+1, y] and \
            img[x, y] >= img[x+1, y+1]:
            cent.append(xy)
    cent = np.asarray(cent).transpose()
    return cent

def maxk(array, num_max):
    """
    Sort a numerical array and return the maximum :code:`num_max` elements.

    :param array: input array
    :type array: 1-d numerical array
    :param num_max: number of maximal elements to return
    :type num_max: int
    :return: index of maximal elements
    :rtype: int array
    """
    array = np.asarray(array)
    length = array.size
    array = array.reshape((1, length))
    idx = np.argsort(array)
    idx2 = np.flip(idx)
    return idx2[0, 0: num_max]

def track_spheres_dt(img, num_particles):
    """
    Use correlation tracking method to find spheres in an image.
    """
    def gauss1(x,a,x0,sigma):
        return a*np.exp(-(x-x0)**2/(2*sigma**2))
    cent = FastPeakFind(img)
    num_particles = min(num_particles, cent.shape[1])
    peaks = img[cent[0], cent[1]]
    ind = maxk(peaks, num_particles)
    max_coor_tmp = cent[:, ind]
    max_coor = max_coor_tmp.astype('float32')
    pk_value = peaks[ind]
    for num in range(0, num_particles):
        try:
            x = max_coor_tmp[0, num]
            y = max_coor_tmp[1, num]
            fitx1 = np.asarray(range(x-7, x+8))
            fity1 = np.asarray(img[range(x-7, x+8), y])
            popt,pcov = curve_fit(gauss1, fitx1, fity1, p0=[1, x, 3])
            max_coor[0, num] = popt[1]
            fitx2 = np.asarray(range(y-7, y+8))
            fity2 = np.asarray(img[x, range(y-7, y+8)])
            popt,pcov = curve_fit(gauss1, fitx2, fity2, p0=[1, y, 3])
            max_coor[1, num] = popt[1]
        except:
            print('Fitting failed')
            max_coor[:, num] = max_coor_tmp[:, num]
            continue
    return max_coor, pk_value

def gauss1(x,a,x0,sigma,b):
    """
    1-d gaussian function. Usually used for fitting.
    """
    return a*np.exp(-(x-x0)**2/(2*sigma**2)) + b

def show_progress(progress, label='', bar_length=60):
    """
    Display a progress bar in command line environment, which looks like

    .. code-block:: console

      label [##############-----------] 62%

    This is a useful tool for tracking work progress in a batch processing task on a server.

    :param progress: the progress of the work. It is a number between 0 and 1, where 0 is start and 1 is finish
    :type progress: float
    :param label: a string to put before the progress bar. It can be the name of the work, or the actual number of files that have been processed, and so on. Default to :code:`''`.
    :type label: str
    :param bar_length: length of the progress bar, in the unit of characters. Default to :code:`60`.
    :type bar_length: int
    :return: None
    """
    N_finish = int(progress*bar_length)
    N_unfinish = bar_length - N_finish
    print('{0} [{1}{2}] {3:.1f}%'.format(label, '#'*N_finish, '-'*N_unfinish, progress*100), end="\r")

def readdata(folder, ext='csv', mode="i"):
    """
    Wrapper of :py:func:`dirrec`, but easier to use when reading one type of files in a given folder. Instead of returning a list of directories as :py:func:`dirrec` does, :py:func:`readdata` puts the file names and corresponding full directories in a :code:`pandas.DataFrame`. The table will be sorted by the file names (strings), so the order would likely be correct. In the worst case, it is still easier to resort the :code:`pandas.DataFrame`, compared to the list of strings returned by :py:func:`dirrec`.

    :param folder: the folder to read files from
    :type folder: str
    :param ext: optional param, default to "csv", specifies the extension of files to be read
    :type ext: str
    :param mode: "i" for immediate, "r" for recursive. Default to "i"
    :type mode: str
    :return: a 2-column table containing file names and the corresponding full directories
    :rtype: pandas.DataFrame

    .. rubric:: EDIT

    :11152022: Add mode optional argument, to specify whether to read data only in the immediate folder, or read recursively.
    """
    dataDirs = dirrec(folder, '*.' + ext)
    dataDirsCopy = dataDirs.copy()
    if mode == "i":
        for dataDir in dataDirsCopy:
            relpath = dataDir.replace(folder, "").strip(os.sep)
            if os.sep in relpath:
                dataDirs.remove(dataDir)
    nameList = []
    dirList = []
    for dataDir in dataDirs:
        path, file = os.path.split(dataDir)
        name, ext = os.path.splitext(file)
        nameList.append(name)
        dirList.append(dataDir)
    fileList = pd.DataFrame()
    fileList = fileList.assign(Name=nameList, Dir=dirList)
    fileList = fileList.sort_values(by=['Name']).reset_index(drop=True)
    return fileList

def normxcorr2(template, image, mode="full"):
    """
    Compute normalized cross-correlation map between an image and a template. Input arrays should be floating point numbers.

    :param template: N-D array, of template or filter you are using for cross-correlation. Must be less or equal dimensions to image. Length of each dimension must be less than length of image.
    :type template: float array
    :param image: N-D array
    :type image: float array
    :param mode: Options, "full", "valid", "same". full (Default): The output of fftconvolve is the full discrete linear convolution of the inputs. Output size will be image size + 1/2 template size in each dimension. valid: The output consists only of those elements that do not rely on the zero-padding. same: The output is the same size as image, centered with respect to the ‘full’ output.
    :return: N-D array of same dimensions as image. Size depends on mode parameter.
    :rtype: float array
    """

    # If this happens, it is probably a mistake
    if np.ndim(template) > np.ndim(image) or \
            len([i for i in range(np.ndim(template)) if template.shape[i] > image.shape[i]]) > 0:
        print("normxcorr2: TEMPLATE larger than IMG. Arguments may be swapped.")

    template = template - np.mean(template)
    image = image - np.mean(image)

    a1 = np.ones(template.shape)
    # Faster to flip up down and left right then use fftconvolve instead of scipy's correlate
    ar = np.flipud(np.fliplr(template))
    out = fftconvolve(image, ar.conj(), mode=mode)

    image = fftconvolve(np.square(image), a1, mode=mode) - \
            np.square(fftconvolve(image, a1, mode=mode)) / (np.prod(template.shape))

    # Remove small machine precision errors after subtraction
    image[np.where(image < 0)] = 0

    template = np.sum(np.square(template))
    out = out / np.sqrt(image * template)

    # Remove any divisions by 0 or very close to 0
    out[np.where(np.logical_not(np.isfinite(out)))] = 0

    return out

def match_hist(im1, im2):
    """
    Match the histogram of im1 to that of im2

    :param im1: image
    :type im1: 2d array
    :param im2: image
    :type im2: 2d array
    :return: a modified version of im1, that matches im2's histogram
    :rtype: 2d array

    .. rubric:: EDIT

    :11142022: Move from ``corrLib`` to ``myImageLib``.
    """
    return (abs(((im1 - im1.mean()) / im1.std() * im2.std() + im2.mean()))+1).astype('uint8')

def xy_bin(xo, yo, n=100, mode='log', bins=None):
    """
    Bin x, y data on log or linear scale


    :param xo: input x
    :param yo: input y
    :param n: points after binning
    :param mode: "lin" or "log", scale to bin the data
    :param bins: set the bins to bin data together

    :return:
        * x: binned x
        * y: means in bins

    .. rubric: Edit

    :11042020: Change function name to xy_bin, to incorporate the mode parameter, so that the function can do both log space binning and linear space binning.
    :11172020: add bins kwarg, allow user to enter custom bins.
    :12162021: fix divided by 0 issue.
    :11142022: Move from ``corrLib`` to ``myImageLib``.
    """
    assert(len(xo)==len(yo))
    if bins is None:
        if mode == 'log':
            x = np.logspace(np.log10(xo[xo>0].min()), np.log10(xo.max()), n+1)
        elif mode == 'lin':
            x = np.linspace(xo.min(), xo.max(), n+1)
    else:
        x = np.sort(bins)
    top = np.histogram(xo, x, weights=yo)[0]
    bot = np.histogram(xo, x)[0]
    ind = bot > 0
    xb = ((x[1:] + x[:-1]) / 2)[ind]
    yb = top[ind] / bot[ind]
    return xb, yb
# %% codecell

class rawImage:
    """
    This class converts raw images to tif sequences. Throughout my research, I have mostly worked with two raw image formats: *\*.nd2* and *\*.raw*. Typically, they are tens of GB large, and are not feasible to load into the memory of a PC as a whole. Therefore, the starting point of my workflow is to convert raw images into sequences of *\*.tif* images. """

    def __init__(self, file_dir):
        """
        Construct rawImage object using the file directory.
        """
        self.file = file_dir
        self.type = os.path.splitext(self.file)[1]
        if self.type == ".nd2":
            with ND2Reader(self.file) as images:
                self.images = images
        elif self.type == ".raw":
            print("raw image handling is pending implementation.")
        else:
            raise ValueError
    def __repr__(self):
        """Ideally, I can see some general informations about this image. For example, the number of frames and the frame size. Frame rate would also be helpful."""
        repr_str = "source file: {0}\nimage shape: {1}".format(self.file, self.images.shape)
        return repr_str
    def extract_tif(self):
        """Wrapper of all format-specific extractors."""
        file, ext = os.path.splitext(self.file)
        if ext == ".raw":
            self._extract_raw()
        elif ext == ".nd2":
            self._extract_nd2()
        else:
            raise ValueError("Unrecognized image format {}".format(ext))
    def _extract_raw(self, cutoff=None):
        """Extract tif sequence from *\*.raw* file.
        :param cutoff: number of images to extract

        .. rubric:: Edit

        * Dec 07, 2022: fix progress bar error.
        """
        # read info from info_file
        folder, file = os.path.split(self.file)
        info_file = os.path.join(folder, "RawImageInfo.txt")
        if os.path.exists(info_file):
            fps, h, w = self.read_raw_image_info(info_file)
        else:
            print("Info file missing!")

        # create output folders, skip if both folders exist
        save_folder = folder
        out_raw_folder = os.path.join(save_folder, 'raw')
        out_8_folder = os.path.join(save_folder, '8-bit')
        if os.path.exists(out_raw_folder) and os.path.exists(out_8_folder):
            print(time.asctime() + " // {} tif folders exists, skipping".format(self.file))
            return None
        if os.path.exists(out_raw_folder) == False:
            os.makedirs(out_raw_folder)
        if os.path.exists(out_8_folder) == False:
            os.makedirs(out_8_folder)

        # check disk
        if self._disk_capacity_check() == False:
            raise SystemError("No enough disk capacity!")

        # calculate buffer size based on available memory, use half of it
        file_size = os.path.getsize(self.file)
        avail_mem = psutil.virtual_memory().available
        unit_size = (h * w + 2) * 2 # the size of a single unit in bytes (frame# + image)
        buffer_size = ((avail_mem // 2) // unit_size) * unit_size # integer number of units
        remaining_size = file_size

        # print("Memory information:")
        # print("Available memory: {:.1f} G".format(avail_mem / 2 ** 30))
        # print("File size: {:.1f} G".format(file_size / 2 ** 30))
        # print("Buffer size: {:.1f} G".format(buffer_size / 2 ** 30))

        # read the binary files, in partitions if needed
        num = 0
        n_images = int(file_size // unit_size)
        t0 = time.monotonic()
        while remaining_size > 0:
            # load np.array from buffer
            if remaining_size > buffer_size:
                read_size = buffer_size
            else:
                read_size = remaining_size
            with open(self.file, "rb") as f:
                f.seek(-remaining_size, 2) # offset bin file reading, counting remaining size from EOF
                bytestring = f.read(read_size)
                a = np.frombuffer(bytestring, dtype=np.uint16)
            remaining_size -= read_size

            # manipulate the np.array
            assert(a.shape[0] % (h*w+2) == 0)
            num_images = a.shape[0] // (h*w+2)
            img_in_row = a.reshape(num_images, h*w+2)
            labels = img_in_row[:, :2] # not in use currently
            images = img_in_row[:, 2:]
            images_reshape = images.reshape(num_images, h, w)

            # save the image sequence
            for label, img in zip(labels, images_reshape):
                # num = label[0] + label[1] * 2 ** 16 + 1 # convert image label to uint32 to match the info in StagePosition.txt
                io.imsave(os.path.join(save_folder, 'raw', '{:05d}.tif'.format(num)), img, check_contrast=False)
                io.imsave(os.path.join(save_folder, '8-bit', '{:05d}.tif'.format(num)), to8bit(img), check_contrast=False)
                t1 = time.monotonic() - t0
                show_progress((num+1 / n_images), label="{:.1f} frame/s".format(num / t1))
                num += 1
                if cutoff is not None:
                    if num > cutoff:
                        return None

    def read_raw_image_info(self, info_file):
        """
        Read image info, such as fps and image dimensions, from *\*.RawImageInfo.txt*.
        Helper function of :py:func:`myImageLib.rawImage.extract_raw`.
        """
        with open(info_file, 'r') as f:
            a = f.read()
        fps, h, w = a.split('\n')[0:3]
        return int(fps), int(h), int(w)

    def _extract_nd2(self):
        """
        Extract tif sequence from *\*.nd2* file.
        """
        # check disk
        if self._disk_capacity_check() == False:
            raise SystemError("No enough disk capacity!")

        folder, file = os.path.split(self.file)
        name, ext = os.path.splitext(file)
        saveDir = os.path.join(folder, name, 'raw')
        saveDir8 = os.path.join(folder, name, '8-bit')
        if os.path.exists(saveDir) == False:
            os.makedirs(saveDir)
        if os.path.exists(saveDir8) == False:
            os.makedirs(saveDir8)
        t0 = time.monotonic()
        with ND2Reader(self.file) as images:
            n_images = len(images)
            for num, image in enumerate(images):
                io.imsave(os.path.join(saveDir8, '{:05d}.tif'.format(num)), to8bit(image))
                io.imsave(os.path.join(saveDir, '%05d.tif' % num), image, check_contrast=False)
                t1 = time.monotonic() - t0
                show_progress((num+1) / n_images, label="{:.1f} frame/s".format(num/t1))

    def _disk_capacity_check(self):
        """Check if the capacity of disk is larger than twice of the file size.
        Args:
        file -- directory of the (.nd2) file being converted
        Returns:
        flag -- bool, True if capacity is enough."""
        d = os.path.split(self.file)[0]
        fs = os.path.getsize(self.file) / 2**30
        ds = shutil.disk_usage(d)[2] / 2**30
        print("File size {0:.1f} GB, Disk size {1:.1f} GB".format(fs, ds))
        return ds > 2 * fs