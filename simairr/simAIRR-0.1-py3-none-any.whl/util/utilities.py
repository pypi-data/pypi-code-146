import os.path
import pandas as pd
import numpy as np
from pathlib import Path
import yaml


def concatenate_files(files_path, file_pattern):
    found_files = Path(files_path).glob(file_pattern)
    li = []
    for i, filename in enumerate(found_files):
        fn = pd.read_csv(filename, header=None, sep='\t')
        li.append(fn)
    concatenated_df = pd.concat(li, axis=0, ignore_index=True)
    return concatenated_df, len(li)


def makedir_if_not_exists(some_path, fail_if_exists=False):
    if os.path.exists(some_path):
        files = [fn for fn in os.listdir(some_path) if
                 os.path.isfile(os.path.join(some_path, fn))]
        files_exists = f"Output folder may already contain relevant files: {some_path}"
        if fail_if_exists:
            assert len(files) == 0, files_exists
    else:
        os.makedirs(some_path)


def split_dataframe(data_frame, number_of_splits, split_files_path):
    for idx, chunk in enumerate(np.array_split(data_frame, number_of_splits)):
        chunk.to_csv(os.path.join(split_files_path, f'rep_{idx}.tsv'), index=None, header=None, sep='\t')


def sort_olga_seq_by_pgen(olga_sequence_file, olga_pgen_file):
    pgen_file = pd.read_csv(olga_pgen_file, header=None, sep='\t', index_col=None)
    seq_file = pd.read_csv(olga_sequence_file, header=None, sep='\t', index_col=None)
    pgen_file.columns = ['aa_seq_pgen', 'pgen']
    seq_file.columns = ['nt_seq', 'aa_seq', 'v_gene', 'j_gene']
    pgen_file['row_index_pgen'] = np.arange(len(pgen_file))
    seq_file['row_index_seq'] = np.arange(len(seq_file))
    merged_df = pd.merge(seq_file, pgen_file, how="left", left_on=['aa_seq', 'row_index_seq'],
                         right_on=['aa_seq_pgen', 'row_index_pgen'])
    sorted_df = merged_df.sort_values(by='pgen')
    seq_df = sorted_df[['nt_seq', 'aa_seq', 'v_gene', 'j_gene']]
    pgen_df = sorted_df[['aa_seq_pgen', 'pgen']]
    seq_df.to_csv(olga_sequence_file, header=None, sep='\t', index=None)
    pgen_df.to_csv(olga_pgen_file, header=None, sep='\t', index=None)


def write_yaml_file(yaml_dict, out_file_path):
    with open(out_file_path, "w+") as yaml_file:
        yaml.dump(yaml_dict, yaml_file)


def merge_dicts(dicts_list):
    merged_dict = {k: v for d in dicts_list for k, v in d.items()}
    return merged_dict
