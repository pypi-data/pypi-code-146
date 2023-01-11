# encoding: utf-8
"""
@project: sky-excel->excel_exporter
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: excel输出者
@created_time: 2022/9/29 17:01
"""
from io import BytesIO
import os
import platform
import re
import uuid

import xlrd
from xlutils.copy import copy
from xlwt import Workbook

from ..utils.j_dict import JDict


def catch_except(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            err_detail = " file:" + str(e.__traceback__.tb_frame.f_globals["__file__"]) + " line:" + str(e.__traceback__.tb_lineno) if platform.python_version()[0] == "3" else ""
            return None, "系统异常：" + str(e) + err_detail

    return wrapper


class ExcelExport:
    __err_msg = None
    max_row_resolve = []  # 最后一行单元格解析 单元格列表
    max_row_resolve_map = {}  # 最后一行单元格解析,映射字典
    max_row_merged_start_map = {}  # 追后一行合并单元格解析,映射字典
    is_additional_write = True  # 是否可以追加读写

    @property
    def err_msg(self):
        return self.__err_msg

    @err_msg.setter
    def err_msg(self, err):
        # 返回最先暴出来的错误，按照顺序返回，避免覆盖错误无法排查
        if self.__err_msg is None:
            self.__err_msg = err

    def __init__(self, excel_templet_path=None):
        """
        :param excel_templet_path: 模板的路径，可用则追加读写方式，不可用只写模式
        """
        if excel_templet_path and os.path.exists(excel_templet_path):
            # 追加读写方式
            self.is_additional_write = True
            self.read_wb = xlrd.open_workbook(excel_templet_path, formatting_info=True)  # 直接解析模板，获取可操作的excel对象
            self.additional_write_wb = copy(wb=self.read_wb)  # 完成xlrd对象向xlwt对象转换
            self.sheet_names = self.read_wb.sheet_names()
        else:
            # 仅写模式
            self.is_additional_write = False
            self.only_write_wb = Workbook()  # 完成xlrd对象向xlwt对象转换

    # 解析最大行（表达式行）
    def parse_max_row(self, excel_templet_title="Sheet1"):
        """
        :param excel_templet_title: 在追加读写模式下，指定读取的sheet，默认Sheet1
        :return: (data,err); data：{0: {'col_coord': (0, 1), 'value': '{{col_1}}'},....}
        """
        if not self.is_additional_write:
            return None, "当前不是追加读写模式，或者您传的模板路径不正确，所以不可以进行解析操作"
        if not excel_templet_title in self.sheet_names:
            return None, "不存在名称为：%s 的工作簿" % excel_templet_title
        read_sheet = self.read_wb.sheet_by_name(excel_templet_title)
        self.max_row_merged_start_map = {s_c: (s_c, e_c) for s_r, e_r, s_c, e_c in read_sheet.merged_cells if e_r == read_sheet.nrows}  # 追后一行合并单元格解析
        try:
            # 获取表达式的注意 merged_cells 坐标从0开始，max_row从1开始，merged_cells包括开始不包括结束;
            self.max_row_resolve = []
            self.max_row_resolve_map = {}
            start_merge = end_merge = -1
            for index in range(read_sheet.row_len(read_sheet.nrows - 1)):
                # 因为excel合并单元格数据存放在左上角的单元格之中
                if start_merge <= index < end_merge:
                    continue
                cell = JDict({})
                if self.max_row_merged_start_map.get(index):
                    start_merge, end_merge = self.max_row_merged_start_map.get(index)
                    cell["col_coord"] = (index, end_merge)
                else:
                    cell["col_coord"] = (index, index + 1)
                cell["value"] = read_sheet.cell(read_sheet.nrows - 1, index).value

                # 数据填充
                self.max_row_resolve.append(cell)
                self.max_row_resolve_map.update({index: cell})
            return self.max_row_resolve_map, None
        except Exception as e:
            err_detail = " file:" + str(e.__traceback__.tb_frame.f_globals["__file__"]) + " line:" + str(e.__traceback__.tb_lineno) if platform.python_version()[0] == "3" else ""
            return None, "系统异常：" + str(e) + err_detail

    # 追加写入body
    def additional_write(self, input_dict, excel_templet_title="Sheet1"):
        """
        追加读写
        :param input_dict: [{..},{..}..]
        :param excel_templet_title: 操作的sheet,需要与parse_max_row保持一致
        :return: data,err
        """
        # 合法性判断
        if not self.is_additional_write:
            return None, "当前不是追加读写模式，或者您传的模板路径不正确，所以不可以进行解析操作"
        if not excel_templet_title in self.sheet_names:
            return None, "不存在名称为：%s 的工作簿" % excel_templet_title
        if not isinstance(input_dict, list):
            self.err_msg = "input_dict格式应该是[{..},{..}..]"
        if not self.max_row_resolve:
            data, err = self.parse_max_row()
            if err:
                return None, err

        # 初始化
        read_sheet = self.read_wb.sheet_by_name(excel_templet_title)
        write_sheet = self.additional_write_wb.get_sheet(excel_templet_title)
        max_row = read_sheet.nrows  # 最大行
        max_col_num = read_sheet.row_len(max_row - 1)  # 计算出一共有多少列
        for row_num, row_input_dict in zip(range(max_row - 1, len(input_dict) + max_row), input_dict):  # 行遍历
            start_merge_cell = end_merge_cell = -1
            for col_index in range(max_col_num):  # 列遍历
                if start_merge_cell <= col_index < end_merge_cell:  # 被合并单元格，跳过
                    continue
                this_cell_value = self.parse_expression(self.max_row_resolve_map.get(col_index).value, row_input_dict)
                # 写入数据，单个单元格写入与合并单元表格写入
                if self.max_row_merged_start_map.get(col_index):
                    start_merge_cell, end_merge_cell = self.max_row_merged_start_map.get(col_index)
                    write_sheet.write_merge(row_num, row_num, start_merge_cell, end_merge_cell - 1, this_cell_value)
                else:
                    write_sheet.write(row_num, col_index, this_cell_value)

        return write_sheet, None

    def only_write(self, input_dict, excel_templet_title):
        """
        只写模式进行写入
        :param input_dict:[{..},{..}..]
        :param excel_templet_title: 创建sheet的名称
        :return: (data,err);
        """
        if not isinstance(input_dict, list):
            self.err_msg = "input_dict格式应该是[{..},{..}..]"
        try:
            headers = list(input_dict[0].keys())
            max_row = len(input_dict)
            max_col = len(headers)
            write_sheet = self.only_write_wb.add_sheet(excel_templet_title)
            for row in range(max_row):
                this_row = input_dict[row]
                for header_key, col in zip(headers, range(max_col)):
                    if not this_row.get(header_key):
                        continue
                    write_sheet.write(row, col, this_row[header_key])
        except Exception as e:
            err_detail = " file:" + str(e.__traceback__.tb_frame.f_globals["__file__"]) + " line:" + str(e.__traceback__.tb_lineno) if platform.python_version()[0] == "3" else ""
            return None, "系统异常：" + str(e) + err_detail

    def parse_expression(self, expression_value=None, row_input_dict=None):
        """
        把存在'{{...}}'的字符串，解析出来然后根据键值对匹配替换成 row_input_dict里面的值
        :param expression_value:
        :param row_input_dict:
        :return: 解析后的字符换
        """
        """解析表达式"""
        if not expression_value:
            return ""
        if not row_input_dict:
            return ""

        # 表达式解析数据
        this_cell_value_match = re.compile("{{.*?}}").findall(str(expression_value) if expression_value else "")
        this_cell_value_replaces = {i: row_input_dict.get(i.replace("{{", "").replace("}}", ""), "") for i in this_cell_value_match}
        for k, v in this_cell_value_replaces.items():
            expression_value = expression_value.replace(k, str(v))
        return expression_value

    def save(self, workbook=None, save_path=None, ):
        """
        保存excel，当没有save_path的时候返回流，存在则返回流
        :param workbook: 操作的Workbook对象
        :param save_path: 保存路径
        :return: data,err; data: None或者文件流
        """
        # 有存在的文件路径则保存文件，否则直接返回文件流
        if not workbook or not isinstance(workbook, Workbook):
            return None, "workbook 不是一个可写入的 Workbook对象"
        if save_path:
            try:
                # 递归创建目录
                if not os.path.exists(save_path):
                    os.makedirs(save_path)
                # 保存文件
                file_path_name = (save_path + "/" + str(uuid.uuid3(uuid.NAMESPACE_DNS, str(uuid.uuid1()))) + ".xls").replace("//", "/")
                workbook.save(file_path_name)
                return file_path_name, None
            except Exception as e:
                return None, "excel 写入异常：" + str(e)
        else:
            return self.__export_stream(workbook), None

    #  exce保存文件流
    def __export_stream(self, new_wb):
        try:
            from StringIO import StringIO
        except ImportError:
            from io import StringIO

        if platform.python_version()[0] == "2":
            # python 2.*.*
            output = StringIO()
            new_wb.save(output)
            output.seek(0)
            return output.getvalue()
        else:
            # python 3.*.*
            output = BytesIO()
            new_wb.save(output)
            output.seek(0)
            return output.getvalue()
