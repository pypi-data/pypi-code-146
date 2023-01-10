import numpy as np
from creek.tools import apply_func_to_index, fanout_and_flatten
import umap
import umap.plot
from functools import partial
from odat.mdat.vacuum import (
    DFLT_CHUNKER,
    DFLT_FEATURIZER,
)


chunker = DFLT_CHUNKER
featurizer = DFLT_FEATURIZER


def store_to_key_fvs(wf_store, chunker=DFLT_CHUNKER, featurizer=DFLT_FEATURIZER):
    wf_items = wf_store.items()
    key_chk_tuples = fanout_and_flatten(wf_items, chunker, 1)
    featurizer_iter = partial(apply_func_to_index, apply_to_idx=1, func=featurizer)
    yield from map(featurizer_iter, key_chk_tuples)


def key_fvs_to_tag_fvs(key_fvs, annots_df):
    func = partial(key_to_tag_from_annots, annots_df=annots_df)
    tagger = partial(apply_func_to_index, apply_to_idx=0, func=func)

    yield from map(tagger, key_fvs)


def key_to_tag_from_annots(key, annots_df):
    tag = annots_df['tag'][annots_df['key'] == key].values[0]
    return tag


def mk_Xy(tag_fv_iterator):
    y, X = zip(*list(tag_fv_iterator))
    return np.array(X), y


def preprocess(X_train):

    from shaded.chained_spectral_projector import learn_chain_proj_matrix

    proj_matrix = learn_chain_proj_matrix(X_train)
    X_train_proj = np.dot(X_train, proj_matrix)

    return proj_matrix, X_train_proj


def plot_umap(X, y, show_legend=True):
    mapper = umap.UMAP().fit(X)
    umap.plot.points(mapper, labels=np.array(y), show_legend=show_legend)
