### 需求：
批量提取网页固定格式简历中的信息，文件格式包括html（智联招聘）或mht（51job）。
其中mht是单一网页格式，通过base64编码，将文字内容和图片合并显示，常见的eml也是使用此编码方式，需要切分不同的数据块并重新解码后才能正确还原，
随手百度了下，目前mht并没有太友好的python组件，甚至有些还是收费的，因此简单使用re+base64模块处理

##### 说明:
本示例仅演示从简历中提取特定信息（和爬虫功能非常近似），素材为智联招聘简历若干、51job简历若干。

其实对于HR工作贡献更大的，是通过设立评分卡机制，对候选人的材料进行自动打分和排序，如毕业院校为海外名校、211/985、研究生/本科、给与不同的分值，
如工作履历上包含用人部门优先考虑的同业公司名称，也予以加分，并对定期收集整理的简历进行排序后，对分值高的候选人优先安排推荐或面谈，提高效率和成功率，
处理机制可以排入定时任务，自动处理招聘网站和邮箱投递的简历，方便HR部门将资料整理、筛选、汇总等流程相对固定、规则明确的业务由人工转为自动化处理。

![示例](https://github.com/QingYu2017/pic/blob/master/16.gif)

### 基础知识
- python基础；
- bs4模块、re模块、base64模块使用基础；
- html语言基础

### 代码示例
```python
# -*- coding: utf-8 -*- 
#/root/Envs/v36/bin

from bs4 import BeautifulSoup as bs
import sys,os,base64,re

def parserHTML(file):
    f=open(file,'r',encoding='UTF-8')
    body=bs(f.read(),"html.parser")
    print(body.find(id='userName').text.strip())
    print(body.find(class_='main-title-fr').text.strip())
    #print(body.find(class_='summary-top').text.strip())
    print(body.find(class_='summary-bottom').text.strip())
    print(body.find(class_='resume-preview-dl educationContent').text.strip())

def parserMHT(file):
    f=open(file,'r')
    body=f.read()
    str=re.findall('\n\n[\s\S]*\n\n',re.findall('Content-Type:text/html;[\s\S]*?---',body)[0])[0][3:-2]
    tables=bs(base64.b64decode(str).decode('gb2312'),"html.parser").find_all('table')
    tds=tables[1].find_all('tr')[1].find_all('td')
    print(tds[2].text)
    print(tds[8].text)
    print(tds[10].text)
    print(tds[12].text)
    print(tds[14].text)
    print(tds[25].text)

files=os.listdir(sys.path[0]+'\\resume')

for i in range(len(files)):
    file=sys.path[0]+'\\resume\\'+files[i]
    print(file)
    try:
        try:
            parserMHT(file)
        except:
            parserHTML(file)
    except:
        pass
```
