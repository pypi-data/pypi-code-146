from re import findall


def head_format(header_data):  # 请求数据格式化函数
    head_dict = {}
    for data in header_data.splitlines():  # 将文本以行进行分割
        data = data.lstrip()  # 去重字符串左边的空格
        if not data:  # 过滤掉空的数据 ''  '    '
            continue
        if data[0] == ':':  # 去重字符串的第一个冒号
            data = data[1:]
        html = findall('([a-zA-Z-]*?)\s*:\s*(.*?$)', data)

        for k, v in html:
            if 'Accept-Encoding' == k:  # 过滤掉Accept-Encoding参数
                continue
            head_dict[k] = v

    return head_dict


if __name__ == '__main__':
    data1 = '''
    type: 0
username: 18670221752
pwd: 111
pc_vcode: 
country: 86_zh-CN
mobile: 
vcode: 
pincode: 
formhash: CDD4E5BDEA
backurl: %2F%2Fwww.yaozh.com
    '''
    print(head_format(data1))
