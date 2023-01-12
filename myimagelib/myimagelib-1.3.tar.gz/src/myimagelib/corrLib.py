import numpy as np
import matplotlib.pyplot as plt
from myimagelib.myImageLib import dirrec, bpass
from skimage import io, util
import os
import pandas as pd
import sys
import time
from numpy.polynomial.polynomial import polyvander

def corrS(X, Y, U, V):
    """
    Compute the spatial autocorrelations of a velocity field.

    :param X,Y,U,V: the result of PIV analysis. Each is a 2D array. Use :py:func:`pivLib.read_piv` to construct thses arrays from PIV data files.
    :type X,Y,U,V: 2d arrays
    :return: x, y, CA, CV -- The angle autocorrelation (CA) and velocity autocorrelation (CV). x, y are the associated distances.

    .. note::

        We only consider half of the length in each dimension, so x, y are different from the input X, Y.

    .. rubric:: Edit

    * Dec 13, 2021 -- i) Replace all the `mean()` function to nanmean, to handle masked PIV data. ii) Add doc string.
    * Dec 15, 2021 -- if norm `vsqrt` is 0, set it to np.nan to avoid divided by zero warning!
    * Dec 16, 2021 -- Shift the output X, Y origin to 0, 0, so that 0 distance will have the correlation function = 1. More intuitive.
    * Jan 05, 2023 -- Adapt myimagelib import style.
    """
    row, col = X.shape
    r = int(row/2)
    c = int(col/2)
    vsqrt = (U ** 2 + V ** 2) ** 0.5
    vsqrt[vsqrt==0] = np.nan # if norm is 0, set it to np.nan to avoid divided by zero warning!
    U = U - np.nanmean(U)
    V = V - np.nanmean(V)
    Ax = U / vsqrt
    Ay = V / vsqrt
    CA = np.ones((r, c))
    CV = np.ones((r, c))
    # pdb.set_trace()
    for xin in range(0, c):
        for yin in range(0, r):
            if xin != 0 or yin != 0:
                CA[yin, xin] = np.nanmean((Ax[0:row-yin, 0:col-xin] * Ax[yin:row, xin:col] + Ay[0:row-yin, 0:col-xin] * Ay[yin:row, xin:col]))
                CV[yin, xin] = np.nanmean((U[0:row-yin, 0:col-xin] * U[yin:row, xin:col] + V[0:row-yin, 0:col-xin] * V[yin:row, xin:col])) / (np.nanstd(U)**2+np.nanstd(V)**2)
    return X[0:r, 0:c] - X[0, 0], Y[0:r, 0:c] - Y[0, 0], CA, CV

def corrI(X, Y, I):
    """
    Compute pixel intensity spatial autocorrelation of an image.

    :param X: x coordinates of image pixels
    :type X: 2d array
    :param Y: y coordinates of image pixels
    :type Y: 2d array
    :param I: image
    :type I: 2d array
    :return: XI, YI, CI, where CI is the autocorrelation map and XI and YI are the corresponding coordinates.
    :rtype: 2d arrays
    """
    row, col = I.shape
    I = I - I.mean()
    # CI = np.ones(I.shape)
    r = int(row/2)
    c = int(col/2)
    CI = np.ones((r, c))
    XI = X[0: r, 0: c]
    YI = Y[0: r, 0: c]
    normalizer = I.std() ** 2
    for xin in range(0, int(col/2)):
        for yin in range(0, int(row/2)):
            if xin != 0 or yin != 0:
                I_shift_x = np.roll(I, xin, axis=1)
                I_shift = np.roll(I_shift_x, yin, axis=0)
                CI[yin, xin] = (I[yin:, xin:] * I_shift[yin:, xin:]).mean() / normalizer
    return XI, YI, CI


def divide_windows(img, windowsize=[20, 20], step=10):
    """
    Divide an image into windows with specified size and step. Size and step can be different, so that we generate a downsampled image with either overlap or gaps.

    :param img: image
    :type img: 2d array
    :param windowsize: window size in x and y
    :type windowsize: list(int)
    :param step: distance between the centers of adjacent windows
    :type step: int
    :return: X,Y,I -- I is the downsampled image, while X, Y are the corresponding coordinates in x an y
    :rtype: 2d arrays
    """
    row, col = img.shape
    windowsize[0] = int(windowsize[0])
    windowsize[1] = int(windowsize[1])
    step = int(step)
    if isinstance(windowsize, list):
        windowsize = tuple(windowsize)
    X = np.array(range(0, col-windowsize[0], step))
    Y = np.array(range(0, row-windowsize[1], step))
    X, Y = np.meshgrid(X, Y)
    I = util.view_as_windows(img, windowsize, step=step).mean(axis=(2, 3))
    return X, Y, I


def distance_corr(X, Y, C):
    """ Convert 2d correlation matrix into 1d.

    :param X,Y: 2d coordinates, can be either 2d matrices or flattened matrices
    :param C: correlation matrix, can be either 2d matrices or flattened matrices
    :return: a DataFrame of ["R", "C"].

    .. rubric:: Edit

    :12162021:
     * check input dimension, if it's 1, do not use `flatten`,
     * add doc string
    """
    if len(X.shape) == 2:
        r_corr = pd.DataFrame({'R': (X.flatten()**2 + Y.flatten()**2) ** 0.5, 'C': C.flatten()}).sort_values(by='R')
    else:
        r_corr = pd.DataFrame({'R': (X**2 + Y**2) ** 0.5, 'C': C}).sort_values(by='R')
    return r_corr



def density_fluctuation(img8):
    """
    This is the first attempt to calculate density fluctuations in bacterial suspensions. There exists 2 methods: i) compute the spatial variation in each image, with respect to various box size, then average over time; ii) compute temporal variation in at different spot, with respect to various box size, then average over space.

    Method implemented in this function is the first one. It turned out that even for a static video, we can easily measure a very strong density fluctuation, which cannot be true. We later realize that, this is due to the intrinsic spatial light variation of the bright field microscopy.

    One way to solve this problem is to subtract the intrinsic variation from the raw images. However, at that time we did not succeed in doing it (as I am writing this document, I konw better how to do it). So we chose the second way: to use method (ii) for the density fluctuation calculation. Different from method (i), method (ii) is not sensitive to the spatial variation in each image, but considers how the intensities evolve over time. Therefore, we can get density fluctuations that make sense.

    .. warning::

        Currently, we deprecate this method. It is not used in our publication *Soft Matter* **17**: 10806–17. https://doi.org/10.1039/D1SM01183A.


    :param img8: 8-bit grayscale image
    :type img8: 2d array
    :return: density fluctuation data, a 2-column table containing the box size (area) "n" and the intensity standard deviation over time "d"

    """
    row, col = img8.shape
    l = min(row, col)
    size_min = 5
    boxsize = np.unique(np.floor(np.logspace(np.log10(size_min), np.log10((l-size_min)/2), 100)))
    # Gradually increase box size and calculate dN=std(I) and N=mean(I)
    # choose maximal box size to be (l-size_min)/2
    # to guarantee we have multiple boxes for each calculation, so that
    # the statistical quantities are meaningful.
    # Step is chosen as 5*size_min to guarantee speed as well as good statistics
    # instead of box size. When box size is large, number of boxes is too small
    # to get good statistics.
    # Papers by Narayan et al. used different method to calculate density fluctuation
    # Igor Aranson commented on the averaging methods saying that in a spatially
    # homogeneous system (small spatial temporal correlation) two methods should match.
    # This suggests that I need to test both methods.

    NList = []
    dNList = []
    for bs in boxsize:
        X, Y, I = divide_windows(img8, windowsize=[bs, bs], step=bs)
        N = bs*bs
        # dN = np.log10(I).std()*bs*bs
        dN = I.std()*bs*bs
        NList.append(N)
        dNList.append(dN)
    df_data = pd.DataFrame().assign(n=NList, d=dNList)
    return df_data


def div_field(img, pivData, winsize, step):
    """
    Compute multiple divergence fields from PIV data and microscopy image.

    :param img: 2d array
    :param pivData: DataFrame with columns (x, y, u, v)
    :param winsize: window size of PIV data
    :param step: step size of PIV data

    .. note::

        :code:`winsize` and :code:`step` should be consistent with the parameters of pivData, be extra coutious!

    :return: divergence fields of given data. (c, v, divcn, divcv, divv). *c* is concentration inferred from the image.


    """
    X, Y, I = divide_windows(img, windowsize=[winsize, winsize], step=step)
    # concentration field
    I0 = 255
    c = I0 - I

    # calculation for divcn and divcv
    row, col = I.shape
    vx = np.array(pivData.u).reshape(I.shape)
    vy = np.array(pivData.v).reshape(I.shape)
    v = (vx**2 + vy**2)**.5
    nx = np.array(pivData.u / (pivData.u**2 + pivData.v**2)**.5).reshape(I.shape)
    ny = np.array(pivData.v / (pivData.u**2 + pivData.v**2)**.5).reshape(I.shape)
    cnx = c * nx
    cny = c * ny
    cvx = c * vx
    cvy = c * vy
    divcn = np.zeros(I.shape)
    divcv = np.zeros(I.shape)
    divv = np.zeros(I.shape)
    for x in range(0, col-1):
        for y in range(0, row-1):
            divcn[y, x] = cnx[y,x+1] - cnx[y,x] + cny[y+1,x] - cny[y,x]
            divcv[y, x] = cvx[y,x+1] - cvx[y,x] + cvy[y+1,x] - cvy[y,x]
            divv[y, x] = vx[y,x+1] - vx[y,x] + vy[y+1,x] - vy[y,x]
    return c, v, divcn, divcv, divv


def df2(imgstack, size_min=5, step=250, method='linear'):
    """
    This is used for small scale test of temporal variation based density fluctuation analysis.
    Here the input is a 3 dimensional array that contains all the images in a video [stack_index, height, width].
    For larger scale application, use the script df2.py or a later implementation of df2 which can take directory as argument 1.

    :param imgstack: 3-D array with dimensions [stack_index, height, width]
    :param size_min: minimal box size to sample
    :param step: distance between adjacent boxes in a frame
    :param method: use pixel intensity directly as concentration ('linear'), or use the log of it ('log')

    :return: the spatial average of temporal variations
    """

    L = min(imgstack.shape[1:3])
    boxsize = np.unique(np.floor(np.logspace(np.log10(size_min),
                        np.log10((L-size_min)/2),100)))

    df = pd.DataFrame()
    for i, img in enumerate(imgstack):
        framedf = pd.DataFrame()
        for bs in boxsize:
            X, Y, I = divide_windows(img, windowsize=[bs, bs], step=step)
            tempdf = pd.DataFrame().assign(I=I.flatten(), t=int(i), size=bs,
                           number=range(0, len(I.flatten())))
            framedf = framedf.append(tempdf)
        df = df.append(framedf)

    if method == 'log':
        df['I'] = np.log(df['I'])

    df_out = pd.DataFrame()
    for number in df.number.drop_duplicates():
        subdata1 = df.loc[df.number==number]
        for s in subdata1['size'].drop_duplicates():
            subdata = subdata1.loc[subdata1['size']==s]

            d = s**2 * np.array(subdata.I).std()
            n = s**2
            tempdf = pd.DataFrame().assign(n=[n], d=d, size=s, number=number)
            df_out = df_out.append(tempdf)

    average = pd.DataFrame()
    for s in df_out['size'].drop_duplicates():
        subdata = df_out.loc[df_out['size']==s]
        avg = subdata.drop(columns=['size', 'number']).mean().to_frame().T
        average = average.append(avg)

    return average

def df2_(img_stack, boxsize=None, size_min=5, step=250):
    """
    Compute number fluctuations of an image stack (3D np.array, frame*h*w)

    :param img_stack: a stack of image, a 3D array
    :param boxsize: a list-like of integers, specify the subsystem size to look at. If None, generate a log spaced array within (size_min, L/2) (pixels), with 100 points
    :param size_min: the smallest box size
    :param step: step used when dividing image into windows

    :return: DataFrame of n and d, where n is box area (px^2) and d is total number fluctuations (box_area*dI)
    """
    L = min(img_stack.shape[1:3])
    if boxsize == None:
        boxsize = np.unique(np.floor(np.logspace(np.log10(size_min), np.log10(L/2), 100)))

    dI_list = []
    for bs in boxsize:
        I = divide_stack(img_stack, winsize=[bs, bs], step=step)
        dI = I.std(axis=0).mean() * bs ** 2
        dI_list.append(dI)

    return pd.DataFrame({'n': np.array(boxsize)**2, 'd': dI_list})

def divide_stack(img_stack, winsize=[50, 50], step=25):
    """
    Divide image stack into several evenly spaced windows of stack. Average the pixel intensity within each window. For example, a 30*30*30 image stack, if we apply a divide_stack, with winsize=[15, 15] and step=15, the resulting divided stack will be (30, 4).

    :param img_stack: a stack of image, a 3D array, axis0 should be frame number
    :param winsize: division scheme, default to [50, 50]
    :param step: division scheme, default ot 25

    :return: the result
    """
    length = img_stack.shape[0]
    divide = util.view_as_windows(img_stack, window_shape=[length, *winsize], step=step).mean(axis=(-1, -2))
    # reshape
    divided_array = divide.reshape((np.prod(divide.shape[:3]), length)).transpose()

    return divided_array

def plot_gnf(gnf_data):
    """
    Used for small scale test of gnf analysis. It incorporates the guide of the eye slope already in the function, which usually needs further adjustment when preparing paper figures.

    :param gnf_data: gnf data generated by df2()

    :return ax: axis on which the data are plotted
    :return slope: the slope of the gnf_data curve
    """
    x = gnf_data.n / 100
    y = gnf_data.d / x ** 0.5
    y = y / y.iat[0]
    fig = plt.figure()
    ax = fig.add_axes([0,0,1,1])
    ax.plot(x, y)
    xf, yf, xt, yt, slope = label_slope(x, y, location='n')
    ax.plot(xf, yf, ls='--', color='black')
    ax.text(xt, yt, '{:.2f}'.format(slope))
    ax.loglog()
    ax.set_xlabel('$l^2/l_b^2$')
    ax.set_ylabel('$\Delta N/\sqrt{N}$')
    return ax, slope

def vorticity(pivData, step=None, shape=None):
    """
    Compute vorticity field based on piv data (x, y, u, v)

    :param pivData: DataFrame of (x, y, u, v)
    :param step: distance (pixel) between adjacent PIV vectors

    :return: vorticity field of the velocity field. unit: [u]/pixel, [u] is the unit of u, usually px/s
    """
    x = pivData.sort_values(by=['x']).x.drop_duplicates()
    if step == None:
        # Need to infer the step size from pivData
        step = x.iat[1] - x.iat[0]

    if shape == None:
        # Need to infer shape from pivData
        y = pivData.y.drop_duplicates()
        shape = (len(y), len(x))

    X = np.array(pivData.x).reshape(shape)
    Y = np.array(pivData.y).reshape(shape)
    U = np.array(pivData.u).reshape(shape)
    V = np.array(pivData.v).reshape(shape)

    dudy = np.gradient(U, step, axis=0)
    dvdx = np.gradient(V, step, axis=1)
    vort = dvdx - dudy

    return vort

def convection(pivData, image, winsize, step=None, shape=None):
    """
    Compute convection term u.grad(c) based on piv data (x, y, u, v) and image.

    :param pivData: -- DataFrame of (x, y, u, v)
    :param image: -- the image corresponding to pivData
    :param winsize: -- coarse-graining scheme of image
    :param step: -- (optional) distance (pixel) between adjacent PIV vectors
    :param shape: -- (optional) shape of piv matrices

    :return: convection term u.grad(c). unit: [u][c]/pixel, [u] is the unit of u, usually px/s, [c] is the unit of concentration measured from image intensity, arbitrary.
    """
    x = pivData.sort_values(by=['x']).x.drop_duplicates()
    if step == None:
        # Need to infer the step size from pivData
        step = x.iat[1] - x.iat[0]

    if shape == None:
        # Need to infer shape from pivData
        y = pivData.y.drop_duplicates()
        shape = (len(y), len(x))

    # check coarse-grained image shape
    X, Y, I = divide_windows(image, windowsize=[winsize, winsize], step=step)
    assert(I.shape==shape)

    X = np.array(pivData.x).reshape(shape)
    Y = np.array(pivData.y).reshape(shape)
    U = np.array(pivData.u).reshape(shape)
    V = np.array(pivData.v).reshape(shape)

    # compute gradient of concentration
    # NOTE: concentration is negatively correlated with intensity.
    # When computing gradient of concentration, the shifting direction should reverse.

    dcx = np.gradient(I, -step, axis=1)
    dcy = np.gradient(I, -step, axis=0)

    udc = U * dcx + V * dcy

    return udc

def divergence(pivData, step=None, shape=None):
    """
    Compute divergence field based on piv data (x, y, u, v)

    :param pivData: DataFrame of (x, y, u, v)
    :param step: distance (pixel) between adjacent PIV vectors

    :return: vorticity field of the velocity field. unit: [u]/pixel, [u] is the unit of u, usually px/s
    """
    x = pivData.sort_values(by=['x']).x.drop_duplicates()
    if step == None:
        # Need to infer the step size from pivData
        step = x.iat[1] - x.iat[0]

    if shape == None:
        # Need to infer shape from pivData
        y = pivData.y.drop_duplicates()
        shape = (len(y), len(x))

    X = np.array(pivData.x).reshape(shape)
    Y = np.array(pivData.y).reshape(shape)
    U = np.array(pivData.u).reshape(shape)
    V = np.array(pivData.v).reshape(shape)

    dudx = np.gradient(U, step, axis=1)
    dvdy = np.gradient(V, step, axis=0)
    div = dudx + dvdy

    return div

def local_df(img_folder, seg_length=50, winsize=50, step=25):
    """
    Compute local density fluctuations of given image sequence in img_folder

    :param img_folder: folder containing .tif image sequence
    :param seg_length: number of frames of each segment of video, for evaluating standard deviations
    :param winsize: window size
    :param step: step between adjacent windows

    :return: dict containing 't' and 'local_df', 't' is a list of time (frame), 'std' is a list of 2d array with local standard deviations corresponding to 't'
    """

    l = readseq(img_folder)
    num_frames = len(l)
    assert(num_frames>seg_length)

    stdL = []
    tL = range(0, num_frames, seg_length)
    for n in tL:
        img_nums = range(n, min(n+seg_length, num_frames))
        l_sub = l.loc[img_nums]
        img_seq = []
        for num, i in l_sub.iterrows():
            img = io.imread(i.Dir)
            X, Y, I = divide_windows(img, windowsize=[50, 50], step=25)
            img_seq.append(I)
        img_stack = np.stack([img_seq], axis=0)
        img_stack = np.squeeze(img_stack)
        std = np.std(img_stack, axis=0)
        stdL.append(std)

    return {'t': tL, 'std': stdL}

def compute_energy_density(pivData, d=25*0.33, MPP=0.33):
    """
    Compute kinetic energy density in k space from piv data. The unit of the return value is [velocity] * [length], where [velocity] is the unit of pivData, and [length] is the unit of sample_spacing parameter. Note, the default value of sampling_spacing does not have any significance. It is just the most convenient value for my first application, and should be set with caution when a different magnification and PIV are used.

    :param pivData: 2D piv data, DataFrame of x, y, u, v
    :param d: sample spacing, in unit of microns
    :param MPP: microns per pixel

    :return: kinetic energy field in wavenumber (k) space

    .. rubric:: Test

    >>> pivData = pd.read_csv(r'E:\\moreData\\08032020\piv_imseq\\01\\3370-3371.csv')
    >>> compute_energy_density(pivData)

    .. rubric:: Edit

    :11020202:
        Add parameter sample_spacing, the distance between adjacent velocity (or data in general. The spacing is used to rescale the DFT so that it has a unit of [velocity] * [length]. In numpy.fft, the standard fft function is defined as

        .. math::

            A_k = \\sum\\limits^{n-1}_{m=0} a_m \\exp \\left[ -2\pi i \\frac{mk}{n} \\right]

        The unit of this Fourier Transform :math:`A_k` is clearly the same as :math:`a_m`. In order to get unit [velocity] * [length], and to make transform result consistent at different data density, I introduce sample_spacing :math:`d` as a modifier of the DFT. After this modification, the energy spectrum computed at various step size (of PIV) should give quantitatively similar results.

    :11042020:
        Replace the (* sample_spacing * sample_spacing) after v_fft with ( / row / col). This overwrites the edit I did on 11022020.

    :11112020: removed ( / row / col), add the area constant in energy_spectrum() function. Details can be found `here <https://zloverty.github.io/research/DF/blogs/energy_spectrum_2_methods_11112020.html>`_

    :11302020:
        *  Convert unit of velocity, add optional arg MPP (microns per pixel);
        * Add * d * d to both velocity FFT's to account for the missing length in default FFT algorithm;
        * The energy spectrum calculated by this function shows a factor of ~3 difference when comparing \int E(k) dk with v**2.sum()/2
    """

    row = len(pivData.y.drop_duplicates())
    col = len(pivData.x.drop_duplicates())
    U = np.array(pivData.u).reshape((row, col)) * MPP
    V = np.array(pivData.v).reshape((row, col)) * MPP

    u_fft = np.fft.fft2(U) * d * d
    v_fft = np.fft.fft2(V) * d * d

    E = (u_fft * u_fft.conjugate() + v_fft * v_fft.conjugate()) / 2

    return E

def compute_wavenumber_field(shape, d):
    """
    Compute the wave number field Kx and Ky, and magnitude field k.
    Note that this function works for even higher dimensional shape.

    :param shape: shape of the velocity field and velocity fft field, tuple
    :param d: sample spacing. This is the distance between adjacent samples, for example, velocities in PIV. The resulting frequency space has the unit which is inverse of the unit of d. The preferred unit of d is um.

    :return:
        * k -- wavenumber magnitude field
        * K -- wavenumber fields in given dimensions

    .. rubric:: Test

    >>> shape = (5, 5)
    >>> k, K = compute_wavenumber_field(shape, 0.2)

    .. rubric:: Edit

    :12022020: multiply 2pi to the wavenumber to account for the built-in 2pi in the fft method. This factor leads to a difference in the magnitude of 1D energy spectra.

        .. note:: The dimensionless wavenumber should remain unchanged.
    """

    for num, length in enumerate(shape):
        kx = np.fft.fftfreq(length, d=d)
        if num == 0:
            k = (kx,)
        else:
            k += (kx,)

    K = np.meshgrid(*k, indexing='ij')

    for num, k1 in enumerate(K):
        if num == 0:
            ksq = k1 ** 2
        else:
            ksq += k1 ** 2

    k_mag = ksq ** 0.5 * 2 * np.pi

    return k_mag, K

def energy_spectrum(pivData, d=25*0.33):
    """
    Compute energy spectrum (E vs k) from pivData.


    :param pivData: piv data
    :param d: sample spacing. This is the distance between adjacent samples, for example, velocities in PIV. The resulting frequency space has the unit which is inverse of the unit of d. The default unit of d is um.

    :return: energy spectrum, DataFrame (k, E)

    .. rubric:: Edit

    :10192020: add argument d as sample spacing
    :11112020: add area constant, see details `here <https://zloverty.github.io/research/DF/blogs/energy_spectrum_2_methods_11112020.html>`_
    :11302020: The energy spectrum calculated by this function shows a factor of ~3 difference when comparing \int E(k) dk with v**2.sum()/2
    """

    row = len(pivData.y.drop_duplicates())
    col = len(pivData.x.drop_duplicates())

    E = compute_energy_density(pivData, d) / (row * d * col * d)
    k, K = compute_wavenumber_field(E.shape, d)

    ind = np.argsort(k.flatten())
    k_plot = k.flatten()[ind]
    E_plot = E.real.flatten()[ind]

    es = pd.DataFrame(data={'k': k_plot, 'E': E_plot})

    return es

def autocorr1d(x, t):
    """Compute the temporal autocorrelation of a 1-D signal.

    :param x: 1-D signal,
    :param t: the corresponding time of the signal, should be np.array 1d
    :return:
        * corr -- correlation array, with lag time as index
        * lagt -- lag time of the correlation function

    .. rubric:: Edit

    :07272022: Handle time series with missing values.
    """
    if any(np.isnan(x)):
        xn = x - np.nanmean(x)
        x2 = np.nanmean(xn * xn)
        c_list = []
        for s in range(0, len(xn)//2):
            xx = np.roll(xn, shift=s)
            xx[:s] = np.nan
            c_list.append(np.nanmean(xn * xx ))
        corr = np.array(c_list) / x2
    else:
        xn = x - np.nanmean(x)
        corr = np.correlate(xn, xn, mode="same")[len(xn)//2:] / np.inner(xn, xn)
    lagt = (t - t[0])[:len(corr)]
    return corr, lagt

def vacf_piv(vstack, dt, mode="direct"):
    """
    Compute averaged vacf from PIV data. This is a wrapper of function autocorr_t(), adding the averaging over all the velocity spots.

    :param vstack: a 2-D np array of velocity data. axis-0 is time and axes-1,2 are spots in velocity field. Usually, this stack can be constracted by `np.stack(u_list)` and then reshape to flatten axes 1 and 2.
    :param dt: time between two data points
    :param mode: the averaging method, can be "direct" or "weighted". "weighted" will use mean velocity as the averaging weight, whereas "direct" uses 1.
    :return: DataFrame of (corr, t)

    .. rubric:: Edit

    :10262022: add condition :code:`x.sum() != 0`, avoids nan in all-zero columns.
    """
    # rearrange vstack
    assert(len(vstack.shape)==3)
    stack_r = vstack.reshape((vstack.shape[0], -1)).T
    # compute autocorrelation
    corr_list = []
    weight = 1
    normalizer = 0
    for x in stack_r:
        if np.isnan(x.sum()) == False and x.sum() != 0: # masked out part has velocity as nan, which cannot be used for correlation computation
            if mode == "weighted":
                weight = abs(x).mean()
            normalizer += weight
            corr = autocorr1d(x) * weight
            corr_list.append(corr)
            print(x.sum(), corr.sum())
    corr_mean = np.stack(corr_list, axis=0).sum(axis=0) / normalizer

    return pd.DataFrame({"c": corr_mean, "t": np.arange(len(corr_mean)) * dt}).set_index("t")

if __name__ == '__main__':
    img = io.imread(r'I:\Github\Python\Correlation\test_images\GNF\stat\40-1.tif')
    df_data = density_fluctuation(img)
