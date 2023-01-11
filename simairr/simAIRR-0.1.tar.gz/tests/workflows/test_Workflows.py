import os
import pandas as pd
from simAIRR.workflows.Workflows import Workflows


def prepare_test_data_signal_implantation_workflow():
    public_seq_pgen_count_map = os.path.abspath(
        os.path.join(__file__, "../../../simAIRR/config_validator/public_seq_pgen_count_map.tsv"))
    signal_seq_pgen_count_map = os.path.abspath(
        os.path.join(__file__, "../../../simAIRR/config_validator/signal_seq_pgen_count_map.tsv"))
    signal_sequences = pd.DataFrame.from_dict(
        {'n_seqs': ['TGCAGTGCTAGAGATCTTTACGACAGGGAACTTTGGTCACAGCTGGAGGGAGGGGGTTATGAGCAGTTCTTC',
                    'TGTGCCACCAGTGATTATCCGACAGGGGGCTACACCTTC',
                    'TGTGCCAGCAGTGCAATCCTTGGGGGTGGGAGGGCTCCCTACGAGCAGTACTTC',
                    'TGTGCCAGCAGCAAATTCAGGGGACAGGAAACGGCTCAGCCCCAGCATTTT',
                    'TGTGCCAGCAGCATCACGGGCGGGAGCCATCAGCCCCAGCATTTT',
                    'TGTGCCAGCAGAGACTGGCGACAGGCAGATACGCAGTATTTT',
                    'TGTGCCACCAGTGATTTGCGCACGTGTGAGGGTCAGCCCCAGCATTTT',
                    'TGCGCCAGCGGGCCATCAGTTGTCGCCACCAAAAACGAGCAGTACTTC',
                    'TGCGCCAGCAGCCAAGCAATAGATTGGGGGACAGGGGGACAAGAGACCCAGTACTTC',
                    'TGTGCCAGCAGTTTCAGGTTGAATCAGCCCCAGCATTTT',
                    'TGTGCCAGCAGTTACCCATTGGGACATGGGGGGAGTAACAGAAGGGGTGGAAACACCATATATTTT',
                    'TGCATTATCCTGGGGGATCAGCCCCAGCATTTT',
                    'TGTGCCAGTAGGGCCCCAGCCCGAGAGACGAATGAAAAACTGTTTTTT',
                    'TGTGCCACCGGGACTAGGGGCAATGAGCAGTTCTTC',
                    'TGCGCCAGCAGCCAAGAAAAGCGACAGAAAGGGAACACTGAAGCTTTCTTT',
                    'TGTGCCAGCAGCCTAATCCTTGCCCCCCGGGACAGGAGAAGCAACACTGAAGCTTTCTTT',
                    'TGTGCCAGCAGCCAAGTCTCCGGGGGACAGACTGAAGCTTTCTTT',
                    'TGTGCCAGCAGTTACTCGATACGGGGGACAGAGGAGCAGTACTTC',
                    'TGTGCCAGCAGTTTAGGGTTATGTGCTATCTCACACGAGCAGTACTTC',
                    'TGTGCCAGCAGCACATCAGGGACCACGAACACTGAAGCTTTCTTT'],
         'a_seqs': ['CSARDLYDRELWSQLEGGGYEQFF',
                    'CATSDYPTGGYTF',
                    'CASSAILGGGRAPYEQYF',
                    'CASSKFRGQETAQPQHF',
                    'CASSITGGSHQPQHF',
                    'CASRDWRQADTQYF',
                    'CATSDLRTCEGQPQHF',
                    'CASGPSVVATKNEQYF',
                    'CASSQAIDWGTGGQETQYF',
                    'CASSFRLNQPQHF',
                    'CASSYPLGHGGSNRRGGNTIYF',
                    'CIILGDQPQHF',
                    'CASRAPARETNEKLFF',
                    'CATGTRGNEQFF',
                    'CASSQEKRQKGNTEAFF',
                    'CASSLILAPRDRRSNTEAFF',
                    'CASSQVSGGQTEAFF',
                    'CASSYSIRGTEEQYF',
                    'CASSLGLCAISHEQYF',
                    'CASSTSGTTNTEAFF'],
         'v_genes': ['TRBV20-1', 'TRBV24-1', 'TRBV6-1', 'TRBV13', 'TRBV7-3', 'TRBV28', 'TRBV24-1',
                     'TRBV10-1', 'TRBV4-1', 'TRBV6-6', 'TRBV6-2', 'TRBV20-1', 'TRBV19', 'TRBV7-9',
                     'TRBV4-3', 'TRBV13', 'TRBV3-1', 'TRBV6-5', 'TRBV27', 'TRBV7-9'],
         'j_genes': ['TRBJ2-1', 'TRBJ1-2', 'TRBJ2-7', 'TRBJ1-5', 'TRBJ1-5', 'TRBJ2-3',
                     'TRBJ1-5', 'TRBJ2-7', 'TRBJ2-5', 'TRBJ1-5', 'TRBJ1-3', 'TRBJ1-5',
                     'TRBJ1-4', 'TRBJ2-1', 'TRBJ1-1', 'TRBJ1-1', 'TRBJ1-1', 'TRBJ2-7',
                     'TRBJ2-7', 'TRBJ1-1']})
    user_config_dict = {'mode': 'signal_implantation',
                        'olga_model': 'humanTRB',
                        'output_path': None,
                        'n_repertoires': 10,
                        'seed': 1234,
                        'n_sequences': 10,
                        'n_threads': 2,
                        'public_seq_proportion': 0.1,
                        'public_seq_pgen_count_mapping_file': public_seq_pgen_count_map,
                        'signal_pgen_count_mapping_file': signal_seq_pgen_count_map,
                        'signal_sequences_file': None,
                        'positive_label_rate': 0.5,
                        'phenotype_burden': 2,
                        'phenotype_pool_size': None,
                        'allow_closer_phenotype_burden': True,
                        'store_intermediate_files': True}
    return user_config_dict, signal_sequences


# this covers all the other workflows
def test_signal_implantation_workflow(tmp_path):
    out_path = tmp_path / "workflow_output"
    user_config_dict, signal_sequences = prepare_test_data_signal_implantation_workflow()
    signal_file_path = os.path.join(tmp_path, 'signal_sequences.tsv')
    signal_sequences.to_csv(signal_file_path, index=None, header=None, sep='\t')
    user_config_dict['signal_sequences_file'] = signal_file_path
    user_config_dict['output_path'] = out_path
    desired_workflow = Workflows(**user_config_dict)
    desired_workflow.execute()
    simulated_files_path = os.path.join(out_path, "simulated_repertoires")
    sim_files = [fn for fn in os.listdir(simulated_files_path) if
                 os.path.isfile(os.path.join(simulated_files_path, fn))]
    assert len(sim_files) == user_config_dict['n_repertoires'] + 1
