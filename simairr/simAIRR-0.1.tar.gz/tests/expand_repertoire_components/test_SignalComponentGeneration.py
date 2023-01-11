from simAIRR.expand_repertoire_components.SignalComponentGeneration import SignalComponentGeneration
from simAIRR.expand_repertoire_components.ImplantationHelper import ImplantationHelper
from simAIRR.pgen_count_map.PgenCountMap import PgenCountMap
import pandas as pd
import importlib_resources as pkg_resources


def prepare_test_data(tmp_path, phen_pool_size, write_file=True):
    simairr_test_path = tmp_path / "simairr_tests"
    rep_file_path = simairr_test_path / "signal_components"
    pgen_file_path = simairr_test_path / "signal_components" / "pgen_files"
    pgen_dat = pd.DataFrame.from_dict({'aa_seq': ['CASRSRSGNTIYF', 'CATGGQWANEQFF'],
                                       'pgen': [2.1830784134836584e-09, 3.738093342333351e-13]})
    if write_file:
        simairr_test_path.mkdir()
        rep_file_path.mkdir()
        pgen_file_path.mkdir()
        pgen_dat.to_csv(pgen_file_path / 'pgen_dat.tsv', index=None, header=None, sep='\t')
        rep_0 = pd.DataFrame.from_dict({'n_seqs': ['TGTGCCAGCAGGAGCCGCTCTGGAAACACCATATATTTT',
                                                   'TGTGCCACAGGGGGGCAGTGGGCCAATGAGCAGTTCTTC'],
                                        'a_seqs': ['CASRSRSGNTIYF', 'CATGGQWANEQFF'],
                                        'v_genes': ['TRBV12-3', 'TRBV12-3'], 'j_genes': ['TRBJ1-3', 'TRBJ2-1']})
        rep_0.to_csv(rep_file_path / 'dat.tsv', index=None, header=None, sep='\t')
    with pkg_resources.as_file(pkg_resources.files("simAIRR.config_validator").joinpath(
            "signal_seq_pgen_count_map.tsv")) as count_map_file:
        signal_pgen_count_map = PgenCountMap(number_of_repertoires=10, pgen_count_map_file=count_map_file)
    test_gen = SignalComponentGeneration(outdir_path=simairr_test_path,
                                         pgen_count_map_obj=signal_pgen_count_map,
                                         desired_num_repertoires=10, desired_phenotype_burden=3, seed=1234,
                                         phenotype_pool_size=phen_pool_size, allow_closer_phenotype_burden=True)
    return test_gen, signal_pgen_count_map, pgen_dat


def test__get_avg_total_implantation_count(tmp_path):
    test_gen, signal_pgen_count_map, pgen_dat = prepare_test_data(tmp_path=tmp_path, phen_pool_size=8)
    pgen_intervals_array = ImplantationHelper.get_pgen_intervals(pgen_dat=pgen_dat,
                                                                 pgen_count_map_obj=signal_pgen_count_map)
    avg_implant_count = test_gen._get_avg_total_implantation_count(pgen_intervals_array)
    assert isinstance(avg_implant_count, int)
    assert avg_implant_count == 4  # because of thresholding in PgenCountMap.get_absolute_number_of_repertoires


def test__determine_signal_sequence_combination(tmp_path):
    test_gen, signal_pgen_count_map, pgen_dat = prepare_test_data(tmp_path=tmp_path, phen_pool_size=8)
    pgen_intervals_array = ImplantationHelper.get_pgen_intervals(pgen_dat=pgen_dat,
                                                                 pgen_count_map_obj=signal_pgen_count_map)
    sequence_proportion, implantation_count, implantable_seq_subset_indices = test_gen._determine_signal_sequence_combination(
        pgen_intervals_array, round(len(pgen_intervals_array) * 0.5))
    assert sequence_proportion == 0.4
    assert implantation_count == 2
    assert implantable_seq_subset_indices == [1]


def test__get_signal_seq_combination(tmp_path):
    test_gen, signal_pgen_count_map, pgen_dat = prepare_test_data(tmp_path=tmp_path, phen_pool_size=None)
    pgen_intervals_array = ImplantationHelper.get_pgen_intervals(pgen_dat=pgen_dat,
                                                                 pgen_count_map_obj=signal_pgen_count_map)
    obtained_pool_size, implantation_stats = test_gen._get_signal_seq_combination(pgen_intervals_array)
    assert obtained_pool_size == 0
    assert implantation_stats == [0.95, 0, []]


def test_generate_signal_components(tmp_path):
    test_gen, signal_pgen_count_map, pgen_dat = prepare_test_data(tmp_path=tmp_path, phen_pool_size=8, write_file=True)
    status_code = test_gen.generate_signal_components()
    assert status_code == 1