from simAIRR.expand_repertoire_components.PublicRepertoireGeneration import PublicRepertoireGeneration
from simAIRR.pgen_count_map.PgenCountMap import PgenCountMap
import pandas as pd
import os
import importlib_resources as pkg_resources


def test_public_repertoire_generation(tmp_path):
    public_repertoires_path = tmp_path / "public_repertoires"
    outfiles_path = tmp_path / "corrected_public_repertoires"
    pgen_files_path = public_repertoires_path / "pgen_files"
    public_repertoires_path.mkdir()
    pgen_files_path.mkdir()
    pgen_rep_0 = pd.DataFrame.from_dict({'seqs': ['CASRSRSGNTIYF', 'CATGGQWANEQFF'],
                                         'pgens': [2.1830784134836584e-09, 3.738093342333351e-13]})
    pgen_rep_1 = pd.DataFrame.from_dict({'seqs': ['CSVGSTDTQYF', 'CAWSKQGEDEQFF'],
                                         'pgens': [5.644193474880578e-08, 5.4944937692245696e-11]})
    rep_0 = pd.DataFrame.from_dict({'n_seqs': ['TGTGCCAGCAGGAGCCGCTCTGGAAACACCATATATTTT',
                                               'TGTGCCACAGGGGGGCAGTGGGCCAATGAGCAGTTCTTC'],
                                    'a_seqs': ['CASRSRSGNTIYF', 'CATGGQWANEQFF'],
                                    'v_genes': ['TRBV12-3', 'TRBV12-3'], 'j_genes': ['TRBJ1-3', 'TRBJ2-1']})
    rep_1 = pd.DataFrame.from_dict({'n_seqs': ['TGCAGCGTAGGGAGCACAGATACGCAGTATTTT',
                                               'TGTGCCTGGAGTAAACAGGGGGAGGATGAGCAGTTCTTC'],
                                    'a_seqs': ['CSVGSTDTQYF', 'CAWSKQGEDEQFF'],
                                    'v_genes': ['TRBV29-1', 'TRBV30'], 'j_genes': ['TRBJ2-3', 'TRBJ2-1']})
    pgen_rep_0.to_csv(pgen_files_path / 'pgen_rep_0.tsv', index=None, header=None, sep='\t')
    pgen_rep_1.to_csv(pgen_files_path / 'pgen_rep_1.tsv', index=None, header=None, sep='\t')
    rep_0.to_csv(public_repertoires_path / 'rep_0.tsv', index=None, header=None, sep='\t')
    rep_1.to_csv(public_repertoires_path / 'rep_1.tsv', index=None, header=None, sep='\t')
    with pkg_resources.as_file(pkg_resources.files("simAIRR.config_validator").joinpath("public_seq_pgen_count_map.tsv")) as count_map_file:
        test_gen = PublicRepertoireGeneration(
            public_repertoires_path=public_repertoires_path,
            n_threads=2, pgen_count_map_obj=PgenCountMap(number_of_repertoires=4, pgen_count_map_file=count_map_file),
            desired_num_repertoires=4)
        test_gen.execute()
    out_files = [fn for fn in os.listdir(outfiles_path) if os.path.isfile(os.path.join(outfiles_path, fn))]
    assert len(out_files) == 4
    corpus = []
    for file_path in out_files:
        with open(os.path.join(outfiles_path, file_path)) as f_input:
            corpus.append(f_input.read().splitlines())
    flat_list = [line for rep in corpus for line in rep]
    assert 'TGTGCCAGCAGGAGCCGCTCTGGAAACACCATATATTTT\tCASRSRSGNTIYF\tTRBV12-3\tTRBJ1-3' in flat_list
