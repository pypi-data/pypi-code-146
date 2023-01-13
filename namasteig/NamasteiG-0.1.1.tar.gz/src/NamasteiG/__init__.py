import uuid
import string
import requests
import random
import time
import json
import base64
from Cryptodome.Cipher import AES, PKCS1_v1_5
from Cryptodome.PublicKey import RSA
from Cryptodome.Random import get_random_bytes
value=[]
value1=[]

def password_encrypt(password):
    resp = requests.get('https://i.instagram.com/api/v1/qe/sync/')
    publickeyid = int(resp.headers.get('ig-set-password-encryption-key-id'))
    publickey = resp.headers.get('ig-set-password-encryption-pub-key')
    session_key = get_random_bytes(32)
    iv = get_random_bytes(12)
    timestamp = str(int(time.time()))
    decoded_publickey = base64.b64decode(publickey.encode())
    recipient_key = RSA.import_key(decoded_publickey)
    cipher_rsa = PKCS1_v1_5.new(recipient_key)
    rsa_encrypted = cipher_rsa.encrypt(session_key)
    cipher_aes = AES.new(session_key, AES.MODE_GCM, iv)
    cipher_aes.update(timestamp.encode())
    aes_encrypted, tag = cipher_aes.encrypt_and_digest(password.encode("utf8"))
    size_buffer = len(rsa_encrypted).to_bytes(2, byteorder='little')
    payload = base64.b64encode(b''.join([
        b"\x01",
        publickeyid.to_bytes(1, byteorder='big'),
        iv,
        size_buffer,
        rsa_encrypted,
        tag,
        aes_encrypted
    ]))
    return payload.decode()

def generate_jazoest(symbols):
    amount = sum(ord(s) for s in symbols)
    return f'2{amount}'

class Instagram:
    def __init__(self,User,Password):
        self.user = User
        self.passw=Password
    def Login(self):
        g1=requests.get('https://i.instagram.com/api/v1/accounts/login/').cookies
        mid=g1['mid']
        PigeonSession=f'UFS-{str(uuid.uuid4())}-0'
        IgDeviceId=uuid.uuid4()
        IgFamilyDeviceId=uuid.uuid4()
        a1=''.join(random.choices(string.ascii_letters+string.digits,k=16))
        AndroidID=f'android-{a1}'
        a2=''.join(random.choices(string.digits,k=6))
        useragent=f'Instagram 267.0.0.0.10 Android (30/11; 320dpi; 720x1513; Xiaomi/POCO; {a2}MI; angelicain; mt6765; en_IN; 437412294)'
        self.Blockversion='a7230560b5078ccef167a197a18954fa265dacb75c224b0de7922d1086c43cfb'
        headers = {
            'Host': 'i.instagram.com',
            'X-Ig-App-Locale': 'en_IN',
            'X-Ig-Device-Locale': 'en_IN',
            'X-Ig-Mapped-Locale': 'en_US',
            'X-Pigeon-Session-Id': str(PigeonSession),
            'X-Pigeon-Rawclienttime': str(time.time()),
            'X-Ig-Bandwidth-Speed-Kbps': '-1.000',
            'X-Ig-Bandwidth-Totalbytes-B': '0',
            'X-Ig-Bandwidth-Totaltime-Ms': '0',
            'X-Bloks-Version-Id': self.Blockversion,
            'X-Ig-Www-Claim': '0',
            'X-Bloks-Is-Layout-Rtl': 'false',
            'X-Ig-Device-Id':str(IgDeviceId),
            'X-Ig-Family-Device-Id': str(IgFamilyDeviceId),
            'X-Ig-Android-Id': str(AndroidID),
            'X-Ig-Timezone-Offset': '19800',
            'X-Ig-Nav-Chain': f'LoginLandingFragment:login_landing:1:warm_start:{time.time()}::',
            'X-Fb-Connection-Type': 'WIFI',
            'X-Ig-Connection-Type': 'WIFI',
            'X-Ig-Capabilities': '3brTv10=',
            'X-Ig-App-Id': '567067343352427',
            'Priority': 'u=3',
            'User-Agent': str(useragent),
            'Accept-Language': 'en-IN, en-US',
            'X-Mid': str(mid),
            'Ig-Intended-User-Id': '0',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Fb-Http-Engine': 'Liger',
            'X-Fb-Client-Ip': 'True',
            'X-Fb-Server-Cluster': 'True',
        }
        data = {
            'signed_body': 'SIGNATURE.{"jazoest":"'+str(generate_jazoest(str(IgFamilyDeviceId)))+'","country_codes":"[{\\"country_code\\":\\"91\\",\\"source\\":[\\"default\\"]}]","phone_id":"'+str(IgFamilyDeviceId)+'","enc_password":"#PWD_INSTAGRAM:0:'+str(round(time.time()))+':'+str(self.passw)+'","username":"'+str(self.user)+'","adid":"'+str(uuid.uuid4())+'","guid":"'+str(IgDeviceId)+'","device_id":"'+str(AndroidID)+'","google_tokens":"[]","login_attempt_count":"0"}',
        }
        response = requests.post('https://i.instagram.com/api/v1/accounts/login/', headers=headers, data=data)
        self.response = response
        self.mid = mid
        self.PigeonSession = PigeonSession
        self.IgDeviceId = IgDeviceId
        self.IgFamilyDeviceId = IgFamilyDeviceId
        self.AndroidID = AndroidID
        self.UserAgent = useragent
        value = {
            "Response": self.response,
            "Mid": self.mid,
            'PigeonSession': self.PigeonSession,
            "IgDeviceId": self.IgDeviceId,
            "IgFamilyDeviceId": self.IgFamilyDeviceId,
            "AndroidID": self.AndroidID,
            'UserAgent': self.UserAgent,
            'BlockVersion':self.Blockversion
        }
        if 'ig-set-authorization' in response.headers:
            self.sessionid=response.headers['ig-set-authorization'].split(':')[2]
            self.xclaim = response.headers['x-ig-set-www-claim']
            self.igrur = response.headers['ig-set-ig-u-rur'].split(':')[1]
            self.userid = response.headers['ig-set-ig-u-ds-user-id']
        else:
            print(response.text)
        return value
    def head(self):
        headers = {
            'Host': 'i.instagram.com',
            'X-Ig-App-Locale': 'en_US',
            'X-Ig-Device-Locale': 'en_US',
            'X-Ig-Mapped-Locale': 'en_US',
            'X-Pigeon-Session-Id': str(self.PigeonSession),
            'X-Pigeon-Rawclienttime': str(time.time()),
            'X-Ig-Bandwidth-Speed-Kbps': '12195.000',
            'X-Ig-Bandwidth-Totalbytes-B': '8370095',
            'X-Ig-Bandwidth-Totaltime-Ms': '631',
            'X-Ig-App-Startup-Country': 'IN',
            'X-Bloks-Version-Id': str(self.Blockversion),
            'X-Ig-Www-Claim': str(self.xclaim),
            'X-Bloks-Is-Layout-Rtl': 'false',
            'X-Ig-Device-Id': str(self.IgDeviceId),
            'X-Ig-Family-Device-Id': str(self.IgFamilyDeviceId),
            'X-Ig-Android-Id': str(self.AndroidID),
            'X-Ig-Timezone-Offset': '28800',
            'X-Ig-Nav-Chain': '',
            'X-Fb-Connection-Type': 'WIFI',
            'X-Ig-Connection-Type': 'WIFI',
            'X-Ig-Capabilities': '3brTv10=',
            'X-Ig-App-Id': '567067343352427',
            'Priority': 'u=3',
            'User-Agent': str(self.UserAgent),
            'Accept-Language': 'en-US',
            'Authorization': 'Bearer IGT:2:' + str(self.sessionid),
            'X-Mid': str(self.mid),
            'Ig-U-Ig-Direct-Region-Hint': f'RVA,{self.userid},{31536000 + round(time.time())}:{self.igrur}',
            'Ig-U-Shbid': f'{random.randint(100, 9999)},{self.userid},{31536000 + round(time.time())}:{self.igrur}',
            'Ig-U-Shbts': f'{round(time.time())},{self.userid},{31536000 + round(time.time())}:{self.igrur}',
            'Ig-U-Ds-User-Id': f'{self.userid}',
            'Ig-U-Rur': f'EAG,{self.userid},{31536000 + round(time.time())}:{self.igrur}',
            'Ig-Intended-User-Id': f'{self.userid}',
            'X-Fb-Http-Engine': 'Liger',
            'X-Fb-Client-Ip': 'True',
            'X-Fb-Server-Cluster': 'True',
        }
        return headers

    def Scrape_Followers(self,UserID,Next_Max_Id=None):
        global value
        self.value=value
        self.UserID1=UserID
        self.ranktoken=str(uuid.uuid4())
        if Next_Max_Id == None:
            params = {
                'search_surface': 'follow_list_page',
                'query': '',
                'enable_groups': 'true',
                'rank_token': str(self.ranktoken),
            }
        else:
            params = {
                'search_surface': 'follow_list_page',
                'max_id': str(self.maxid),
                'query': '',
                'enable_groups': 'true',
                'rank_token': str(self.ranktoken),
            }
        response = requests.get(
            f'https://i.instagram.com/api/v1/friendships/{self.UserID1}/followers/',
            params=params,
            headers=Instagram.head(self),
        )
        if 'Oops, an error occurred.' in response.text:
            print('Oops, an error occurred.')
        elif 'The link you followed may be broken, or the page may have been removed' in response.text:
            print('The link you followed may be broken, or the page may have been removed')
        elif 'Please wait a few minutes before you try again.' in response.text:
            print(response.text)
        elif "challenge_required" in response.text:
            print(response.text)
        elif 'next_max_id' in response.text:

            try:
                self.maxid=response.json()['next_max_id']
                for Items in response.json()['users']:
                    value.append(Items)
                Instagram.Scrape_Followers(self,self.UserID1,self.maxid)
            except KeyError as key:
                return value
        else:
            try:
                for Items in response.json()['users']:
                    value.append(Items)
            except KeyError as key:
                pass
        return value
    def Scrape_Followings(self,UserID,Next_Max_Id=None):
        global value1
        self.value1 = value1
        self.UserID1 = UserID
        self.ranktoken = str(uuid.uuid4())
        if Next_Max_Id == None:
            params = {
            'includes_hashtags': 'true',
            'search_surface': 'follow_list_page',
            'query': '',
            'enable_groups': 'true',
            'rank_token': str(self.ranktoken),
            }
        else:
            params = {
                'includes_hashtags': 'true',
                'search_surface': 'follow_list_page',
                'max_id': str(self.maxid),
                'query': '',
                'enable_groups': 'true',
                'rank_token':str(self.ranktoken),
            }

        response = requests.get(
            f'https://i.instagram.com/api/v1/friendships/{self.UserID1}/following/',
            params=params,
            headers=Instagram.head(self),
        )
        if 'Oops, an error occurred.' in response.text:
            print('Oops, an error occurred.')
        elif 'The link you followed may be broken, or the page may have been removed' in response.text:
            print('The link you followed may be broken, or the page may have been removed')
        elif 'Please wait a few minutes before you try again.' in response.text:
            print(response.text)
        elif "challenge_required" in response.text:
            print(response.text)
        elif 'next_max_id' in response.text:

            try:
                self.maxid=response.json()['next_max_id']
                for Items in response.json()['users']:
                    value1.append(Items)
                Instagram.Scrape_Followings(self,self.UserID1,self.maxid)
            except KeyError as key:
                return value1
        else:
            try:
                for Items in response.json()['users']:
                    value1.append(Items)
            except KeyError as key:
                pass
        return value1
