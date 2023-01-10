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
Command-line tool to package files/configs necessary to run the Incident-Alert pipeline.
Required by 'incident_alert_cli_runner.py'
"""

import argparse
import h5py as h5
from oculus_features_cli_runner import TRAINSET_X_KEY, TRAINSET_DESCR_KEY
import os
import shutil
import glob
import json


def assemble_config_and_package_all(package_dir, feafn, modelfn, num_layers, cell_size, l2_weight, encoder_version,
                                    time_resolution, dicts_fn, timefield, force=False):
    if os.path.exists(package_dir) and os.listdir(package_dir):
        if not force:
            raise RuntimeError("ERROR: Package directory \"%s\" already exists and is not empty. (Use \"-f\" to force)"
                               % package_dir)
        else:
            print("WARN: Package directory \"%s\" already exists and is not empty. REMOVING! (-f)" % package_dir)
            shutil.rmtree(package_dir)

    print("INFO: Creating target directory: ", package_dir)
    os.makedirs(package_dir, exist_ok=True)
    publish_package_dir = '.' + os.sep + os.path.normpath(package_dir).split(os.sep)[-1]  # needs to be rel. path

    infostr = ""

    print("INFO: Reading feature file: ", feafn)
    with h5.File(feafn, 'r') as f:
        assert (TRAINSET_X_KEY in f)
        trshape = f[TRAINSET_X_KEY].shape
        descr = json.loads(f[TRAINSET_DESCR_KEY][()])

    fea_dim = len(descr)
    seq_len = trshape[1]
    print("INFO: Determined seq_len=%d, fea_dim=%d, and descr=%s" % (seq_len, fea_dim, descr))

    # Export a copy of the model
    mdldir, mdlbasefn = os.path.split(modelfn)
    print("INFO: Copying model files...")
    for fn in glob.glob(modelfn + r'*'):
        print("INFO:\t\t%s --> %s" % (fn, package_dir))
        shutil.copy2(fn, package_dir)
    newmodelfn = os.path.join(publish_package_dir, mdlbasefn)
    infostr += "Original model location: " + modelfn + "; "

    # Export a copy of the dicts file
    dictsdir, dictsbasefn = os.path.split(dicts_fn)
    print("INFO: Copying dict file...")
    print("INFO:\t\t%s --> %s" % (dictsbasefn, package_dir))
    shutil.copy2(dicts_fn, package_dir)
    newdictsfn = os.path.join(publish_package_dir, dictsbasefn)
    infostr += "Original dictsfn location: " + dicts_fn + "; "

    infostr += "Original feature file location: " + feafn + "; "

    config = {
        'modelfn': newmodelfn,
        'num_layers': num_layers,
        'cell_size': cell_size,
        'seq_length': seq_len,
        'l2_weight': l2_weight,
        'fea_dim': fea_dim,
        'encoder_version': encoder_version,
        'timefield': timefield,
        'fea_descr': descr,
        'time_resolution': time_resolution,
        'dicts_fn': newdictsfn,
        'origin_info': infostr
    }

    outconfigfn = os.path.join(package_dir, "config.json")
    with open(outconfigfn, 'wt') as of:
        json.dump(config, of, indent=4,)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Autoencoder Model Packager ")
    parser.add_argument('-packdir', '--packdir', dest='package_dir', required=True, metavar='<dir>', default=None,
                        help="Directory to package all files (will be created, must not be occupied). ")
    parser.add_argument('-feafn', '--feafn', dest='feafn', required=True, metavar='<fn>', default=None,
                        help="H5 feature file used to train the model (will not be packaged, used for info)")
    parser.add_argument('-modelfn', '--modelfn', dest='modelfn', required=True, metavar='<fn>', default=None,
                        help="TF Model to use. This is a checkpoint base name excluding the extension."
                             "(Ex.: \"path/checkpoints-3999\" which matches three files (.index, .meta, .data)")
    parser.add_argument('-num_layers', '--num_layers', dest='num_layers', required=True, metavar='<int>', default=None,
                        help="Number of LSTM layers in the model.")
    parser.add_argument('-cell_size', '--cell_size', dest='cell_size', required=True, metavar='<int>', default=None,
                        help="LSTM cell size of the trained model.")
    parser.add_argument('-l2_weight', '--l2_weight', dest='l2_weight', required=True, metavar='<float>', default=None,
                        help="L2 penalty used to train the model.")
    parser.add_argument('-encoder_version', '--encoder_version', dest='encoder_version', required=True, metavar='<str>',
                        help="Version of the feature encoder. Value of the -v option used with the trainer.")
    parser.add_argument('-time_resolution', '--time_resolution', dest='time_resolution', required=True, metavar='<int>',
                        default=None, help="Duration of one time step in seconds (as used in training).")
    parser.add_argument('-dicts_fn', '--dicts_fn', dest='dicts_fn', required=True, metavar='<fn>',
                        help="Dicts file created by the trainer (usually named <hdf5feafile>.dicts.json)")
    parser.add_argument('-timefield', '--timefield', dest='timefield', required=True, metavar='<str>',
                        help="Field/key name used to retrieve timestamp from alert file (Ex. 'updateTime')")
    parser.add_argument('-f', '--force', dest='force', required=False, default=False, action="store_true",
                        help="Forces overwriting existing directories.")

    args = parser.parse_args()
    assemble_config_and_package_all(args.package_dir, args.feafn, args.modelfn, int(args.num_layers),
                                    int(args.cell_size), float(args.l2_weight), args.encoder_version,
                                    int(args.time_resolution), args.dicts_fn, args.timefield,
                                    force=args.force)

    print("INFO: Packaging completed successfully. Package directory: %s" % args.package_dir)
