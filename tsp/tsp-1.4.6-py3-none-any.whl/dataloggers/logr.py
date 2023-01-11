import pandas as pd
import regex as re
import numpy as np


class LogR:
    
    SEP = ","

    def __init__(self):
        pass

    def read(self, file):
        headers = read_logr_header(file)
        
        columns = [line.strip().split(',') for line in headers if is_columns_row(line)][0]
        labels = [line.strip().split(',') for line in headers if is_label_row(line)][0]
        data = pd.read_csv(file, skiprows=len(headers))
        
        data.columns = ["TIME" if c == 'timestamp' else c for c in columns]
        data['TIME'] = pd.to_datetime(data['TIME'], format=dateformat())
        
        channels = pd.Series(data.columns).str.match("^CH")
        
        self.DATA = data
        self.META = {
            'label': labels,
            'guessed_depths': guess_depths(labels)[-sum(channels):]
        }

        return self.DATA


def read_logr_header(file: str) -> "list":
    """ Read metadata / header lines from LogR file 

    Parameters
    ----------
    file : str
        path to a LogR file

    Returns
    -------
    list
        list of lines in the header block

    Raises
    ------
    ValueError
        _description_
    """
    found_data = False
    max_rows = 50
    header_lines = []

    with open(file) as f:
        while not found_data and max_rows:
            max_rows -= 1
            
            line = f.readline()

            if is_data_row(line):
                found_data = True
                break

            else: 
                header_lines.append(line)

    if not found_data:
        raise ValueError("Could not find start of data")

    return header_lines 


def guess_depths(labels: "list[str]") -> "list[float]":
    pattern = re.compile(r"(-?[\d\.]+)")

    matches = [pattern.search(l) for l in labels]
    depths = [float(d.group(1)) if d else None for d in matches]

    return depths


def guessed_depths_ok(depths, n_channel) -> bool:
    """ Evaluate whether the guessed depths are valid """
    d = np.array(depths, dtype='float64')

    # monotonic (by convention)
    if not (np.diff(d) > 0).all() or (np.diff(d) < 0).all():
        return False

    # equal to number of channels
    if not sum(~np.isnan(d)) == n_channel:
        return False

    return True


def dateformat():
    return "%Y/%m/%d %H:%M:%S"


def is_data_row(line: str) -> bool:
    pattern = re.compile(r"^,\d{4}/\d{2}/\d{2}\s\d{2}:")
    return bool(pattern.match(line))


def is_columns_row(line:str) -> bool:
    pattern = re.compile(r"^SensorId")
    return bool(pattern.match(line))


def is_label_row(line: str) -> bool:
    pattern = re.compile(r"^Label")
    return bool(pattern.match(line))
