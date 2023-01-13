# 2022.9.2 
import time, requests ,json, platform,os,re,builtins

url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal/"
post_data = {"app_id":"cli_a390c187f1f9d00b", "app_secret":"sL6udKjwYarn3y8QKb4nyfO18OFqyp3F"}
r = requests.post(url, data=post_data)
tat = r.json()["tenant_access_token"]
print ( r.json()) 

def test():
	url = "https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/:shtcnyJFiHPwDkAeXGi0RdGVW3b/values/(sheet的id)!(rang)?valueRenderOption=ToString&dateTimeRenderOption=FormattedString"
	r = requests.get(url, headers = {"content-type":"application/json", "Authorization":"Bearer " + str(tat)})
	# print(r.json())
	print(r.json()["data"]["valueRange"]["values"])

if __name__	== '__main__': 
	pass

'''

requests.get("https://open.feishu.cn/open-apis/sheets/v3/spreadsheets/shtcnyJFiHPwDkAeXGi0RdGVW3b", headers = {"content-type":"application/json", "Authorization":"Bearer u-0GdTGaPqpco8wd8ciROSQFkk6Zvx50QHPi00h0y00CVM"}).json()

https://open.feishu.cn/open-apis/sheets/v3/spreadsheets/shtcnyJFiHPwDkAeXGi0RdGVW3b/sheets/a5a229

requests.get("https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/shtcnyJFiHPwDkAeXGi0RdGVW3b/values/a5a229!A1:D2?valueRenderOption=ToString&dateTimeRenderOption=FormattedString", headers = {"content-type":"application/json", "Authorization":"Bearer u-3RftxLdZtcR9uraAwzL6TZkk6_vx50SxNO0055O00zUR"}).json()

requests.post("https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/shtcnyJFiHPwDkAeXGi0RdGVW3b/values_prepend",
json = {
"valueRange":{
  "range": "a5a229!C6:F9",
  "values": [
    [
      "a",1,"http://www.xx.com",12
    ],
    [
      "b",2,8,"me@HelloWorld.com"
    ],
    [
      "c",3,2,6
    ],
    [
      "d",4,6,"@Jack"
    ]
  ]
  }
}
, headers = {"content-type":"application/json", "Authorization":"Bearer u-3RftxLdZtcR9uraAwzL6TZkk6_vx50SxNO0055O00zUR"}).text

https://open.feishu.cn/document/ukTMukTMukTM/uUDNxYjL1QTM24SN0EjN

curl --location --request POST 'https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/shtcngNygNfuqhxTBf588jwgWbJ/values_prepend' \
--header 'Authorization: Bearer t-e346617a4acfc3a11d4ed24dca0d0c0fc8e0067e' \
--header 'Content-Type: application/json' \
--data-raw '{
"valueRange":{
  "range": "a5a229!C6:F9",
  "values": [
    [
      "a",1,"http://www.xx.com",12
    ],
    [
      "b",2,8,"me@HelloWorld.com"
    ],
    [
      "c",3,2,6
    ],
    [
      "d",4,6,"@Jack"
    ]
  ]
  }
}'

{
  "id": "ap-136:penlist",
  "acl": [
    {
      "access": "allow",
      "value": "everyone",
      "type": "user"
    }
  ],
  "metadata": {
    "title": 1005,
    "source_url": "1002,1003,1004"
  },
  "structured_data": "{\"key\":\"value\"}",
  "content": {
    "format": "html",
    "content_data": "这是一个很长的文本"
  }
}

你可以根据 error 中返回的权限名称（例如：people_admin:department），在 “开发者后台>打开你的应用>权限管理”中搜索并开通所需的权限。
{
  "code": 0,
  "data": {
    "files": [
      {
        "name": "sound词性分布",
        "parent_token": "nodcnjDMDRZp54gY0bB4ryC0Gah",
        "token": "doxcn4NXLXxR6qrIwsMkisLCMfd",
        "type": "docx",
        "url": "https://sentbase.feishu.cn/docx/doxcn4NXLXxR6qrIwsMkisLCMfd"
      },
      {
        "name": "任务跟进看板",
        "parent_token": "nodcnjDMDRZp54gY0bB4ryC0Gah",
        "token": "shtcnc5b69VVFIPG0rRnOXLM0Eg",
        "type": "sheet",
        "url": "https://sentbase.feishu.cn/sheets/shtcnc5b69VVFIPG0rRnOXLM0Eg"
      },
      {
        "name": "test1",
        "parent_token": "nodcnjDMDRZp54gY0bB4ryC0Gah",
        "token": "shtcnyJFiHPwDkAeXGi0RdGVW3b",
        "type": "sheet",
        "url": "https://sentbase.feishu.cn/sheets/shtcnyJFiHPwDkAeXGi0RdGVW3b"
      },
      {
        "name": "open",
        "parent_token": "nodcnjDMDRZp54gY0bB4ryC0Gah",
        "token": "bascn4TSwzSYOrTDnfng1vv7Lsf",
        "type": "bitable",
        "url": "https://sentbase.feishu.cn/base/bascn4TSwzSYOrTDnfng1vv7Lsf"
      },
      {
        "name": "open",
        "parent_token": "nodcnjDMDRZp54gY0bB4ryC0Gah",
        "token": "shtcnF9vcd5s0eJJzAoFp6gAbnd",
        "type": "sheet",
        "url": "https://sentbase.feishu.cn/sheets/shtcnF9vcd5s0eJJzAoFp6gAbnd"
      },
      {
        "name": "open + NOUNs",
        "parent_token": "nodcnjDMDRZp54gY0bB4ryC0Gah",
        "token": "shtcnZ0D7knnI7XrnwTYcDi0tHe",
        "type": "sheet",
        "url": "https://sentbase.feishu.cn/sheets/shtcnZ0D7knnI7XrnwTYcDi0tHe"
      }
    ],
    "has_more": false
  },
  "msg": "success"
}

CHALLENGE 
challenge
'''