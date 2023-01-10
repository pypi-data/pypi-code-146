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
Command-line tool to generate feature files for the autonencoder trainer 'lstm_encdec_ae_oh_cli_runner'
INPUT: Oculus data source (json format)
OUTPUT: HDF5-formatted feature file with various partitions
"""
import collections
import numpy as np
import h5py as h5
import json
import argparse
import os.path
import datetime
from copy import deepcopy
import pickle
from autoai_ts_libs.deps.tspy.ml.causal_modeling.algorithms.csd_input_adapters import timeEquidistantToWindowed, timeStampedToTimeEquidistant
from autoai_ts_libs.deps.tspy.ml.causal_modeling.examples.public_cloud_IA_pipeline.app_adapter_oculus_features import appAdapterOculusFeatures

# Keys used to store features in hdf5 files
# Legacy: These are taken from surrogate/surrogate/surrogate_common.py to keep things consistent
TRAINSET_X_KEY = 'X_train'
TRAINSET_Y_KEY = 'Y_train'
TRAINSET_Y_ORIG_KEY = 'Y_train_original'
TRAINSET_FILENAMES = 'trainset_filenames'
TRAINSET_DESCR_KEY = 'X_train_descr'
TRAINSET_SIMID = 'trainset_simid'
TRAINSET_UNQID = 'trainset_info'
DEVSET_X_KEY = 'X_dev'
DEVSET_Y_KEY = 'Y_dev'
DEVSET_Y_ORIG_KEY = 'Y_dev_original'
DEVSET_FILENAMES = 'devset_filenames'
DEVSET_SIMID = 'devset_simid'
DEVSET_UNQID = 'devset_info'
METASET_X_KEY = 'X_meta'
METASET_Y_KEY = 'Y_meta'
METASET_Y_ORIG_KEY = 'Y_meta_original'
METASET_FILENAMES = 'metaset_filenames'
METASET_SIMID = 'metaset_simid'
METASET_UNQID = 'metaset_info'
TESTSET_X_KEY = 'X_test'
TESTSET_Y_KEY = 'Y_test'
TESTSET_Y_ORIG_KEY = 'Y_test_original'
TESTSET_FILENAMES = 'testset_filenames'
TESTSET_SIMID = 'testset_simid'
TESTSET_UNQID = 'testset_info'
X_STDSCALER = 'x_stdscalerobj'
INP_STDSCALER = 'inp_stdscalerobj'
INP_STDDIMS = 'inp_stddims'


def partition_features(F, rd, rt, verbose=True):
    """
    :param F: features array
    :param rd: dev set proportion
    :param rt:  test set proportion
    :return: dict with train/dev/test partitions
    """
    nalerts = len(F)
    devsize = int(rd * nalerts)
    testsize = int(rt * nalerts)
    assert (testsize + devsize <= nalerts)
    test_idx = range(nalerts - testsize, nalerts)
    dev_idx = range(test_idx[0] - devsize, test_idx[0])
    train_idx = range(dev_idx[0]) if devsize > 0 else []
    # Split into train, dev, meta, eval
    D = {}
    D[TRAINSET_X_KEY] = deepcopy(F[train_idx])
    D[TRAINSET_Y_KEY] = deepcopy(F[train_idx])
    D[DEVSET_X_KEY] = deepcopy(F[dev_idx])
    D[DEVSET_Y_KEY] = deepcopy(F[dev_idx])
    D[TESTSET_X_KEY] = deepcopy(F[test_idx])
    D[TESTSET_Y_KEY] = deepcopy(F[test_idx])
    if verbose: print("INFO: Partitions: |train| = %d, |dev| = %d, |test| = %d samples."
          % (len(train_idx), len(dev_idx), len(test_idx)))
    D[TRAINSET_SIMID] = train_idx
    D[DEVSET_SIMID] = dev_idx
    D[TESTSET_SIMID] = test_idx
    return D


def filter_alerts(alerts, constraints, verbose=True):
    """
    retains only alerts complying with the constraint object
    :param alerts:
    :param constraints: dict 'field':<substr> - positive if an alert's field value contains <substr>
    :return: new list (copy)
    """
    if constraints is None:
        return deepcopy(alerts)
    newalerts = []
    for a in alerts:
        # check if all constraints active
        if all([(s in a[fld]) for fld, s in constraints.items()]):
            newalerts.append(a)
    if verbose: print("INFO: Filtered alerts using constraints=%s\n --> got %d out of %d" % (
        str(constraints), len(newalerts), len(alerts)))
    for k in constraints.keys():
        keylist = [newalerts[i][k] for i in range(len(newalerts)) if k in newalerts[i]]
        c = collections.Counter(keylist)
        if verbose: print("INFO: --> after filtering the field %s has unique values %s. Check if that is ok." %
              (k, ", ".join([v for v, _ in c.most_common(1000)])))
    return newalerts


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Extract windowed features from Oculus json file list.")
    parser.add_argument('-i', '--inFile', dest='infof', required=True, metavar='<fof>', default=None,
                        help="list of json files (file of files)")
    parser.add_argument('-o', '--outFile', dest='outfn', required=True, metavar='<outfn>',
                        help="h5 file with preprocessed features, sequenced by time")
    parser.add_argument('-t', '--timeRes', dest='timeres', required=True, metavar='<int>',
                        help="Time resolution in seconds. If not activated, no event padding will be done.")
    parser.add_argument('-tpstr', '--tpstr', dest='timeparsestr', required=False, metavar='<str>',
                        help="Time parsing string.", default='%Y-%m-%dT%H:%M:%SZ')
    parser.add_argument('-tfield', '--tfield', dest='timefield', required=False, metavar='<str>',
                        help="Key within alert carrying timestamp", default='lastReceiveTime')
    parser.add_argument('-r', '--ratioDevTest', dest='rdevtest', required=False, metavar='<float,float>',
                        default="0.1,0.1",
                        help="comma-separated: fractions of data to be used for dev and test, e.g., \"0.2,0.2\"")
    parser.add_argument('-C', '--C', dest='constraints', required=False, metavar='<str,str,...>',
                        default=None,
                        help="Comma-separated list of fieldname:substring pairs, e.g., \"datacenter:dal05\""
                             "to be used to filter alerts. Multiple fields are AND-connected.")
    parser.add_argument('-win', '--win', dest='winlen', required=True, metavar='<int>',
                        help="Window length.")
    parser.add_argument('-owin', '--owin', dest='outwinlen', required=False, metavar='<int>', default=None,
                        help="Output window length, if different from -win")
    parser.add_argument('-dropz', '--dropz', dest='dropzeros', required=False, action='store_true',
                        help="Drop windows with all-zeros vectors.")
    parser.add_argument('-v', '--v', dest='format_version', required=True, metavar='<int>',
                        help="Input data format: \'v1\'=REST-API, \'v2\'=dbdump, \'v3\'=dbdump-simplified")
    parser.add_argument('-LD', '--loadDicts', dest='readdicts', metavar='<fn>', default=None,
                        help="Will attempt to read dictionaries from <fn> file (pkl).")
    parser.add_argument('-s', '--silent', dest='silent', action='store_true', default=False,
                        help="Shh, silent.")

    args = parser.parse_args()
    verbose = not bool(args.silent)
    timeres = float(args.timeres) if args.timeres is not None else None
    winlen = int(args.winlen)
    if args.outwinlen is not None:
        owinlen = int(args.outwinlen)
        assert (owinlen >= winlen)
        if owinlen != winlen: print("INFO: Setting the output window length to %d" % owinlen)
    else:
        owinlen = winlen
    with open(args.infof, 'rt') as f:
        fof = f.read().splitlines()
        if verbose: print("INFO: Got %d input files to read from." % len(fof))
    alerts = []
    load_dicts = args.readdicts  # if not None will skip dict generation and instead will read them from a file
    alerts_ofn = args.outfn
    dicts_ofn = alerts_ofn + ".dicts.json"
    if load_dicts is not None and not os.path.exists(load_dicts):
        raise ValueError("ERROR: loading dicts requested but file %s does not exist." % dicts_ofn)
    for fn in fof:
        if fn.endswith('.pkl'):
            with open(fn, 'rb') as f:
                tmp = pickle.load(f)
                print("INFO: Read %d alerts from %s" % (len(tmp), fn))
                alerts += tmp
        elif fn.endswith('.json'):
            with open(fn, 'rb') as f:
                tmp = json.load(f)
                print("INFO: Read %d alerts from %s" % (len(tmp), fn))
                alerts += tmp
        else:
            raise ValueError("ERROR: donno how to handle this file type: %s" % fn)

    print("INFO: Total alerts: %d" % len(alerts))
    constraints = None
    if args.constraints is not None:
        constraints = {}
        for tok in args.constraints.split(','):
            fld, val = tok.strip().split(':')
            assert (len(fld) > 0 and len(val) > 0)
            constraints[fld.strip()] = val.strip()
        print("INFO: User-supplied constraints: %s" % str(constraints))
        print("INFO: Now filtering alerts...")
        alerts = filter_alerts(alerts, constraints)
    if verbose:
        print("INFO: Sorting alerts by timestamp...")
    if args.format_version == 'v1':
        alerts = sorted(alerts,
                        key=lambda i: datetime.datetime.strptime(i[args.timefield], args.timeparsestr).timestamp())
    elif args.format_version == 'v2':
        alerts = sorted(alerts, key=lambda i: i[args.timefield]['epoch_time'])
    elif args.format_version == 'v3':
        alerts = sorted(alerts, key=lambda i: i[args.timefield]['epoch_time'])
    elif args.format_version == 'v4':
        alerts = sorted(alerts, key=lambda i: i[args.timefield]['epoch_time'])
    else:
        raise ValueError("ERROR: unknown input format...")

    rd, rt = [float(i) for i in args.rdevtest.split(",")]
    if verbose:
        print("INFO: Ratio dev=%f / test=%f" % (rd, rt))
    if verbose: print("INFO: Encoding features...")

    # Step 1: Encode timestamped events (CSD360 adapter class)
    fe = appAdapterOculusFeatures(feature_version=args.format_version, verbose=verbose)
    if load_dicts is not None:
        fe.load(load_dicts)
    else:
        fe.fit(alerts=alerts)
        fe.save(dicts_ofn)
    alert_feavecs, alert_ids, alert_encoding_descr = fe.encode(alerts=alerts)
    assert (len(alert_feavecs) == len(alerts))
    # Step 1.1: grab the corresponding timestamps
    alert_timestamps = [float(i[args.timefield]['epoch_time']) for i in alerts]
    # Step 2: time to equidistant (CSD360 class)
    # Step 2.1. Generate zeropadding object to indicate "no alert"
    # we add extra element in each set
    # so cardinality of the dicts has to be incremented
    zero_pad_code = [i[1] for i in alert_encoding_descr]
    # and change the descr to reflect the increase
    new_alert_encoding_descr = [(i[0], i[1] + 1) for i in alert_encoding_descr]
    ts2te = timeStampedToTimeEquidistant(time_resolution=timeres, padding_object=zero_pad_code,
                                         bucket_assignment_func=timeStampedToTimeEquidistant._min_distance_bucket_assignment_function,
                                         reconciliation_func=timeStampedToTimeEquidistant._default_reconciliation_function,
                                         verbose=verbose)
    feavecs, feavecs_timestamps, feavecs_origidx = ts2te.transform(events=alert_feavecs,
                                                                   timestamp_list=alert_timestamps,
                                                                   drop_n_consecutive_paddings=2*winlen)
    # Step 3: windowing (CSD360 class)
    if verbose: print("INFO: Windowing features...")
    te2win = timeEquidistantToWindowed(wlen=winlen, padding_mode=timeEquidistantToWindowed.PADDING_MODE_TAILPADDING,
                                       verbose=verbose)
    winfeavecs = te2win.fit(feavecs, zeroobj=zero_pad_code, dropz=bool(args.dropzeros))
    winfeavecs_indexes = te2win.getOriginalIndexes()
    # get the original alert ids
    aux = np.where(winfeavecs_indexes == timeEquidistantToWindowed.PADDING_INDEX_MARKER,
                   len(feavecs_origidx), winfeavecs_indexes)
    winfeavecs_orig_idx = np.append(feavecs_origidx, timeEquidistantToWindowed.PADDING_INDEX_MARKER)[aux]
    aux2 = np.where(winfeavecs_orig_idx == timeEquidistantToWindowed.PADDING_INDEX_MARKER, len(alert_ids),
                    winfeavecs_orig_idx)
    winfeavecs_orig_ids = np.append(alert_ids, timeEquidistantToWindowed.PADDING_INDEX_MARKER)[aux2]
    if verbose: print("INFO: Partitioning...")
    D = partition_features(winfeavecs, rd, rt)
    D[TRAINSET_DESCR_KEY] = new_alert_encoding_descr
    D[TRAINSET_UNQID] = winfeavecs_orig_ids[list(D[TRAINSET_SIMID])]
    if DEVSET_SIMID in D:
        D[DEVSET_UNQID] = winfeavecs_orig_ids[list(D[DEVSET_SIMID])]
    if METASET_SIMID in D:
        D[METASET_UNQID] = winfeavecs_orig_ids[list(D[METASET_SIMID])]
    if TESTSET_SIMID in D:
        D[TESTSET_UNQID] = winfeavecs_orig_ids[list(D[TESTSET_SIMID])]

    # write out
    with h5.File(alerts_ofn, 'w') as of:
        print("INFO: Saving...")
        for key in D.keys():
            if 'descr' in key:
                saux = json.dumps(D[key])
                of.create_dataset(key, data=saux)
            elif 'info' in key:
                xaux = np.fromstring(pickle.dumps(D[key]), dtype='uint8')
                of.create_dataset(key, data=xaux)
            else:
                if D[key] is not None and len(D[key]) > 0:
                    of.create_dataset(key, data=D[key])
    if verbose:
        print("INFO: New data saved in %s (keys=%s)" % (args.outfn, ",".join(D.keys())))
