#!/usr/bin/env python 
# -*- coding:utf-8 -*-

'''
Author: GanJun
Date: 2022.8
Usage: 解析excel表格
'''
import xlrd

def fetch_row(excel , sheet_name, start_key, end_key = "END"):
    """用于解析类似于SAMPLES这样的数据块

    Args:
        table: excel sheet table;
        start_key: the start key for information fields;
        end_key: the end key for information fields;
    Returns:
        a list : every element is a row of the excel 
    """
    table = xlrd.open_workbook(excel).sheet_by_name(sheet_name)
    start_index = table.col_values(0).index(start_key)
    end_index = table.col_values(0).index(end_key,start_index)
    row_contents = []
    for index in range(start_index + 1, end_index):
        if str(table.row_values(index)[0]).startswith("#"):
            continue
        row_contents.append(table.row_values(index))
    return row_contents

def fetch_col(excel, sheet_name, start_key, end_key = "END"):
    """用于解析SERIES这样的数据块

    :Args:
        table: xlrd.open_workbook(excel).sheet_by_name("name")
        start_key: the start key of the information fields
        end_key: the end key of the information fields
    :Return:
        a dict : {key1 : value1 , key2 : value2}
    """
    table = xlrd.open_workbook(excel).sheet_by_name(sheet_name)
    start_index = table.col_values(0).index(start_key)
    end_index = table.col_values(0).index(end_key,start_index)
    col_contents = {}
    for index in range(start_index + 1 , end_index):
        if str(table.row_values(index)[0]).startswith("#"):
            continue
        col_contents[table.row_values(index)[0]] = table.row_values(index)[1]
    return col_contents

