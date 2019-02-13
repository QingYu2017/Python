```shell
#Auth:Qing.Yu
#Mail:1753330141@qq.com
# Ver:V1.0
#Date:2019-02-13
```

### 背景说明：
- 网络设备、服务器设备，通过标准管理接口（snmp、ipmi、jmx）和Zabbix代理方式，可以方便的进行监控。但是对于非标接口的数据，如数据库系统、应用系统关键
数据（交易指令数、当日累计交易量、业务系统响应时间）、网页发布的信息（外汇行情、贵金属行情）等，使用缺省的模板无法直接管理。而Oracle等常见应用场景，
虽然有定制模板，但是需要在服务器端安装特定应用甚至新增额外的账户，在影响系统稳定性的同时，也存在安全隐患。
- Zabbix具备强大的扩展功能，对于上述内嵌模板未包含的监控管理需求，可以通过外部检查功能，可以轻松的进行完善。
- 本次案例，使用ZBX对web发布的外汇行情进行采集和监控，新增监控项定期从web端获取数据，并对价格的异常波动进行监控。

### 方案设计：
1. 使用python从网页获取汇率行情；
1. 将python脚本返回数据作为监控项采集进zbx；
1. 对行情数据设置价格异常波动监控并触发提示信息；

### 参考资料：
- 佚名. Python宝典[M]. 2014.
- 佚名. Zabbix Documentation 3.4[EB／OL]. 2018. 
- 佚名. Beautiful Soup 4.4.0 文档[EB／OL]. 2018. 
- Qing Yu. 汇率信息的获取示例[EB／OL]. 2018. 

### 功能示例：
执行脚本，输入币种和汇率类型做为参数，返回相应的当前美元现钞卖出价行情
![示例](https://github.com/QingYu2017/pic/blob/master/21.png)

zbx中配置外部检查项
![示例](https://github.com/QingYu2017/pic/blob/master/22.png)

美元现钞卖出价行情的图形展示
![示例](https://github.com/QingYu2017/pic/blob/master/23.png)

投资交易系统交易笔数示例
![示例](https://github.com/QingYu2017/pic/blob/master/24.png)

### 代码参考：
```python
import requests as r,sys
from bs4 import BeautifulSoup as bs

url='http://www.boc.cn/sourcedb/whpj/index.html'

if len(sys.argv) == 1 :
    par1='美元'
    par2=1
else:
    par1=sys.argv[1]
    par2=int(sys.argv[2])

p=r.get(url)
tables=bs(p.content, "html.parser").find_all('table')
tr=tables[1].find(string=[par1]).parent.parent.find_all('td')
print(tr[par2].text)
```
