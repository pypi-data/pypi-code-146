import numpy as np

class Environment():
    def __init__(self, config, dataObj):
        self.param_U = np.zeros((dataObj.n_items, config.get_latent_feature_dim()))
        self.param_V = np.zeros((dataObj.n_items, config.get_latent_feature_dim()))