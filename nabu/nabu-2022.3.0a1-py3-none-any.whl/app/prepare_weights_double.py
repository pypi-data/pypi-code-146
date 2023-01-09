import h5py
import numpy as np
from scipy.special import erf  # pylint: disable=all
from scipy.special import erf
import sys
import os
from scipy.ndimage import gaussian_filter


def main():
    """auxiliary program that can be called to create  default input detector profiles, for nabu helical,
    concerning the weights of the pixels and the "double flat" renormalisation denominator.
    The result is an hdf5 file that can be used as a "processes" nabu file and is used by nabu-helical.
    In particulars cases the user may have fancy masks and correction map and will provide its own processes file,
    and will not need this.

    This code, and in particular the auxiliary function below (that by the way tomwer can use)
    provide a default construction of such maps. The double-flat is set to one and
    the weight is build on the basis of the flat fields   from the dataset with an apodisation on the borders
    which allows to eliminate discontinuities in the contributions from the borders, above and below
    for the z-translations, and on the left or roght border for half-tomo.

    The usage is ::

       nabu-helical-prepare-weights-double nexus_file_name entry_name

    Then the resulting file can be used as processes file in the configuration file of nabu-helical

    """
    if len(sys.argv) not in [3, 4]:
        message = f""" Usage:
            {os.path.basename(sys.argv[0])}   nexus_file_name entry_name [target file name]
        """
        print(message)
        sys.exit(1)

    file_name = sys.argv[1]
    entry_name = sys.argv[2]
    if len(sys.argv) != 4:
        process_file_name = "double.h5"
    else:
        process_file_name = sys.argv[3]

    f = h5py.File(file_name, "r")

    im_keys = f[entry_name]["data/image_key"][()]
    which_slices = list(np.where(np.equal(im_keys, 1))[0])
    mappe = np.array([f[entry_name]["data/data"][i] for i in which_slices])
    mappe = mappe.sum(0)
    f.close()

    create_heli_maps(mappe, process_file_name, entry_name)


def create_heli_maps(profile, process_file_name, entry_name):
    profile = profile / profile.max()
    profile = profile.astype("f")

    profile = gaussian_filter(profile, 10)

    if os.path.exists(process_file_name):
        fd = h5py.File(process_file_name, "r+")
    else:
        fd = h5py.File(process_file_name, "w")

    def f(L, m, w):

        x = np.arange(L)

        d = (x - L + m).astype("f")
        res_r = (1 - erf(d / w)) / 2

        d = (x - m).astype("f")
        res_l = (1 + erf(d / w)) / 2

        return res_r * res_l

    border = f(profile.shape[1], 20, 13.33)

    path_weights = entry_name + "/weights_field/results/data"
    path_double = entry_name + "/double_flatfield/results/data"

    if path_weights in fd:
        del fd[path_weights]
    if path_double in fd:
        del fd[path_double]

    fd[path_weights] = profile * border
    fd[path_double] = np.ones_like(profile)
