"""
Init for qnn
"""
# pylint: disable=redefined-builtin
from .data_process import load_data as qsvm_load_data
from .data_process import data_process as qsvm_data_process
from .qsvm import QSVM