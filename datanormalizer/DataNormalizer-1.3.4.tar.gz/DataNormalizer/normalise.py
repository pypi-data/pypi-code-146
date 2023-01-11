# See if we can find the mismatch causing the error and fix it in normalise
import bisect
import json
import re
from collections import namedtuple
from difflib import SequenceMatcher
from math import floor
from time import time
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
import numpy as np


class Normalise:

    def __init__(self):
        self._dataframe = None
        self._rules = None

    @property
    def dataframe(self):
        return self._dataframe

    @dataframe.setter
    def dataframe(self, value):
        self._dataframe = value

    @property
    def rules(self):
        return self._rules

    @rules.setter
    def rules(self, value):
        self._rules = value

    def check_rules(self) -> pd.DataFrame:
        """Pass a dataframe and a JSON rules file to check if the rules are valid"""
        dataframe = self._dataframe
        rules = self._rules

        # Global settings
        reset_coverage = False
        global_check_coverage = False
        global_action = False
        global_verbose = "to_console"

        # Which rows to drop in one go
        drop_array = []
        
        # Which rows to np.nan in one go
        nan_array = []

        # Which rows to none in one go
        none_array = []

        error_file = None

        # regex to match the string to_file in between quotes or double quotes
        regex = re.compile(r'\"(to_file)\"|\'(to_file)\'')
        if regex.search(str(rules)):
            error_file = open(str(floor(time())) + ".txt", "a")

        global_mapping = False

        # Contains "action" and "verbose"
        errors_found = False

        def is_value_array(key, value) -> bool:
            if type(rules[j][key]) != list:
                print(f'{key} expects an array but got "{value}" maybe try ["{value}"]')
                return False
            return True

        # Gets called when row doesn't match rule
        def handle_mismatch(i, value, rows):
            nonlocal errors_found
            errors_found = True

            action = global_action
            if "action" in rules[j]:
                action = rules[j]["action"]

            if action in ("np.nan", "np_nan", "nan", "NaN", "np-nan"):
                # Which rows to np.nan later on in one go
                nan_array.append(i)

            if action in ("None", "none"):
                # Which rows to None later on in one go
                none_array.append(i)

            if action == "drop":
                # Which rows to drop later onin one go
                drop_array.append(i)

            # Feedback management to user
            verbose = global_verbose
            if "verbose" in rules[j]:
                verbose = rules[j]["verbose"]

            if verbose == "to_file":
                error_file.write(
                    str(rules[j]["column"]) + " mismatch row " + str(i) + " - " + str(value) + "\n")

            if verbose == "to_console" or "verbose" in rules[j] == False:
                print(str(rules[j]["column"]) +
                      " mismatch row " + str(i) + " - " + str(value))

        def find_global_rules(j, rules):
            if not ("column" in rules[j]):
                nonlocal global_check_coverage
                nonlocal reset_coverage
                nonlocal global_action
                nonlocal global_verbose
                nonlocal global_mapping
                nonlocal dataframe

                # Change all column names
                if "normalise_columns" in rules[j]:
                    if is_value_array(key = "normalise_columns", value = rules[j]["normalise_columns"]) is False:
                        return

                    for option in rules[j]["normalise_columns"]:
                        if option == "lowercase":
                            dataframe.columns = dataframe.columns.str.lower()
                        elif option == "uppercase":
                            dataframe.columns = dataframe.columns.str.upper()
                        elif option == ("capitalize", "capitalise"):
                            dataframe.columns = dataframe.columns.str.capitalize()
                        elif option == "remove_special":
                            dataframe.columns = dataframe.columns.str.replace(r'[^A-Za-z0-9 ]+', '', regex=True)
                        elif option == "remove_whitespace":
                            dataframe.columns = dataframe.columns.str.replace(r'\s+', '', regex=True)
                        elif option == "spaces_to_underscore":
                            dataframe.columns = dataframe.columns.str.replace(r'\s+', '_', regex=True)
                        elif option == "spaces_to_hyphen":
                            dataframe.columns = dataframe.columns.str.replace(r'\s+', '-', regex=True)

                if "check_coverage" in rules[j]:
                    global_check_coverage = rules[j]["check_coverage"]

                if "reset_coverage" in rules[j]:
                    if (bool)(rules[j]["reset_coverage"]):
                        reset_coverage = bool(rules[j]["reset_coverage"])

                if "action" in rules[j]:
                    global_action = rules[j]["action"]

                if "verbose" in rules[j]:
                    global_verbose = rules[j]["verbose"]

                if "column_mapping" in rules[j]:
                    for old, new in rules[j]["column_mapping"].items():
                        dataframe[new] = dataframe[old]

                if "mapping" in rules[j]:
                    global_mapping = rules[j]["mapping"]

                if "drop_duplicates" in rules[j]:
                    dataframe.drop_duplicates(
                        subset=rules[j]["drop_duplicates"], inplace=True)

                if "shared_colname_drop" in rules[j]:
                    dups = dataframe.T.duplicated()
                    true_values = dups.loc[dups]
                    print("Dropping: " + str(true_values.loc[dups].keys().tolist()))

                    dataframe = dataframe.drop(dataframe.loc[:, dups], axis=1)

                if "concat" in rules[j]:
                    name = rules[j]["concat"]["name"]
                    dataframe[name] = ""
                    for column in rules[j]["concat"]["columns"]:
                        dataframe[name] += dataframe[column].astype(str)

                if "fillna" in rules[j]:
                    dataframe = dataframe.fillna(rules[j]["fillna"])
                
                if "fillna_median" in rules[j]:
                    dataframe = dataframe.fillna(dataframe.median())

                if "fillna_mean" in rules[j]:
                    dataframe = dataframe.fillna(dataframe.mean())
                
                if "fillna_diffcol" in rules[j]:
                    dataframe = dataframe.fillna(dataframe[rules[j]["fillna_diffcol"]])

                if "operator" in rules[j]:
                    operator = rules[j]["operator"]["type"]
                    column = rules[j]["operator"]["columns"]
                    name = rules[j]["operator"]["name"]
                    try: 
                        if operator == "divide":
                            dataframe[name] = dataframe[column[0]]/dataframe[column[1]]

                        if operator == "multiply":
                            dataframe[name] = dataframe[column[0]] * dataframe[column[1]]
                    except TypeError:
                        print("Operator failed: expected numbers")

                # Continue with next rule
                return True

            # No global rules found
            return False

        # Loop through all rules
        j = -1
        while j < len(rules):
            # We're starting at -1 so j increment is at the top of the while loop
            j += 1
            if j >= len(rules):
                break

            if find_global_rules(j, rules) is True:
                continue

            # Column not found in dataset
            try:
                column_values = dataframe[rules[j]["column"]]
            except KeyError:
                print("Column " + rules[j]["column"] + " not found")
                continue

            if "normalise" in rules[j]:
                if is_value_array(key = "normalise", value = rules[j]["normalise"]) is False:
                    continue

                for option in rules[j]["normalise"]:
                    
                    if option == "lowercase":
                        column_values = column_values.str.lower()
                    elif option == "uppercase":
                        column_values = column_values.str.upper()
                    elif option in ("capitalize", "capitalise"):
                        column_values = column_values.str.capitalize()
                    elif option == "remove_special":
                        column_values = column_values.str.replace(r'[^a-zA-Z0-9]', '', regex=True)
                    elif option == "remove_whitespace":
                        column_values = column_values.str.replace(r'\s+', '', regex=True)
                    elif option == "spaces_to_underscore":
                        column_values = column_values.str.replace(r'\s+', '_', regex=True)
                    elif option == "spaces_to_hyphen":
                        column_values = column_values.str.replace(r'\s+', '-', regex=True)

            # Same as global rule but now only for one column
            if "normalise_columns" in rules[j]:
                if is_value_array(key = "normalise_columns", value = rules[j]["normalise_columns"]) is False:
                    continue

                for option in rules[j]["normalise_columns"]:

                    if option == "lowercase":
                        dataframe.rename(columns={rules[j]["column"]: rules[j]["column"].lower()}, inplace=True)
                    elif option == "uppercase":
                        dataframe.rename(columns={rules[j]["column"]: rules[j]["column"].upper()}, inplace=True)
                    elif option in ("capitalize", "capitalise"):
                        dataframe.rename(columns={rules[j]["column"]: rules[j]["column"].capitalize()}, inplace=True)
                    elif option == "remove_special":
                        dataframe.rename(columns={rules[j]["column"]: re.sub(r'[^a-zA-Z0-9]', '', rules[j]["column"])}, inplace=True)
                    elif option == "remove_whitespace":
                        dataframe.rename(columns={rules[j]["column"]: re.sub(r'\s+', '', rules[j]["column"])}, inplace=True)
                    elif option == "spaces_to_underscore":
                        dataframe.rename(columns={rules[j]["column"]: re.sub(r'\s+', '_', rules[j]["column"])}, inplace=True)
                    elif option == "spaces_to_hyphen":
                        dataframe.rename(columns={rules[j]["column"]: re.sub(r'\s+', '-', rules[j]["column"])}, inplace=True)
                continue

            if "mapping" in rules[j] or global_mapping is not False:
                mapping = global_mapping
                if "mapping" in rules[j]:
                    mapping = rules[j]["mapping"]

                column_values = column_values.replace(mapping)

            if "reset_coverage" in rules[j]:
                if (bool)(rules[j]["reset_coverage"]):
                    reset_coverage = (bool(rules[j]["reset_coverage"]))

            if "check_coverage" in rules[j] or global_check_coverage != False:
                if errors_found and reset_coverage:
                    errors_found = False
                else:
                    check_coverage = global_check_coverage
                    if "check_coverage" in rules[j]:
                        check_coverage = (rules[j]["check_coverage"])
                    if re.match(r"^[1-9][0-9]?$|^100$", check_coverage):
                        column_values = column_values.sample(
                            frac=int(check_coverage) / 100)

            if "one_hot_encoding" in rules[j]:
                if len(rules[j]["one_hot_encoding"]) == 0:
                    dataframe = dataframe.join(pd.get_dummies(dataframe[rules[j]["column"]]))
                else:
                    dataframe = dataframe.join(pd.get_dummies(dataframe[rules[j]["column"]], prefix=rules[j]["one_hot_encoding"]))

            if "selection" in rules[j]:
                sorted_selection = sorted(rules[j]["selection"])
                for i, value in column_values.items():
                    index = bisect.bisect_left(sorted_selection, str(value))
                    if index >= len(sorted_selection) or sorted_selection[index] != value:
                        handle_mismatch(i, value, column_values)

            if "regex" in rules[j]:
                for i, value in column_values.items():
                    if not re.match(rules[j]["regex"], str(value)):
                        handle_mismatch(i, value, column_values)

            if "range" in rules[j]:
                for i, value in column_values.items():
                    try:
                        if not (float(rules[j]["range"][0]) <= float(value) <= float(rules[j]["range"][1])):
                            handle_mismatch(i, value, column_values)
                    except ValueError:
                        handle_mismatch(i, value, column_values)
            
            # Make the data inside the column Panda timestamps
            if "timestamp" in rules[j]:
                try:
                    dataframe[rules[j]["column"]] = pd.to_datetime(dataframe[rules[j]["column"]], utc=True).dt.strftime(rules[j]["timestamp"])
                except TypeError:
                    print("Timestamping failed: " + str(rules[j]["column"]))

            # Check if a column lays between to dates
            if "range_time" in rules[j]:
                left = pd.to_datetime(rules[j]["range_time"][0], utc=True)
                right = pd.to_datetime(rules[j]["range_time"][1], utc=True)

                for i, value in column_values.items():
                    try:
                        value = pd.to_datetime(value, utc=True)
                        if not (left <= value <= right):
                            handle_mismatch(i, value, column_values)
                    except ValueError:
                        handle_mismatch(i, value, column_values)

            # Check if a column matches a specific format
            if "type" in rules[j]:
                    
                if rules[j]["type"] == "percentage":
                    for i, value in column_values.items():
                        # Regex to match float between 0 and 100
                        if not re.match(r"^([0-9]|[1-9][0-9]|100)(\.[0-9]+)?$", str(value)):
                            handle_mismatch(i, value, column_values)

                if rules[j]["type"] == "boolean":
                    for i, value in column_values.items():
                        if value != True and value != False:
                            handle_mismatch(i, value, column_values)

                if rules[j]["type"] == "float":
                    if (column_values.dtype == float):
                        continue

                    for i, value in column_values.items():
                        try:
                            float(value)
                        except ValueError:
                            handle_mismatch(i, value, column_values)

                if rules[j]["type"] == "int":
                    if (column_values.dtype == int):
                        continue

                    for i, value in column_values.items():
                        try:
                            int(value)
                        except ValueError:
                            handle_mismatch(i, value, column_values)

                if rules[j]["type"] == "positive-int":
                    for i, value in column_values.items():
                        try:
                            if int(value) < 0:
                                handle_mismatch(i, value, column_values)
                        except ValueError:
                            handle_mismatch(i, value, column_values)

                if rules[j]["type"] == "negative-int":
                    for i, value in column_values.items():
                        try:
                            if int(value) >= 0:
                                handle_mismatch(i, value, column_values)
                        except ValueError:
                            handle_mismatch(i, value, column_values)

                if rules[j]["type"] == "letters":
                    for i, value in column_values.items():
                        if (value.isalpha() is False):
                            handle_mismatch(i, value, column_values)

                if rules[j]["type"] == "postal_code":
                    # Remove special characters and make uppercase
                    column_values.astype(str).str.replace(
                        r"[^a-zA-Z0-9]+", "", regex=True)

                    for i, value in column_values.items():
                        if not re.match(r"^[1-9][0-9]{3}\s?[a-zA-Z]{2}$", str(value)):
                            handle_mismatch(i, value, column_values)

                if rules[j]["type"] == "longitude":
                    for i, value in column_values.items():
                        if not re.match(r"^[-+]?([1-8]?\d(\.\d+)?|90(\.0+)?)$", str(value)):
                            handle_mismatch(i, value, column_values)

                if rules[j]["type"] == "latitude":
                    for i, value in column_values.items():
                        if not re.match(r"^[-+]?([1-8]?\d(\.\d+)?|90(\.0+)?)$", str(value)):
                            handle_mismatch(i, value, column_values)

                if rules[j]["type"] == "street":
                    for i, value in column_values.items():
                        value = list(value)
                        for idx, character in enumerate(value):
                            # Remove all non-alphanumeric except ' - and whitespaces
                            if character not in ("'", "-", " ") and character.isalpha() is False:
                                handle_mismatch(i, value, column_values)
                                break

                            value[0] = value[0].upper()

                            if character in ("'", "-"):
                                try:
                                    # Make next character uppercase after ' or -
                                    value[idx + 1] = value[idx + 1].upper()
                                except IndexError:
                                    continue

                            column_values[i] = "".join(value)

            # Loop again because error in sample
            if (reset_coverage and errors_found and len(column_values) < len(dataframe[rules[j]["column"]])):
                j -= 1
                continue

            # Bulk drop rows
            dataframe.drop(drop_array, inplace=True)

            # Make all the indexes inside the np.nan array nan values
            column_values.loc[nan_array] = np.nan

            # Make all the indexes inside the none array None values
            column_values.loc[none_array] = None

            # If there are any values in drop_array, nan_aray or none_array print the column name and the length of the array
            for array in (drop_array, none_array, nan_array):
                if len(array) > 0:
                    array_name = 'dropped: ' if array == drop_array else 'made None: ' if array == none_array else 'made NaN: '
                    print(f"Column {rules[j]['column']}, {array_name}{len(array)} values")

            drop_array = none_array = nan_array =  []

            # Fill the NaN values with something else
            try:
                if "fillna" in rules[j]:
                    column_values = column_values.fillna(rules[j]["fillna"])
                
                if "fillna_median" in rules[j]:
                    column_values = column_values.fillna(column_values.median())

                if "fillna_mean" in rules[j]:
                    column_values = column_values.fillna(column_values.mean())
                
                if "fillna_diffcol" in rules[j]:
                    column_values = column_values.fillna(dataframe[rules[j]["fillna_diffcol"]])
            except TypeError:
                pass

            # Update final dataframe with cached values
            dataframe[rules[j]["column"]].update(column_values)

            errors_found = False
        return dataframe
