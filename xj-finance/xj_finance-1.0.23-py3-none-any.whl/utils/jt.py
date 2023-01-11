# -*- encoding:utf-8 -*-
import time, os
from datetime import datetime
from hashlib import md5
#import xlsxwriter
#from apps.resource.models import ResourceImage

#from main.settings import STATICFILES_DIRS


class Jt:
    # 判断是否是数字，包括浮点型
    @staticmethod
    def is_number(s):
        try:
            float(s)
            return True
        except ValueError:
            pass

        try:
            import unicodedata
            unicodedata.numeric(s)
            return True
        except (TypeError, ValueError):
            pass

        return False

    @staticmethod
    # 生成交易号：2位数（当前年份后2位数字）+8位数（当前时间戳去头2位）+6位数（用户名 经过hash crc16生成的 4位十六进制 转成5位数 然后头为补0）
    def make_unicode_16(salt=''):
        # 当前时间戳
        date_time = time.localtime(time.time())
        # 截取第3位到第4位
        year_code = str(date_time.tm_year)[2:4]

        # 当前时间戳
        timestamp = str(int(time.time()))
        # 截取第3位到第10位
        timestamp_code = timestamp[2:10]

        # 十六进制校验码
        crc_hex = Jt.crc16(salt) if salt else '0'
        # 十六进制转十进制
        crc_int = int(crc_hex, 16)
        # 头位补0
        crc_code = str('000000' + str(crc_int))[-6:]
        unicode = year_code + timestamp_code + crc_code

        return unicode

    # 生成日期yyyymmdd（8位）+时间（6位）hhmmss+毫秒（3位）=17位日期时间型数字
    @staticmethod
    def make_datetime_17():
        # 8位数+6+3=17位数
        t = time
        ms = int((t.time() - int(t.time()))*1000)
        return t.strftime('%Y%m%d%H%M%S',) + str(ms)

    @staticmethod
    def make_datetime_14():
        return time.strftime('%Y%m%d%H%M%S', )

    # crc16
    @staticmethod
    def crc16(x):
        a = 0xFFFF
        b = 0xA001
        for byte in x:
            a ^= ord(byte)
            for i in range(8):
                last = a % 2
                a >>= 1
                if last == 1:
                    a ^= b
        s = hex(a).upper()

        return s[2:6]

    # 文件生成md5
    @staticmethod
    def make_file_md5(file):
        if not os.path.exists(file):
            return None
        f = open(file, "rb")
        m = md5()
        m.update(f.read())
        f.close()
        result = m.hexdigest()
        return result

    # # 将数据导出为Excel
    # @staticmethod
    # def write_data_to_excel(save_dir, filename, format, header_list, data_list):
    #     '''
    #     瑛式备注
    #     :param save_dir: 保存文件的目录
    #     :param filename: 生成文件的文件名
    #     :param format: 生成文件的文件格式，只能是xlsx,xls,csv
    #     :param header_list: 文件的表头，即第一行标题
    #     :return:
    #     '''
    #
    #     folder_name = os.path.join(STATICFILES_DIRS[0], save_dir)
    #     # 没有该目录，则创建
    #     Jt.make_dir(folder_name=folder_name)
    #
    #     save_path = os.path.join(STATICFILES_DIRS[0], save_dir + filename + '.' + format)
    #
    #     # 打开文件
    #     wb = xlsxwriter.Workbook(save_path)
    #
    #     # 添加名字为Sheet1的Sheet
    #     ws = wb.add_worksheet('Sheet1')
    #
    #     # 设置表头
    #     row_num = 0
    #     columns = header_list
    #     for col_num in range(len(columns)):
    #         # 表头写入第一行
    #         ws.write(row_num, col_num, columns[col_num])
    #
    #     for index, it in enumerate(data_list):
    #         ws.write(index + 1, 0, it[0])  # A2 写入第A列数据
    #         ws.write(index + 1, 1, it[1])  # B2 写入第B列数据
    #         ws.write(index + 1, 2, it[2])  # C2 写入第C列数据
    #         ws.write(index + 1, 3, it[3])  # D2 写入第D列数据
    #         ws.write(index + 1, 4, it[4])  # E2 写入第E列数据
    #         ws.write(index + 1, 5, it[5])  # F2 写入第F列数据
    #         ws.write(index + 1, 6, it[6])  # G2 写入第G列数据
    #         ws.write(index + 1, 7, it[7])  # H2 写入第H列数据
    #         ws.write(index + 1, 8, it[8])  # I2 写入第I列数据
    #     wb.close()
    #
    #     return 1

    # 如果没有目录，则创建目录
    @staticmethod
    def make_dir(folder_name):
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        return 1







