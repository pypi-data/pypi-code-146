from quantplay.broker import motilal
import hashlib
# import requests
# import json
# import pyotp
#
# class MotilalTest:
#     headers = {
#         "Accept": "application/json",
#         "ApiKey": "ypdJRIbZkCTHV5Tp",
#         "vendorinfo": "EMUM755714",
#         "User-Agent": "MOSL/V.1.1.0",
#         "SourceId": "WEB",
#         "MacAddress": "00:50:56:BD:F4:0B",
#         "ClientLocalIp": "192.168.165.165",
#         "ClientPublicIp": "106.193.137.95",
#         "osname": "Ubuntu",
#         "osversion": "10.0.19041",
#         "devicemodel": "AHV",
#         "manufacturer": "DELL",
#         "productname": "Your Product Name",
#         "productversion": "Your Product Version",
#         "installedappid": "AppID",
#         "browsername": "Chrome",
#         "browserversion": "105.0"
#     }
#     url = "https://uatopenapi.motilaloswal.com/rest/login/v3/authdirectapi"
#     ltp_utl = "https://uatopenapi.motilaloswal.com/rest/report/v1/getltpdata"
#     place_order_url = "https://uatopenapi.motilaloswal.com/rest/trans/v1/placeorder"
#
#     def generate_token(self, totp):
#         str = "Quant@123ypdJRIbZkCTHV5Tp"
#         result = hashlib.sha256(str.encode())
#
#         data = {
#             "userid": "EMUM755714",
#             "password": result.hexdigest(),
#             "2FA": "25/03/1993",
#             "totp": totp
#         }
#
#         response = requests.post(MotilalTest.url, headers=MotilalTest.headers, data=json.dumps(data))
#         resp_json = response.json()
#         print(resp_json)
#
#         auth_token = resp_json['AuthToken']
#
#         MotilalTest.headers['Authorization'] = auth_token
#
#     def get_ltp(self):
#         data = {
#             "userid": "EMUM755714",
#             "exchange": "NSE",
#             "scripcode": 3045
#         }
#
#         response = requests.post(MotilalTest.ltp_utl, headers=MotilalTest.headers, data=json.dumps(data))
#         print(response.json())
#         return response.json()["data"]["ltp"] / 100.0
#
#     def place_order(self, price, quantity):
#         data = {
#             "exchange": "NSE",
#             "symboltoken": 3045,
#             "buyorsell": "BUY",
#             "ordertype": "LIMIT",
#             "producttype": "NORMAL",
#             "orderduration": "DAY",
#             "price": price,
#             "triggerprice": 0,
#             "quantityinlot": quantity,
#             "disclosedquantity": 0,
#             "amoorder": "N",
#             "algoid": "",
#             "tag": "test"
#         }
#
#         response = requests.post(MotilalTest.place_order_url, headers=MotilalTest.headers, data=json.dumps(data)).json()
#         print(response)
#
#
# motilal = MotilalTest()
# secret_key = "7TGIDZBCUCCF66Z3ANJIEZBVALQUB7MN"
# totp = pyotp.TOTP(secret_key)
# current_totp = totp.now()
# motilal.generate_token(current_totp)
# # motilal.send_otp()
# # motilal.verify_otp(otp)
# # ltp = motilal.get_ltp("NSE", "SBIN")
# ltp = motilal.get_ltp()
# print("LTP: %d", ltp)
#
# motilal.place_order(ltp, 1)
#
# # motilal.place_order("SBIN", "NSE", 1, "LIMIT", "BUY", "test", "NORMAL", ltp, 0)
# # orders_placed = motilal.get_orders()
# # print(orders_placed)
# #
# # motilal.modify_orders_till_complete(orders_placed)

motilal = Motilal(is_uat=True)
motilal.generate_token()