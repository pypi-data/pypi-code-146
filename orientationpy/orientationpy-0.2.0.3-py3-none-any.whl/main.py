"""Orientation analysis"""

import math
import multiprocessing

import numba
import numba_progress
import numpy
import scipy.ndimage
from scipy.interpolate import CubicSpline
from tqdm import tqdm

gradientModes = ["finite_difference", "splines", "gaussian"]
orientationModes = ["fibre", "fiber", "membrane"]
symmetricComponents3d = [[0, 0], [0, 1], [0, 2], [1, 1], [1, 2], [2, 2]]
symmetricComponents2d = [[0, 0], [0, 1], [1, 1]]
nProcessesDefault = multiprocessing.cpu_count()


def _unfoldMatrix(a):
    """
    Takes an array of length 3 or 6 and repacks it into a full symmetric matrix 2x2 or 3x3
    """
    if len(a) == 6:
        m = numpy.empty((3, 3), dtype="<f8")
        symmetricComponents = symmetricComponents3d
    elif len(a) == 3:
        m = numpy.empty((2, 2))
        symmetricComponents = symmetricComponents2d
    # else:
    # return None

    for n, [i, j] in enumerate(symmetricComponents):
        m[i, j] = a[n]
        # if not on diagonal fill in other side
        if i != j:
            m[j, i] = a[n]

    return m


def computeGradient(im, mode="gaussian", mask=None):
    """
    Returns the gradient of passed greylevel image.

    Parameters
    -----------
        im : array_like
            Input greyscale image, 2D or 3Da

        mode : string, optional
            Selects method to compute gradients, can be either "splines", "gaussian" or "finite_difference".
            Default is "gaussian"

    Returns
    --------
        gradients : tuple of arrays
            2 or 3-component tuple of arrays (depending on 2D or 3D input)
            corresponding to (DZ) DY DX
    """
    # The sigma for the gaussian derivative, unlikely to change
    sigma = 1

    im = numpy.squeeze(im)

    twoD = im.ndim == 2

    if mode not in gradientModes:
        raise ValueError(f"{mode} not in allowable options: {gradientModes}")

    if not twoD:
        # Computing derivatives (scipy implementation truncates filter at 4 sigma).
        # 3D case
        if mode == "gaussian":
            Gx = scipy.ndimage.gaussian_filter(im, sigma, order=[0, 0, 1], mode="nearest")
            Gy = scipy.ndimage.gaussian_filter(im, sigma, order=[0, 1, 0], mode="nearest")
            Gz = scipy.ndimage.gaussian_filter(im, sigma, order=[1, 0, 0], mode="nearest")

        elif mode == "splines":
            cs_x = CubicSpline(numpy.linspace(0, im.shape[2] - 1, im.shape[2]), im, axis=2)
            Gx = cs_x(numpy.linspace(0, im.shape[2] - 1, im.shape[2]), 1)

            cs_y = CubicSpline(numpy.linspace(0, im.shape[1] - 1, im.shape[1]), im, axis=1)
            Gy = cs_y(numpy.linspace(0, im.shape[1] - 1, im.shape[1]), 1)

            cs_z = CubicSpline(numpy.linspace(0, im.shape[0] - 1, im.shape[0]), im, axis=0)
            Gz = cs_z(numpy.linspace(0, im.shape[0] - 1, im.shape[0]), 1)

        elif mode == "finite_difference":
            Gz, Gy, Gx = numpy.gradient(im)

        return (Gz, Gy, Gx)

    else:
        # 2D case
        if mode == "gaussian":
            Gx = scipy.ndimage.gaussian_filter(im, sigma, order=[0, 1], mode="nearest")
            Gy = scipy.ndimage.gaussian_filter(im, sigma, order=[1, 0], mode="nearest")

        elif mode == "splines":
            cs_x = CubicSpline(numpy.linspace(0, im.shape[1] - 1, im.shape[1]), im, axis=1)
            Gx = cs_x(numpy.linspace(0, im.shape[1] - 1, im.shape[1]), 1)

            cs_y = CubicSpline(numpy.linspace(0, im.shape[0] - 1, im.shape[0]), im, axis=0)
            Gy = cs_y(numpy.linspace(0, im.shape[0] - 1, im.shape[0]), 1)

        elif mode == "finite_difference":
            Gy, Gx = numpy.gradient(im)

        return (Gy, Gx)


def computeStructureTensor(gradients, sigma, mask=None):
    """
    Computes the structure tensor for every pixel of the image, averaging in a Gaussian window defined by sigma.
    Sigma is a very important parameter defining the spatial scale of interest.

    In 2D the structure tensor is a 2x2 matrix attached to each pixel and in 3D it is a 3x3 matrix, but since this tensor is symmetric
    this matrix is flattened to keep only to top-right half, and so in 2D that makes 3 components to store and
    in 3D that makes 6.
    We save in this flattened format to save memory, but also for pseudo-compatibility with skimage.feature.structure_tensor (they output a list rather than a big array)
    See https://en.wikipedia.org/wiki/Structure_tensor

    Parameters
    -----------
        gradients : tuple of array_like
            Tuple of gradient images from orientationpy.compute_gradient(im),
            This means in the 2D case a tuple of 2x2D arrays of gradients Y, X
            and in the 3D case a tuple of 3x3D arrays of Z, Y, X gradients

        sigma : float
            An integration scale giving the size over the neighbourhood in which the
            orientation is to be analysed.

        mask : boolean array, optional
            Array the same size as one of the gradients, indicating which pixels to include in the computation.

    Returns
    -------
        S : ndarray
            An array containing the computed structure tensor for each pixel.
            Output shape in 2D: 3 x Y x X
            Output shape in 2D: 6 x Z x Y x X
    """

    def multiplyAndFilter(gradients, i, j, sigma):
        return scipy.ndimage.gaussian_filter(numpy.multiply(gradients[i], gradients[j]), sigma, mode="nearest")

    if len(gradients) == 3:  # 3D
        symmetricComponents = symmetricComponents3d
    elif len(gradients) == 2:  # 2D
        symmetricComponents = symmetricComponents2d
    else:
        return None

    # Initializing structureTensor
    structureTensor = numpy.empty((len(symmetricComponents), *gradients[0].shape), dtype=float)

    # Integrating elements of structure tensor (scipy uses sequence of 1D).
    for n, [i, j] in enumerate(symmetricComponents):
        structureTensor[n] = multiplyAndFilter(gradients, i, j, sigma)

    return structureTensor


def computeGradientStructureTensor(im, sigma, mode="gaussian"):
    """
    This function calls `computeGradient` with the mode passed in `mode` and then computes the structure tensor for each pixel (integrating in a Gaussian window of size `sigma`) with `computeStructureTensor` and returns that directly as a 3 x N x M or a 6 x N x M x O array.
    """
    print("Computing gradients...", end="")
    g = computeGradient(im, mode=mode)
    print("done")
    print("Computing structure tensor...", end="")
    st = computeStructureTensor(g, sigma)
    print("done")
    return st


def computeGradientStructureTensorBoxes(im, boxSize, mode="gaussian"):
    """
    This function calls `computeGradient` with the mode passed in `mode` and then computes the structure tensor in touching 2/3D boxes with `computeStructureTensorBoxes` and returns the structure tensor for each box as a flattened 3 x N x M or a 6 x N x M x O array
    """
    print("Computing gradients...", end="")
    g = computeGradient(im, mode=mode)
    print("done")
    print("Computing structure tensor...", end="")
    st = computeStructureTensorBoxes(g, boxSize)
    print("done")
    return st


def computeStructureTensorBoxes(gradients, boxSize, mask=None, returnBoxCenters=False):
    """
    Computes the structure tensor in touching (no gaps and no overlaps) squares/cubes.
    This means first computing it per-pixel and then summing it in boxes.

    In 2D the structure tensor is a 2x2 matrix attached to each pixel and in 3D it is a 3x3 matrix, but since this tensor is symmetric
    this matrix is flattened to keep only to top-right half, and so in 2D that makes 3 components to store and
    in 3D that makes 6.
    We save in this flattened format to save memory, but also for pseudo-compatibility with skimage.feature.structure_tensor (they output a list rather than a big array)
    See https://en.wikipedia.org/wiki/Structure_tensor

    Parameters
    -----------
        gradients : tuple of array_like
            Tuple of gradient images from orientationpy.compute_gradient(im),
            This means in the 2D case a tuple of 2x2D arrays of gradients Y, X
            and in the 3D case a tuple of 3x3D arrays of Z, Y, X gradients

        boxSize : int or tuple
            If int, the box size in pixels in all directions.
            If tuple, should have have as many items as dimensions of the input image, and is the box size,
            in pixels in (Z), Y, X directions

        mask : boolean array, optional
            Array the same size as one of the gradients, indicating which pixels to include in the computation.

        returnBoxCenters : bool, optional
            Return the centers of the boxes?
            Optional, default = False

    Returns
    -------
        structureTensor : ndarray
            An array containing the computed structure tensor for each box.
            Output shape in 2D: 3 x Yboxes x Xboxes
            Output shape in 2D: 6 x Zboxes x Yboxes x Xboxes
    """
    if len(gradients) == 3:
        if type(boxSize) == list or type(boxSize) == tuple:
            if len(boxSize) != 3:
                print(f"computeStructureTensorBoxes(): Received 3D gradients but got len(boxSize) = {len(boxSize)}")
                return
            else:
                boxSizeZYX = boxSize
        else:
            boxSize = int(boxSize)
            boxSizeZYX = (boxSize, boxSize, boxSize)

        # Compute number of boxes, assuming top one at 0,0
        nBoxesZ = gradients[0].shape[0] // boxSizeZYX[0]
        nBoxesY = gradients[0].shape[1] // boxSizeZYX[1]
        nBoxesX = gradients[0].shape[2] // boxSizeZYX[2]

        # New empty variable to fill per-box
        structureTensorBoxes = numpy.empty((6, nBoxesZ, nBoxesY, nBoxesX))

        # Loop over boxes and integrate
        for boxZ in tqdm(range(nBoxesZ)):
            for boxY in range(nBoxesY):
                for boxX in range(nBoxesX):
                    for n, [i, j] in enumerate(symmetricComponents3d):
                        # Compute i, j component of the structure tensor for all pixels in the box
                        structureTensorComponentPixelsInBox = numpy.multiply(
                            gradients[i][boxZ * boxSizeZYX[0] : (boxZ + 1) * boxSizeZYX[0], boxY * boxSizeZYX[1] : (boxY + 1) * boxSizeZYX[1], boxX * boxSizeZYX[2] : (boxX + 1) * boxSizeZYX[2]],
                            gradients[j][boxZ * boxSizeZYX[0] : (boxZ + 1) * boxSizeZYX[0], boxY * boxSizeZYX[1] : (boxY + 1) * boxSizeZYX[1], boxX * boxSizeZYX[2] : (boxX + 1) * boxSizeZYX[2]],
                        )

                        # Average it into the value for this box
                        structureTensorBoxes[n, boxZ, boxY, boxX] = numpy.mean(structureTensorComponentPixelsInBox)

        if returnBoxCenters:
            print("returnBoxCenters not yet implemented, just returning ST")
            return structureTensorBoxes
        else:
            return structureTensorBoxes

    elif len(gradients) == 2:
        # Check box sizes is either a two-element list or a single int
        if type(boxSize) == list or type(boxSize) == tuple:
            if len(boxSize) != 2:
                print(f"computeStructureTensorBoxes(): Received 2D gradients but got len(boxSize) = {len(boxSize)}")
                return
            else:
                boxSizeYX = boxSize
        else:
            boxSize = int(boxSize)
            boxSizeYX = (boxSize, boxSize)

        # Compute number of boxes, assuming top one at 0,0
        nBoxesY = gradients[0].shape[0] // boxSizeYX[0]
        nBoxesX = gradients[0].shape[1] // boxSizeYX[1]

        # New empty variable to fill per-box
        structureTensorBoxes = numpy.empty((3, nBoxesY, nBoxesX))

        # Loop over boxes and integrate
        for boxY in tqdm(range(nBoxesY)):
            for boxX in range(nBoxesX):
                for n, [i, j] in enumerate(symmetricComponents2d):
                    # Compute i, j component of the structure tensor for all pixels in the box
                    structureTensorComponentPixelsInBox = numpy.multiply(
                        gradients[i][boxY * boxSizeYX[0] : (boxY + 1) * boxSizeYX[0], boxX * boxSizeYX[1] : (boxX + 1) * boxSizeYX[1]],
                        gradients[j][boxY * boxSizeYX[0] : (boxY + 1) * boxSizeYX[0], boxX * boxSizeYX[1] : (boxX + 1) * boxSizeYX[1]],
                    )
                    # Average it!
                    structureTensorBoxes[n, boxY, boxX] = numpy.mean(structureTensorComponentPixelsInBox)

        if returnBoxCenters:
            print("returnBoxCenters not yet implemented, just returning ST")
            return structureTensorBoxes
        else:
            return structureTensorBoxes
    else:
        print(f"computeStructureTensorBoxes(): Unknown number of gradient dimensions: {len(gradients)}")


@numba.njit(parallel=True)
def orientationFunction(structureTensor, progressProxy, fibre=True, computeEnergy=False, computeCoherency=False):
    symmetricComponents3d = [[0, 0], [0, 1], [0, 2], [1, 1], [1, 2], [2, 2]]

    theta = numpy.zeros(structureTensor.shape[1:], dtype="<f4")
    phi = numpy.zeros(structureTensor.shape[1:], dtype="<f4")

    energy = numpy.zeros(structureTensor.shape[1:], dtype="<f4")
    coherency = numpy.zeros(structureTensor.shape[1:], dtype="<f4")

    # if computeEnergy:
    # energy = numpy.zeros(structureTensor.shape[1:], dtype=float)
    # else:
    # energy = None

    # if computeCoherency:
    # coherency = numpy.zeros(structureTensor.shape[1:], dtype="<f4)"
    # else:
    # coherency = None

    for z in numba.prange(0, structureTensor.shape[1]):
        for y in range(0, structureTensor.shape[2]):
            for x in range(0, structureTensor.shape[3]):
                structureTensorLocal = numpy.empty((3, 3), dtype="<f4")
                for n, [i, j] in enumerate(symmetricComponents3d):
                    structureTensorLocal[i, j] = structureTensor[n, z, y, x]
                    # if not on diagonal fill in other side
                    if i != j:
                        structureTensorLocal[j, i] = structureTensor[n, z, y, x]

                w, v = numpy.linalg.eig(structureTensorLocal)
                if not fibre:
                    m = numpy.argmax(w)
                else:  # (mode == "fibre")
                    # m = numpy.argmin(w, axis=0)
                    m = numpy.argmin(w)

                selectedEigenVector = v[:, m]

                # Flip over -z
                if selectedEigenVector[0] < 0:
                    selectedEigenVector *= -1

                # polar angle
                theta[z, y, x] = numpy.rad2deg(math.acos(numpy.abs(selectedEigenVector[0])))
                # azimuthal angle
                phi[z, y, x] = numpy.rad2deg(math.atan2(selectedEigenVector[1], selectedEigenVector[2]))
                if phi[z, y, x] < 0:
                    phi[z, y, x] += 360
                elif phi[z, y, x] >= 360:
                    phi[z, y, x] -= 360

                if computeEnergy:
                    energy[z, y, x] = numpy.trace(structureTensorLocal)

                if computeCoherency:
                    evalMin = numpy.min(w)
                    evalMid = numpy.median(w)
                    evalMax = numpy.max(w)
                    # print(evalMin, evalMid, evalMax)
                    if not fibre:
                        bothAvg = (evalMid + evalMin) / 2
                        coherency[z, y, x] = (evalMax - bothAvg) / (evalMax + bothAvg)
                    else:  # Fibers
                        bothAvg = (evalMax + evalMid) / 2
                        coherency[z, y, x] = (bothAvg - evalMin) / (bothAvg + evalMin)
        progressProxy.update(1)

    return theta, phi, energy, coherency


def computeOrientation(structureTensor, mode="fibre", computeEnergy=False, computeCoherency=False, nProcesses=nProcessesDefault):
    """
    Takes in a pre-computed field of Structure Tensors and returns orientations, and optionally
    energies (strength of the orientation signal) and coherency (local strength of alignment), in that order

    Parameters
    -----------
        structureTensor : numpy array
            2D or 3D structureTensor array from computeStructureTensor() or computeStructureTensorBoxes()

        mode : string, optional
            What mode to use for orientations -- N.B., this is only relevant in 3D.
            Are you looking for a "fibre" (1D object) or "membrane" (2D object)?
            Default = "fibre"

        computeEnergy : bool, optional
            Returns an array of the "energy" for each point
            Default = False

        computeCoherency : bool, optional
            Returns an array of the "coherency" for each point
            Default = False

    Returns
    --------
        A dictionary containing:
          - theta

        if computeEnergy and computeCoherency are False, then an array the same as the last 2 dimensions in 2D and last 3 dimensions in 3D of the passed structureTensor is returned, with orientations

        if either are true, a list contining, in order:

            - orientation
            - energy if requested
            - coherency if requested
    """
    outputDict = {}

    if mode not in orientationModes:
        raise ValueError(f"orientation mode {mode} not in supported modes: {orientationModes}")

    if len(structureTensor.shape) == 4:
        # We're in 3D!
        assert structureTensor.shape[0] == 6

        # return [z, [thetaL, phiL], energyL, coherencyL]
        with numba_progress.ProgressBar(total=structureTensor.shape[1]) as progress:
            theta, phi, energy, coherency = orientationFunction(
                structureTensor,
                progress,
                fibre=not (mode == "membrane"),
                computeEnergy=computeEnergy,
                computeCoherency=computeCoherency,
            )

        outputDict["theta"] = theta
        outputDict["phi"] = phi
        outputDict["energy"] = energy
        outputDict["coherency"] = coherency

        return outputDict

    elif len(structureTensor.shape) == 3:
        # We're in 2D!
        assert structureTensor.shape[0] == 3

        if mode == "membrane":
            raise ValueError(f"membrane doesn't exist in 2D")

        outputDict["theta"] = numpy.rad2deg(1 / 2 * numpy.arctan2(structureTensor[1, :, :] + structureTensor[1, :, :], structureTensor[0, :, :] - structureTensor[2, :, :]))

        if computeEnergy:
            outputDict["energy"] = structureTensor[0] + structureTensor[2]

        if computeCoherency:
            evalues, _ = _decomposeStructureTensor(structureTensor)
            # Selecting the min and the max eigenvalues for each voxel position
            max_eigenvalue = numpy.max(evalues, axis=0)
            min_eigenvalue = numpy.min(evalues, axis=0)

            # Computing the coherency
            outputDict["coherency"] = (max_eigenvalue - min_eigenvalue) / (max_eigenvalue + min_eigenvalue)

        return outputDict

    else:
        raise ValueError(f"structure tensor has unexpected shape {len(structureTensor)}, should be 3 for 2D and 4 for 3D")


def anglesToVectors(orientations):
    """
    Takes in angles in degrees and returns corresponding unit vectors in Z Y X.

    Parameters
    ----------
        orientations : dictionary
            Dictionary containing a numpy array of  'theta' in degrees in 2D,
            and also a numpy array of 'phi' if 3D.

    Returns
    -------
        unitVectors : 2 or 3 x N x M (x O)
            YX or ZYX unit vectors
    """
    if type(orientations) is not dict:
        raise TypeError(f"dictionary with 'theta' (and optionally 'phi') key needed, you passed a {type(orientations)}")

    if "phi" in orientations.keys():
        # print("orientationAngleToOrientationVector(): 3D!")
        theta = numpy.deg2rad(orientations["theta"])
        phi = numpy.deg2rad(orientations["phi"])
        coordsZYX = numpy.zeros(
            (
                3,
                theta.shape[0],
                theta.shape[1],
                theta.shape[2],
            )
        )
        coordsZYX[2, :, :] = numpy.sin(theta) * numpy.cos(phi)
        coordsZYX[1, :, :] = numpy.sin(theta) * numpy.sin(phi)
        coordsZYX[0, :, :] = numpy.cos(theta)

        return coordsZYX
    # if type(orientations) == numpy.array:
    elif "theta" in orientations.keys():
        # print("orientationAngleToOrientationVector(): 2D!")
        # 2D case
        coordsYX = numpy.zeros(
            (
                2,
                orientations["theta"].shape[0],
                orientations["theta"].shape[1],
            )
        )

        coordsYX[0] = -numpy.sin(numpy.deg2rad(orientations["theta"]))
        coordsYX[1] = numpy.cos(numpy.deg2rad(orientations["theta"]))

        return coordsYX

    else:
        raise KeyError("couldn't find 'theta' (and optionally 'phi') key in passed orientations")


def _decomposeStructureTensor(structureTensor):
    """
    Returns the structure tensor of input structure tensor.
    Note: this function only works for 3D and 2D image data

    Parameters
    -----------
        structure_tensor : Array of shape (2/3, 2/3, ...)
            The second moment matrix of the im that you want to calculate
            the orientation of.

    Returns
    -------
        eigenvalues : Array of shape (..., M)
            The eigenvalues, each repeated according to its multiplicity.
            The eigenvalues are not necessarily ordered. The resulting
            array will be of complex type, unless the imaginary part is
            zero in which case it will be cast to a real type. When `structure_tensor`
            is real the resulting eigenvalues will be real (0 imaginary
            part) or occur in conjugate pairs

        eigenvectors : (..., M, M) array
            The normalized (unit "length") eigenvectors, such that the
            column ``eigenvectors[:,i]`` is the eigenvector corresponding to the
            eigenvalue ``eigenvalues[i]``.

    Notes
    -----
        Built upon the numpy.linalg.eig function, for more information:
        https://github.com/numpy/numpy/blob/v1.23.0/numpy/linalg/linalg.py#L1182-L1328
    """

    # 2D
    if len(structureTensor.shape) == 3:
        assert structureTensor.shape[0] == 3
        # Initializing eigen images
        eigenvectors = numpy.zeros(shape=(2, 2, structureTensor.shape[1], structureTensor.shape[2]))
        eigenvalues = numpy.zeros(shape=(2, structureTensor.shape[1], structureTensor.shape[2]))
        for y in range(0, structureTensor.shape[1]):
            for x in range(0, structureTensor.shape[2]):
                eigenvalues[:, y, x], eigenvectors[:, :, y, x] = numpy.linalg.eig(_unfoldMatrix(structureTensor[:, y, x]))
    # else:
    # print(f"_decomposeStructureTensor(): Passed structure tensor has {len(structureTensor.shape)} dimensions, don't know what to do")

    return eigenvalues, eigenvectors
