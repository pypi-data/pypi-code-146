import requests

headers = {
  'Accept-language'
  'en',
  'User-Agent'
  'Mozilla5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit531.21.10 (KHTML, like Gecko) '
  'Version4.0.4 Mobile7B334b Safari531.21.102011-10-16 202310'
}

def download(url):
  request_url = f'httpsapi.douyin.wtfapiurl={url}'
  response = requests.get(request_url, headers=headers)
  video = response.json()['video_data']['nwm_video_url_HQ']
  return video