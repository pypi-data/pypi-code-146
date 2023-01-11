# See if we can find the mismatch causing the error and fix it in Validate
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

class Validate:
    def __init__(self):
        self._app_data = None
        self._dataframe = None

    @property
    def app_data(self):
        return self._app_data

    @app_data.setter
    def app_data(self, value):
        self._app_data = json.dumps(value)

    @property
    def dataframe(self):
        return self._dataframe

    @dataframe.setter
    def dataframe(self, value):
        self._dataframe = value
        
    def obtain_keys(self) -> set:
        """Obtain all keys an app needs"""
        keys = {}
        json_data = self._app_data

        # Find uuid rename keys using negative lookahead regex; text between { and "type": "rename"
        rename_uuid_keys = re.findall(
            r'\{(?:(?!\{|' + re.escape('"type": "rename"') + r')[\s\S])*' + re.escape('"type": "rename"'), json_data)
        uuid_regex = re.compile(
            r'[0-9a-z]{9}\_[0-9a-z]{4}\_[0-9a-z]{4}\_[0-9a-z]{4}\_[0-9a-z]{12}')
        uuidDollarRegex = re.compile(
            r'\$[0-9a-z]{9}\_[0-9a-z]{4}\_[0-9a-z]{4}\_[0-9a-z]{4}\_[0-9a-z]{12}')
        rename_uuid_keys = list(
            set(re.findall(uuid_regex, str(rename_uuid_keys))))

        # Find all $uuid keys
        dollar_uuid_keys = re.findall(uuidDollarRegex, json_data)
        dollar_uuid_keys = [s.replace('$', '') for s in dollar_uuid_keys]

        # Remove styling parts
        json_data = re.sub(
            re.escape('config": [') + '.*?' + re.escape('"id"'), '', json_data)
        json_data = re.sub(
            re.escape('styling": {') + '.*?' + re.escape('}'), '', json_data)
        json_data = re.sub(
            re.escape('styling": [') + '.*?' + re.escape(']'), '', json_data)

        # Search normal and join keys
        normal_keys = re.findall(r'"key": "(.*?)"', json_data)
        join_keys = re.findall(r'"join_key": "(.*?)"', json_data)

        # Merge all key findings
        keys = set(normal_keys + join_keys +
                   rename_uuid_keys + dollar_uuid_keys)
        return keys

    def match_keys(self):
        """Pass a dataframe and appData to this function to find differences in keys"""
        keys = Validate.obtain_keys(self)

        # Compare the two lists of keys to eachother
        additional_keys = list(self._dataframe.columns.difference(keys))
        missing_keys = list(keys.difference(self._dataframe.columns))

        values = namedtuple('keys', 'missing_keys additional_keys')
        return values(missing_keys, additional_keys)

    def fix_mismatch(self, strictness=0.8):
        """Pass a dataframe and appData to this function to fix the mismatch between the two"""
        keys = Validate.match_keys(self)
        dataframe = self._dataframe

        if len(keys.missing_keys) < 1:
            return print("No missing keys")

        suggestions = []

        for i, missing_key in enumerate(keys.missing_keys):
            for additional_key in keys.additional_keys:
                similarity = SequenceMatcher(None, missing_key, additional_key)

                # Check if missing_key looks like additional_key
                if similarity.ratio() > strictness:
                    values = namedtuple('keys', 'missing_key additional_key')
                    suggestions.append(values(missing_key, additional_key))
                    keys.missing_keys.pop(i)

        print("\nWe did not find " + str(len(keys.missing_keys)) +
              " keys:\n" + str(sorted(keys.missing_keys, key=len)) + "\n")

        if len(suggestions) < 1:
            print("No matches, try lowering strictness")
            return dataframe

        # Propose suggestions
        for i, suggestion in enumerate(suggestions):
            print("Suggestion {}: missing '{}' might be additional: '{}'".format(
                i + 1, suggestion.missing_key, suggestion.additional_key))

        # Ask user which suggestions to fix and then rename dataframe columns
        suggestions_to_fix = list(map(int, input(
            "Which suggestion(s) do you want to fix? (example: 1 2 3): ").split()))
        for i in suggestions_to_fix:
            dataframe = dataframe.rename(
                columns={suggestions[i - 1].additional_key: suggestions[i - 1].missing_key})

        return dataframe