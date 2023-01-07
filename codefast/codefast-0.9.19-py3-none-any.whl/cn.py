'''Chinese
'''
import re
from typing import List

punctuations = list('，。‘’“”！？（）、：；《》／-【】『』￥——')


def is_cn(c: str) -> bool:
    return '\u4e00' <= c <= '\u9fa5'


def contains_chinese(text: str) -> bool:
    return any(re.findall(r'[\u4e00-\u9fff]+', text))


def is_cn_or_punc(c) -> bool:
    if is_cn(c): return True
    return c in punctuations


def split_by_punc(sentence: str) -> List[str]:
    return list(filter(len, re.split('|'.join(punctuations), sentence)))


def strip_punc(text: str) -> str:
    '''replace punctuations with whitespaces'''
    _punc = set(punctuations)
    return ''.join(' ' if c in _punc else c for c in text)
