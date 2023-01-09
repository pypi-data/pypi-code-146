import argparse
import os
import sys

import pandas as pd

sys.path.append('../../../..')

from zeno_etl_libs.db.db import MongoDB
from zeno_etl_libs.logger import get_logger

parser = argparse.ArgumentParser(description="This is ETL script.")
parser.add_argument('-e', '--env', default="dev", type=str, required=False,
                    help="This is env(dev, stag, prod)")

args, unknown = parser.parse_known_args()
env = args.env
os.environ['env'] = env

logger = get_logger()

mg_db = MongoDB()
mg_client = mg_db.open_connection("generico-crm")

db = mg_client['generico-crm']
collection = db["exotelOutgoingCallLogs"].find(
    {"CallType": {"$in": ["zeno-order-list", "zeno-order-details"]}, "status": "connected"})
callog_outbound = pd.DataFrame(list(collection))

print(callog_outbound)