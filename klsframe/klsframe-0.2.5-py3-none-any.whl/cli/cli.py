import re
from typing import Union
from klsframe.utilities.utils import validate, text_padding, dict_to_table


def confirm_yes_no(selection=None, default=True, allow_empty=True, shortened=True):
    a = 'yes'
    b = 'no'
    if shortened:
        a = 'y'
        b = 'n'
    if isinstance(default, bool) and default:
        hint = f'[{a.upper()}/{b}]'
    elif isinstance(default, bool) and not default:
        hint = f'[{b.upper()}/{a}]'
    else:
        raise ValueError("Unexpected value for parameter 'default'")

    if selection is None:
        sel_str = ''
    else:
        sel_str = f"You selected:\n{text_padding(selection, decorator='*', decorate_lines='first')}\n"
    while True:
        opt = input(f"{sel_str}>> Do you want to continue? {hint}\t").strip().lower()
        if opt == '':
            if allow_empty:
                return default
            else:
                print("Please provide an answer")
        elif re.match('(no|n)', opt):
            return False
        elif re.match('(yes|y)', opt):
            return True
        else:
            print(f"Option '{opt}' not recognized")


def continue_or_exit():
    # TODO: develop continue_or_exit(). A function that allows the program to continue or stops it
    # Based on confirm_yes_no(), although the 'no' option implies exit()
    if confirm_yes_no():
        return None
    else:
        exit(0)


def safe_string_input(validations=None, prompt=None, error_msg=None, confirm=False, allow_empty=True):
    """
    Safe input for string values. Reads input from terminal, performing some security checks on the input

    Arguments:
        :param validations: Set of RegExp indicating the possible values of the input, like a whitelist
        :param prompt: Custom text to be displayed before reading the input
        :param error_msg: Custom text to be displayed when input does not match valid regex
        :param confirm: Enables/Disables the prompt confirmation after entering a value
        :param allow_empty: Allow/Disallow empty as input
    """
    # Validate the parameters
    if validations is None:
        validations = []
    if error_msg is None:
        error_msg = "Error. Invalid input"
    if prompt is None:
        prompt = "Please introduce a value:"
    while True:
        inval = input(f"{prompt}\t")
        if not allow_empty and inval == "":
            print(f"{error_msg} (Input cannot be empty)")
        elif validate(inval, validations):
            if bool(confirm) and not confirm_yes_no(inval):  # Confirmation prompt enabled
                continue  # Confirmation: rejected. Continue the questioning loop
            else:  # Confirmation prompt disabled, or accepted
                return inval
        else:  # Validation failed
            print(f"{error_msg} (Validation failed)")


def safe_number_input(min_val=None, max_val=None, prompt=None,
                      decimal_digits=None, decimal_sep='.', default=None, **kwargs) -> Union[int, float]:
    """
    Safe input for numeric values.

    :param min_val: Min value allowed. None (-infinite) by default
    :param max_val: Max value allowed. None (infinite) by default
    :param prompt: Custom message for the input prompt
    :param decimal_digits: Decimal digit count. 0 (default) for integer numbers.
        If not None, the input is rounded to ``decimal_digits``
    :param decimal_sep: Character used to separate the decimal part from the integer part.
        Allowed chars: '.' | ','. Note: decimal_sep = '.' <==> thousand_sep = ',' (and vice versa)
    :param default: Default value for the input. If not None, if the user inputs an empty value,
        the default value will be returned. If None, the user input cannot be empty
    :return: The validated and sanitized number input by the user
    """
    if decimal_sep == '.':
        thousand_sep = ','
    elif decimal_sep == ',':
        thousand_sep = '.'
    else:
        raise ValueError("Unexpected value for parameter 'decimal_sep'. Allowed: ,|.")
    if decimal_digits is not None and not isinstance(decimal_digits, int):
        raise TypeError("Unexpected type for parameter 'decimal_digits'. Allowed: int")
    bounds = f"[{min_val}, {max_val}]".replace('[None', '(-infinite').replace('None]', 'infinite)')
    # General number regex
    custom_regex = "^-?([0-9]{1,3}" + thousand_sep + ")*[0-9]+"
    if decimal_digits is None:
        _prompt = f'Please introduce a number within {bounds}'
        custom_regex += "(\\" + decimal_sep + "[0-9]+)?"
    elif decimal_digits > 0:
        custom_regex += "(\\" + decimal_sep + "[0-9]+)?"
        _prompt = f'Please introduce an decimal number (up to {decimal_digits} decimal digits) within {bounds}'
    else:
        _prompt = f'Please introduce an integer number within {bounds}'
    if prompt is not None:
        _prompt = prompt
    # Check parameter `default`
    if 'allow_empty' in kwargs and kwargs['allow_empty'] and isinstance(kwargs['allow_empty'], bool):
        _allow_empty = kwargs['allow_empty']
        if _allow_empty:
            custom_regex = f"({custom_regex})?"  # Include the empty input in the regex
    else:
        _allow_empty = False
    if default is not None:
        _prompt += f" [default: {default}]"  # Inform the user about the default value
    # Questioning loop
    while True:
        inval = safe_string_input(prompt=_prompt, validations=custom_regex,
                                  error_msg="Error. Not a number, or expecting an integer but received a float",
                                  allow_empty=_allow_empty).replace(thousand_sep, '')
        if inval == '' and _allow_empty:  # If user input is empty, use the default value
            return default
        elif decimal_digits is None:
            try:
                if inval.find(decimal_sep) != -1:
                    inval = float(inval)
                else:
                    inval = int(inval)
            except ValueError:
                print(f"[ERROR] Unexpected numeric value ({inval})")
        elif decimal_digits > 0:
            inval = float(inval).__round__(decimal_digits)
        else:
            inval = int(inval)
        if (min_val is None or min_val <= inval) and (max_val is None or max_val >= inval):
            return inval
        else:
            print(f"[ERROR] Value out of bounds {bounds}")


def safe_list_input(max_size=-1, fixed_size=-1, sep=",", ltype="string", allow_repeated=True, validations=None,
                    prompt=None, confirm=False, allow_empty=True, **kwargs):
    """
    TODO: selectable list using the arrows
    :param max_size:
    :param fixed_size:
    :param sep:
    :param ltype:
    :param allow_repeated:
    :param validations:
    :param prompt:
    :param confirm:
    :param allow_empty:
    :param kwargs:
    :return:
    """
    _allowed_types = ['string', 'number']
    if fixed_size is not None and fixed_size > 0:
        print(f"[WARN] 'fixed_size' = {fixed_size} != {max_size} = 'max_size'."
              f" Overwriting 'max_size' value with 'fixed_size")
        max_size = fixed_size
    if prompt is None:
        pre_prompt = ''
    else:
        pre_prompt = f"{prompt}\n"
    while True:
        user_input = []
        if sep == 'new-line':
            # read each item in a new line
            # empty input to finish or max size reached
            # prompt = (i-th) value
            print(f"{pre_prompt}Press enter to add a value. Empty input to finish")
            counter = 1
            while True:
                if ltype == 'string':
                    inval = safe_string_input(
                        validations=validations,
                        prompt=f"({counter})"
                    )
                elif ltype == 'number':
                    inval = safe_number_input(
                        prompt=f"({counter})",
                        allow_empty=True,
                        **kwargs
                    )
                else:
                    raise ValueError("Unexpected value for parameter 'ltype'. Allowed: string|number")
                if inval is None or inval == '':
                    if fixed_size == -1 or len(user_input) == fixed_size:
                        break
                    else:
                        print(f"Required values: {fixed_size}. Missing: {fixed_size - len(user_input)}")
                        continue
                else:
                    if bool(allow_repeated) or inval not in user_input:
                        user_input.append(inval)
                        counter += 1
                    else:
                        print(f"[ERROR] Duplicates not allowed ({inval})")

                if max_size != -1 and len(user_input) >= max_size:
                    break
        else:
            # Single line input using sep
            # Read up to ``size`` items
            inval = safe_string_input(
                validations=validations,
                prompt=f"{pre_prompt}Enter the values separated by '{sep}':"
            )
            if max_size is not None and max_size > 0:
                _limit = max_size
            else:
                _limit = len(inval)
            if ltype == 'number':
                for num in [item.strip() for item in inval.split(sep)[0:_limit]]:
                    try:
                        if num.find('.') != -1:
                            user_input.append(float(num))
                        else:
                            user_input.append(int(num))
                    except ValueError:
                        print(f"[WARN] Invalid value found in the input list ({num})")
            elif ltype == 'string':
                if inval != '':
                    user_input.extend([item.strip() for item in inval.split(sep)[0:_limit]])
            else:
                raise ValueError("Unexpected value for parameter 'ltype'. Allowed: number|string")
            if not allow_repeated:
                user_input = list(set(user_input))
        if not allow_empty and len(user_input) == 0:
            print("Error. The list cannot be empty")
            continue
        elif fixed_size is not None and 0 < fixed_size != len(user_input):
            print(f"Error. Required values: {fixed_size}. Missing: {fixed_size - len(user_input)}")
            continue
        elif not confirm or (confirm and confirm_yes_no(user_input)):
            break
    return user_input


# def safe_number_list_input(size=-1, sep=",", min_val=0, max_val=0, decimal_digits=2, default=0, prompt=f"()",
#                            confirm=False):
#     # TODO: Differentiate between safe_number_list_input() and safe_string_list_input()?
#     pass

def selectable_list(args: list, placeholder=None, custom_prompt=None, enable_custom=False, verbose=False):
    # I disabled the param allow_empty because if a custom opt is offered, the empty option should not be available,
    # If you want to offer an "empty" option, you should include it in the list
    # :param allow_empty:
    #       Enables/disables empty input. Only applied on custom inputs (when ``enable_custom`` is ``True``)
    """
    TODO: Update selectable_list() docstring
    Examples:
        tcp_sc = selectable_list(scan_policy.tcp_scans(), placeholder=lambda x: f"Custom prefix {x}")
        recon_sc = selectable_list(scan_policy.recon_scans(), 'An additional scan')

    :param args: List of things (object, list, dictionaries) to be listed
    :param placeholder: function or lambda that generates a custom string for each element of the list.
    If it is None the string representation of the item is used. The strings are used for the list representation
    :param custom_prompt: custom function that request an input and return a value
    :param enable_custom: Enables/disables the custom option
    :param verbose: True to increase verbosity. False by default
    :return: A dict like: {'index': index of the selected element within the list, 'value': element selected}
    """
    if placeholder is None:
        placeholder = lambda x: x
    if (enable_custom is None or enable_custom is False) and custom_prompt is not None:
        # In the case of providing a custom prompt, enabled_custom is supposed to be True
        enable_custom = True
    aux = []  # List used to expand the selectable list with Cancel and Custom options
    # Generate the printable prompt
    indent = ' ' * 2
    counter = 0
    printable_prompt = ['Available options', '>', f'{indent}0. Cancel operation', '>']
    for elem in args:
        if isinstance(elem, list):
            for i in elem:
                counter += 1
                printable_prompt.insert(-1, f'{indent}{counter}. {placeholder(i)}')
                aux.append(i)
        # each dict item should not be selectable and independent of the rest of its sibling items
        elif isinstance(elem, dict):
            counter += 1
            val = text_padding(placeholder(f"\n{dict_to_table(elem)}"), padding=5)
            printable_prompt.insert(-1, f'{indent}{counter}. {val}')
            aux.append(elem)
        elif isinstance(elem, MenuEntry) and isinstance(elem.value, dict):
            counter += 1
            val = text_padding(placeholder(f"\n{dict_to_table(elem.value)}"), padding=5)
            printable_prompt.insert(-1, f'{indent}{counter}. {val}')
            aux.append(elem)
        else:
            counter += 1
            printable_prompt.insert(-1, f'{indent}{counter}. {placeholder(elem)}')
            aux.append(elem)
    # Add the custom option in the end. Maybe is better at the beginning?
    if enable_custom:
        counter += 1
        printable_prompt.insert(-1, f'{indent}{counter}. Custom value')
    while True:
        try:
            print("\n".join(printable_prompt))
            selection = int(input(f'\nPlease select one:\t'))
            if selection == 0:
                print(f'Operation canceled. Exiting...')
                exit(0)
            elif selection not in range(1, counter + 1):
                raise IndexError()
            else:
                if enable_custom and selection == counter:  # Custom option selected
                    # Counter = -1 => clarify that the (custom) option is not included in the list provided by the user
                    counter = -1
                    if custom_prompt is None:
                        value = safe_string_input(allow_empty=False)
                    else:
                        value = custom_prompt()
                else:  # Any other option selected
                    if verbose:
                        print(f"You selected: ({selection}) {aux[selection - 1]}")
                    counter = selection - 1  # Update counter to store the selected index
                    value = aux[selection - 1]
                break
        except ValueError:
            print(f'Error. Option not recognized')
        except IndexError:
            print(f'Error. Option out of bounds. Please select a number within the list')
    return {"index": counter, "value": value}


# --------------------------------------------------------------------------
# --------------------<| M E N U |>-----------------------------------------
# --------------------------------------------------------------------------
class MenuEntry:
    def __init__(self, val, desc=None, callback=None):
        self.value = val
        if desc is not None:
            self.description = str(desc)
        else:
            self.description = None
        self.callback = callback

    def __str__(self):
        if self.description is not None and self.description != self.value:
            return f"'{str(self.value)}' ({self.description})"
        else:
            return f"'{str(self.value)}'"

    def __repr__(self):
        return str(self.value)


class Menu:
    def __init__(self, title=None, desc=None, allowcustom=False, customprompt=None):
        if title is None:
            self.title = 'Untitled menu'
        else:
            self.title = f"{title} menu"
        if desc is None:
            self.description = 'no description provided'
        else:
            self.description = str(desc)
        self.entries = []
        self.allow_custom = allowcustom
        self.custom_prompt = customprompt

    def add_entry(self, value, description=None, callback=None):
        self.entries.append(MenuEntry(value, description, callback))

    def add_entries(self, iterable: Union[dict, list]):
        """

        :param iterable: a dict like {'option1 description': 'option1 value', opt2...}
            or a list of serialized (dictionaries) MenuEntry instances
        :return:
        """
        if isinstance(iterable, dict):
            for k, v in iterable.items():
                self.add_entry(v, k)
        elif isinstance(iterable, list):
            for elem in iterable:
                if isinstance(elem, dict) and 'value' in elem:
                    val = elem['value']
                else:
                    val = elem
                if isinstance(elem, dict) and 'description' in elem:
                    desc = elem['description']
                else:
                    desc = None
                if isinstance(elem, dict) and 'callback' in elem:
                    cb = elem['callback']
                else:
                    cb = None
                self.add_entry(val, description=desc, callback=cb)
        else:
            raise TypeError("Unexpected type for parameter 'iterable'. Allowed: dict | list")

    def open(self, verbose=False):
        if verbose:
            print(f"{self.title} - {self.description}")
        ret = selectable_list(self.entries, enable_custom=self.allow_custom, custom_prompt=self.custom_prompt)
        if isinstance(ret['value'], MenuEntry) and ret['value'].callback is not None:
            ret['value'].callback()
        return ret


# --------------------------------------------------------------------------
# --------------------<| F O R M S |>---------------------------------------
# --------------------------------------------------------------------------

class StringField:
    def __init__(self, name: str, description='', example='', ftype='string', regex=None, allow_empty=True,
                 confirm=False, defaultval=None):
        _allowed_types = ['string', 'numeric', 'list']
        if ftype not in _allowed_types:
            raise ValueError(f"Invalid value for FormField.ftype. Allowed values are: {', '.join(_allowed_types)}")
        elif not isinstance(allow_empty, bool):
            raise TypeError("Invalid value for FormField.is_nullable. Only bool allowed")
        else:
            self.ftype = str(ftype)
            self.name = str(name)
            self.description = str(description)
            self.example = str(example)
            self.confirm = bool(confirm)
            self.regex = regex
            self.allow_empty = bool(allow_empty)
            self.default_value = defaultval

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        name = self.name
        desc = self.description
        eg = self.example
        if self.description == '':
            desc = 'Description not provided'
        if self.example == '':
            eg = 'not provided'
        return f"'{name}': {desc}. (e.g.: {eg})"

    def long_str(self):
        name = self.name
        desc = self.description
        eg = self.example
        if self.description == '':
            desc = 'Not provided'
        if self.example == '':
            eg = 'Not provided'
        return f"  Title: {name}\n  Description: {desc}\n  Example: {eg}"

    def input(self):
        # while True:
        return safe_string_input(
            validations=self.regex,
            prompt=f'>> {self.name} = ',
            confirm=self.confirm,
            allow_empty=self.allow_empty
        )
        # inval = input(f'>> {self.name} = ')
        # if inval == '' and not self.is_nullable:
        #     print(f'[ERROR] This field cannot be empty and must match')
        #     continue
        # # Check field syntax
        # if self.regex is not None and re.fullmatch(self.regex, inval) is None:
        #     print(f'[ERROR] Invalid input syntax')
        #     continue
        # return inval


class NumericField(StringField):
    def __init__(self, name, decimal_digits=None, decimal_separator='.', min_val=None, max_val=None, **kwargs):
        _allowed_separators = [',', '.']
        if min_val > max_val:
            raise ArithmeticError("Parameter 'min_val' is greater than 'max_val'")
        elif decimal_separator not in _allowed_separators:
            raise ValueError("Unexpected value for the parameter 'decimal_separator'. Allowed: ',' | '.'")
        else:
            super().__init__(name=name, ftype='numeric', **kwargs)
            self.min_val = min_val
            self.max_val = max_val
            self.decimal_digits = decimal_digits
            self.decimal_separator = decimal_separator

    @property
    def get_regex(self):
        # TODO: Build regex from min_val, max_val, decimal_digits and decimal_separator
        custom_regex = "^"
        if self.min_val < 0 or self.max_val < 0:
            custom_regex += "-?"
        if self.max_val is None:
            custom_regex += "[0-9]+"
        else:
            custom_regex += "[0-9]{1," + str(
                len(str(self.max_val).replace('-', '').split(self.decimal_separator))) + "}"
        if self.decimal_digits > 0:
            custom_regex += f"(\\{self.decimal_separator}[0-9]" + "{1," + str(self.decimal_digits) + "})?"
        return custom_regex

    def input(self):
        return safe_number_input(
            min_val=self.min_val,
            max_val=self.max_val,
            decimal_digits=self.decimal_digits,
            decimal_sep=self.decimal_separator,
            default=self.default_value,
            prompt=f'>> {self.name} = ',
            confirm=self.confirm,
            allow_empty=self.allow_empty
        )
        # if self.decimal_digits > 0:
        #     inval = float(inval)
        # else:
        #     inval = int(inval)
        # if self.min_val <= inval <= self.max_val:
        #     return inval
        # else:
        #     raise ValueError(f"Value out of range. Allowed: [{self.min_val}, {self.max_val}]")


class ListField(StringField):
    def __init__(self, name, sep=',', max_size=-1, fixed_size=-1, ltype="string", allow_repeated=True, **kwargs):
        if ltype in ['string', 'number']:
            super().__init__(name=name, ftype='list', **kwargs)
            self.ltype = ltype
            self.sep = sep
            self.max_size = max_size
            self.fixed_size = fixed_size
            self.allow_repeated = bool(allow_repeated)
            self.properties = kwargs
        else:
            raise ValueError("Unexpected value for parameter 'ltype'. Allowed: string|number")

    def input(self):
        return safe_list_input(
            max_size=self.max_size,
            fixed_size=self.fixed_size,
            sep=self.sep,
            ltype=self.ltype,
            allow_repeated=self.allow_repeated,
            validations=self.regex,
            confirm=self.confirm,
            allow_empty=self.allow_empty,
            **self.properties
        )


class PromptForm:
    """
    Contrary to the class ``Menu``, which allows the user to select an option from a list,
    the Form class allows the user to input values
    """

    def __init__(self, title='untitled', desc=''):
        self.title = str(title)
        self.description = str(desc)
        self.fields = []
        self.last_result = {}
        # TODO: usar pandas
        # las columnas son los tries
        # Las filas los campos del formulario

    def __str__(self):
        return f"PromptForm('{self.title}')"

    def show_info(self):
        print(f"---< Form '{self.title}' >---\n{self.description}\n---------")
        for f in self.fields:
            print(f"- {f}")

    def get_summary_table(self):
        return f"\n----< Form '{self.title}' >----\n{dict_to_table(self.last_result)}"

    def add_string_field(self, name, **kwargs):
        self.fields.append(StringField(name=name, **kwargs))

    def add_numeric_field(self, name, **kwargs):
        self.fields.append(NumericField(name=name, **kwargs))

    def add_list_field(self, name, **kwargs):
        self.fields.append(ListField(name=name, **kwargs))

    def reset(self):
        self.last_result.clear()

    def fill_in(self, compact_mode=True, confirm=False):
        while True:
            input_form = {}
            print(f"---< Form '{self.title}' >---")
            if not compact_mode:
                print(f"{self.description}\n{'-' * 20}")
            field_num = 0
            while True:
                if field_num >= len(self.fields):
                    break
                field = self.fields[field_num]
                if isinstance(field, StringField):
                    # Print field information
                    prompt = f"[Field {field_num + 1}/{len(self.fields)}]"
                    if compact_mode:
                        prompt += f" {field}"
                    else:
                        prompt += f"\n{field.long_str()}"
                    print(prompt)
                    input_form[field.name] = field.input()
                    field_num += 1
                else:
                    raise TypeError("Invalid field type. Only cli.StringField allowed")
            self.last_result.update(input_form)
            if not confirm or (confirm and confirm_yes_no(self.get_summary_table())):
                break
            else:
                continue
        return input_form

    def export(self):
        # TODO: cli.PromptForm.export()
        # Exports the lasts results into a txt or json file
        pass


# --------------------------------------------------------------------------
# --------------------<| M A I N |>-----------------------------------------
# --------------------------------------------------------------------------


if __name__ == '__main__':
    # Do some quick tests here
    pass
