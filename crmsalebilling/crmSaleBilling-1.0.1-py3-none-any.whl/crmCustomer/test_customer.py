from crmCustomer import customerOAInterface as rc


def run():
    # 4D18 新账套数据库totken
    # token_erp = '57DEDF26-5C00-4CA9-BBF7-57ECE07E179B'
    # A59 培训账套数据库token
    token_erp = 'A597CB38-8F32-40C8-97BC-111823AA7765'
    # token_erp = 'B405719A-772E-4DF9-A560-C24948A3A5D6'
    token_china = '9B6F803F-9D37-41A2-BDA0-70A7179AF0F3'

    # 培训账套 ERPtoken
    option1 = {
        "acct_id": '63310e555e38b1',
        "user_name": '杨斌',
        "app_id": '240072_1e2qRzvGzulUR+1vQ6XK29Tr2q28WLov',
        # "app_sec": 'd019b038bc3c4b02b962e1756f49e179',
        "app_sec": '224f05e7023743d9a0ab51d3bf803741',
        "server_url": 'http://cellprobio.gnway.cc/k3cloud',
    }
    res = rc.customerInterface(option1, token_erp, token_china)
    return res
print(run())