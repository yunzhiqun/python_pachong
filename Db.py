# -*- codeing: utf-8 -*-
# @Time :2022/6/26 15:49
# @Author :shilingming
# @Site :
# @File :Db.py.py
# @Software: PyCharm

#连接MySQL数据库
def connect_mysql():
    import pymysql
    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123', db='test', charset='utf8')
    return conn

#查询数据库
def select_mysql(conn,sql):
    cursor = conn.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    return data

#插入数据库
def insert_mysql(conn,sql):
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    return True

#更新数据库
def update_mysql(conn,sql):
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    return True

#删除数据库
def delete_mysql(conn,sql):
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    return True

#关闭数据库
def close_mysql(conn):
    conn.close()
    return True

def main():
    conn = connect_mysql()
    sql = "select * from exchange_rate"
    data = select_mysql(conn,sql)
    print("共"+str(len(data))+"条数据")
    close_mysql(conn)

if __name__ == '__main__':
    main()
    # connect_mysql()
    # sql = "select * from exchange_rate"
    # data = select_mysql(sql)
    # print(data)
    # close_mysql()
    # insert_mysql()
    # update_mysql()
    # delete_mysql()
    # main() 