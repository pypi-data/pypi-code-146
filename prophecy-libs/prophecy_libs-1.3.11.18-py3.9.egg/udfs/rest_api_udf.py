from pyspark.sql.functions import *
from pyspark.sql.types import *

@udf(returnType=StructType(
    [StructField("status_code", StringType(), True), StructField("reason", StringType(), True),
     StructField("url", StringType(), True), StructField("content", StringType(), True)
     ]))
def get_rest_api(input_cols, await_time_col):
    import json
    import requests
    import time
    inputs = json.loads(input_cols)
    new_dict = {}
    for key, value in inputs.items():
        if value is not None and value.lower() not in ["", "none", "null"]:
            if key in ["json", "params", "headers", "cookies", "proxies"]:
                try:
                    new_dict[key] = json.loads(value)
                except:
                    continue
            elif key in ["data"]:
                try:
                    new_dict[key] = json.loads(value)
                except:
                    new_dict[key] = value
            elif key in ["auth"]:
                new_dict[key] = (value.split(":")[0], value.split(":")[1])
            elif key in ["allow_redirects", "stream"]:
                new_dict[key] = True if value.lower() == "true" else False
            elif key in ["verify"]:
                new_dict[key] = True if value.lower() in ["true", "false"] else value
            elif key in ["timeout"]:
                if ':' in value:
                    new_dict[key] = (float(value.split(":")[0]), float(value.split(":")[1]))
                else:
                    new_dict[key] = float(value)
            elif key in ["cert"]:
                if ':' in value:
                    new_dict[key] = (value.split(":")[0], value.split(":")[1])
                else:
                    new_dict[key] = value
            else:
                new_dict[key] = value
    response = requests.request(**new_dict)
    if await_time_col.lower() not in ["", "none", "null"]:
        time.sleep(float(await_time_col))
    return response.status_code, response.reason, response.url, response.text