from unicodedata import normalize as nm
import re


def normalize_html_text(text: str) -> str:
    """一般用于清洗解析html得到的文本
    """
    if text is not None:
        t = text.strip()
        t = nm('NFKC', t) # 去除一下 x34 类似的特殊字符
        t = t.replace('\n\t', '')
        t = t.replace('\n', '')
        t = re.sub('^[\[][1-9]*[\]]$', '', t) # 去除[12]这样的标签
        return t
    else:
        return ''
    
def is_all_chinese(strs: str):
    """判断是否全是中文
    """
    for _char in strs:
        if not '\u4e00' <= _char <= '\u9fa5':
            return False
    return True

def is_all_english(strs: str):
    """判断一个字符串是否全是英文
    """
    return strs.encode('utf-8').isalpha()