from robertcommonio.system.io.file import FileType, FileConfig, FileAccessor
from robertcommonbasic.basic.dt.utils import parse_time
from robertcommonio.system.io.http import HttpTool
import base64
import json
import re
import pyzipper
import pandas as pd
from io import BytesIO

def test_csv():
    accessor = FileAccessor(FileConfig(PATH='E:/test.csv', MODE=FileType.CSV))
    accessor.save('ss')


def test_zip_csv():
    accessor = FileAccessor(FileConfig(PATH=r'E:\Beop\Code\Git\datapushserver\file\real\testdtu\20220711\request_20220711081000.zip', PSW='123456', MODE=FileType.AES_ZIP))
    json_contents = accessor.read()
    for file_name, file_content in json_contents.items():
        if len(file_content) > 0:
            if file_name.endswith('.json'):
                body = json.loads(file_content.decode())
                body = body.get('body')
                file_type = body.get('type', '')
                file_psw = body.get('psw', '')
                file_path = body.get('path', '')
                file_name = body.get('name', '')
                file_content = body.get('content', '')
                accessor = FileAccessor(FileConfig(PATH=BytesIO(base64.b64decode(file_content.encode())), PSW='RNB.beop-2019', MODE=FileType.AES_ZIP))
                json_contents = accessor.read()
                for file_name, file_content in json_contents.items():
                    datas = [p.split(',') for p in file_content.decode('gbk').split(';')]
                    points = {}
                    for data in datas:
                        if len(data) >= 2 and len(data[0]) > 0:
                            points[data[0]] = data[1]

                    value = {'dtuName': 'test2020',
                    'dataType': 0,
                    'dataSource': '',
                    'serverCode': 6,
                    'updateTime': '2022-07-11 08:10:00',
                    'dataStruct': [{'time': '2022-07-11 08:10:00', 'type': 0, 'points': points}]}
                    body = json.dumps(value, ensure_ascii=False).encode("utf-8")
                    rt = HttpTool().send_request(url=f"http://beopservice.smartbeop.com/site/v1.0/update_raw_data_v2", method='POST', headers={'content-type': 'application/json'}, data=body, timeout=30)
                    print(rt)
def test_zip_csv1():
    content = b''
    with open(r'E:\DTU\real\atlanta\20210907\his_20210907095301.zip', 'rb') as f:
        content = f.read()

    accessor = FileAccessor(FileConfig(PATH=BytesIO(content), PSW=['aa', '123456', 'RNB.beop-2019', ''],
                                       MODE=FileType.AES_ZIP))
    results = accessor.read()
    for k, v in results.items():
        print(k)
    results = {}
    with pyzipper.AESZipFile(BytesIO(content)) as zip:
        zip.setpassword('RNB.beop-2019'.encode('utf-8'))
        for file in zip.namelist():
            results[file] = zip.read(file)
    print(results)


def test_excel():
    #import pandas as pd
    #df = pd.read_excel(r'E:\DTU\point\hongqiao_api\point202202221.xls', sheet_name=None)

    accessor = FileAccessor(FileConfig(PATH=r'E:\DTU\point\hongqiao_api\point20220224.xls', MODE=FileType.Excel, NAME=None))
    results = accessor.read()
    for k, v in results.items():
        print(k)
    del accessor

    accessor1 = FileAccessor(FileConfig(PATH=r'E:\DTU\point\hongqiao_api\point20220224_new.xls', MODE=FileType.Excel, NAME=None))
    accessor1.save(file_content=results)
    print()

def test_pcc():
    records = pd.read_csv('E:/PCC_AB_Davis_AirHandlers_Analog (3).csv', keep_default_na=False)
    for index, row in records.iterrows():
        row_value = row.to_dict()
        values = {}
        for k, v in row_value.items():
            if v is not None and len(str(v)) > 0:
                if isinstance(v, str) and v.find(',') > 0:
                    v = v.replace(',', '')
                print(v)

test_zip_csv()