from big_thing_py.utils import *
import requests
from enum import Enum


class RequestMethod(Enum):
    GET = 0
    POST = 1
    PUT = 2
    DELETE = 3

# class GoogleAPIClient():
#     def __init__(self, client_id: str = None, api_key: str = None) -> None:
#         self.client_id = client_id
#         self.api_key = api_key
#         self.headers = {"X-Naver-Client-Id": self.client_id,
#                         "X-Naver-Client-Secret": self.api_key}


class NaverAPIClient():
    def __init__(self, client_id: str = None, api_key: str = None) -> None:
        self.client_id = client_id
        self.api_key = api_key
        self.headers = {"X-Naver-Client-Id": self.client_id,
                        "X-Naver-Client-Secret": self.api_key}

    # def search(self, ):
    #     url = "https://openapi.naver.com/v1/datalab/search"
    #     self.headers['Content-Type'] = 'application/json'

    #     files = "{\"startDate\":\"2017-01-01\",\"endDate\":\"2017-04-30\",\"timeUnit\":\"month\",\"keywordGroups\":[{\"groupName\":\"한글\",\"keywords\":[\"한글\",\"korean\"]},{\"groupName\":\"영어\",\"keywords\":[\"영어\",\"english\"]}],\"device\":\"pc\",\"ages\":[\"1\",\"2\"],\"gender\":\"f\"}"

    #     request = urllib.request.Request(url)
    #     request.add_header("X-Naver-Client-Id", self.client_id)
    #     request.add_header("X-Naver-Client-Secret", self.api_key)
    #     request.add_header("Content-Type", "application/json")
    #     response = urllib.request.urlopen(request, data=files.encode("utf-8"))
    #     rescode = response.getcode()
    #     if (rescode == 200):
    #         response_body = response.read()
    #         print(response_body.decode('utf-8'))
    #     else:
    #         print("Error Code:" + rescode)

    def face_detect(self, image: str):
        url = "https://openapi.naver.com/v1/vision/face"  # 얼굴감지

        files = {'image': open(image, 'rb')}
        response = requests.post(url,  files=files, headers=self.headers)
        rescode = response.status_code
        if (rescode == 200):
            return response.text
        else:
            return f"Error Code: {rescode}"

    def face_detect_celebrity(self, image: str) -> str:
        url = "https://openapi.naver.com/v1/vision/celebrity"  # 유명인 얼굴인식

        files = {'image': open(image, 'rb')}
        response = requests.post(url,  files=files, headers=self.headers)
        rescode = response.status_code
        if (rescode == 200):
            return json_string_to_dict(response.text)['faces'][0]['celebrity']['value']
        else:
            return "해당없음"

    def papago(self, text: str, src: str, dst: str):
        url = "https://openapi.naver.com/v1/papago/n2mt"

        data = {'source': src,
                'target': dst,
                'text': text.encode('utf-8')}

        response = requests.post(url, data=data, headers=self.headers)
        rescode = response.status_code

        if (rescode == 200):
            return json_string_to_dict(response.text)['message']['result']['translatedText']
        else:
            return f"Error Code: {rescode}"

    def papago_detect_lang(self, text: str):
        url = "https://openapi.naver.com/v1/papago/detectLangs"

        data = {'query': text.encode('utf-8')}

        response = requests.post(url, data=data, headers=self.headers)
        rescode = response.status_code

        if (rescode == 200):
            return response.text
        else:
            return f"Error Code: {rescode}"


class KakaoAPIClient():
    def __init__(self, api_key: str = None) -> None:
        self.api_key = api_key
        self.headers = {
            'Authorization': f'KakaoAK {self.api_key}'
        }

    def search(self, text) -> dict:
        '''
        Ref: https://developers.kakao.com/docs/latest/ko/daum-search/dev-guide
        '''
        url = 'https://dapi.kakao.com/v2/search/web'
        params = {
            'query': text
        }
        data = None
        response = requests.get(
            url, headers=self.headers, params=params, data=data)
        return response.json()

    def pose(self, image: str) -> dict:
        '''
        Ref: https://developers.kakao.com/docs/latest/ko/pose/dev-guide
        '''

        url = "https://cv-api.kakaobrain.com/pose"
        params = None
        data = {'image_url': image} if 'http' in image else None
        files = {'file': open(image, 'rb').read()
                 } if 'http' not in image else None
        response = requests.post(
            url=url, headers=self.headers, params=params, data=data, files=files)
        return response.json()

    def OCR(self, image: str):
        '''
        Ref: https://www.kakaoicloud.com/service/detail/6-9
        '''
        url = "https://dapi.kakao.com/v2/vision/text/ocr"
        params = None
        data = None
        files = {'image': open(image, 'rb').read()
                 } if 'http' not in image else None
        response = requests.post(
            url=url, headers=self.headers, params=params, data=data, files=files)
        return response.json()

    def translation(self, text: str, src: str, dst: str):
        '''
        Ref: https://www.kakaoicloud.com/service/detail/6-10
        '''
        from kakaotrans import Translator
        translator = Translator()
        # result = translator.translate("Try your best rather than be the best.")
        result = translator.translate(text, src, dst)
        return result

        # url = 'https://dapi.kakao.com/v2/translation/translate'
        # params = None
        # data = { 'query': '안녕하세요. 반갑습니다.',}
        # files = {'image': open(image, 'rb').read()
        #          } if 'http' not in image else None
        # response = requests.post(
        #     url=url, headers=self.headers, params=params, data=data, files=files)
        # return response.json()

    # def speech_to_text(self):
    #     '''
    #     Ref: https://www.kakaoicloud.com/service/detail/6-23
    #     '''
    #     from pydub import AudioSegment

    #     url = "https://kakaoi-newtone-openapi.kakao.com/v1/recognize"
    #     headers = {
    #         "Content-Type": "application/octet-stream",
    #         "Transfer-Encoding": "chunked",
    #         "Authorization": "KakaoAK " + self.api_key,
    #     }

    #     src = "transcript.mp3"
    #     dst = "test.wav"

    #     audSeg = AudioSegment.from_mp3(src)
    #     audSeg.export(dst, format="wav")

    #     with open('heykakao.wav', 'rb') as fp:
    #         audio = fp.read()

    #     res = requests.post(url, headers=headers, data=audio)
    #     print(res.text)

    # def text_to_speech(self, text: str):
    #     from playsound import playsound
    #     url = "https://kakaoi-newtone-openapi.kakao.com/v1/synthesize"
    #     self.headers["Content-Type"] = "application/xml"

    #     data = f"<speak>{text}</speak>".encode('utf-8')
    #     res = requests.post(url, headers=self.headers, data=data)
    #     file_name = 'test_file.wav'
    #     with open(file_name, 'wb') as f:
    #         f.write(res.content)

    #     playsound(file_name)

    # def NLP(self):
    #     '''
    #     Ref: https://www.kakaoicloud.com/service/detail/6-25
    #     '''

    # def Vision(self, image: str):
    #     '''
    #     Ref: https://www.kakaoicloud.com/service/detail/6-28
    #     '''

    # def Conversion(self):
    #     '''
    #     Ref: https://www.kakaoicloud.com/service/detail/6-29
    #     '''


def API_response_check(res: requests.Response):
    if res.status_code not in [200, 204]:
        return False
    else:
        return res


def API_request(url, method=RequestMethod.GET, header='', body='', verify=None) -> dict:
    try:
        if method == RequestMethod.GET:
            res = requests.get(url, headers=header, verify=verify)
            if API_response_check(res):
                if res.status_code == 200:
                    data = res.json()
                elif res.status_code == 204:
                    data = {}
                return data
            else:
                return False
        elif method == RequestMethod.POST:
            res = requests.post(url, headers=header, data=body, verify=verify)
            if API_response_check(res):
                return res
            else:
                return False
        elif method == RequestMethod.PUT:
            res = requests.put(url, headers=header, data=body, verify=verify)
            if API_response_check(res):
                return res
            else:
                return False
        elif method == RequestMethod.DELETE:
            SOPLOG_DEBUG('Not implement yet')
        else:
            SOPLOG_DEBUG(
                f'[decode_MQTT_message] Unexpected request!!!', 'red')
    except Exception as e:
        print_error(e)
        return False


# def kakao_test():
#     api_client = KakaoAPIClient(api_key='feba82a01e28a99ca2c11322ef6896e9')
#     # print(api_client.OCR('./inspirational-1254724_960_720.png'))
#     # print(api_client.search('수리남'))
#     # print(api_client.pose(
#     #     'https://cdn.pixabay.com/photo/2016/03/09/09/30/woman-1245817_960_720.jpg'))
#     print(api_client.translation('안녕하세요.', 'kr', 'en'))


# def naver_test():
    # api_client = NaverAPIClient(
    #     client_id='RsSPHxj1l7VJsLTHs4eA', api_key='_nhJeYeoND')
    # print(api_client.search())
    # print(api_client.face_detect_celebrity(
    #     './KakaoTalk_20220929_071045111.jpg'))
    # print(api_client.papago('안녕하세요. 반갑습니다.', 'ko', 'en'))
    # print(api_client.papago_detect_lang('안녕하세요. 반갑습니다.'))
if __name__ == '__main__':
    # naver_test()
    pass
