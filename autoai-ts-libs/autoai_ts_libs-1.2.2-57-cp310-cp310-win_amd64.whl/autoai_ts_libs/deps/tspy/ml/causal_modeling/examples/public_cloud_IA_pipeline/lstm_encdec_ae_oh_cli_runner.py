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
Command-line trainer of the autoencoder embedder used in the IA pipeline.
"""
import h5py
import os
import argparse
import json
import numpy as np
import common_stuff as scommon
from regression_encoder_decoder_ae_oh import regression_encoder_decoder_ae_oh

DEFAULT_GO_VALUE = -1

parser = argparse.ArgumentParser(description="Encoder-Decoder Autoencoder Trainer.")
parser.add_argument('-i', '--inFile', dest='datafn', required=True, metavar='<alertsfn>',
                    help="preprocessed data file in h5 format. Must contain following keys: {%s, %s,%s,%s,%s}"
                         % (scommon.TRAINSET_DESCR_KEY, scommon.TRAINSET_X_KEY, scommon.TRAINSET_Y_KEY,
                            scommon.DEVSET_X_KEY, scommon.DEVSET_Y_KEY))
parser.add_argument('-rd', '--runDir', dest='run_dir', required=True, metavar='<dir>',
                    help="Base dir for models + checkpoints. An experiment-specific subdir will be created there.")
parser.add_argument('-ld', '--logDir', dest='log_dir', required=True, metavar='<dir>',
                    help="Base dir for tensorboard logs. An experiment-specific subdir will be created there.")
parser.add_argument('-lr', '--learningRate', dest='lr', required=False, metavar='<float>', default=0.001,
                    help="Learning rate.")
parser.add_argument('-m', '--modelFile', dest='mdlfn', required=False, default=None, metavar='<mdlfn>',
                    help="Load pre-existing model (continue updating it)")
parser.add_argument('-e', '--numEpochs', dest='num_epochs', required=True, metavar='<int>',
                    help="Number of training epochs over train set")
parser.add_argument('-exp', '--expPrefix', dest='exp_pref', metavar='<str>',
                    default="exp_", help="String will be prefixed to experiment-specific signature.")
parser.add_argument('-compress', '--compress', dest='compress_layers', metavar='<int,int,...>',
                    default=None, help="comma-separated layer sizes, e.g., 10,2,10")
parser.add_argument('-nl', '--numLayers', dest='num_layers', required=True,
                    help="Number of layers.")
parser.add_argument('-H', '--cellSize', dest='cell_size', required=True,
                    help="Cell size.")
parser.add_argument('-use_dev_partition', '--use_dev_partition', dest='use_dev_part', action='store_true',
                    default=False,
                    help="Use DEV to train instead of TRAIN (which is used to cros-val).")
parser.add_argument('-train_dev_suffixes', '--train_dev_suffixes', dest='train_dev_suffixes', metavar="<str, str>",
                    required=False, default=None,
                    help="Comma-separated list of suffixes identifying partitions within the h5 to train and dev on"
                         "The suffixes must give valid keys in the h5 when affixed to 'X' and 'Y'."
                         "Example: \"_train,_dev2\"")
parser.add_argument('-B', '--batchSize', dest='batch_size', required=False, default=10, help="Batch size.")
parser.add_argument('-maxcpt', '--maxCheckpoints', dest='max_checkpoints', required=False, default=None,
                    help="This many most recent checkpoints to keep [All]")
parser.add_argument('-tv', '--tensorboardVerbose', dest='tensorboard_verbose', required=False, default=None,
                    help="Pass this int value to tensorboard logger [0]")
parser.add_argument('-l2', '--l2RegularizerWeight', dest='l2_weight', required=False, default=None,
                    help="L2-regularizer weight [0]")
parser.add_argument('-go', '--goValue', dest='go_value', required=False, default=float(DEFAULT_GO_VALUE),
                    help="Initial value to start off the decoder [%.1f]" % float(DEFAULT_GO_VALUE))
parser.add_argument('-att', '--attHeads', dest='attention_heads', default=None, required=False,
                    help="Specify number of attention reader heads [Default 0 == no attention]")
parser.add_argument('-up', '--usePrevious', dest='use_previous', action='store_true', default=False,
                    help="Train with decoder getting previous output as input [Off].")
parser.add_argument('-up_t', '--usePreviousFromT', dest='use_previous_t', default=None,
                    help="As -up but start using previous from t=<value> (0-based indexing).")
parser.add_argument('-AL', '--attLayers', dest='att_all_layers', action='store_true', default=False, required=False,
                    help="Attention will look at all input layers instead of the top [Off].")
parser.add_argument('-dropout', '--dropout', dest='dropout_str', default=None,
                    help="Comma-separated list of keep probs, corresp. to {inp, state, out}")
parser.add_argument('-dropout_encdec', '--dropout_encdec', dest='dropout_encdec', action='store_true', default=False, required=False,
                    help="Apply dropout to both the encoder and the decoder [Off].")
parser.add_argument('-infofn_exploc', '--infofn_exploc', dest='infofn_exploc', required=False, default=None,
                    help="File will be created, containing full directory name pointing to the checkpoints.")
parser.add_argument('-subsample_train', '--subsample_train', dest='subsample_train_frac', required=False, default=None,
                    help="Subsample the trainset randomly to a fraction.")
parser.add_argument('-subsample_dev', '--subsample_dev', dest='subsample_dev_frac', required=False, default=None,
                    help="Subsample the devset randomly to a fraction.")
parser.add_argument('-v', '--v', dest='verbose', action='store_true',
                    default=False,
                    help="Be verbose.")



# parser.add_argument('-variances_fixed', '--variances_fixed', dest='output_variances_fixed', action='store_true',
#                     default=False,
#                     help="Fix variance at 1.0 (graph will have it but it will be not trained).")
args = parser.parse_args()
num_epochs = int(args.num_epochs)
datafn = args.datafn
exp_pref = args.exp_pref
batch_size = int(args.batch_size)
cell_size = int(args.cell_size)
go_value = float(args.go_value)
if go_value != DEFAULT_GO_VALUE:
    print("INFO: Using non-default go value of %f" % go_value)
what_to_train_on = (scommon.TRAINSET_X_KEY, scommon.TRAINSET_Y_KEY)
what_to_validate_on = (scommon.DEVSET_X_KEY, scommon.DEVSET_Y_KEY)
what_to_train_on_aux_dec_input = None
what_to_validate_on_aux_dec_input = None
train_partition_descr = ''
if args.use_dev_part:
    what_to_train_on = (scommon.DEVSET_X_KEY, scommon.DEVSET_Y_KEY)
    what_to_validate_on = (scommon.TRAINSET_X_KEY, scommon.TRAINSET_Y_KEY)
    train_partition_descr = '_trOnDev'
    print("INFO: Will train on DEV partition!")
if args.train_dev_suffixes is not None:
    trsuffix, devsuffix = [s.strip() for s in args.train_dev_suffixes.split(",")]
    what_to_train_on = ('X' + trsuffix, 'Y' + trsuffix)
    what_to_validate_on = ('X' + devsuffix, 'Y' + devsuffix)
    train_partition_descr = '_trOn' + trsuffix[1:].capitalize()
    print("INFO: Will train/dev on %s/%s " % (trsuffix, devsuffix))

learning_rate = float(args.lr)

dec_input_descr = ""
dec_fuse_previous_from_to = None

num_layers = int(args.num_layers)
dec_use_previous = args.use_previous
dec_use_previous_t = 0
if args.use_previous_t is not None:
    dec_use_previous_t = int(args.use_previous_t)
    dec_use_previous = True

attention_heads = int(args.attention_heads) \
    if (args.attention_heads is not None and int(args.attention_heads) > 0) else None
att_all_layers = True if (num_layers > 1 and args.att_all_layers) else False
dropout_keep_probs = None
dropout_descr = ""
if args.dropout_str is not None:
    if attention_heads is not None:
        raise NotImplementedError("ERROR: Dropout not implemented for Attention EncDec!")
    dropout_keep_probs = [float(s) for s in args.dropout_str.split(",")]
    if len(dropout_keep_probs) != 3:
        raise ValueError("ERROR: Dropout keep probs must come in threes. (\"%s\"" % args.dropout_str)
    if args.dropout_encdec:
        dropout_descr = "DrOutEncDec"
    else:
        dropout_descr = "DrOut"
    dropout_descr += args.dropout_str.replace(",", "_")
compress_ls = None
compress_descr = ""
if args.compress_layers is not None:
    compress_ls = [int(i) for i in args.compress_layers.split(",")]
    compress_descr = "Compr%s" % ("_".join([str(i) for i in compress_ls]))
subsample_descr = ""
if args.subsample_train_frac is not None:
    subsample_descr = "TrSubsamp%.2f" % float(args.subsample_train_frac)

exp_id = "%s%slr%.4f_LS%dx%d%s%s%s%sB%d" % (exp_pref, subsample_descr, learning_rate, int(args.cell_size), num_layers, compress_descr,
                                     ("noL2" if args.l2_weight is None else "L2%.4f" % float(args.l2_weight)),
                                     ("" if attention_heads is None else ("Att%s%d" %
                                                                      (("" if not att_all_layers else "AL"),
                                                                       attention_heads))),
                                     ("" if not dec_use_previous else (
                                             "UsePrev%s" % ("" if dec_use_previous_t < 1 else "t" + str(dec_use_previous_t)))
                                      ),
                                     batch_size)
exp_id += train_partition_descr
exp_id += dec_input_descr
exp_id += dropout_descr
run_dir = "%s/%s/checkpoints" % (args.run_dir, exp_id)
max_checkpoints = None
if args.max_checkpoints is not None:
    max_checkpoints = int(args.max_checkpoints)
tensorboard_dir = args.log_dir
if not tensorboard_dir.endswith('/'):
    tensorboard_dir += '/'
tensorboard_verbose = 0
if args.tensorboard_verbose is not None:
    tensorboard_verbose = int(args.tensorboard_verbose)
    if tensorboard_verbose > 4:
        tensorboard_verbose = 4
        print("\n\nWARNING: capping -tv value %d to 4 - max. supported by tflearn\n\n" % tensorboard_verbose)
log_id = exp_id  # tensorboards marker that will be created as a subdir of tensorboard_dir
load_model_fn = None

if args.mdlfn is not None:
    load_model_fn = args.mdlfn
if args.infofn_exploc is not None:
    print("INFO: Logging checkpoint and tensorboard location info to file: " + args.infofn_exploc)
    with open(args.infofn_exploc, "wt") as of:
        of.write("Rundir=%s\n" % run_dir)
        of.write("Logdir=%s\n" % (tensorboard_dir + log_id))

Y_train_auxdecinp = None
Y_dev_auxdecinp = None
with h5py.File(datafn, "r") as h5f:
    print("INFO: Loading data from %s" % datafn)
    X_train_dims = h5f[what_to_train_on[0]].shape
    if len(X_train_dims) != 3:
        raise RuntimeError("ERROR: input data expected to be a 3d-tensor (found %s)." % str(X_train_dims))
    Y_train_dims = h5f[what_to_train_on[1]].shape
    if len(Y_train_dims) != 3:
        raise RuntimeError("ERROR: target data expected to be a 3d-tensor (found %s)." % str(Y_train_dims))
    X_train = h5f[what_to_train_on[0]][()]
    Y_train = h5f[what_to_train_on[1]][()]
    if what_to_train_on_aux_dec_input is not None:
        Y_train_auxdecinp = h5f[what_to_train_on_aux_dec_input][()]

    X_dev = h5f[what_to_validate_on[0]][()]
    Y_dev = h5f[what_to_validate_on[1]][()]
    if what_to_validate_on_aux_dec_input is not None:
        Y_dev_auxdecinp = h5f[what_to_validate_on_aux_dec_input][()]
    descr = json.loads(h5f[scommon.TRAINSET_DESCR_KEY][()])
if args.subsample_dev_frac is not None:
    ndev = X_dev.shape[0]
    ndevsub = int(float(args.subsample_dev_frac) * ndev)
    idx = list(range(ndev))
    np.random.shuffle(idx)
    subidx = idx[:ndevsub]
    X_dev = X_dev[subidx, ...]
    Y_dev = Y_dev[subidx, ...]
    print("INFO Randomly subsampled DEV set from %d to %d samples (fraction %.3f)" %
          (ndev, ndevsub, float(args.subsample_dev_frac)))
if args.subsample_train_frac is not None:
    ntrain = X_train.shape[0]
    nsub = int(float(args.subsample_train_frac) * ntrain)
    idx = list(range(ntrain))
    np.random.shuffle(idx)
    subidx = idx[:nsub]
    X_train = X_train[subidx, ...]
    Y_train = Y_train[subidx, ...]
    print("INFO Randomly subsampled TRAIN set from %d to %d samples (fraction %.3f)" %
          (ntrain, nsub, float(args.subsample_train_frac)))
raw_input_def = descr
raw_inp_seq_len = X_train_dims[1]
raw_out_seq_len = Y_train_dims[1]
raw_out_dim = Y_train_dims[2]

if not os.path.exists(run_dir):
    print("INFO: Creating run dir: \"%s\"" % run_dir)
    os.makedirs(run_dir)
else:
    print("INFO: Using existing dir \"%s\"" % run_dir)
aux = tensorboard_dir + log_id
if not os.path.exists(aux):
    os.makedirs(aux)

model_ref = regression_encoder_decoder_ae_oh

seq2seq_model_type = "basic_rnn" if not attention_heads else "attention_rnn"
seq2seq_model_type = "basic_rnn_with_vardropout" if dropout_keep_probs is not None else seq2seq_model_type
train_mode = "train" if not dec_use_previous else "predict"  # optional training with feed-previous mode (non-std)
dec_inp_dim = None
if Y_train_auxdecinp is not None:
    dec_inp_dim = Y_train_auxdecinp.shape[-1]
rmdl = model_ref(raw_inp_seq_len, raw_input_def, verbose=bool(args.verbose),
                 l2_weight=args.l2_weight, go_value=go_value, seq2seq_model=seq2seq_model_type,
                 num_att_heads=attention_heads, att_look_at_all_layers=att_all_layers,
                 hidden_state_ae_layers=compress_ls, out_seq_len=raw_out_seq_len)
input_keep_prob = 1.0 if dropout_keep_probs is None else dropout_keep_probs[0]
state_keep_prob = 1.0 if dropout_keep_probs is None else dropout_keep_probs[1]
output_keep_prob = 1.0 if dropout_keep_probs is None else dropout_keep_probs[2]
seq_model, graph = rmdl.get_model_graph(train_mode, num_layers=num_layers, cell_size=cell_size,
                                        checkpoint_path=run_dir, learning_rate=learning_rate,
                                        tensorboard_verbose=tensorboard_verbose,
                                        max_checkpoints=max_checkpoints, tensorboard_dir=tensorboard_dir,
                                        use_previous_from_t=dec_use_previous_t,
                                        input_keep_prob=input_keep_prob,
                                        state_keep_prob=state_keep_prob,
                                        output_keep_prob=output_keep_prob,
                                        apply_encoder_dropout=args.dropout_encdec)
if load_model_fn:
    with graph.as_default():
        seq_model.load(load_model_fn)
        print("INFO: loading pre-existing model from %s" % load_model_fn)

print("\n=================================\nINFO: Starting training. Parameters as follows:\n"
      "Cellsize=%d\nNumLayers=%d\nBatchsize=%d\nNum epochs=%d\nLearning rate=%f" %
      (cell_size, num_layers, batch_size, num_epochs, learning_rate))
if dropout_keep_probs is not None:
    print("Dropout ACTIVE with pkeep = {%s}" % ",".join(str(f) for f in dropout_keep_probs))
if load_model_fn is not None:
    print("Starting point=%s" % load_model_fn)
if args.max_checkpoints is not None:
    print("Will only keep most recent %d checkpoints (per option)" % (int(args.max_checkpoints)))
if compress_ls is not None:
    print("Compress network active (sizes=%s)" % compress_descr)
print("\n")

# prepare input data acc. to inp_def
raw_x_train_feed = rmdl.create_input_feed_list(raw_input_def, X_train)
raw_x_dev_feed = rmdl.create_input_feed_list(raw_input_def, X_dev)
raw_y_train_feed = rmdl.create_input_feed_list(raw_input_def, Y_train)
raw_y_dev_feed = rmdl.create_input_feed_list(raw_input_def, Y_dev)
# do we feed the decoder with auxiliary data (cmd line option), or the usual, i.e., target
# NOTE: we need to hack tflearn (sorry!) as follows:
# line 187 in file  /usr/local/lib/python3.6/dist-packages/tflearn/models/dnn.py
# change: >>if not (is_none(valX) or is_none(valY)):<< to >>if not (is_none(valX)):<<
seq_model.fit(raw_x_train_feed + raw_y_train_feed + raw_y_train_feed, None, n_epoch=num_epochs, shuffle=False,
              validation_set=(raw_x_dev_feed + raw_y_dev_feed + raw_y_dev_feed, []),
              show_metric=True, batch_size=batch_size, run_id=log_id)
print("INFO: Training completed. Locations:\nModel dir = %s\nLog dir = %s" % (run_dir, tensorboard_dir))
