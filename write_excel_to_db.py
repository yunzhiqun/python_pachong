# -*- codeing: utf-8 -*-
# @Time :2022/6/26 19:54
# @Author :shilingming
# @Site :
# @File :write_excel_to_db.py.py
# @Software: PyCharm
import os

import Db
import Excel


#excel写入数据库
def write_to_db(path):
    db_name_list = ['type','xianhui_buy','xianchao_buy','xianhui_sale','xianchao_sale','zhesuan_price','id','time']
    excel_name_list = ['货币名称','现汇买入价','现钞买入价','现汇卖出价','现钞卖出价','中行折算价','发布时间']
    #读取excel文件
    data = Excel.read_excel(path)
    con = Db.connect_mysql()
    #插入数据库
    for i in range(1,len(data)):
        db_name = ""
        excel_val = ""
        select_sql = "select * from exchange_rate where id = '"+str(data[i][len(excel_name_list)-1]) +"'"
        select_data = Db.select_mysql(con,select_sql)
        if len(select_data) == 0:
            for j in range(len(excel_name_list)):
                db_name += db_name_list[j] + ',' 
                excel_val += '\''+str(data[i][j]) + '\''+ ',' 
            db_name += str(db_name_list[len(excel_name_list)])  
            excel_val += '\''+str(data[i][len(excel_name_list)-1]) + '\''
            insert_sql = 'insert into exchange_rate (%s) values (%s)' % (db_name,excel_val) #拼接sql语句
            # print(insert_sql) 
            Db.insert_mysql(con,insert_sql)
    Db.close_mysql(con)
    return True

#获取当前层级路径所有excel文件
def get_excel_list_in_current_folder():
    excel_list = []
    for root, dirs, files in os.walk(os.getcwd()):
        for file in files:
            if file.endswith('汇率.xls'):
                excel_list.append(os.path.join(root, file))
    return excel_list
 

if __name__ == '__main__':
    #获取当前路径
    path = os.path.dirname(os.path.abspath(__file__))
    excel_list = get_excel_list_in_current_folder()
    for excel in excel_list:
        write_to_db(excel)
