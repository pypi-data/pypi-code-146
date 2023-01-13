#! /usr/bin/env python
'''
@Author: xiaobaiTser
@Time  : 2022/8/29 0:15
@File  : networkSpeedUtils.py
'''
from speedtest import Speedtest
from saf import Union

def unitConversion(speed: Union[int, float]):
    '''
    网速单位转换
    :param speed        :  网络传输值
    :return             :  (网速单位, 网速转换值, 网速原值, 单位级别)
    '''
    if 0 <= speed < 1024 ** 1:
        return f'{speed} bit/s', speed//(1024 ** 0), speed, 0
    elif 1024 ** 1 <= speed < 1024 ** 2:
        return f'{speed//1024 ** 1} Kbit/s', speed//(1024 ** 1), speed, 1
    elif 1024 ** 2 <= speed < 1024 ** 3:
        return f'{speed // 1024 ** 2} Mbit/s', speed//(1024 ** 2), speed, 2
    elif 1024 ** 3 <= speed < 1024 ** 4:
        return f'{speed // 1024 ** 3} Gbit/s', speed//(1024 ** 3), speed, 3
    elif 1024 ** 4 <= speed < 1024 ** 5:
        return f'{speed // 1024 ** 4} Tbit/s', speed//(1024 ** 4), speed, 4
    elif 1024 ** 5 <= speed < 1024 ** 6:
        return f'{speed // 1024 ** 5} Pbit/s', speed//(1024 ** 5), speed, 5
    else:
        return '您的网速太快的，外星球来的吧~，~'

def testNetworkSpeed():
    test = Speedtest()
    test.get_servers()
    return unitConversion(test.download()), unitConversion(test.upload())

# if __name__ == '__main__':
#     print(testNetworkSpeed())