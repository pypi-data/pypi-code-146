from k3cloud_webapi_sdk.main import K3CloudApiSdk
from pyrda.dbms.rds import RdClient
from rdreturnsales.operation import getCode
from rdreturnsales.utility import classification_process
from rdreturnsales.metadata import associated


def returnSale():
    app2 = RdClient(token='4D181CAB-4CE3-47A3-8F2B-8AB11BB6A227')
    app3 = RdClient(token='9B6F803F-9D37-41A2-BDA0-70A7179AF0F3')

    # utility.writeSRC(startDate,endDate,app3)

    data = getCode(app3)


    res = classification_process(app3, data)
    # 新账套
    option1 = {
        "acct_id": '62777efb5510ce',
        "user_name": 'DMS',
        "app_id": '235685_4e6vScvJUlAf4eyGRd3P078v7h0ZQCPH',
        # "app_sec": 'd019b038bc3c4b02b962e1756f49e179',
        "app_sec": 'b105890b343b40ba908ed51453940935',
        "server_url": 'http://cellprobio.gnway.cc/k3cloud',
    }

    api_sdk = K3CloudApiSdk()

    msg = associated(app2, api_sdk, option1, res, app3)

    return msg


