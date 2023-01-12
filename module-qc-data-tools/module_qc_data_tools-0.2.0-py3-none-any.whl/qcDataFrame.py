import json
import os
import re

import numpy as np
from _ctypes import PyObj_FromPtr  # see https://stackoverflow.com/a/15012814/355230
from tabulate import tabulate

# class NoIndent(object):
# 	""" Value wrapper. """
# 	def __init__(self, value):
# 		if not isinstance(value, (list, tuple)):
# 			raise TypeError('Only lists and tuples can be wrapped')
# 		self.value = value


class MyEncoder(json.JSONEncoder):
    FORMAT_SPEC = "@@{}@@"  # Unique string pattern of NoIndent object ids.
    regex = re.compile(FORMAT_SPEC.format(r"(\d+)"))  # compile(r'@@(\d+)@@')

    def __init__(self, **kwargs):
        # Keyword arguments to ignore when encoding NoIndent wrapped values.
        ignore = {"cls", "indent"}

        # Save copy of any keyword argument values needed for use here.
        self._kwargs = {k: v for k, v in kwargs.items() if k not in ignore}
        super().__init__(**kwargs)

    def default(self, obj):
        # return (self.FORMAT_SPEC.format(id(obj)) if isinstance(obj, NoIndent)
        return (
            self.FORMAT_SPEC.format(id(obj))
            if isinstance(obj, list)
            else super().default(obj)
        )

    def iterencode(self, obj, **kwargs):
        format_spec = self.FORMAT_SPEC  # Local var to expedite access.

        # Replace any marked-up NoIndent wrapped values in the JSON repr
        # with the json.dumps() of the corresponding wrapped Python object.
        for encoded in super().iterencode(obj, **kwargs):
            match = self.regex.search(encoded)
            if match:
                id = int(match.group(1))
                no_indent = PyObj_FromPtr(id)
                json_repr = json.dumps(no_indent.value, **self._kwargs)
                # Replace the matched id string with json formatted representation
                # of the corresponding Python object.
                encoded = encoded.replace(f'"{format_spec.format(id)}"', json_repr)

            yield encoded


def save_dict_list(path, output):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as fp:
        json.dump(output, fp, cls=MyEncoder, indent=4)


def load_json(path):
    with open(path) as serialized:
        inputdata = json.load(serialized)
    alldf = []
    for _dict in inputdata:
        alldf += [outputDataFrame(_dict=_dict)]
    return alldf


def get_test_type(name, returnall=False):
    all_types = {
        "adc_calib": "ADC_CALIBRATION",
        "vcal_calib": "VCAL_CALIBRATION",
        "sldo": "SLDO",
        "analog_readback": "ANALOG_READBACK",
    }
    if returnall:
        return list(all_types.values())
    else:
        official_test_name = all_types.get(name, "Unknown")
        if official_test_name == "Unknown":
            print(f"Warning: Test name {name} not recognized")
        return official_test_name


class qcDataFrame:
    """
    The QC data frame which stores meta data and task data.
    """

    def __init__(self, columns=None, units=None, x=None, _dict=None):
        self._identifiers = {}
        self._meta_data = {}
        self._data = {}
        self._property = {}
        self._parameter = {}
        self._comment = ""
        if _dict:
            self.from_dict(_dict)
            return

        columns = columns or []

        for i, column in enumerate(columns):
            self._data[column] = {
                "X": x[i] if x else False,
                "Unit": units[i] if units else None,
                "Values": [],
            }

    def add_meta_data(self, key, value):
        self._meta_data[key] = value

    def add_data(self, data):
        for key, value in data.items():
            self._data[key]["Values"] += list(value)

    def add_column(self, column, unit=False, x=False, data=None):
        data = data or []
        if column in self._data:
            print(f"Warning: column {column} already exists! Will overwrite.")
        self._data[column] = {"X": x, "Unit": unit, "Values": list(data)}

    def add_property(self, key, value):
        if self._property.get(key):
            print(f"Warning: property {key} already exists! Will overwrite.")
        self._property[key] = value

    def add_parameter(self, key, value):
        if self._parameter.get(key):
            print(f"Warning: parameter {key} already exists! Will overwrite.")
        self._parameter[key] = value

    def add_comment(self, comment, override=False):
        if override or self._comment == "":
            self._comment = comment
        else:
            self._comment += ". " + str(comment)

    def __getitem__(self, column):
        return np.array(self._data[column]["Values"])

    def set_unit(self, column, unit):
        self._data[column]["Unit"] = unit

    def get_unit(self, column):
        return self._data[column]["Unit"]

    def set_x(self, column, x):
        self._data[column]["X"] = x

    def get_x(self, column):
        return self._data[column]["X"]

    def __len__(self):
        return max(len(value["Values"]) for value in self._data.values())

    def sort_values(self, by, reverse=False):
        for key, value in self._data.items():
            if key == by:
                continue
            value["Values"] = list(
                next(
                    zip(
                        *sorted(
                            zip(
                                value["Values"], self._data[by]["Values"], strict=False
                            ),
                            key=lambda x: x[1],
                            reverse=reverse,
                        ),
                        strict=False,
                    )
                )
            )
        self._data[by]["Values"].sort(reverse=reverse)

    def get_meta_data(self):
        return self._meta_data

    def get_identifiers(self):
        return {
            k: self._meta_data.get(k)
            for k in (
                "ChipID",
                "Name",
                "Institution",
                "TestType",
                "TimeStart",
                "TimeEnd",
            )
        }

    def __str__(self):
        text = "Identifiers:\n"
        text += str(json.dumps(self.get_identifiers(), cls=MyEncoder, indent=4))
        text += "\n"
        # text += "Meta data:\n"
        # text += str(json.dumps(self._meta_data, cls=MyEncoder, indent=4))
        # text += "\n"
        table = []
        for key, value in self._data.items():
            table.append(
                [key + (f" [{value['Unit']}]" if value["Unit"] else "")]
                + value["Values"]
            )
        text += tabulate(table, floatfmt=".3f")
        return text

    def to_dict(self):
        _dict = {
            "property": self._property,
            "parameter": self._parameter,
            "comment": self._comment,
            "Measurements": self._data,
            "Metadata": self._meta_data,
        }
        return _dict

    def from_dict(self, _dict):
        self._meta_data = _dict["Metadata"]
        self._identifiers = self.get_identifiers()
        self._data = _dict["Measurements"]

    def to_json(self):
        _dict = self.to_dict()
        return json.dumps(_dict, cls=MyEncoder, indent=4)

    def save_json(self, path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        _dict = self.to_dict()
        with open(path, "w") as fp:
            json.dump(_dict, fp, cls=MyEncoder, indent=4)


class outputDataFrame:
    """
    The output file format, designed to work well with localDB and prodDB
    """

    def __init__(self, _dict=None):
        self._serialNumber = "Unknown"
        self._testType = "Not specified"
        self._results = qcDataFrame()  # holds qcDataFrame
        self._passed = "Not specified"
        if _dict:
            self.from_dict(_dict)
            return

    def set_serial_num(self, serial_num=None):  # TODO: Finish this
        if serial_num is not None:
            self._serialNumber = "Unknown"
        else:
            try:
                chipName = self._results._meta_data["Name"]
            except Exception:
                print("Warning: Can't find chip name for serial number conversion")
                return
            try:
                self._serialNumber = int(chipName, base=16)
            except Exception:
                print(
                    f"Warning: Can't convert chip name ({chipName}) into serial number, setting serial number to 0"
                )
                self._serialNumber = 0

    def set_test_type(self, test_type=None):
        if test_type is not None:
            self._testType = test_type
        else:
            self._testType = "Not specified"

    def set_pass_flag(self, passed=False):
        self._passed = passed

    def set_results(self, results=None):
        if results is not None:
            self._results = results
        else:
            self._results = qcDataFrame()
        self.set_serial_num()

    def get_results(self):
        return self._results

    def to_dict(self, forAnalysis=False):
        _dict = {
            "serialNumber": self._serialNumber,
            "testType": self._testType,
        }
        all_results = self.get_results().to_dict()
        parameters = all_results.get("parameter")
        all_results.pop("parameter")

        # Write out different information, depending on if we are in measurement or analysis step
        if forAnalysis:
            all_results.pop("Measurements")
            all_results.pop("Metadata")
            all_results.pop("comment")
            for key, value in parameters.items():
                all_results[key] = value
            _dict["passed"] = self._passed
        results = {"results": all_results}
        _dict.update(results)
        return _dict

    def save_json(self, path, forAnalysis=False):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        _dict = self.to_dict(forAnalysis)
        with open(path, "w") as fp:
            json.dump(_dict, fp, cls=MyEncoder, indent=4)

    def from_dict(self, _dict):
        self._serialNumber = _dict["serialNumber"]
        self._testType = _dict["testType"]
        self._results = qcDataFrame(_dict=_dict["results"])
