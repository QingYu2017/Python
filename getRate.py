# -*- coding: utf-8 -*- 
#! /root/Envs/v36/bin/python
#Auth:Qing.Yu
#Mail:1753330141@qq.com
# Ver:V1.0
#Date:2018-08-05
#中国银行汇率，每分钟发布一次，使用requests、bs4库，自定义cls_mssql库（base pymssql）

import requests as r,cls_mssql
from bs4 import BeautifulSoup as bs

url='http://www.boc.cn/sourcedb/whpj/index.html'
s=cls_mssql.db_mssql()

(hbmc,xhmrj,xcmrj,xhmcj,xcmcj,zhzsj,fbrq,fbsj)=('null','null','null','null','null','null','null','null')

p=r.get(url)
tables=bs(p.content, "html.parser").find_all('table')
trs=tables[1].find_all('tr')
for i in range(1,len(trs)):
    tds=trs[i].find_all('td')
    (hbmc,xhmrj,xcmrj,xhmcj,xcmcj,zhzsj,fbrq,fbsj)=(tds[0].text,fill_blank(tds[1].text),fill_blank(tds[2].text),fill_blank(tds[3].text),fill_blank(tds[4].text),tds[5].text,tds[6].text,tds[7].text)
    s.sql_str="insert into exchange_rate values('%s',%s,%s,%s,%s,%s,'%s','%s')"%(hbmc,xhmrj,xcmrj,xhmcj,xcmcj,zhzsj,fbrq,fbsj)
    s.db_exec()

