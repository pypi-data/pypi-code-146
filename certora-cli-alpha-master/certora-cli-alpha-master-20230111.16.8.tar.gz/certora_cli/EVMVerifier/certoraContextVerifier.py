import logging

import EVMVerifier.certoraRunType as Tc
from EVMVerifier.certoraRunType import CertoraTypeError

from EVMVerifier.certoraRunContext import CertoraContext
from typing import Callable, List, Dict, Optional
from Shared.certoraUtils import RULE_SANITY_VALUES
from EVMVerifier.certoraDualArg import check_arg_and_setting_consistency

arg_logger = logging.getLogger("arguments")


def dict_to_str(dictionary: Dict[str, str]) -> str:
    """
    convert Dict to a string of the form "A=1,B=2,C=3"
    """

    return ",".join("=".join([key, value]) for key, value in dictionary.items())


def type_sanity_value(value: str) -> str:
    if not value.lower() in RULE_SANITY_VALUES:
        raise CertoraTypeError(f"sanity rule value {value} should be one of the following {RULE_SANITY_VALUES}")
    return value


class CertoraContextVerifier:
    def __init__(self, context: CertoraContext):
        self.context = context

    def verify(self) -> None:
        self.verify_has_value("files")
        self.verify_array_of_strings("files", Tc.type_input_file)
        self.verify_array_of_strings("verify", Tc.type_verify_arg)
        self.verify_array_of_strings("assert_contracts", Tc.type_contract)
        self.verify_array_of_strings("bytecode_jsons", Tc.type_json_file)
        self.verify_a_single_string("bytecode_spec", Tc.type_readable_file)
        self.verify_a_single_string("solc", Tc.type_exec_file)
        self.verify_array_of_strings("solc_args", None)
        self.verify_dictionary("solc_map", Tc.type_solc_map)
        self.verify_dictionary("optimize_map", Tc.type_optimize_map)
        self.verify_a_single_string("path", Tc.type_dir)
        self.verify_a_single_string("optimize", Tc.type_non_negative_integer)
        self.verify_a_single_string("loop_iter", Tc.type_non_negative_integer)
        self.verify_a_single_string("packages_path", Tc.type_dir)
        self.verify_array_of_strings("packages", Tc.type_package)
        self.verify_boolean("optimistic_loop")
        self.verify_a_single_string("method", Tc.type_method)
        self.verify_a_single_string("cache", lambda val: str(val))
        self.verify_a_single_string("smt_timeout", Tc.type_positive_integer)
        self.verify_array_of_strings("link", Tc.type_link_arg)
        self.verify_array_of_strings("address", Tc.type_address)
        self.verify_array_of_strings("structLink", Tc.type_struct_link)
        self.verify_array_of_strings("prototype", Tc.type_prototype_arg)
        # there is already a bug in master with this dual. Dual should be first fixed
        # how to get an error in Bank
        # certoraRun.py Bank.sol --verify Bank:Bank.spec --solc solc4.25  --settings
        #                                                              -rules=depositCorrectness --get_conf a.conf
        # and then
        # certoraRun.py a.conf
        # self.single_or_array_of_strings("rule")
        # self.single_or_array_of_strings("rules")
        self.verify_a_single_string("rule_sanity", type_sanity_value)
        self.verify_a_single_string("dynamic_bound", Tc.type_non_negative_integer)
        self.verify_boolean("dynamic_dispatch")
        self.always_true("debug")  # -- set to [] but in other no value attr the value is different
        self.always_true("debug_topics")
        self.always_true("version")
        self.always_true("staging")
        self.verify_a_single_string("cloud", lambda val: str(val))
        self.verify_a_single_string("jar", Tc.type_jar)
        self.verify_array_of_strings("java_args", Tc.type_java_arg)
        self.verify_boolean("check_args")
        self.verify_boolean("send_only")
        self.verify_boolean("build_only")
        self.verify_boolean("typecheck_only")
        self.verify_a_single_string("build_dir", Tc.type_build_dir)
        self.verify_boolean("disableLocalTypeChecking")
        self.verify_boolean("include_empty_fallback")
        self.verify_boolean("no_compare")
        self.verify_a_single_string("expected_file", Tc.type_optional_readable_file)
        self.verify_a_single_string("queue_wait_minutes", Tc.type_non_negative_integer)
        self.verify_a_single_string("max_poll_minutes", Tc.type_non_negative_integer)
        self.verify_a_single_string("log_query_frequency_seconds", Tc.type_non_negative_integer)
        self.verify_a_single_string("max_attempts_to_fetch_output", Tc.type_non_negative_integer)
        self.verify_a_single_string("delay_fetch_output_seconds", Tc.type_non_negative_integer)
        self.always_true("process")
        self.validate_settings()
        self.always_true("log_branch")
        self.verify_boolean("disable_auto_cache_key_gen")
        self.verify_boolean("multi_assert_check")
        self.verify_boolean("short_output")
        self.verify_a_single_string("max_graph_depth", Tc.type_non_negative_integer)
        self.verify_a_single_string("tool_output", Tc.type_tool_output_path)
        self.verify_a_single_string("internal_funcs", Tc.type_json_file)
        self.verify_boolean("coinbaseMode")  # --coinbaseMode  ??? used
        self.verify_a_single_string("get_conf", Tc.type_conf_file)
        self.always_true("skip_payable_envfree_check")  # --skip_payable_envfree_check  ??? used
        sort_deduplicate_list_args(self.context)

    def verify_dictionary(self, key: str, verify_func: Optional[Callable[[str], Dict[str, str]]]) -> None:
        value = getattr(self.context, key, None)
        if value is None:
            return
        if not isinstance(value, Dict):
            raise CertoraTypeError(f"value of {key} {value} is not a Dictionary")
        if verify_func is not None:
            verify_func(dict_to_str(value))

    def single_or_array_of_strings(self, key: str) -> None:
        value = getattr(self.context, key, None)
        if value is None:
            return
        if isinstance(value, List):
            self.verify_array_of_strings(key, None)
        elif not isinstance(value, str):
            raise CertoraTypeError(f"value of {key} must be a list or a string")

    def verify_array_of_strings(self, key: str, verify_func: Optional[Callable[[str], str]]) -> None:
        value = getattr(self.context, key, None)
        if value is None:
            return
        if not isinstance(value, List):
            raise CertoraTypeError(f"value of {key} {value} is not a list")
        for f in value:
            if verify_func is None:
                if not isinstance(f, str):
                    raise CertoraTypeError(f"value in {key} {f} is not a string")
            else:
                verify_func(f)

    def verify_a_single_string(self, key: str, verify_func: Optional[Callable[[str], str]]) -> None:
        value = getattr(self.context, key, None)
        if value is None:
            return
        if not isinstance(value, str):
            raise CertoraTypeError(f"value of {key} {value} is not a string")
        if verify_func is not None:
            verify_func(value)

    # keys without value appear in conf file as <key>: true
    def verify_boolean(self, key: str) -> None:
        value = getattr(self.context, key, None)
        if value is not None and value not in [True, False]:
            raise CertoraTypeError(f"value of {key} must be a boolean (true or false)")

    def verify_has_value(self, key: str) -> None:
        if not hasattr(self.context, key):
            raise CertoraTypeError(f"{key} must be set")

    # For all args with no validation rules
    @staticmethod
    def always_true(*_: str) -> None:
        pass

    def validate_settings(self) -> None:
        check_arg_and_setting_consistency(self.context)
        if getattr(self.context, "settings", None) is None:
            return
        self.verify_array_of_strings("settings", Tc.type_settings_arg)


def sort_deduplicate_list_args(context: CertoraContext) -> None:
    """
    This function takes all list arguments in the namespace and formats them in two ways:
    1. Removes all duplicate values. If any duplicate value were removed, gives an appropriate warning to the user.
    2. Sorts the values in the list in alphabetical order
    :param context: The namespace generated by the argParse, contains all the options the user gave as input
    """
    for arg_name in vars(context):
        arg_val = getattr(context, arg_name)
        if isinstance(arg_val, list) and len(arg_val) > 0:
            setattr(context, arg_name, __sort_dedup_list_arg(arg_val, arg_name))


def __sort_dedup_list_arg(arg_list: List[str], arg_name: str) -> List[str]:
    """
    This function takes a list of strings and formats it in two ways:
    1. Removes all duplicate values. If any duplicate value was removed, gives an appropriate warning to the user.
    2. Sorts the values in the list in alphabetical order
    :param arg_list: A list of strings that represents the value of a named argument.
    :param arg_name: Name of the argument this list is the value of. The name is only used in warning prints when
                     removing duplicate values.
    :return: A list with the same values as the original, without duplicates, sorted in alphabetical order.
    """
    all_members = set()
    all_warnings = set()

    for member in arg_list:
        if member in all_members:
            all_warnings.add(f'value {member} for option {arg_name} appears multiple times')
        else:
            all_members.add(member)

    for warning in sorted(list(all_warnings)):
        arg_logger.warning(warning)

    return sorted(list(all_members))
