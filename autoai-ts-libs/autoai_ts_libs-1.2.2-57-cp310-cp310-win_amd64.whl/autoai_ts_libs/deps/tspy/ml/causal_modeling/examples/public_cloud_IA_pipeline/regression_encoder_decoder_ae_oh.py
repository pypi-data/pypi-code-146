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
Encoder-Decoder architecture definitions (Tensorflow) with multi-embedding input and regression output
"""
from __future__ import division, print_function
import tflearn
import tensorflow as tf
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)
import copy
from six.moves import xrange
import numpy as np
from tensorflow.python.ops import array_ops
# from tensorflow.contrib.legacy_seq2seq.python.ops import seq2seq as seq2seq_lib
from tensorflow.python.ops import rnn_cell
# from tensorflow.contrib.rnn.python.ops import core_rnn_cell #TODO remove
from tensorflow.python.ops import rnn
from tensorflow.python.ops import nn_ops
from tensorflow.python.util import nest
import inspect
import modified_multi_rnn as altrnn

if hasattr(inspect, 'getfullargspec'):
    getargspec = inspect.getfullargspec
else:
    getargspec = inspect.getargspec
DISCRETE_KEYWORD = "discrete"  # defines an embedding segment in input data
tf.compat.v1.GraphKeys.ATTENTION_MASKS = "attention_masks"
tf.compat.v1.GraphKeys.WHITEBOX_FEATURES = "whitebox_features"
tf.compat.v1.GraphKeys.HIDDEN_STATE = "hidden_state"
tf.compat.v1.GraphKeys.BOTTLENECK_FEATURES = "bottleneck_features"
# tf.compat.v1.disable_eager_execution()

# the below is a function from legacy.seq2seq modified for mixed GT/UsePrev mode
def rnn_decoder(decoder_inputs,
                initial_state,
                cell,
                projection_dim=None,
                loop_function=None,
                use_previous_from_t=0,
                loop_fuse_range=None,
                scope=None,
                verbose=True):
    """RNN decoder for the sequence-to-sequence model.

    Args:
      decoder_inputs: A list of 2D Tensors [batch_size x input_size].
      initial_state: 2D Tensor with shape [batch_size x cell.state_size].
      cell: rnn_cell.RNNCell defining the cell function and size.
      projection_dim: None or int. If not None, a linear projection layer with 'dim' outputs will be used
        to transform cell output.
      loop_function: If not None, this function will be applied to the i-th output
        in order to generate the i+1-st input, and decoder_inputs will be ignored,
        except for the first element ("GO" symbol). This can be used for decoding,
        but also for training to emulate http://arxiv.org/abs/1506.03099.
        Signature -- loop_function(prev, i) = next
          * prev is a 2D Tensor of shape [batch_size x output_size],
          * i is an integer, the step number (when advanced control is needed),
          * next is a 2D Tensor of shape [batch_size x input_size].
      use_previous_from_t: (JIRI added) used with loop_function!=None. Will turn on loop_function only
        starting from this time-slot (0-based). Way to have first n steps use
        decoder inputs, followed by using previous outputs from there on.
      loop_fuse_range: (JIRI added) when not None, a tupe with from-to indexes (inclusive!)
                             delineating the range of the inputs that will be replaced
                              by previous outputs. You better know whatya doin.
      scope: VariableScope for the created subgraph; defaults to "rnn_decoder".

    Returns:
      A tuple of the form (outputs, state), where:
        outputs: A list of the same length as decoder_inputs of 2D Tensors with
          shape [batch_size x output_size] containing generated outputs.
        state: The state of each cell at the final time-step.
          It is a 2D Tensor of shape [batch_size x cell.state_size].
          (Note that in some cases, like basic RNN cell or GRU cell, outputs and
           states can be the same. They are different for LSTM cells though.)
    """
    if loop_fuse_range is not None:
        di = decoder_inputs[0].shape[-1]
        assert (len(loop_fuse_range) == 2 and np.max(loop_fuse_range) < di and np.min(loop_fuse_range) >= 0)
    with tf.compat.v1.variable_scope(scope or "rnn_decoder"):
        state = initial_state
        outputs = []
        states = []
        prev = None
        for i, inp in enumerate(decoder_inputs):
            if prev is not None:
                if loop_fuse_range is None:  # default behavior
                    if loop_function is not None:
                        if i >= use_previous_from_t:
                            if verbose: print("INFO: using previous decoder output for time slot t=%d" % i)
                            with tf.compat.v1.variable_scope("loop_function", reuse=True):
                                inp = loop_function(prev, i)
                        else:
                            if verbose: print("INFO: using decoder inputs (GT) for time slot t=%d" % i)
                else:  # mask not None means fuse prev and inp
                    if i >= use_previous_from_t:
                        if verbose: print(
                                "INFO: using masked FUSION (from/to=%d/%d) of previous decoder output for time slot t=%d" %
                                (loop_fuse_range[0], loop_fuse_range[1], i))
                        with tf.compat.v1.variable_scope("loop_function", reuse=True):
                            fromi = loop_fuse_range[0]
                            toi = loop_fuse_range[1]
                            inp = tf.concat([inp[..., :fromi], prev[..., fromi:toi + 1], inp[..., toi + 1:]], axis=-1)
                    else:
                        if verbose: print("INFO: using decoder inputs (GT) for time slot t=%d" % i)
            if i > 0:
                tf.compat.v1.get_variable_scope().reuse_variables()
            output, state = cell(inp, state)
            if projection_dim is not None:
                output = tflearn.fully_connected(output, projection_dim, activation='linear', scope='cell_proj',
                                                 reuse=(i>0))
            outputs.append(output)
            states.append(state)
            if loop_function is not None:
                prev = output
    return outputs, states


class regression_encoder_decoder_ae_oh(object):
    '''
    Main class for encoder-decoder regressor
    '''
    AVAILABLE_MODELS = ["basic_rnn", "attention_rnn", "basic_rnn_with_variances", "basic_rnn_with_vardropout"]

    def __init__(self, in_seq_len, input_descr,
                 seq2seq_model=None, verbose=None, name=None, data_dir=None, go_value=-1,
                 l2_weight=None, num_att_heads=1, att_look_at_all_layers=False, nll_variance_mode=0,
                 hidden_state_ae_layers=None, out_seq_len=None):
        '''
        :param in_seq_len: int
        :param input_descr: list of tuples. tuple=('emb', nsymbols, embedding_dim) or ('vec', dim, proj_dim)
        :param out_seq_len: int
        :param seq2seq_model: string (for now only 'basic_rnn')
        :param verbose: int
        :param name: string
        :param data_dir: string
        :param go_value: float (initial value to start decoder)
        :param l2_weight: float or None (L2 regularization)
        :param num_att_heads: int (only with seq_seq_model == "attention_rnn"
        :param nll_variance_mode: 0 - no var modeling; 1 - joint var NLL; 2 - fixed variance, 3 - update only variance
        :param hidden_state_ae_layers: None or a list with layer sizes. This is for an AE compresor of the hidden
        :param out_seq_len: if None output len will be same as input length (AE). This param can change that.
        state passed from the encoder to the decoder.
        '''
        self.seq2seq_model = seq2seq_model or "basic_rnn"
        assert self.seq2seq_model in self.AVAILABLE_MODELS
        self.in_seq_len = in_seq_len
        self.out_seq_len = self.in_seq_len  if out_seq_len is None else out_seq_len# AE
        self.out_seq_dim = None
        self.dec_inp_dim = self.out_seq_dim
        self.verbose = verbose or 0
        self.input_descr = input_descr
        assert isinstance(self.input_descr, list) and len(self.input_descr) > 0
        self.model_instance = None
        self.name = name
        self.data_dir = data_dir
        self.go_value = go_value
        self.initializer = None
        self.l2_weight = float(l2_weight) if l2_weight is not None else None
        self.regularizer = None
        if self.l2_weight and self.l2_weight > 0.:
            self.regularizer = tf.keras.regularizers.l2(l=0.5 * (self.l2_weight))
        self.graph = None
        self.num_att_heads = num_att_heads
        self.att_look_at_all_layers = att_look_at_all_layers
        self.nll_variance_mode = nll_variance_mode
        self.hidden_state_ae = hidden_state_ae_layers
        if self.verbose and self.in_seq_len!=self.out_seq_len:
            print("WARN: AE re-configured for prediction!")

    @staticmethod
    def _mean_square_loss(targets, preds):
        with tf.compat.v1.name_scope("MeanSquare"):
            return tf.reduce_mean(input_tensor=tf.square(preds - targets))

    @staticmethod
    def _cross_entropy(targets, preds):
        with tf.compat.v1.name_scope("CE"):
            return tf.reduce_mean(input_tensor=tf.nn.softmax_cross_entropy_with_logits(labels=targets, logits=preds))


    @staticmethod
    def _mean_loglikelihood_loss(targets, preds, lvariance):
        # L = 0.5*((preds-targets)^2/variances + log(variances))
        # Omitting the 0.5 scale
        with tf.compat.v1.name_scope("NegLogLikelihood"):
            # lvariance = tf.Print(lvariance, [targets, preds, lvariance], '(targs, preds, vars) = ')
            return tf.reduce_mean(input_tensor=tf.square(preds - targets) / tf.exp(lvariance) + lvariance)
            # return tf.reduce_mean(tf.square(preds - targets))

    @staticmethod
    def _mean_loglikelihood_loss_no_variance(targets, preds, lvariance):
        # same as _mean_loglikelihood_loss() but with variance fixed at 1
        with tf.compat.v1.name_scope("NegLogLikelihood"):
            # lvariance = tf.Print(lvariance, [targets, preds, lvariance], '(targs, preds, vars) = ')
            # return tf.reduce_mean(tf.square(preds - targets) / tf.exp(lvariance) + lvariance)
            return tf.reduce_mean(input_tensor=tf.square(preds - targets))

    @staticmethod
    def _seq_loss_by_example(logits, targets, average_across_timesteps=True,
                             loss_function=_mean_square_loss, name=None, normfactor=1.0):
        '''
        Calculates loss sample-wise
        :param logits: predicted values tensor (batch, seq, dim)
        :param targets:  ground truth tensor
        :param average_across_timesteps: true == will average over output sequence
        :param loss_function: user function
        :param normfactor: used to descale multi-segment one-hot encodings
        :param name:
        :return: loss (batch)
        '''
        if len(targets) != len(logits):
            raise ValueError("Lengths of logits, and targets must be the same "
                             "%d, %d." % (len(logits), len(targets)))
        with tf.compat.v1.name_scope(name, "sequence_loss_by_example", logits + targets):
            L = []
            for logit, target in zip(logits, targets):
                loss = loss_function(target/normfactor, logit)
                L.append(loss)
            if average_across_timesteps:
                L = tf.reduce_mean(input_tensor=L)
        return L

    @staticmethod
    def _seq_loss_with_variance_by_example(logits, targets, average_across_timesteps=True,
                                           loss_function=_mean_loglikelihood_loss, name=None):
        '''
        Calculates likelihood loss sample-wise
        :param logits: predicted values tensor (batch, seq, dim)
        :param targets:  ground truth tensor
        :param average_across_timesteps: true == will average over output sequence
        :param name:
        :return: loss (batch)
        '''
        if len(targets) != len(logits):
            raise ValueError("Lengths of logits, and targets must be the same "
                             "%d, %d." % (len(logits), len(targets)))
        targsdim = int(targets[0].shape[-1])
        assert (targsdim * 2 == logits[0].shape[-1])
        with tf.compat.v1.name_scope(name, "sequence_likelihood_loss_by_example", logits + targets):
            L = []
            for logit, target in zip(logits, targets):
                loss = loss_function(target, logit[..., :targsdim], logit[..., targsdim:])
                L.append(loss)
            if average_across_timesteps:
                L = tf.reduce_mean(input_tensor=L)
        return L

    @staticmethod
    def _direct_loop_function(prev, _):
        return prev

    @staticmethod
    def _direct_loop_function_with_variances(prev, _):
        # i am returning first half, i.e., the target predictions, ignoring variances stored in second half
        assert (prev.shape[-1] % 2 == 0)
        return prev[..., :int(int(prev.shape[-1]) / 2)]

    def _sequence_loss(self, y_pred, y_true):
        '''
        Entry point for sequence loss
        :param y_pred: predicted values
        :param y_true: ground truth values
        :return: loss
        '''
        if self.verbose > 2: print("my_sequence_loss y_pred=%s, y_true=%s" % (y_pred, y_true))
        logits = tf.unstack(y_pred, axis=1)
        targets = tf.unstack(y_true, axis=1)

        with tf.name_scope(name="sequence_loss"):
            cost = tf.reduce_sum(input_tensor=self._seq_loss_by_example(logits, targets, loss_function=self._mean_square_loss))
            reg_losses = None
            if self.graph is not None:
                reg_losses = self.graph.get_collection(tf.compat.v1.GraphKeys.REGULARIZATION_LOSSES)
            if reg_losses and len(reg_losses) > 0:
                l2_loss = tf.reduce_sum(input_tensor=reg_losses, name="acc_L2_loss")
                # l2_loss = tf.Print(l2_loss, [l2_loss, cost], 'scaled_L2_loss, cost=')
                cost += l2_loss  # note that scale has already been applied self.l2_weight
        return cost

    def _sequence_ae_loss_ce(self, y_pred, y_true):
        '''
        Entry point for sequence loss
        :param y_pred: predicted values
        :param y_true: ground truth values
        :return: loss
        '''
        if self.verbose > 2: print("my_sequence_loss y_pred=%s" % (y_pred))
        logits = tf.unstack(y_pred, axis=1)
        targets = self.outputs
        normfactor = float(len(self.input_descr))
        with tf.name_scope(name="sequence_ae_loss_ce"):
            cost = tf.reduce_sum(input_tensor=self._seq_loss_by_example(logits, targets, normfactor=normfactor,
                                                           loss_function=self._cross_entropy))
            reg_losses = None
            if self.graph is not None:
                reg_losses = self.graph.get_collection(tf.compat.v1.GraphKeys.REGULARIZATION_LOSSES)
            if reg_losses and len(reg_losses) > 0:
                l2_loss = tf.reduce_sum(input_tensor=reg_losses, name="acc_L2_loss")
                # l2_loss = tf.Print(l2_loss, [l2_loss, cost], 'scaled_L2_loss, cost=')
                cost += l2_loss  # note that scale has already been applied self.l2_weight
        return cost

    def _sequence_loss_with_variances(self, y_pred, y_true):
        '''
        Entry point for sequence loss
        :param y_pred: predicted values
        :param y_true: ground truth values
        :return: loss
        '''
        if self.verbose > 2: print("_sequence_likelihood_loss y_pred=%s, y_true=%s" % (y_pred, y_true))
        logits = tf.unstack(y_pred, axis=1)
        targets = tf.unstack(y_true, axis=1)
        which_loss_fct = self._mean_loglikelihood_loss  # this includes joint training w/variance
        if self.nll_variance_mode == 2:  # non-trainable fixed variance
            # use simple L2 loss (but we are still keeping the graph consistent with the variance graph for later)
            # needed for pretraining
            which_loss_fct = self._mean_loglikelihood_loss_no_variance
        with tf.name_scope(name="sequence_likelihood_loss"):
            cost = tf.reduce_sum(
                input_tensor=self._seq_loss_with_variance_by_example(logits, targets, loss_function=which_loss_fct))
            reg_losses = None
            if self.graph is not None:
                reg_losses = self.graph.get_collection(tf.compat.v1.GraphKeys.REGULARIZATION_LOSSES)
            if reg_losses and len(reg_losses) > 0:
                l2_loss = tf.reduce_sum(input_tensor=reg_losses, name="acc_L2_loss")
                # l2_loss = tf.Print(l2_loss, [l2_loss, cost], 'scaled_L2_loss, cost=')
                cost += l2_loss  # note that scale has already been applied self.l2_weight
            # cost = tf.Print(cost, [cost], 'TOTAL COST =')
        return cost

    @staticmethod
    def rectify_tf2_tflearn_issues():
        """
        Going from TF1x to TF2x, a weird problem between tflearn and tf occurs
        in that regularization losses are created as _LazyEvalTensor type, which do not have the method ref()
        but tflearn passes them down to tf which then relies on that method and crashes.
        To prevent this, we convert the lazy tensors to tensors here.
        """
        losses = tf.compat.v1.get_collection_ref(tf.compat.v1.GraphKeys.REGULARIZATION_LOSSES)
        for i in range(len(losses)):
          losses[i] = losses[i]._as_tensor() \
            if "_LazyEvalTensor" in str(type(losses[i])) else losses[i]

    @staticmethod
    def create_input_feed_list(input_descr, X):
        """
        generates a list from X according to descr that is consumable by TF placeholders
        :param input_descr: list if tuples with input description
        :param X: data tensor
        :return: list
        """
        # if not isinstance(X, list):
        #     X = [X]
        out_lst = []
        fromdim = 0
        feadim = X.shape[-1]
        nsamples = X.shape[0]
        assert(feadim==len(input_descr))
        for c,l in enumerate(input_descr):
            (kwd, cardinality) = l
            x = X[..., c]
            if kwd == DISCRETE_KEYWORD:  # interpret data as discrete symbols
                xoh = np.zeros([x.shape[0], x.shape[1], cardinality])
                for i in range(x.shape[-1]):
                    cards = x[..., i].astype(np.int32)
                    if not (np.min(cards) >= 0 and np.max(cards) < cardinality):
                        raise RuntimeError("ERROR: interpreting input data segment %d as discrete symbol seq."
                                           "(range=[%d,%d] but vocab is [0,%d])"
                                           % (c, np.min(cards), np.max(cards), cardinality - 1))
                    xoh[range(len(cards)), i, cards] = 1
            else:
                raise RuntimeError("ERROR: unsupported keyword in inp_def (%s)" % kwd)
            out_lst.append(xoh)
        return out_lst


    def get_model_graph(self, mode="train", num_layers=1, cell_size=32, cell_type="BasicLSTMCell", learning_rate=0.0001,
                        tensorboard_verbose=0, tensorboard_dir="/tmp/tensorboard_log", checkpoint_path=None,
                        max_checkpoints=0, use_previous_from_t=0, dec_fuse_previous_from_to=None,
                        input_keep_prob=1.0, output_keep_prob=1.0, state_keep_prob=1.0, apply_encoder_dropout=False):
        '''
        Builds the seq2seq graph
        :param mode: string ("train"|"predict")
        :param num_layers:  int
        :param cell_size: int (hidden state size)
        :param cell_type: (lstm, gru, etc.)
        :param learning_rate: float
        :param tensorboard_verbose: int
        :param tensorboard_dir:
        :param checkpoint_path:
        :use_previous_from_t:
        :use_prev_mask: None --> use default loop behavior. if list of indexes provided, a loop function will be
                created and passed to decoder builder. Only indexed variables TODO
        :return: tflearn_model, graph
        '''
        assert mode in ["train", "predict"]
        checkpoint_path = checkpoint_path or (
                "%s%ss2s_checkpoint.tfl" % (self.data_dir or "", "/" if self.data_dir else ""))
        GO_VALUE = self.go_value  # unique integer value used to trigger decoder outputs in the seq2seq RNN
        tfG = tf.Graph()
        self.graph = tfG
        model = None
        trainable_vars = None  # None eventually means all will be trained
        segc = 0
        oh_inputs = []
        oh_outputs = []
        oh_decinputs = []
        with tfG.as_default():
            # Create encoder input by assembling indiv. segments as defined
            segc = 0
            # parse input specs and generate one-hot segments
            # ...for inputs
            for segtup in self.input_descr:
                (segtype, cardinality) = segtup
                if segtype == DISCRETE_KEYWORD:
                    seg_raw_input = tf.compat.v1.placeholder(tf.float32, shape=[None, self.in_seq_len, cardinality],
                                                   name='seg%d_inputoh' % segc)
                    tf.compat.v1.add_to_collection(tf.compat.v1.GraphKeys.INPUTS, seg_raw_input)
                    oh_inputs.append(seg_raw_input)
                else:
                    # raw input is a vector
                    raise RuntimeError("This implementation does not allow vector input.")
                segc += 1
            # ...for decoder inputs
            segc = 0
            for segtup in self.input_descr:
                (segtype, cardinality) = segtup
                seg_raw_dec_input = tf.compat.v1.placeholder(tf.float32, shape=[None, self.out_seq_len, cardinality],
                                                   name='seg%d_decinoh' % segc)
                tf.compat.v1.add_to_collection(tf.compat.v1.GraphKeys.INPUTS, seg_raw_dec_input)
                oh_decinputs.append(seg_raw_dec_input)
                segc += 1
            # ...for outputs
            segc = 0
            for segtup in self.input_descr:
                (segtype, cardinality) = segtup
                seg_raw_output = tf.compat.v1.placeholder(tf.float32, shape=[None, self.out_seq_len, cardinality],
                                                name='seg%d_outputoh' % segc)
                tf.compat.v1.add_to_collection(tf.compat.v1.GraphKeys.INPUTS, seg_raw_output)
                oh_outputs.append(seg_raw_output)
                segc += 1

            # concatenate segment into single encoder input
            encoder_inputs = tf.concat([s for s in oh_inputs], 2)
            # save the dims (they are same for inp/outp as this is an AE)
            self.dec_inp_dim = self.out_seq_dim =  encoder_inputs.shape[-1]
            encoder_inputs = tf.unstack(encoder_inputs, axis=1)
            decoder_inputs = tf.concat([s for s in oh_decinputs], 2)
            decoder_inputs = tf.unstack(decoder_inputs, axis=1)
            # insert "GO" symbol as the first decoder input; drop the last decoder input
            go_input = tf.multiply(tf.ones_like(decoder_inputs[0], dtype=tf.float32), GO_VALUE)
            decoder_inputs = [go_input] + decoder_inputs[: self.out_seq_len - 1]

            decoder_outputs = tf.concat([s for s in oh_outputs], 2)
            decoder_outputs = tf.unstack(decoder_outputs, axis=1)
            self.inputs = decoder_inputs
            self.outputs = decoder_outputs

            # single_cell = getattr(rnn_cell, cell_type)(cell_size, state_is_tuple=True)
            def _get_a_cell(cell_size):
                return getattr(rnn_cell, cell_type)(cell_size, state_is_tuple=True)

            if num_layers == 1:
                dec_cell = _get_a_cell(cell_size)
            else:
                # check API compatibility and quit if not satisfied
                if self.att_look_at_all_layers:
                    # if 'output_is_tuple' not in inspect.getargspec(altrnn.MultiRNNCell).args:
                    if 'output_is_tuple' not in getargspec(altrnn.MultiRNNCell).args:
                        raise RuntimeError("ERROR: User requested a feature (attention from all layers)"
                                           "that is not supported by currently installed TF version. "
                                           "The module \"rnn_cell_impl.py\" needs to be patched by modifed stuff -"
                                           " talk to Jiri, maybe (gonna costya).")
                    dec_cell = altrnn.MultiRNNCell([_get_a_cell(cell_size) for _ in range(num_layers)],
                                                   output_is_tuple=self.att_look_at_all_layers)
                else:
                    # use the default API
                    dec_cell = altrnn.MultiRNNCell([_get_a_cell(cell_size) for _ in range(num_layers)])

            which_loss_function = self._sequence_ae_loss_ce
            if self.seq2seq_model == "basic_rnn":
                with tf.compat.v1.variable_scope("basic_rnn_seq2seq", regularizer=self.regularizer):
                    # encoder
                    enc_cell = copy.deepcopy(dec_cell)
                    _, enc_state = rnn.static_rnn(enc_cell, encoder_inputs, dtype=tf.float32)
                    tf.compat.v1.add_to_collection(tf.compat.v1.GraphKeys.HIDDEN_STATE, enc_state)
                    if self.hidden_state_ae is not None:
                        init_state = []
                        assert (isinstance(self.hidden_state_ae, list))
                        # optional AE compression: create an ae network with a bottleneck layer
                        # to create a compression. Both h and c hidden states get transformed separately
                        # The outer loop accounts for decoder layers
                        for l in range(num_layers):
                            if num_layers == 1:
                                htensor = enc_state._asdict()['h']
                                ctensor = enc_state._asdict()['c']
                            else:  # concatenate all input layer of on type to project
                                htensor = tf.concat([enc_state[i]._asdict()['h'] for i in range(len(enc_state))], axis=-1)
                                ctensor = tf.concat([enc_state[i]._asdict()['c'] for i in range(len(enc_state))], axis=-1)
                            net_h = htensor
                            net_c = ctensor
                            # identify bottleneck layer
                            bottleneck_id = np.argmin(self.hidden_state_ae)
                            for i, ls in enumerate(self.hidden_state_ae):
                                net_h = tflearn.fully_connected(net_h, ls,
                                                                              activation='linear',
                                                                              scope='hidden_ae_h_%d_%d' % (i, l))
                                net_c = tflearn.fully_connected(net_c, ls,
                                                                              activation='linear',
                                                                              scope='hidden_ae_c_%d_%d' % (i, l))
                                if i == bottleneck_id:
                                    tf.compat.v1.add_to_collection(tf.compat.v1.GraphKeys.BOTTLENECK_FEATURES, net_h)
                            net_h = tflearn.fully_connected(net_h, cell_size, activation='linear',
                                                            scope='hidden_ae_h_%d_%d' % (i+1, l))
                            net_c = tflearn.fully_connected(net_c, cell_size, activation='linear',
                                                            scope='hidden_ae_c_%d_%d' % (i+1, l))
                            init_state.append(tf.compat.v1.nn.rnn_cell.LSTMStateTuple(net_c, net_h))
                        if num_layers == 1:
                            enc_state = init_state[0]
                        else:
                            enc_state = tuple(init_state)

                    # decoder
                    # hidden-to-output projection
                    # dec_cell = core_rnn_cell.OutputProjectionWrapper(dec_cell, self.out_seq_dim, activation=None) # TODO remove
                    # loop function active only in "predict" mode (feeds previous)
                    loop_function = self._direct_loop_function if not (mode == "train") else None
                    model_outputs, states = rnn_decoder(decoder_inputs, enc_state, dec_cell,
                                                        projection_dim=self.out_seq_dim,
                                                        loop_function=loop_function,
                                                        use_previous_from_t=use_previous_from_t,
                                                        loop_fuse_range=dec_fuse_previous_from_to,
                                                        verbose=self.verbose)

                    tf.compat.v1.add_to_collection(tf.compat.v1.GraphKeys.WHITEBOX_FEATURES, states)
            # elif self.seq2seq_model == "basic_rnn_with_vardropout":
            #     with tf.compat.v1.variable_scope("basic_rnn_seq2seq", regularizer=self.regularizer):
            #         # encoder
            #         enc_cell = copy.deepcopy(dec_cell)
            #         # Encoder dropout (Variational Dropout as per Gal et al)
            #         if apply_encoder_dropout:
            #             enc_inp_dim = encoder_inputs[0].shape[-1]
            #             enc_cell = DropoutWrapper(enc_cell, input_keep_prob=input_keep_prob,
            #                                       output_keep_prob=output_keep_prob,
            #                                       state_keep_prob=state_keep_prob, variational_recurrent=True,
            #                                       input_size=enc_inp_dim, dtype=tf.float32)
            #
            #         _, enc_state = rnn.static_rnn(enc_cell, encoder_inputs, dtype=tf.float32)
            #         # decoder
            #         # dropout (Variational Dropout as per Gal et al)
            #         dec_cell = DropoutWrapper(dec_cell, input_keep_prob=input_keep_prob,
            #                                   output_keep_prob=output_keep_prob,
            #                                   state_keep_prob=state_keep_prob, variational_recurrent=True,
            #                                   input_size=self.dec_inp_dim, dtype=tf.float32)
            #         # hidden-to-output projection
            #         dec_cell = core_rnn_cell.OutputProjectionWrapper(dec_cell, self.out_seq_dim, activation=None)
            #         # loop function active only in "predict" mode (feeds previous)
            #         loop_function = self._direct_loop_function if not (mode == "train") else None
            #         model_outputs, states = rnn_decoder(decoder_inputs, enc_state, dec_cell,
            #                                             loop_function=loop_function,
            #                                             use_previous_from_t=use_previous_from_t,
            #                                             loop_fuse_range=dec_fuse_previous_from_to,
            #                                             verbose=self.verbose)
            #         tf.compat.v1.add_to_collection(tf.compat.v1.GraphKeys.WHITEBOX_FEATURES, states)
            else:
                raise NotImplementedError('Unknown seq2seq model requested %s' % self.seq2seq_model)
            # The below is an alternative to OutputProjectionWrapper
            # # learn mapping to desired output dimension
            # scope = tf.get_default_graph().get_name_scope()
            # model_outputs[0] = tflearn.fully_connected(model_outputs[0], self.out_seq_dim, activation=None,
            #                                            regularizer='L2', weight_decay=0.001, scope=scope, reuse=False)
            # for i in range(1, len(model_outputs)):
            #     model_outputs[i] = tflearn.fully_connected(model_outputs[i], self.out_seq_dim, activation=None,
            #                                                regularizer='L2', weight_decay=0.001, scope=scope,
            #                                                reuse=True)
            tf.compat.v1.add_to_collection(tf.compat.v1.GraphKeys.LAYER_VARIABLES + '/' + "seq2seq_model",
                                 model_outputs)  # for TFLearn to know what to save and restore
            network = tf.stack(model_outputs, axis=1)
            if self.verbose > 3:
                all_vars = tf.compat.v1.get_collection(tf.compat.v1.GraphKeys.VARIABLES)
                print("INFO: all_vars = %s" % all_vars)

            network = tflearn.regression(network,
                                         placeholder=None,
                                         optimizer='adam',
                                         learning_rate=learning_rate,
                                         loss=which_loss_function,
                                         metric=None,
                                         name="Y",
                                         trainable_vars=trainable_vars)

            self.rectify_tf2_tflearn_issues()  # prevents crashes going from TF1x t TF2x (see descr.)
            model = tflearn.DNN(network, tensorboard_verbose=tensorboard_verbose, tensorboard_dir=tensorboard_dir,
                                checkpoint_path=checkpoint_path, max_checkpoints=max_checkpoints)

        return model, tfG
