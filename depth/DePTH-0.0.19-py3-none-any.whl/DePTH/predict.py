# -------------------
# take an input file of (TCR, HLA) pairs and make prediction
# -------------------

import os
import sys
import pandas as pd
import tensorflow as tf

import pkg_resources
#from importlib import resources

import argparse


from DePTH import _utils


def predict(test_file, hla_class, output_dir, default_model, model_dir=None, enc_method=None):

    input_args = locals()
    print("input args are", input_args)

    default_model = (default_model == 'True')

    if default_model:
        enc_method = 'one_hot'
    # load pair list
    df_pair = pd.read_csv(test_file, header=0)

    pair_list = [(tcr, hla) for tcr, hla in \
                  zip(df_pair['tcr'].tolist(), df_pair['hla_allele'].tolist())]

    # get the elements for encoding
    (allele_dict, hla_len, HLA_enc, CDR3len_enc, CDR3_enc, cdr1_enc,
            cdr2_enc, cdr25_enc) = _utils.prepare_encoders(hla_class, enc_method)

    # get encoded pairs
    components_test = _utils.encode(pair_list, enc_method, allele_dict, hla_len, HLA_enc, CDR3len_enc, CDR3_enc,
                              cdr1_enc, cdr2_enc, cdr25_enc)

    HLA_encoded, CDR3_encoded, CDR3_len_encoded, cdr1_encoded, cdr2_encoded, cdr25_encoded = components_test

    print(HLA_encoded.shape)
    print(CDR3_encoded.shape)
    print(CDR3_len_encoded.shape)
    print(cdr1_encoded.shape)
    print(cdr2_encoded.shape)
    print(cdr25_encoded.shape)

    if default_model:
        if hla_class == "HLA_I":
            default_model_folder = "HLA_I_all_match_one_hot_n_pos_3854_n_neg_19270_0001_dense2_n_units_64_16_dropout_p_2"
        else:
            default_model_folder = "HLA_II_all_match_one_hot_n_pos_6622_n_neg_33110_0001_dense1_n_units_64_dropout_p_5"
        default_model_path = pkg_resources.resource_filename(__name__, 'data/trained_models/'+default_model_folder)
        #with resources.path('DePTH.data', default_model_folder) as default_model_path:
        print("model path is: ", default_model_path)
        model = tf.keras.models.load_model(default_model_path)
    else:
        print("model path is: ", model_dir)
        model = tf.keras.models.load_model(model_dir)

    yhat = model.predict(components_test)
    yhat_reshape = yhat.reshape(len(pair_list), )
    df_pair['score'] = yhat_reshape.tolist()

    df_pair.to_csv(output_dir + "/predicted_scores.csv", index=False)
