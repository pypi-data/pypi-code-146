from caddo_file_parser.models.fold import Fold
import pandas as pd


class CaddoFile:
    def __init__(self, folds: [Fold], data: pd.DataFrame, settings=None):
        self.folds = folds
        self.data = data
        self.settings = settings

