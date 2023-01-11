from simAIRR.expand_repertoire_components.ImplantationHelper import ImplantationHelper
from simAIRR.pgen_count_map.PgenCountMap import PgenCountMap
import pandas as pd
import numpy as np
import os
import importlib_resources as pkg_resources


def prepare_test_data():
    pgen_dat = pd.DataFrame.from_dict({'aa_seq': ['CASRSRSGNTIYF', 'CATGGQWANEQFF'],
                                       'pgen': [2.1830784134836584e-09, 3.738093342333351e-13]})
    with pkg_resources.as_file(pkg_resources.files("simAIRR.config_validator").joinpath(
            "signal_seq_pgen_count_map.tsv")) as count_map_file:
        signal_pgen_count_map = PgenCountMap(number_of_repertoires=4, pgen_count_map_file=count_map_file)
    return pgen_dat, signal_pgen_count_map


def test_get_pgen_intervals():
    pgen_dat, signal_pgen_count_map = prepare_test_data()
    pgen_intervals_array = ImplantationHelper.get_pgen_intervals(pgen_dat=pgen_dat,
                                                                 pgen_count_map_obj=signal_pgen_count_map)
    assert pgen_intervals_array == [(-9, -8), (-100, -12)]


def test_get_absolute_number_of_repertoires():
    pgen_dat, signal_pgen_count_map = prepare_test_data()
    pgen_intervals_array = ImplantationHelper.get_pgen_intervals(pgen_dat=pgen_dat,
                                                                 pgen_count_map_obj=signal_pgen_count_map)
    abs_rep_num = ImplantationHelper.get_absolute_number_of_repertoires(pgen_intervals_array, signal_pgen_count_map)
    assert abs_rep_num == [2, 2]


def test_get_repertoire_sequence_presence_indices():
    pgen_dat, signal_pgen_count_map = prepare_test_data()
    pgen_intervals_array = ImplantationHelper.get_pgen_intervals(pgen_dat=pgen_dat,
                                                                 pgen_count_map_obj=signal_pgen_count_map)
    abs_rep_num = ImplantationHelper.get_absolute_number_of_repertoires(pgen_intervals_array, signal_pgen_count_map)
    seq_presence_indices = ImplantationHelper.get_repertoire_sequence_presence_indices(6, abs_rep_num)
    assert len(seq_presence_indices) == 6
    assert len(np.concatenate(seq_presence_indices).ravel().tolist()) == 4  # see prepare_test_data why this value is 4


def test_write_public_repertoire_chunks(tmp_path):
    public_repertoires_path = tmp_path / "public_repertoires"
    signal_chunks_path = tmp_path / "signal_rep_chunks"
    chunks_path = signal_chunks_path / "chunk_0"
    public_repertoires_path.mkdir()
    signal_chunks_path.mkdir()
    rep_0 = pd.DataFrame.from_dict({'n_seqs': ['TGTGCCAGCAGGAGCCGCTCTGGAAACACCATATATTTT',
                                               'TGTGCCACAGGGGGGCAGTGGGCCAATGAGCAGTTCTTC'],
                                    'a_seqs': ['CASRSRSGNTIYF', 'CATGGQWANEQFF'],
                                    'v_genes': ['TRBV12-3', 'TRBV12-3'], 'j_genes': ['TRBJ1-3', 'TRBJ2-1']})
    rep_0.to_csv(os.path.join(public_repertoires_path, 'rep_0.tsv'), index=None, header=None, sep='\t')
    pgen_dat, signal_pgen_count_map = prepare_test_data()
    pgen_intervals_array = ImplantationHelper.get_pgen_intervals(pgen_dat=pgen_dat,
                                                                 pgen_count_map_obj=signal_pgen_count_map)
    abs_rep_num = ImplantationHelper.get_absolute_number_of_repertoires(pgen_intervals_array, signal_pgen_count_map)
    seq_presence_indices = ImplantationHelper.get_repertoire_sequence_presence_indices(6, abs_rep_num)
    ImplantationHelper.write_public_repertoire_chunks(original_repertoire_file=os.path.join(public_repertoires_path, 'rep_0.tsv'),
                                                      output_files_path=signal_chunks_path,
                                                      repertoire_sequence_presence_indices=seq_presence_indices,
                                                      file_type="tsv")
    out_files = [fn for fn in os.listdir(chunks_path) if os.path.isfile(os.path.join(chunks_path, fn))]
    assert len(out_files) == 6

