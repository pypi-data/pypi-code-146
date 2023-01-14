from urllib import parse

from pyrda.dbms.rds import RdClient

token_china = '9B6F803F-9D37-41A2-BDA0-70A7179AF0F3'
app2 = RdClient(token=token_china)

bad_password = 'rds@2022'
conn = {'DB_USER': 'DMS',
        'DB_PASS': parse.quote_plus(bad_password),
        'DB_HOST': '115.159.201.178',
        'DB_PORT': 1433,
        'DATABASE': 'cprds',
        'baseUrl': "https://jycloud.jinzay.com.cn:6443/payService/",
        'orgCode': "CP001001",
        'secretKey': "HmSMQeUkhUKfWf3mNOc_5hmbO1J-gX0D",
        'dms_token': '9B6F803F-9D37-41A2-BDA0-70A7179AF0F3'
        }
sql = f"select FAccountNo from RDS_CAS_SRC_ACCOUNTLIST where FIsdo = 0"
res = app2.select(sql)
bank_accounts = []
for i in res:
    bank_accounts.append(i.get("FAccountNo", None))
