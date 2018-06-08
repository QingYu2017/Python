#!/usr/bin/python
#_*_coding:utf-8 _*_
#Auth:Qing.Yu
#Mail:1753330141@qq.com
# Ver:V1.0
#Date:2018-05-09

import requests as r
from bs4 import BeautifulSoup as bs

def txt_wr(txt):
    f=open('c:\list.txt','ab+')
    f.write(txt.encode())
    f.close()

for m in range(10):#830):
    url='http://www.csisc.cn/fund-webapp/fundCode/fundSearch_fundCode.action?fundCode.fundNumber=&fundCode.fundNameL=&fundCode.fundManager=&currPage=&pageData.pageNeeded=%d&pageData.pageSize=10&pageData.maxPageSize=100&pageData.count=8284&pageCount=829&pageData.isNeedCount=false'%(m)
    p=r.get(url)
    p_content = bs(p.content)
    ts=p_content.find_all('table')
    trs=ts[1].find_all('tr')
    for i in range(1,len(trs)):
        tds=trs[i].find_all('td')
        tr_text=""
        for j in range(1,len(tds)):
            tr_text+=" | "+tds[j].get_text().strip()
        print(tr_text)
