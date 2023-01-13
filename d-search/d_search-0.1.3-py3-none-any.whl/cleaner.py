import requests
import json
from unicodedata import normalize


class WuDaoCleaner:
    
    request_url = 'https://dorc.baai.ac.cn/api/clean-data/v1/cleanDataByTool'
    
        
    def clean_url(self, url: str) -> str:
        data = {'cleaningType': 1 , 'inputUrl': url}
        res = requests.post(url=self.request_url, data=data)
        content = json.loads(res.text)['data']['content']
        content = ''.join(content.split('\n'))
        return normalize('NFKC', content)
    
    def clean_text(self, text: str) -> str:
        data = {'cleaningType': 3 , 'inputStr': text}
        res = requests.post(url=self.request_url, data=data)
        content = json.loads(res.text)['data']['content']
        content = content.replace('\n', '')
        return normalize('NFKC', content)