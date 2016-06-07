# -*- coding:utf-8 -*-
# __author__ = 'jakey'

import os
import csv
import xlrd


def __check_file_validate(filename, schema):
    """
    check file name validate
    :param filename: string file_path where import
    :param schema: string
    :return:
    """
    if not os.path.isfile(filename):
        raise Exception("目标文件不存在, 请重新输入")

    if os.path.splitext(filename)[1] != '.csv':
        raise Exception("文件类型有误, 请重新输入")

    if schema not in ['w', 'a']:
        raise Exception("目前只支持w和a模式")


def import_csv_list(filename, contents, headers=None, schema='w'):
    """
    import data to csv
    插入数据格式必须为 [(), ()]
    headers可以为空
    :param filename: string file_path where import
    :param headers: list  csv file table headers
    :param schema: string w or a
    :param contents: list
    :return:
    """
    __check_file_validate(filename, schema)
    if not isinstance(contents, list) and not isinstance(contents, tuple):
        raise Exception("数据格式有误, 请重新输入")

    with open(filename, schema,  newline='') as csvfile:
        writer = csv.writer(csvfile)
        if headers and isinstance(headers, list):
            writer.writerow(headers)
        writer.writerows(contents)


def import_csv_dict(filename, contents, headers=None, schema='a'):
    """
    插入数据格式必须为 [{}, {}]
    headers 不能为空, 必须有头文件
    :param filename: string file_path where import
    :param contents: string list
    :param headers: list  csv file table headers
    :param schema: w or a
    :return:
    """
    __check_file_validate(filename, schema)
    if not isinstance(headers, list) or not headers:
        raise Exception("参数输入有误, 请重新输入")

    if not isinstance(contents, list):
        raise Exception("数据格式有误, 请重新输入")

    with open(filename, schema) as write_file:
        fieldnames = headers
        writer = csv.DictWriter(write_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(contents)


def export_csv(filename, way=1):
    """
    read data from csv file
    :param filename: string exists file path
    :param way: header or not 1 or 2
    :return:
    """
    if not os.path.isfile(filename) or way not in [1, 2]:
        raise Exception("参数有误, 请重新输入")

    with open(filename) as csvfile:
        if way == 1:
            reader = csv.reader(csvfile)
        else:
            reader = csv.DictReader(csvfile)

        return reader


def export_excel(filename, sheet=None):
    """
    export excel from filename and sheet
    :param filename: string
    :param sheet: sheet name
    :return:
    """
    if not os.path.isfile(filename):
        raise Exception("参数有误, 请重新输入")

    data = xlrd.open_workbook(filename)
    if not sheet:
        table = data.sheet_by_index(0)
    else:
        table = data.sheet_by_name(sheet)
    return table

if __name__ == "__main__":
    pass
    """
    way1_data = [
        ("123", "456"),
        ("463", "fsadf")
    ]

    way2_data = [
        {"jingdu": 123, "weidu": "123"},
        {"jingdu": 234, "weidu": "456"}
    ]

    file_path = os.path.dirname(__file__)
    path = os.path.join(file_path, 'test1.csv')

    # 导入csv数据
    import_csv_list(path, way1_data)
    import_csv_dict(path, way2_data, headers=["jingdu", "weidu"])

    # 导出csv数据
    reader = export_csv(path)
    for row in reader:
        print(row)

    # 读取excel数据
    tables = export_excel(path)
    table.row_values(i)
    .......
    """
