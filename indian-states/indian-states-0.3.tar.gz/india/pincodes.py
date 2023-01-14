""" This enables easy access to indian states and union territories """
import csv

# module imports
from . import utils

PINCODES = []
def lookup(val: str) -> str:
    reader = csv.reader(open(utils.FILE_NAME['pincodes'], 'r'))
    for row in reader:
        if row[1] == val:
            PINCODES.append(row[0])
    return PINCODES