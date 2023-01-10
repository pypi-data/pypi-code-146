from feapder import Request
print(False or 0)
res2 = Request('''http://part.csmu.edu.cn:82/zcglc/index.php?_m=mod_article&_a=fullist&caa_id=19''').get_response()
# res2.encoding='utf-8'
print(res2.text)
print(res2.encoding)
print(res2.apparent_encoding)
print(res2.encoding_errors)