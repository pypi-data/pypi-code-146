import jieba
import requests
import pdfplumber
import urllib
import pandas as pd
from io import BytesIO
import re

class Nlp:
    def __init__(self):
        pass
    def today(self):
        url = "https://q5xsbdueopbmh7oykiyrjsjq240rjmgu.lambda-url.ap-southeast-1.on.aws"
        response = urllib.request.urlopen(url)
        a = response.read().decode('utf-8')
        df = pd.read_json(a)
        df.rename(columns={
        'mch': '标题',
        'zhqdm': '证券代码',
        'zhqjc':'证券简称',
        'ggbh':'网址',
        'riqi':'日期'}, inplace=True)
        df.drop('name', axis=1, inplace=True)
        return df    
    def getreport(self,url: str):
        req: Response = requests.get(url)
        with pdfplumber.open(BytesIO(req.content)) as pdf:
            a=""
            for page in pdf.pages:
                text = page.extract_text()
                a=a+text
            a=re.sub(r"\n", '', a)
            a=re.sub(r" ", '', a)
            a = re.sub(r"\.{5,}", '', a)
            return a
    def tokenize(self, text):
        a=jieba.cut(text)
        return list(a)
    def word_frequencies(self,tokens):
        word_freq = {}
        for word in tokens:
            if word in word_freq:
                word_freq[word] += 1
            else:
                word_freq[word] = 1
        return word_freq
    def compute_keywords(self,tokens:[], num_keywords: int):
        # 计算文本的词频
        word_freq = {}
        for word in tokens:
            if word in word_freq:
                word_freq[word] += 1
            else:
                word_freq[word] = 1
        # 按照词频从大到小排序
        sorted_word_freq = sorted(word_freq.items(), key=lambda x: x[1],reverse=True)
        # 返回前num_keywords个词
        return [word for word, freq in sorted_word_freq[:num_keywords]]
    # 计算文本的句子结构
    def sentence_structure(self,text: str):
        # 计算句子数量
        num_sentences = text.count('。') + text.count('！') + text.count('？')
        # 计算平均句子长度
        avg_sentence_length = len(text) / num_sentences
        return num_sentences, avg_sentence_length
if __name__ == '__main__':
    a=Nlp()
    b= a.today()
    print(b.iloc[0, 3])
    d=a.getreport(b.iloc[0, 3])
    f=a.sentence_structure(d)
    print(f)