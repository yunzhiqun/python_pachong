# -*- codeing: utf-8 -*-
# @Time :2022/6/26 19:47
# @Author :shilingming
# @Site :
# @File :Excel.py.py
# @Software: PyCharm

#excel操作
import xlrd
import xlwt
import xlutils
# import openpyxl

#读取excel文件
def read_excel(path):
    #打开excel文件
    workbook = xlrd.open_workbook(path)
    #获取sheet
    sheet = workbook.sheet_by_index(0)
    #获取行数
    rows = sheet.nrows
    #获取列数
    cols = sheet.ncols
    #创建二维数组
    data = []
    #获取单元格数据
    for i in range(rows):
        row_data = []
        for j in range(cols):
            row_data.append(sheet.cell(i,j).value)
            # print(sheet.cell_value(i,j),end='\t')
        data.append(row_data)
    return data
    
#写入excel文件
def write_excel():
    #创建excel文件
    workbook = xlwt.Workbook()
    #创建sheet
    sheet = workbook.add_sheet('test')
    #写入数据
    sheet.write(0,0,'hello')
    sheet.write(1,1,'world')
    #保存文件
    workbook.save('test.xlsx')

#更新excel文件
def update_excel():
    #打开excel文件
    workbook = xlrd.open_workbook('test.xlsx')
    #创建excel文件
    workbook = xlutils.copy.copy(workbook)
    #创建sheet
    sheet = workbook.get_sheet(0)
    #写入数据
    sheet.write(0,0,'hello')
    sheet.write(1,1,'world')
    #保存文件
    workbook.save('test.xlsx')

# #读取excel文件
# def read_excel_openpyxl():
#     #打开excel文件
#     workbook = openpyxl.load_workbook('test.xlsx')
#     #获取sheet
#     sheet = workbook.get_sheet_by_name('test')
#     #获取行数
#     rows = sheet.max_row
#     #获取列数
#     cols = sheet.max_column
#     #获取单元格数据
#     for i in range(rows):
#         for j in range(cols):
#             print(sheet.cell(i,j).value,end='\t')
#         print()

# #写入excel文件
# def write_excel_openpyxl():
#     #创建excel文件
#     workbook = openpyxl.Workbook()
#     #创建sheet
#     sheet = workbook.active
#     #写入数据
#     sheet.cell(0,0,'hello')
#     sheet.cell(1,1,'world')
#     #保存文件
#     workbook.save('test.xlsx')
# #更新excel文件
# def update_excel_openpyxl():
#     #打开excel文件
#     workbook = openpyxl.load_workbook('test.xlsx')
#     #创建excel文件
#     workbook = xlutils.copy.copy(workbook)
#     #创建sheet
#     sheet = workbook.get_sheet(0)
#     #写入数据
#     sheet.cell(0,0,'hello')
#     sheet.cell(1,1,'world')
#     #保存文件
#     workbook.save('test.xlsx')
# #读取excel文件
# def read_excel_openpyxl_cell():
#     #打开excel文件
#     workbook = openpyxl.load_workbook('test.xlsx')
#     #获取sheet
#     sheet = workbook.get_sheet_by_name('test')
#     #获取单元格数据
#     print(sheet.cell(0,0).value)
#     print(sheet.cell(1,1).value)

# #写入excel文件
# def write_excel_openpyxl_cell():
#     #创建excel文件
#     workbook = openpyxl.Workbook()
#     #创建sheet
#     sheet = workbook.active
#     #写入数据
#     sheet.cell(0,0,'hello')
#     sheet.cell(1,1,'world')
#     #保存文件
#     workbook.save('test.xlsx')
# #更新excel文件
# def update_excel_openpyxl_cell():
#     #打开excel文件
#     workbook = openpyxl.load_workbook('test.xlsx')
#     #创建excel文件
#     workbook = xlutils.copy.copy(workbook)
#     #创建sheet
#     sheet = workbook.get_sheet(0)
#     #写入数据
#     sheet.cell(0,0,'hello')
#     sheet.cell(1,1,'world')
#     #保存文件
#     workbook.save('test.xlsx')
# #读取excel文件
# def read_excel_openpyxl_cell_value():
#     #打开excel文件
#     workbook = openpyxl.load_workbook('test.xlsx')
#     #获取sheet
#     sheet = workbook.get_sheet_by_name('test')
#     #获取单元格数据
#     print(sheet.cell(0,0).value)
#     print(sheet.cell(1,1).value)
    
