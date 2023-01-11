import logging

import pandas as pd
from statsu.ui.dialog import OpenCSVDialog

logger = logging.getLogger(__name__)


def load_dataframe_from_file(file_path: str) -> pd.DataFrame:
    file_type = file_path.split('.')[-1]
    # logger.info(f'{file_path} | {file_type}')

    try:
        if file_type == 'xlsx' or file_type == 'xls':
            # 여러 시트에 대한 처리도 필요
            return pd.read_excel(file_path)
        elif file_type == 'csv':
            dialogue = OpenCSVDialog()
            result = dialogue.exec()
            if result == 1:
                # 스캐너 단위도 데이터에 있는데 어떻게 처리
                return pd.read_csv(
                    file_path,
                    sep=dialogue.selected_splitter,
                    header=dialogue.get_header_type()
                )
            else:
                return None
    except Exception as e:
        logger.warn(e)

    logger.warn(f'Unknown Data Type: Cannot open file')
    return None
