import importlib_resources as pkg_resources
import pytest
from simAIRR.pgen_count_map.PgenCountMap import PgenCountMap


def test_get_absolute_number_of_repertoires():
    with pkg_resources.as_file(
            pkg_resources.files("simAIRR.config_validator").joinpath(
                "public_seq_pgen_count_map.tsv")) as count_map_file:
        test_map = PgenCountMap(number_of_repertoires=200, pgen_count_map_file=count_map_file)
        with pytest.raises(KeyError) as e:
            test_map.get_absolute_number_of_repertoires((-200, -100))
        num_reps = []
        for i in range(10):
            num_reps.append(test_map.get_absolute_number_of_repertoires((-100, -20)))
        assert sum(i < 12 for i in num_reps) >= 0.7 * len(num_reps), "Warning: Unusually high number of repertoires given the weights of pgen bin"

