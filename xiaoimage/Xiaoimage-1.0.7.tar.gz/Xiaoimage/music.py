import requests
import jsonpath
import os

def song_download(url,title,author):
    # 创建文件夹
    os.makedirs("music",exist_ok=True)
    path = 'music\{}.mp3'.format(title)
    print('歌曲:{0}-{1},正在下载...'.format(title,author))
    # 下载（这种读写文件的下载方式适合少量文件的下载）
    content = requests.get(url).content
    with open(file = title + author + '.mp3',mode='wb') as f:
      f.write(content)
    print('下载完毕,{0}-{1},请试听'.format(title,author))
class md:
  """
    1.url
    2.模拟浏览器请求
    3.解析网页源代码
    4.保存数据
      """
  def get_music_name(name, platfrom, index):
    """
    搜索歌曲名称
    :return:
    """
    #print("1.网易云:netease\n2.QQ:qq\n3.酷狗:kugou\n4.酷我:kuwo\n5.百度:baidu\n6.喜马拉雅:ximalaya")
    #print("-------------------------------------------------------")
    url = 'https://music.liuzhijin.cn/'
    headers = {
      "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36",
      # 判断请求是异步还是同步
      "x-requested-with":"XMLHttpRequest",
    }
    param = {
      "input":name,
      "filter":"name",
      "type":platfrom,
      "page": 1,
    }
    res = requests.post(url=url,data=param,headers=headers)
    json_text = res.json()

    title = jsonpath.jsonpath(json_text,'$..title')
    author = jsonpath.jsonpath(json_text,'$..author')
    url = jsonpath.jsonpath(json_text, '$..url')
    if title:
      songs = list(zip(title,author,url))
      for s in songs:
        print(s[0],s[1],s[2])
      song_download(url[index],title[index],author[index])
    else:
      raise '没有搜索结果！'
