# -*- codeing: utf-8 -*-
# @Time :2022/7/9 11:17
# @Author :shilingming
# @Site :
# @File :cctv_pachong.py
# @Software: PyCharm

import urllib.request, urllib.error  # 定制url,获取网页数据

import math
import time
import json
import Db

# 得到指定url的网页内容
def askURL(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36 Edg/101.0.1210.53 sec-ch-ua: " Not A;Brand";v="99", "Chromium";v="101", "Microsoft Edge";v="101" sec-ch-ua-mobile: ?0 sec-ch-ua-platform: "Windows"'
    }

    request = urllib.request.Request(url, headers=headers)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
        # print(html)
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return html


#查询并写入数据库 
def query_and_save(baseurl,con,num): 
    html = askURL(baseurl)
    if html == "":
        print(str(num*100)+"网页为空")
        return 
    load_dict = json.loads(html)
    load_dict = load_dict['data'] #拆第一层花括号
    title_list = load_dict['list']
    if len(title_list) == 0:
        print(str(num*100)+"没有数据")
        return 
    # con = Db.connect_mysql()
    for i in range(len(title_list)):
        print('写入第'+str(num*100+i)+'条数据')
        insert_key = ''
        insert_value = '' 
        id = ''
        for key in title_list[i]:
            if key == 'id':
                id = title_list[i][key]
            insert_key = insert_key + key + ','
            insert_value = insert_value + "'" + str(title_list[i][key]) + "',"
        if id != '':
            select_sql = 'select * from cctv_jiaodianfangtan where id = \''+id+'\'' 
            # print(select_sql)
            select_data = Db.select_mysql(con, select_sql)
            if len(select_data) == 0:
                insert_key = insert_key[:-1]
                insert_value = insert_value[:-1]
                insert_sql = 'insert into cctv_jiaodianfangtan('+insert_key+') values('+insert_value+')' 
                # print(insert_sql)
                Db.insert_mysql(con,insert_sql)
            else:
                print('数据已存在\n'+id)
        else:
            print('数据异常,无id')
    # Db.close_mysql(con)

#获取数据总数
def get_total_num(baseurl): 
    html = askURL(baseurl)
    if html == "":
        print(str(num*100)+"网页为空")
        return 0
    load_dict = json.loads(html)
    load_dict = load_dict['data'] #拆第一层花括号
    total = load_dict['total']
    return total

def main():
    limit = 100
    baseurl1 = "http://api.cntv.cn/NewVideo/getVideoListByColumn?id=TOPC1451558976694518&n="+str(limit)+"&sort=desc&p=" 
    baseurl2 = "&mode=0&serviceId=tvcctv"  
    total_num = get_total_num(baseurl1+"0"+baseurl2)
    if total_num == 0:
        print("没有数据")
        return
    loop = math.ceil(total_num/limit)
    con = Db.connect_mysql()
    #循环 
    for i in range(0,loop): 
        query_and_save(baseurl1+str(i)+baseurl2,con,i)
    Db.close_mysql(con)

if __name__ == '__main__':
    main()


