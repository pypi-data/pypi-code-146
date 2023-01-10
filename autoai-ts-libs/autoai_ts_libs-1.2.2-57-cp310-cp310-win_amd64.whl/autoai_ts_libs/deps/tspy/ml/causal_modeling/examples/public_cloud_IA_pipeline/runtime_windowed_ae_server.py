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
Class to encode raw sequence of Oculus alerts, via the dynamic AE embedder (Tensorflow), to a set of dynamic vectors
This class hides from the user the complexity of the TF model and preprocessing.
"""
from regression_encoder_decoder_ae_oh import regression_encoder_decoder_ae_oh
import app_adapter_oculus_features as fe
import autoai_ts_libs.deps.tspy.ml.causal_modeling.algorithms.csd_input_adapters as csd_input_adapters
import numpy as np
import tflearn
import tensorflow as tf
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

class RuntimeWindowedAEServer:
    def __init__(self, modelfn, num_layers, cell_size, seq_length, l2_weight, fea_dim, fea_descr, dicts_fn,
                 time_resolution,
                 timefield='createTime', timeparsestr='%Y-%m-%dT%H:%M:%SZ', verbose=True,
                 encoder_version='v2'):
        self.num_layers = num_layers
        self.cell_size = cell_size
        self.l2_weight = l2_weight
        self.modelfn = modelfn
        self.X_descr = fea_descr
        self.seq_len = seq_length
        self.fea_dim = fea_dim
        self.dicts_fn = dicts_fn
        self.dicts = None
        self.timefield = timefield
        self.time_resolution = time_resolution
        self.timeparsestr = timeparsestr
        self.verbose = verbose
        self.encoder_version = encoder_version
        # Initialize feature extractor:
        self.fea_encoder = fe.appAdapterOculusFeatures(feature_version=self.encoder_version, verbose=self.verbose)
        self.fea_encoder.load(self.dicts_fn)
        if self.verbose: print("INFO: Feature encoder initialized.")

        # initialize model graph
        self.ae = regression_encoder_decoder_ae_oh(self.seq_len, self.X_descr, seq2seq_model='basic_rnn',
                                                   l2_weight=self.l2_weight, verbose=self.verbose)
        self.DNNmodel, self.graph = self.ae.get_model_graph(mode="predict", num_layers=num_layers, cell_size=cell_size,
                                             tensorboard_dir='/dev/null', checkpoint_path='/dev/null')
        with self.graph.as_default():
            if self.verbose: print("INFO: loading model from %s" % self.modelfn)
            self.DNNmodel.load(self.modelfn)

    def _json_to_vec(self, json_input):
        # Step 1: Encode timestamped events (CSD360 adapter class)
        assert(self.fea_encoder is not None)
        alert_feavecs, alert_ids, alert_encoding_descr = self.fea_encoder.encode(alerts=json_input)
        assert (len(alert_feavecs) == len(json_input))
        # Step 1.1: grab the corresponding timestamps
        alert_timestamps = [float(i[self.timefield]['epoch_time']) for i in json_input]
        # Step 2: time to equidistant (CSD360 class)
        # Step 2.1. Generate zeropadding object to indicate "no alert"
        # we add extra element in each set
        # so cardinality of the dicts has to be incremented
        zero_pad_code = [i[1] for i in alert_encoding_descr]
        # and change the descr to reflect the increase
        new_alert_encoding_descr = [(i[0], i[1] + 1) for i in alert_encoding_descr]
        ts2te = csd_input_adapters.timeStampedToTimeEquidistant(time_resolution=self.time_resolution,
                                                                padding_object=zero_pad_code,
                bucket_assignment_func=csd_input_adapters.timeStampedToTimeEquidistant._min_distance_bucket_assignment_function,
                reconciliation_func=csd_input_adapters.timeStampedToTimeEquidistant._default_reconciliation_function,
                verbose=self.verbose)
        feavecs, feavecs_timestamps, feavecs_origidx = ts2te.transform(events=alert_feavecs,
                                                                       timestamp_list=alert_timestamps,
                                                                       drop_n_consecutive_paddings=2*self.seq_len)
        # Step 3: windowing (CSD360 class)
        if self.verbose: print("INFO: Windowing features...")
        te2win = csd_input_adapters.timeEquidistantToWindowed(wlen=self.seq_len,
                                padding_mode=csd_input_adapters.timeEquidistantToWindowed.PADDING_MODE_TAILPADDING,
                                verbose=self.verbose)
        winfeavecs = te2win.fit(feavecs, zeroobj=zero_pad_code, dropz=True, drop_non_tail=True)
        winfeavecs_indexes = te2win.getOriginalIndexes()
        # get the original alert ids
        aux = np.where(winfeavecs_indexes == csd_input_adapters.timeEquidistantToWindowed.PADDING_INDEX_MARKER,
                       len(feavecs_origidx), winfeavecs_indexes)
        winfeavecs_orig_idx = np.append(feavecs_origidx,
                                        csd_input_adapters.timeEquidistantToWindowed.PADDING_INDEX_MARKER)[aux]
        aux2 = np.where(winfeavecs_orig_idx ==
                        csd_input_adapters.timeEquidistantToWindowed.PADDING_INDEX_MARKER, len(alert_ids),
                        winfeavecs_orig_idx)
        winfeavecs_orig_ids = np.append(alert_ids, csd_input_adapters.timeEquidistantToWindowed.PADDING_INDEX_MARKER)[aux2]
        return winfeavecs, None, winfeavecs_orig_ids, feavecs_timestamps[winfeavecs_indexes]

    def _get_feed(self, fea_vec):
        return regression_encoder_decoder_ae_oh.create_input_feed_list(self.X_descr, fea_vec)

    def _get_output_probs(self, X_feed):
        preds = self.DNNmodel.predict(X_feed + X_feed + X_feed)
        predsp = np.exp(preds)
        predsp /= np.expand_dims(np.sum(predsp, axis=-1), axis=-1)
        return predsp

    def _get_embeddings(self, X_feed):
        with self.graph.as_default():
            feed_dict = tflearn.utils.feed_dict_builder(X_feed, None, self.DNNmodel.inputs, None)
            hidden = self.DNNmodel.session.run(tf.compat.v1.get_collection(tf.compat.v1.GraphKeys.HIDDEN_STATE),
                                               feed_dict=feed_dict)[0]
            hidden = hidden._asdict()['h']
        return hidden

    def get_embeddings(self, json_inp):
        X, _, ids, timestamps = self._json_to_vec(json_inp)
        X_feed = self._get_feed(X)
        E = self._get_embeddings(X_feed)
        return E, ids[:,-1], timestamps[:,-1]

    def get_oh_encodings(self, json_inp):
        X, _, info, timeids = self._json_to_vec(json_inp)
        X_oh = np.concatenate(self._get_feed(X), axis=-1)[:,0,:]   # taking the leading vector of the RNN window as the encoding
        return X_oh, info, timeids

