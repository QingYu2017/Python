# -*- coding: utf-8 -*- 
#/root/Envs/v36/bin
#Auth:Qing.Yu
#Mail:1753330141@qq.com
# Ver:V1.0
#Date:2018-09-14


import requests as r
from bs4 import BeautifulSoup as bs
import time
import cls_mssql

url='http://www.sge.com.cn/sjzx/yshqbg'
#url="http://www.dyhjw.com/shanghaihuangjin/"

send_headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
              "Connection":"keep-alive",
              "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
              "Accept-Language":"zh-CN,zh;q=0.8"}
str=bs(r.get(url,headers=send_headers).content, "html.parser")
str=str.find_all('table')

arr=[]
for row in str[0].find_all('tr'):
    #print(row.get_text())
    arr.append(row.get_text().split('\n'))

d=time.strftime('%Y-%m-%d',time.localtime(time.time()))
t=time.strftime('%H:%M:%S',time.localtime(time.time()))
sql=cls_mssql.db_mssql()

for row in arr:
    sql.sql_str="insert into priceGolden values('%s','%s','%s')"%(d,t,"','".join(row[1:-1]))
    #print(sql.sql_str)
    try:
        sql.db_exec()
    except:
        print('数据写入失败')
