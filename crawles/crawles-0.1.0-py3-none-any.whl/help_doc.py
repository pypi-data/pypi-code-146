title = '\033[1;33;3m'
title_ = '\033[0m'

code = '\033[1;34;3m'
code_ = '\033[0m'

sub = '\033[1;36;3m#'
sub_ = '\033[0m'


class HelpDoc:
    @property
    def image_save(self):
        return f'''{title}crawles.image_save 图片保存{title_}

    {sub}单张图片保存方法 以下代码为使用案例{sub_}
    {code}crawles.image_save.image_save(图片的链接，图片的保存位置){code_}
    
    {sub}多张图片保存方法 以下代码为使用案例{sub_}
    {code}crawles.image_save.images_save([
                 [图片的链接，图片的保存位置] ,
                 [图片的链接，图片的保存位置] ,
                 [图片的链接，图片的保存位置] ,
                 [图片的链接，图片的保存位置] ,
                ]){code_}'''

    def __str__(self):
        return f'''{sub}通过‘print(crawles.help_doc.xxxxx)’查看方法使用详情{sub_}
{sub}help_doc.get               get请求{title_}
{sub}help_doc.post              post请求{title_}
{sub}help_doc.session_get       session_get请求{title_}
{sub}help_doc.session_post      session_post请求{title_}
{title}help_doc.image_save        图片存储{title_}
{sub}help_doc.sql_save          mysql存储{title_}
{sub}help_doc.mongo             mongodb存储{title_}
{sub}help_doc.csv_save          csv存储{title_}
{sub}help_doc.execjs            js调用{title_}
        '''

    @staticmethod
    def _colour():
        s = "hello, world"
        print('\033[1;31;3m%s\033[0m' % s)
        print('\033[1;32;3m%s\033[0m' % s)
        print('\033[1;33;3m%s\033[0m' % s)
        print('\033[1;34;3m%s\033[0m' % s)
        print('\033[1;35;3m%s\033[0m' % s)
        print('\033[1;36;3m%s\033[0m' % s)


help_doc = HelpDoc()
