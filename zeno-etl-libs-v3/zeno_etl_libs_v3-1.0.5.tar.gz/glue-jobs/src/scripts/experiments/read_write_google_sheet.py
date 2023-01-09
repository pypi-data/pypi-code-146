import argparse
import os
import sys

sys.path.append('../../../..')

from zeno_etl_libs.logger import get_logger
from zeno_etl_libs.helper.google.sheet.sheet import GoogleSheet


def main(logger):
    gs = GoogleSheet()

    # Read
    ma_stl_data = gs.download(data={
        "spreadsheet_id": "1PiJiVRQh8S5vn7iFc6qHBmJPh5OCBOxmtP4i5Seoh4w",
        "sheet_name": "Sheet2",
        "listedFields": []
    })

    # Write
    # ma_stl_data = gs.upload(data=
    # {
    #     "spreadsheet_id": "1PiJiVRQh8S5vn7iFc6qHBmJPh5OCBOxmtP4i5Seoh4w",
    #     "sheet_name": "Sheet2",
    #     "headers": ["file", "person", "last_name"],
    #     "data": [{"file": "XYZ", "person": "Ram", "last_name": "Sita"}, {"person": "ABC"}]
    # }
    # )

    # df = pd.DataFrame(ma_stl_data)
    # logger.info(f"df: {df}")

    logger.info(f"df: {ma_stl_data}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="This is ETL script.")
    parser.add_argument('-e', '--env', default="dev", type=str, required=False,
                        help="This is env(dev, stage, prod)")

    parser.add_argument('-d', '--data', default=None, type=str, required=False, help="batch size")
    args, unknown = parser.parse_known_args()
    env = args.env
    os.environ['env'] = env

    _logger = get_logger()
    main(_logger)
