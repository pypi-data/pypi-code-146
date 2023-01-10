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
Unit tests for the Tensorflow autoencoder embedder.
"""

from unittest import TestCase
import numpy as np
from copy import deepcopy


class TestRegression_encoder_decoder_ae_oh(TestCase):
    def _generate_mock_data(self, batch_size, inp_seq_len, inp_symbols):
        """
        generate unit test data
        :param batch_size: int
        :param inp_seq_len: int
        :param inp_symbols: int or list(int)
        :param out_seq_len: int
        :return: list(raw_input), raw_output
        """
        if not isinstance(inp_symbols, list):
            inp_symbols = [inp_symbols]
        RI = []
        inpdef = []
        raw_input = np.zeros([batch_size, inp_seq_len, len(inp_symbols)])
        for c, nsym in enumerate(inp_symbols):
            raw_input[..., c:c+1] = np.random.randint(nsym, size=[batch_size, inp_seq_len, 1])
            inpdef.append(("discrete", nsym))
        RI = raw_input
        RO = deepcopy(RI)
        return RI, RO, inpdef

    def test_get_model_graph(self):
        from regression_encoder_decoder_ae_oh import regression_encoder_decoder_ae_oh
        batch_size = 100
        inp_seq_len = 10
        inp_symbols = [5, 3]
        raw_input, raw_output, inp_def = self._generate_mock_data(batch_size, inp_seq_len, inp_symbols)
        r = regression_encoder_decoder_ae_oh(inp_seq_len, inp_def, verbose=4, l2_weight=0.001)
        _, _ = r.get_model_graph("train", num_layers=1, cell_size=10)


    def test_fit(self):
        from regression_encoder_decoder_ae_oh import regression_encoder_decoder_ae_oh
        import uuid
        import shutil
        import os
        import tensorflow as tf
        checkpointdir = None
        try:
            batch_size = 100
            inp_seq_len = 10
            inp_symbols = [5, 3]
            checkpointdir = '/tmp/%s' % str(uuid.uuid4())
            checkpointpath = checkpointdir + '/checkpoints'
            l2_weight = 0.001
            raw_input, raw_output, inp_def = self._generate_mock_data(batch_size, inp_seq_len, inp_symbols)
            r = regression_encoder_decoder_ae_oh(inp_seq_len, inp_def, verbose=4, l2_weight=l2_weight)
            model, graph = r.get_model_graph("train", num_layers=1, cell_size=10, checkpoint_path=checkpointpath,
                                             tensorboard_verbose=3)
            X_train_feed = r.create_input_feed_list(inp_def, raw_input)
            if not isinstance(X_train_feed, list):
                X_train_feed = [X_train_feed]
            model.fit(X_train_feed + X_train_feed + X_train_feed, None, n_epoch=2, shuffle=False,
                      validation_set=(X_train_feed + X_train_feed + X_train_feed, None),
                      show_metric=True, batch_size=batch_size, run_id='unit_test')
        finally:
            if os.path.exists(checkpointdir):
                shutil.rmtree(checkpointdir)

    def test_fit_and_load_and_predict(self):
        from regression_encoder_decoder_ae_oh import regression_encoder_decoder_ae_oh
        import uuid
        import shutil
        import os
        import tensorflow as tf
        tf.compat.v1.disable_v2_behavior()

        checkpointdir = None
        try:
            batch_size = 100
            inp_seq_len = 10
            inp_symbols = [5, 3]
            checkpointdir = '/tmp/%s' % str(uuid.uuid4())
            checkpointpath = checkpointdir + '/checkpoints'
            l2_weight = 0.001
            raw_input, raw_output, inp_def = self._generate_mock_data(batch_size, inp_seq_len, inp_symbols)
            r = regression_encoder_decoder_ae_oh(inp_seq_len, inp_def, verbose=4, l2_weight=l2_weight)
            model, graph = r.get_model_graph("train", num_layers=1, cell_size=10, checkpoint_path=checkpointpath,
                                             tensorboard_verbose=3)
            X_train_feed = r.create_input_feed_list(inp_def, raw_input)
            if not isinstance(X_train_feed, list):
                X_train_feed = [X_train_feed]
            model.fit(X_train_feed + X_train_feed + X_train_feed, None, n_epoch=2, shuffle=False,
                      validation_set=(X_train_feed + X_train_feed + X_train_feed, None),
                      show_metric=True, batch_size=batch_size, run_id='unit_test')
            tf.compat.v1.reset_default_graph()
            r2 = regression_encoder_decoder_ae_oh(inp_seq_len, inp_def, verbose=0, l2_weight=l2_weight)
            model2, graph2 = r2.get_model_graph("predict", num_layers=1, cell_size=10)
            mdlfn = checkpointpath + '-1'
            with graph2.as_default():
                        model2.load(mdlfn)
            pred = model2.predict(X_train_feed + X_train_feed + X_train_feed)
            assert (pred.shape == np.concatenate(X_train_feed, axis=-1).shape)
        finally:
            if os.path.exists(checkpointdir):
                shutil.rmtree(checkpointdir)
