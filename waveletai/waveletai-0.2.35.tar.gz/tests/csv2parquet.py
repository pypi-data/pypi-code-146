# import pandas as pd
# df = pd.read_csv('D:/WS/VSCode/waveletai/tests/dataset_init/csv文件夹/devices_curvy.csv')
# df.to_parquet('output.parquet')
# import pyarrow.parquet as pq
# # table = pd.read_parquet('output.parquet')
# #
# # pq.read_table('output.parquet')
# # table = pq.read_schema("D:/VISIO/AI平台/02 研发/02 数据/x_train.parquet")
# parquet_file = pq.ParquetFile("D:/VISIO/AI平台/02 研发/02 数据/x_train.parquet")
# print(parquet_file.metadata)
# print(parquet_file.read_row_group(0))
# first_ten_rows = next(parquet_file.iter_batches(batch_size = 10))
# print(first_ten_rows)
# df = parquet_file.Table.from_batches([first_ten_rows]).to_pandas()
# print(df)
# print(table.metadata)



# from pyarrow.parquet import ParquetFile
# import pyarrow as pa
#
# pf = ParquetFile('file_name.pq')
# first_ten_rows = next(pf.iter_batches(batch_size = 10))
# df = pa.Table.from_batches([first_ten_rows]).to_pandas()


if __name__ == '__main__':


    #
    # # pd.DataFrame.
    # import json
    #
    #
    # # data = json.loads(open("log1.json").read())
    #
    # # for ind, x in enumerate(data["data"]):
    # #     if len(x)!=15:
    # #         print(ind, x)
    # input = pd.read_json("log1.json", orient='split')
    # print(input.to_json())

    # import pyarrow.parquet as pq
    #
    # import pandas as pd
    # table = pd.read_parquet('dish.parquet')
    #
    # # pq.read_table('output.parquet')
    # print(table.head(10))
    # import simplejson as json
    # res = []
    # res.append({"a":1})
    # res.append({"a": 2})
    # res.append({"a": 3})
    # print(json.loads(json.dumps(res)))

    import base64
    img = open('1.jpg', 'rb')
    image_info = base64.b64encode(img.read())

    data = {
        "columns": [
            "1"
        ],
        "data": [
            [image_info]
        ]
    }
    import pandas as pd
    model_input = pd.DataFrame(data)
    import requests
    res = requests.post(url="http://192.168.2.90:10189/invocations", data=model_input.to_json(), headers={"Content-Type": "application/json"})
    print(res.content)
    # print(table.read_table())
    # print(table.read_table())
    # table = pq.read_schema("dish.parquet")
    # parquet_file = pq.ParquetFile("dish.parquet")
    # print(parquet_file.read())




