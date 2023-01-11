import logging
from typing import Tuple

import pandas as pd
from statsu.ui.data_container import DataContainer
from statsu.ui.dialog import OpenCSVDialog

logger = logging.getLogger(__name__)


def load_dataframe_from_file(file_path: str) -> pd.DataFrame:
    file_type = file_path.split('.')[-1]

    try:
        if file_type == 'xlsx' or file_type == 'xls':
            # 여러 시트에 대한 처리도 필요
            return pd.read_excel(file_path)
        elif file_type == 'csv':
            dialogue = OpenCSVDialog()
            result = dialogue.exec()
            if result == 1:
                raw_data = pd.read_csv(file_path,
                                       sep=dialogue.selected_splitter,
                                       header=dialogue.get_header_type())
                return raw_data
            else:
                return None
    except Exception as e:
        logger.warn(e)

    logger.warn(f'Unknown Data Type: Cannot open file')
    return None


def save_data_to_file(data: DataContainer, file_path: str, file_type: str):
    try:
        if file_type == 'xlsx' or file_type == 'xls':
            data.raw_data.to_excel(file_path, sheet_name=data.name)
        elif file_type == 'csv':
            data.raw_data.to_csv(file_path)
        else:
            logger.warn('Unknown Error Ocurred')
            return False
    except Exception as e:
        logger.warn(e)
        return False

    return True