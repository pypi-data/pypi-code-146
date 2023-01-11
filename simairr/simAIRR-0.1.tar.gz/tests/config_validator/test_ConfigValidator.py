import pytest
from simAIRR.config_validator.ConfigValidator import ConfigValidator


def test_validate_user_config_mode_none():
    usr_yaml = {'olga_model': 'humanTRB', 'n_repertoires': 10,
                'n_sequences': 20, 'n_threads': 2}
    test_conf = ConfigValidator("mock_string_to_replace_path")
    with pytest.raises(AssertionError) as e:
        test_conf._validate_user_config(config_obj=usr_yaml)


def test_validate_user_config_mode_invalid():
    usr_yaml = {'mode': 2, 'olga_model': 'humanTRB', 'n_repertoires': 10,
                'n_sequences': 20, 'n_threads': 2}
    test_conf = ConfigValidator("mock_string_to_replace_path")
    with pytest.raises(AssertionError) as e:
        test_conf._validate_user_config(config_obj=usr_yaml)


def test_validate_user_config_missing_required():
    usr_yaml = {'mode': "signal_implantation", 'olga_model': 'humanTRB', 'n_repertoires': 10,
                'n_sequences': 20, 'n_threads': 2}
    test_conf = ConfigValidator("mock_string_to_replace_path")
    with pytest.raises(AssertionError) as e:
        test_conf._validate_user_config(config_obj=usr_yaml)


def test_update_user_config():
    usr_yaml = {'mode': "public_component_correction", 'olga_model': 'humanTRB', 'n_repertoires': 10,
                'n_sequences': 20, 'n_threads': 2, 'seed': 999, 'public_seq_pgen_count_mapping_file': './mock.tsv'}
    test_conf = ConfigValidator("mock_string_to_replace_path")
    updated_config = test_conf._update_user_config(mode="public_component_correction", config_obj=usr_yaml)
    assert updated_config == {'mode': 'public_component_correction', 'olga_model': 'humanTRB',
                              'output_path': './simairr_output', 'n_repertoires': 10, 'seed': 999, 'n_sequences': 20,
                              'n_threads': 2, 'public_seq_proportion': 0.1,
                              'public_seq_pgen_count_mapping_file': './mock.tsv',
                              'store_intermediate_files': False}, f"Error: user config update failed"
