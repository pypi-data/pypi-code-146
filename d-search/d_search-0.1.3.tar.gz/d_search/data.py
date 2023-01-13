from typing import List
from pydantic import BaseModel, HttpUrl, constr
import requests
from pathlib import Path

    
class Info(BaseModel):
    """百度百科的该词条的相关知识

    Args:
    - key: 键
    - values: 值的列表 
    """
    key: str
    values: List[str]
    
class Image(BaseModel):
    """存放网页上边的有文字描述的图片

    Args:
        src: 图片来源地址
        tag: 图片的描述
    """
    src: str
    tag: str
    
    def _download(self) -> bytes:
        res = requests.get(url=self.src)
        return res.content
    
    def save(self, file_path: Path):
        with open(file_path, 'wb') as f:
            f.write(self._download())

class Item(BaseModel):
    """百科的一个条目
    
    Args:
    - name: 词条名称
    - desc: 词条描述,用于混淆词条
    - summary: 词条摘要
    - synonym: 同义词
    """
    url: HttpUrl = ''
    name: constr(strip_whitespace=True)
    desc: constr(strip_whitespace=True)
    summary: constr(strip_whitespace=True)
    synonyms: List[constr(strip_whitespace=True, min_length=1)]
    infos: List[Info] = []
    images: List[Image] = []  
    
class Question(BaseModel):
    """百度知道的一条提问页面数据

    Args:
        url(str): 页面地址
        title(str): 提问标题
        content(str): 提问追加内容
        answers(str): 页面提取到的答案
    """
    url: str
    title: constr(strip_whitespace=True, min_length=1)
    content: constr(strip_whitespace=True, min_length=0)
    answers: List[constr(strip_whitespace=True, min_length=1) ]