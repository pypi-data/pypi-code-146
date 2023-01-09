# 执行语言编号
class l:
    LANGS = {
        'zh' : 0,
        'en' : 1,
    }
    n = 1  # 当前使用的语言编号

import locale
if 'zh_CN' in locale.getdefaultlocale():
    l.n = l.LANGS['zh']
else :
    l.n = l.LANGS['en']


LANG_TABLE = {
    '测试报告' : ['测试报告','Test Report'],
    '指定测试报告标题' : ['指定测试报告标题','set test report title'],
}


# 返回当前使用语言字符串
def ls(lookupStr):
    return LANG_TABLE[lookupStr][l.n]

class Settings:
    auto_open_report = True
    report_title = '' # 命令行参数会设置,并且有缺省值
    report_url_prefix = '' # 命令行参数会设置,并且有缺省值