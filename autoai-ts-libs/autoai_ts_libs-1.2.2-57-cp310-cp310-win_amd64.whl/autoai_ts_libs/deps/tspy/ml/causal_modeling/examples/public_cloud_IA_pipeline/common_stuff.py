#  /************** Begin Copyright - Do not add comments here **************
#   * Licensed Materials - Property of IBM
#   *
#   *   OCO Source Materials
#   *
#   *   (C) Copyright IBM Corp. 2020, All Rights Reserved
#   *
#   * The source code for this program is not published or other-
#   * wise divested of its trade secrets, irrespective of what has
#   * been deposited with the U.S. Copyright Office.
#   ***************************** End Copyright ****************************/
""" Useful routines for the Incident-Alert Pipeline and Demo """

import matplotlib.colors
import matplotlib.pyplot as plt
import numpy as np

# Keys used to store features in hdf5 files
# These are taken from surrogate/surrogate/surrogate_common.py to keep things consistent
TRAINSET_X_KEY = 'X_train'
TRAINSET_Y_KEY = 'Y_train'
TRAINSET_Y_ORIG_KEY = 'Y_train_original'
TRAINSET_FILENAMES = 'trainset_filenames'
TRAINSET_DESCR_KEY = 'X_train_descr'
TRAINSET_Y_DESCR_KEY = 'Y_train_descr'
TRAINSET_SIMID = 'trainset_simid'
TRAINSET_JID = 'trainset_jrnlid'
DEVSET_X_KEY = 'X_dev'
DEVSET_Y_KEY = 'Y_dev'
DEVSET_Y_ORIG_KEY = 'Y_dev_original'
DEVSET_FILENAMES = 'devset_filenames'
DEVSET_SIMID = 'devset_simid'
DEVSET_JID = 'devset_jrnlid'
METASET_X_KEY = 'X_meta'
METASET_Y_KEY = 'Y_meta'
METASET_Y_ORIG_KEY = 'Y_meta_original'
METASET_FILENAMES = 'metaset_filenames'
METASET_SIMID = 'metaset_simid'
METASET_JID = 'metaset_jrnlid'
TESTSET_X_KEY = 'X_test'
TESTSET_Y_KEY = 'Y_test'
TESTSET_Y_ORIG_KEY = 'Y_test_original'
TESTSET_FILENAMES = 'testset_filenames'
TESTSET_SIMID = 'testset_simid'
TESTSET_JID = 'testset_jrnlid'
X_STDSCALER = 'x_stdscalerobj'
INP_STDSCALER = 'inp_stdscalerobj'
INP_STDDIMS = 'inp_stddims'
WORD_EMBED_LOOKUP = 'word_embed_lookup'
W2V_WEMB_INDEX = 'w2v_index'
W2V_WEMB_DATA = 'w2v_data'

ZEROPAD_TOKEN = -1  # used in feature extraction to denote "no alert"

def generate_data_definition(descr, embed_dims, proj_dims=None):
    """
    From a 'out_descr' object (list) loaded from input h5, generate 'out_descr' object (list) consumable by
    regression_encoder_decoder_v1.build_model_graph()
    :param descr: list with tuples (as loaded from h5)
    :param embed_dims: list with desired embedding dimensions (count must match stuff in out_descr)
    :param proj_dims:  list with desired projection dims
    :return: list with definitions
    """
    data_def = []
    proj_dims = proj_dims or []
    edimi = iter(embed_dims)
    projdi = iter(proj_dims)
    for ds in descr:
        assert (len(ds) == 2 or len(ds) == 3)
        assert (isinstance(ds[0], str) and isinstance(ds[1], int))
        if ds[0] == 'discrete':
            edim = next(edimi, None)
            if edim is None:
                raise RuntimeError("ERROR: count of embedding dims (%s) does not match source data \'%s\'"
                                   % (",".join([str(i) for i in embed_dims]), ", ".join([str(i[0]) + "/" + str(i[1]) for i in descr])))
            data_def.append(('emb', ds[1], edim))
        elif ds[0] == 'vector':
            projd = next(projdi, None)
            data_def.append(('vec', ds[1], projd))
    return data_def


def get_total_input_dim(raw_input_def):
    d = 0
    for (_, _, v) in raw_input_def:
        d += v
    return d


def show_3D_scatter(X, title="", which_norm=None, dotsize=20):
    """
    3D scatter
    :param X: [nsamp, 3] with coords
    :param which_norm: None or 'log'
    :return:  void
    """
    plt.rcParams['figure.figsize'] = (10, 8)
    fig = plt.figure()
    plt.clf()
    ax1 = fig.add_subplot(111, projection='3d')
    # set darker background
    plt.gca().patch.set_facecolor('white')
    if which_norm is not None and which_norm == 'log':
        cum_which_norm = matplotlib.colors.LogNorm
    else:
        cum_which_norm = matplotlib.colors.Normalize
    cax = ax1.scatter(X[:, 2], X[:, 1], X[:, 0], cmap=plt.jet(), marker='s', s=dotsize, norm=cum_which_norm())
    ax1.w_xaxis.set_pane_color((0.8, 0.8, 0.8, 1.0))
    ax1.w_yaxis.set_pane_color((0.8, 0.8, 0.8, 1.0))
    ax1.w_zaxis.set_pane_color((0.8, 0.8, 0.8, 1.0))
    # cbar = fig.colorbar(cax)
    plt.title(title)
    plt.show()

def show_3D_scatter_color(X, labels, title="", dotsize=20):
    """
    3D scatter
    :param X: [nsamp, 3] with coords
    :param labels: array int with labels (same length as X)
    :param which_norm: None or 'log'
    :return:  void
    """
    plt.rcParams['figure.figsize'] = (10, 8)
    fig = plt.figure()
    plt.clf()
    ax1 = fig.add_subplot(111, projection='3d')
    # set darker background
#     plt.gca().patch.set_facecolor('white')
#     if which_norm is not None and which_norm == 'log':
#         cum_which_norm = matplotlib.colors.LogNorm
#     else:
#         cum_which_norm = matplotlib.colors.Normalize
    colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
    for ci, cl in enumerate(range(np.max(labels))):
        I = np.where(labels == cl)[0]
        x = X[I]
        cax = ax1.scatter(x[:, 2], x[:, 1], x[:, 0], color=colors[ci], marker='.', s=dotsize)
#     ax1.w_xaxis.set_pane_color((0.8, 0.8, 0.8, 1.0))
#     ax1.w_yaxis.set_pane_color((0.8, 0.8, 0.8, 1.0))
#     ax1.w_zaxis.set_pane_color((0.8, 0.8, 0.8, 1.0))
#     cbar = fig.colorbar(cax)
    plt.title(title)
    plt.show()
