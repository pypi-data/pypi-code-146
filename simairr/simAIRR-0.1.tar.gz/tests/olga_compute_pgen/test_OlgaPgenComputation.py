from simAIRR.olga_compute_pgen.OlgaPgenComputation import OlgaPgenComputation
import os
import pandas as pd


def test_olga_pgen_computation(tmp_path):
    public_repertoires_path = tmp_path / "public_repertoires"
    public_repertoires_path.mkdir()
    rep_0 = pd.DataFrame.from_dict({'n_seqs': ['TGTGCCAGCAGGAGCCGCTCTGGAAACACCATATATTTT',
                                               'TGTGCCACAGGGGGGCAGTGGGCCAATGAGCAGTTCTTC'],
                                    'a_seqs': ['CASRSRSGNTIYF', 'CATGGQWANEQFF'],
                                    'v_genes': ['TRBV12-3', 'TRBV12-3'], 'j_genes': ['TRBJ1-3', 'TRBJ2-1']})
    rep_1 = pd.DataFrame.from_dict({'n_seqs': ['TGCAGCGTAGGGAGCACAGATACGCAGTATTTT',
                                               'TGTGCCTGGAGTAAACAGGGGGAGGATGAGCAGTTCTTC'],
                                    'a_seqs': ['CSVGSTDTQYF', 'CAWSKQGEDEQFF'],
                                    'v_genes': ['TRBV29-1', 'TRBV30'], 'j_genes': ['TRBJ2-3', 'TRBJ2-1']})
    rep_0.to_csv(public_repertoires_path / 'rep_0.tsv', index=None, header=None, sep='\t')
    rep_1.to_csv(public_repertoires_path / 'rep_1.tsv', index=None, header=None, sep='\t')
    comp_pgen = OlgaPgenComputation(public_repertoires_path, n_threads=2,
                                    model='humanTRB')
    comp_pgen.multi_compute_pgen()
    pgen_files_path = os.path.join(public_repertoires_path, "pgen_files")
    pgen_files = [fn for fn in os.listdir(pgen_files_path) if os.path.isfile(os.path.join(pgen_files_path, fn))]
    assert len(pgen_files) == 2
    pgen_dat_rep_0 = pd.read_csv(os.path.join(pgen_files_path, "pgen_rep_0.tsv"), header=None, index_col=None, sep='\t')
    assert pgen_dat_rep_0.shape == (2, 2)