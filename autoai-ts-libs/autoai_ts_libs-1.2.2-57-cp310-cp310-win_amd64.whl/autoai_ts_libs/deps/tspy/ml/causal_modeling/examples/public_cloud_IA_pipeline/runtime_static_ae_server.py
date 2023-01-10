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
"""
Runtime of the static embedder of Oculus alerts. Used only as a baseline in experiments.
"""

import tensorflow._api.v2.compat.v1 as tf
tf.disable_v2_behavior()
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)
from regression_encoder_decoder_ae_oh import regression_encoder_decoder_ae_oh
from static_autoencoder_graph_oh import static_autoencoder_oh
import common_stuff as com
import app_adapter_oculus_features as fe
import pickle
import numpy as np
import tflearn

class RuntimeStaticAEServer:
    def __init__(self, modelfn, layer_sizes, dropout_prob, l2_weight, dicts_fn,
                 fea_descr, verbose=True, encoder_version='v2', timefield='updateTime', idfield='id'):
        self.layer_sizes = layer_sizes
        self.l2_weight = l2_weight
        self.modelfn = modelfn
        self.X_descr = fea_descr
        self.dicts_fn = dicts_fn
        self.dropout_prob = dropout_prob
        self.dicts = None
        self.tokenize_func = fe.my_tokenize
        self.verbose = verbose
        self.timefield = timefield
        self.idfield = idfield
        self.encoder_version = encoder_version
        self.static_encoder_func = fe.encode_one_oculus_alert_v4
        self.DNNmodel = None
        self.graph = None
        # Initialize feature extractor:
        # --> load dicts
        with open(self.dicts_fn, 'rb') as f:
            self.dicts = pickle.load(f)
            if self.verbose: print("INFO: Read dictionaries from %s" % dicts_fn)

        # initialize model graph
        ae = static_autoencoder_oh(self.X_descr)
        self.DNNmodel, self.graph = ae.get_model_graph(self.layer_sizes, dropoutp=self.dropout_prob,
                                             tensorboard_dir='/dev/null', checkpoint_path='/dev/null',
                                             which_loss='CE')
        with self.graph.as_default():
            print("INFO: loading model from %s" % self.modelfn)
            self.DNNmodel.load(self.modelfn)

    def _json_to_vec(self, json_input):
        alerts = sorted(json_input, key=lambda i: i[self.timefield]['epoch_time'])
        alerts = json_input
        # generate descr
        _, aux_X_descr = self.static_encoder_func(alerts[0], master_dict=self.dicts,
                                                  text_preproc_fct=self.tokenize_func, generate_descr=True)
        assert(aux_X_descr, self.X_descr), "ERROR: feature encoder discrepancy?"
        # process entire batch
        F = []
        info = []
        timeids = []
        for c, h in enumerate(alerts):
            f = self.static_encoder_func(h, master_dict=self.dicts, text_preproc_fct=self.tokenize_func, generate_descr=False)
            F.append(f)
            info.append((h[self.idfield], h[self.timefield]))
            timeids.append(c)
        return F, info, timeids

    def _get_feed(self, fea_vec):
        return static_autoencoder_oh.create_input_feed_list(self.X_descr, fea_vec)

    def _get_output_probs(self, X_feed):
        preds = self.DNNmodel.predict(X_feed)
        predsp = np.exp(preds)
        predsp /= np.expand_dims(np.sum(predsp, axis=-1), axis=-1)
        return predsp

    def _get_embeddings(self, X_feed):
        with self.graph.as_default():
            feed_dict = tflearn.utils.feed_dict_builder(X_feed, None, self.DNNmodel.inputs, None)
            bottleneck = self.DNNmodel.session.run(tf.get_collection(tf.GraphKeys.BOTTLENECK), feed_dict=feed_dict)[0]
        return bottleneck

    def get_embeddings(self, json_inp):
        X, info, timeids = self._json_to_vec(json_inp)
        X = np.asarray(X)
        X_feed = self._get_feed(X)
        return self._get_embeddings(X_feed), np.asarray(info), timeids

    # def get_oh_encodings(self, json_inp):
    #     X, _, info, timeids = self._json_to_vec(json_inp)
    #     X_oh = np.concatenate(self._get_feed(X), axis=-1)[:,0,:]   # taking the leading vector of the RNN window as the encoding
    #     return X_oh, info, timeids

