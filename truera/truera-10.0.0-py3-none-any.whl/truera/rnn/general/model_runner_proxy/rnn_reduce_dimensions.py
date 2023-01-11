from model_runner_proxy.mem_utils import load_memmap
from model_runner_proxy.mem_utils import save_memmap
from MulticoreTSNE import MulticoreTSNE
import numpy as np
from sklearn.decomposition import PCA
from utils import log


def reduce_dim(path, layer, config_args):
    lengths = load_memmap(path, 'output_lengths')
    attrs_per_timestep = load_memmap(path, layer + '_attrs_per_timestep')
    attrs_last_pca_per_class = []
    attrs_last_tsne_per_class = []
    for i in range(config_args.num_classes):
        attrs_last = np.array(
            [
                p[:, :, int(l) - 1, i].sum(0)
                for p, l in zip(attrs_per_timestep, lengths)
            ]
        )
        log.info('Calculating PCA for class {}.'.format(i))
        attrs_last_pca = PCA(n_components=3,
                             whiten=True).fit_transform(attrs_last)
        attrs_last_pca_per_class.append(attrs_last_pca)
        log.info('Calculating TSNE for class {}.'.format(i))
        attrs_last_tsne = MulticoreTSNE(
            n_jobs=2, perplexity=50, n_components=2
        ).fit_transform(attrs_last)
        attrs_last_tsne_per_class.append(attrs_last_tsne)
    attrs_last_pca_per_class = np.expand_dims(
        np.stack(attrs_last_pca_per_class, 1), 0
    )
    attrs_last_tsne_per_class = np.expand_dims(
        np.stack(attrs_last_tsne_per_class, 1), 0
    )
    save_memmap(path, layer + '_attrs_last_pca', attrs_last_pca_per_class)
    save_memmap(path, layer + '_attrs_last_tsne', attrs_last_tsne_per_class)
