from .closest_furthest_value import (
    furthest_value_in_list,
    closest_value_in_list,
    furthest_value_in_dict,
    closest_value_in_dict,
)
from .dublicates import find_dublicates, remove_dublicates
from .percentage import (
    get_percentage_as_fitted_string,
    progress_printer,
    main_and_sub_progress_printer,
)
from .sorter import sorted_dict
from .string_transformation import (
    upper_case_first_letter_of_word,
    upper_case_first_letter_of_words,
)
from .unpack import unpack_list


from . import _version

__version__ = _version.get_versions()["version"]
