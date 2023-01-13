title = '\033[1;33;3m'
code = '\033[1;34;3m'
sub = '\033[1;36;3m#'
end_ = '\033[0m'


class HelpDoc:
    @property
    def data_save(self):
        return f'''{title}crawles.data_save 数据存储{end_}

    {sub}crawles.data_save.image_save 单张图片保存方法 以下代码为使用案例{end_}
    {code}crawles.data_save.image_save(图片的链接，图片的保存位置){end_}
    
    {sub}crawles.data_save.images_save 多张图片保存方法 以下代码为使用案例{end_}
    {code}crawles.data_save.images_save([
                 [图片的链接，图片的保存位置] ,
                 [图片的链接，图片的保存位置] ,
                 [图片的链接，图片的保存位置] ,
                 [图片的链接，图片的保存位置] ,
                ]){end_}'''

    @property
    def api(self):
        return f'''{title}crawles.api 请求方法{end_}
        
    {sub}crawles.get get请求{end_}
    {code}url ='https://www.baidu.com/'
    # head_data数据如果为字符串自动清洗为自动格式/如果没有User-Agent则自动添加
    head_data = 字典数据/字符串文本数据
    # 如果为字符串自动清洗为自动格式/自动判断请求和数据是否传输错误
    param = 字典数据/字符串文本数据
    crawles.get(url,
                headers=head_data,
                params=param,
                **kwargs(其他爬虫参数)){end_}'''

    @property
    def other(self):
        return f'''{title}crawles.other 常用辅助方法{end_}
        
    {sub}crawles.decorator_thread 装饰在函数,可以使函数异步运行{end_}
    {code}@crawles.decorator_thread
    def func(参数):
        time.sleep(3)
              {end_}'''

    def __str__(self):
        return f'''{sub}通过‘print(crawles.help_doc.xxxxx)’查看方法使用详情{end_}
{title}help_doc.api                     请求方法{end_}
    {sub}.get                        get请求{end_}
    {sub}.post                       post请求{end_}
    {sub}.session_get                session_get请求{end_}
    {sub}.session_post               session_post请求{end_}

{title}help_doc.data_save               数据存储方法{end_}
    {sub}.data_save.image_save       图片存储{end_}
    {sub}.data_save.sql_save         mysql存储{end_}
    {sub}.data_save.mongo_save       mongodb存储{end_}
    {sub}.data_save.csv_save         csv存储{end_}

{title}help_doc.other                   常用辅助方法{end_}
    {sub}.execjs                     js调用{end_}
    {sub}.decorator_thread           多线程装饰器{end_}
    {sub}.head_format                请求信息格式化字典格式{end_}
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
