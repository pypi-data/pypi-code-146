import pandas as pd
import numpy as np
import random
import pandas.api.types as ptypes


class PgenCountMap:

    def __init__(self, number_of_repertoires, pgen_count_map_file):
        self.number_of_repertoires = number_of_repertoires
        self.pgen_count_map_file = pgen_count_map_file
        self.pgen_count_map = self._process_pgen_count_map()
        self.pgen_count_map_dict = self._get_pgen_bin_sample_size_weights()

    def _process_pgen_count_map(self):
        pgen_count_map = pd.read_csv(self.pgen_count_map_file, index_col=None, header=0, sep='\t')
        header_fields = ['pgen_left', 'pgen_right', 'sample_size_prop_left', 'sample_size_prop_right', 'prob']
        assert list(pgen_count_map.columns) == header_fields, f"public_seq_pgen_count_mapping_file should have the " \
                                                             f"following fields in the header:{header_fields}"
        assert pgen_count_map.isnull().sum().sum() == 0, f"public_seq_pgen_count_mapping_file cannot have NaNs"
        assert all(ptypes.is_numeric_dtype(pgen_count_map[col]) for col in pgen_count_map.columns), \
            f"All fields of public_seq_pgen_count_mapping_file should be of numeric type"
        pgen_count_map[pgen_count_map < 0] = 1e-100
        pgen_count_map[pgen_count_map > 1] = 1.0
        pgen_count_map[['pgen_left', 'pgen_right']] = np.log10(
            pgen_count_map[['pgen_left', 'pgen_right']]).astype(int)
        return pgen_count_map

    def get_pgen_breaks(self):
        pgen_breaks = sorted(list(set(self.pgen_count_map['pgen_left']).union(set(self.pgen_count_map['pgen_right']))))
        return pgen_breaks

    def _get_pgen_bin_sample_size_weights(self):
        self.pgen_count_map['pgen_bin'] = self.pgen_count_map[['pgen_left', 'pgen_right']].apply(tuple, axis=1)
        self.pgen_count_map['sample_size_prop_bin'] = self.pgen_count_map[
            ['sample_size_prop_left', 'sample_size_prop_right']].apply(tuple, axis=1)
        new_pgen_count_map = self.pgen_count_map[['pgen_bin', 'sample_size_prop_bin', 'prob']]
        new_pgen_count_map = new_pgen_count_map.groupby('pgen_bin')[['sample_size_prop_bin', 'prob']].apply(
            lambda x: x.set_index('sample_size_prop_bin').to_dict(orient='dict')).to_dict()
        new_pgen_count_map = {key: value['prob'] for key, value in new_pgen_count_map.items()}
        return new_pgen_count_map

    def _get_implantation_rate(self, seq_pgen_bin: tuple):
        # pgen_count_map_dict = self._get_pgen_bin_sample_size_weights()
        sample_size_intervals_list = list(self.pgen_count_map_dict[seq_pgen_bin].keys())
        keys_len = len(sample_size_intervals_list)
        weights_list = list(self.pgen_count_map_dict[seq_pgen_bin].values())
        sample_size_lower, sample_size_upper = \
        [sample_size_intervals_list[i] for i in np.random.choice(keys_len, 1, p=weights_list)][0]
        return random.uniform(sample_size_lower, sample_size_upper)

    def get_absolute_number_of_repertoires(self, seq_pgen_bin: tuple):
        implant_rate = self._get_implantation_rate(seq_pgen_bin)
        absolute_number_of_repertoires = round(implant_rate * self.number_of_repertoires)
        if absolute_number_of_repertoires < 2:
            absolute_number_of_repertoires = 2
        return absolute_number_of_repertoires


