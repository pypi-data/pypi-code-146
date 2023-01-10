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
Tensorflow graph of a static autoencoder. Used only for baseline experiments.
"""
import tensorflow._api.v2.compat.v1 as tf
tf.disable_v2_behavior()
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)
from tflearn.layers.core import *
from tflearn.layers.normalization import *
from tflearn.layers.estimator import regression
import math

DISCRETE_KEYWORD = "discrete"  # defines an embedding segment in input data
tf.GraphKeys.BOTTLENECK = "bottleneck"

# One-Hot (OH) input/output autoencoder
class static_autoencoder_oh(object):

    def __init__(self, input_descr):
        self.input_descr = input_descr
        self.inputs = None    # pointer to oh-encoded inputs
        assert isinstance(self.input_descr, list) and len(self.input_descr) > 0


    def _mean_square_autoloss(self, preds, _):
        """
        Ignore true targets (this is a dummy var just to keep tflearn happy). We draw the targets from
        self.inputs.
        :param preds:
        :param _:
        :return:
        """
        with tf.name_scope("MeanSquare"):
            return tf.reduce_mean(tf.square(preds - self.inputs))


    def _cross_entropy(self, preds, _):
        """
        Ignore true targets (this is a dummy var just to keep tflearn happy). We draw the targets from
        self.inputs.
        :param preds:
        :param _:
        :return:
        """
        with tf.name_scope("CE"):
            return tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(labels=self.inputs/len(self.input_descr),
                                                                             logits=preds))

    @staticmethod
    def create_input_feed_list(input_descr, X):
        """
        generates a list from X according to raw_input_def that is consumable by TF placeholders
        :param input_descr: list if tuples with input description
        :param X: data tensor
        :return: list
        """
        out_lst = []
        fromdim = 0
        feadim = X.shape[-1]
        nsamples = X.shape[0]
        for l in input_descr:
            (kwd, cardinality) = l
            if kwd == DISCRETE_KEYWORD:  # interpret data as discrete symbols
                todim = fromdim + 1
                assert (todim <= feadim)
                x = X[..., fromdim:todim][:,0].astype(np.int32)
                if not (np.min(x) >= 0 and np.max(x) < cardinality):
                    raise RuntimeError("ERROR: interpreting input data segment (dims %d:%d) as discrete symbol seq."
                                       "(range=%d:%d, but vocab is [0,%d])"
                                       % (fromdim, todim, np.min(x), np.max(x), cardinality - 1))
                xoh = np.zeros([nsamples, cardinality])
                xoh[range(x.shape[0]),x] = 1
            else:
                raise RuntimeError("ERROR: unsupported keyword in inp_def (%s)" % kwd)
            out_lst.append(xoh)
            fromdim = todim
        return out_lst


    def get_model_graph(self, nhidden, activation='tanh', dropoutp=None, learning_rate=0.001,
                        tensorboard_verbose=0, tensorboard_dir="/tmp/tensorboard_log", checkpoint_path=None,
                        max_checkpoints=0, which_loss='CE'):
        """
        Generates TF graph for an MLP autoencoder with one-hot input encoding
        :param nhidden: list of layer sizes
        :param activation:
        :param dropoutp:
        :param learning_rate:
        :param tensorboard_verbose:
        :param tensorboard_dir:
        :param checkpoint_path:
        :param max_checkpoints:
        :return: model, graph
        """

        tfG = tf.Graph()
        with tfG.as_default():
            # assemble input which can be either embedding segment or a vector
            segc = 0
            oh_inputs = []
            if which_loss == 'CE':
                which_loss = self._cross_entropy
            elif which_loss == 'mean_square':
                which_loss = self._mean_square_autoloss
            else:
                raise ValueError("ERROR: unknown loss requested (%s)" % which_loss)

            # parse input specs and generate one-hot segments
            for segtup in self.input_descr:
                (segtype, cardinality) = segtup
                if segtype == DISCRETE_KEYWORD:
                    seg_raw_input = tf.placeholder(tf.float32, shape=[None, cardinality], name='seg%d_inputoh' % segc)
                    tf.add_to_collection(tf.GraphKeys.INPUTS, seg_raw_input)
                    oh_inputs.append(seg_raw_input)
                else:
                    # raw input is a vector
                    raise RuntimeError("This implementation does not allow vector input.")
                segc += 1
            self.inputs = tf.concat(oh_inputs, axis=-1)

            # autodetermine bottleneck layer
            bottle_layer_id = np.argmin(nhidden)
            # define the layers
            net = self.inputs
            if dropoutp is not None:
                net = tflearn.dropout(net, (1-dropoutp))    # note this takes "keep probability", i.e., 1-dp
            for l in range(len(nhidden)):
                sz = nhidden[l]
                net = tflearn.fully_connected(net, sz, activation=activation, regularizer='L2', weight_decay=0.001)
                if l == bottle_layer_id:   # mark this layer as bottleneck
                    tf.add_to_collection(tf.GraphKeys.BOTTLENECK, net)

            output = tflearn.fully_connected(net, self.inputs.shape[-1].value, activation='linear')
            network = regression(output,
                                 loss=which_loss,
                                 optimizer='adam',
                                 learning_rate=learning_rate,
                                 )

            MLPmodel = tflearn.DNN(network,
                                   tensorboard_verbose=tensorboard_verbose,
                                   tensorboard_dir=tensorboard_dir,
                                   checkpoint_path=checkpoint_path, max_checkpoints=max_checkpoints
                                   )
        return MLPmodel, tfG
