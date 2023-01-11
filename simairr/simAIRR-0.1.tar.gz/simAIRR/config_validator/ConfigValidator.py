import sys
import yaml
import random
import os
from simAIRR.util.utilities import merge_dicts


class ConfigValidator:

    def __init__(self, user_yaml_path):
        self.user_yaml_path = user_yaml_path

    def _parse_user_yaml(self):
        with open(self.user_yaml_path, "r") as yaml_file:
            try:
                yaml_obj = yaml.load(yaml_file, Loader=yaml.FullLoader)
                assert yaml_obj is not None, "The supplied yaml file," + self.user_yaml_path + ", is empty"
            except Exception as e:
                print(
                    "Error: that looks like an invalid yaml file. Consider validating your yaml file using one of the "
                    "online yaml validators; for instance: https://jsonformatter.org/yaml-validator")
                print("Exception: %s" % str(e))
                sys.exit(1)
        return yaml_obj

    def _validate_user_config(self, config_obj):
        assert config_obj.get('mode') is not None, f"Error: argument 'mode' is required"
        allowed_modes = ["baseline_repertoire_generation", "public_component_correction",
                         "signal_implantation", "signal_feasibility_assessment"]
        assert config_obj.get('mode') in allowed_modes, f"Error: Invalid mode. Mode should be one of {allowed_modes}."
        self._schema_validator(schema_dict=self._get_mode_specific_schema_dict(mode=config_obj['mode']),
                               document_dict=config_obj)

    def _get_mode_specific_default_params_dict(self, mode):
        mode_agnostic_dict = {'mode': "signal_implantation", 'olga_model': None,
                              'output_path': os.path.join("./", "simairr_output"), 'n_repertoires': None,
                              'seed': random.randint(1, 10000), 'store_intermediate_files': False}
        baseline_dict = {'n_sequences': None, 'n_threads': None}
        public_component_dict = {'n_threads': None, 'public_seq_proportion': 0.1,
                                 'public_seq_pgen_count_mapping_file': os.path.join(os.path.dirname(__file__),
                                                                                    "public_seq_pgen_count_map.tsv")}
        signal_implant_dict = {
            'signal_pgen_count_mapping_file': os.path.join(os.path.dirname(__file__), "signal_seq_pgen_count_map.tsv"),
            'signal_sequences_file': None, 'positive_label_rate': 0.5, 'phenotype_burden': None,
            'phenotype_pool_size': None, 'allow_closer_phenotype_burden': True, 'export_nt': True}
        mode_specific_dicts = {"baseline_repertoire_generation": merge_dicts([mode_agnostic_dict, baseline_dict]),
                               "public_component_correction": merge_dicts(
                                   [mode_agnostic_dict, baseline_dict, public_component_dict]),
                               "signal_implantation": merge_dicts(
                                   [mode_agnostic_dict, baseline_dict, public_component_dict, signal_implant_dict]),
                               "signal_feasibility_assessment": merge_dicts(
                                   [mode_agnostic_dict, baseline_dict, public_component_dict, signal_implant_dict])}
        return mode_specific_dicts[mode]

    def _get_mode_specific_schema_dict(self, mode):
        mode_agnostic_dict = {'mode': {'required': True, 'type': str,
                                       'allowed': ["baseline_repertoire_generation", "public_component_correction",
                                                   "signal_implantation", "signal_feasibility_assessment"]},
                              'olga_model': {'required': True, 'type': str,
                                             'allowed': ['humanTRA', 'humanTRB', 'humanIGH', 'mouseTRB']},
                              'output_path': {'required': False, 'type': (str, type(None))},
                              'n_repertoires': {'required': True, 'type': int},
                              'seed': {'required': False, 'type': (int, type(None))},
                              'store_intermediate_files': {'required': False, 'type': (bool, type(None))}}
        baseline_dict = {'n_sequences': {'required': True, 'type': int}, 'n_threads': {'required': True, 'type': int}}
        public_component_dict = {'n_threads': {'required': True, 'type': int},
                                 'public_seq_proportion': {'required': False, 'type': (float, type(None))},
                                 'public_seq_pgen_count_mapping_file': {'required': False, 'type': (str, type(None))}}
        signal_implant_dict = {
            'signal_pgen_count_mapping_file': {'required': False, 'type': (str, type(None))},
            'signal_sequences_file': {'required': True, 'type': str},
            'positive_label_rate': {'required': False, 'type': (float, type(None))},
            'phenotype_burden': {'required': True, 'type': int},
            'phenotype_pool_size': {'required': False, 'type': (int, type(None))},
            'allow_closer_phenotype_burden': {'required': False, 'type': (bool, type(None))},
            'export_nt': {'required': False, 'type': (bool, type(None))}}
        mode_specific_dicts = {"baseline_repertoire_generation": merge_dicts([mode_agnostic_dict, baseline_dict]),
                               "public_component_correction": merge_dicts(
                                   [mode_agnostic_dict, baseline_dict, public_component_dict]),
                               "signal_implantation": merge_dicts(
                                   [mode_agnostic_dict, baseline_dict, public_component_dict, signal_implant_dict]),
                               "signal_feasibility_assessment": merge_dicts(
                                   [mode_agnostic_dict, baseline_dict, public_component_dict, signal_implant_dict])}
        return mode_specific_dicts[mode]

    def _update_user_config(self, mode, config_obj):
        default_config_obj = self._get_mode_specific_default_params_dict(mode)
        default_config_obj.update(config_obj)
        return default_config_obj

    def _schema_validator(self, schema_dict, document_dict):
        for key in schema_dict.keys():
            if schema_dict[key]['required']:
                assert document_dict.get(key) is not None, f"Error: argument {key} is required"
            assert isinstance(document_dict.get(key),
                              schema_dict[key]['type']), f"Error: argument {key} should be a {schema_dict[key]['type']}"
            if isinstance(document_dict.get(key), int) and not isinstance(document_dict.get(key), bool):
                assert document_dict.get(key) > 0, f"Error: argument {key} should be a positive integer"
            if isinstance(document_dict.get(key), float):
                assert 0 <= document_dict.get(key) <= 1, f"Error: argument {key} should be a float between 0 and 1"
            if 'allowed' in schema_dict[key].keys():
                assert document_dict.get(key) in schema_dict[key][
                    'allowed'], f"Error: invalid value supplied for argument {key}"

    def execute(self):
        usr_yaml = self._parse_user_yaml()
        self._validate_user_config(config_obj=usr_yaml)
        updated_config = self._update_user_config(mode=usr_yaml['mode'], config_obj=usr_yaml)
        return updated_config
