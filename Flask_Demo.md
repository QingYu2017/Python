Flask + Bootstrap是一种强大的组合，可以优雅的分离后台业务逻辑和前端展示需求，让企业内部的业务需求快速实现，帮助开发人员轻松跨过在UI把握能力上的短板，直接迈入响应式页面布局的时代。

很多年前，PHP + DB + ExtJS的学习最终因为ExtJS的难以驾驭止步，而Flask + Bootstrap可以帮助企业的IT管理人员，更灵活的实践自己的管理思路。

### 配置环境
- Python 3.6.5
- Flask Flas-Bootstrap
- pymssql

![截图示例](https://github.com/QingYu2017/pic/blob/master/09.png)
### 路由页面
```python
# -*- coding: utf-8 -*- 
#! /root/Envs/v36/bin/python
#Auth:Qing.Yu
#Mail:1753330141@qq.com
# Ver:V1.1
#Date:2018-07-19

from flask import Flask,render_template
from app.func_getInfo import returnArr
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)

@app.route('/')
def hello_world():
    return 'Hello Flask! '

@app.route('/ocepay/')
def oceInfo ():
    list=returnArr()
    return render_template("index1.html", title_name='XX货币',list=list)    

if __name__=='__main__':
    app.run(host='0.0.0.0',port=8080, debug=True)
```

### 功能定义
```python
from app.cls_mssql import db_mssql

def returnArr():
    sql=db_mssql()
    sql.sql_str="select * from v_oce_cash_history where left(日期,7)='2018-09' order by 日期 desc,交易时间 desc"
    sql.db_query()
    list = []
    for row in sql.rs:
        list.append(row)
    return list
```

### 基本框架定义
```html
<div class="container">
    {% extends "bootstrap/base.html" %}
    {% block title %}XX控股集团{% endblock %}
    <!--标题栏-->
    {% block navbar %}
        <nav class="navbar navbar-default">
                <ul class="nav navbar-nav"><div class="navbar-brand"><img src="{{ url_for('static',filename='images/logo1.png') }}" alt="" width=100></div>
                    <li class="dropdown"><a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button"  aria-haspopup="true" aria-expanded="false">集团业务管理<span class="caret"></span></a>
                        <ul class="dropdown-menu">
                            <li><a href="#">人员信息管理</a></li>
                            <li><a href="#">需求和事件管理</a></li>
                            <li><a href="#">运维监控平台</a></li>
                            <li><a href="#">运维管理</a></li>                            
                        </ul>
                    </li>
                    <li class="dropdown"><a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button"  aria-haspopup="true" aria-expanded="false">子公司业务管理<span class="caret"></span></a>
                        <ul class="dropdown-menu">
                            <li><a href="#">XX基金</a></li>
                            <li><a href="#">XX国际</a></li>
                            <li><a href="#">XX国际</a></li>
                            <li><a href="#">XX资产</a></li>
                        </ul>
                    </li>
                    <li><a href="#">帮助</a></li>
                </ul>
                <form class="navbar-form navbar-right">
                    <div class="form-group">
                    <input type="text" class="form-control" placeholder="功能快速跳转">
                    <button type="submit" class="btn btn-primary">提交</button>&nbsp;&nbsp; 
                    </div>
                </form>
        </nav>
    {% endblock %}
    
 
    {% block content %}
    <div class="container" font-size="small">
        <div class="row">
            <div class="col-md-2">
                {% block page_left_nav %}{% endblock %}
            </div>
            <div class="col-md-9 offset1">
                {% block page_content %}{% endblock %}
            </div>
        </div>
    </div>
    {% endblock %}
</div>
```
### 数据页面
```html
{% extends "base.html" %}
{% block title %}首页{% endblock %}
<!--页面内容区域-->
{% block page_content %}
<button type="button" class="btn btn-primary">业务报表</button>
<button type="button" class="btn btn-success">财务报表</button>
<button type="button" class="btn btn-info">风险报表</button>
<button type="button" class="btn btn-warning">经营报表</button>
<div class="btn-group">
    <button type="button" class="btn btn-danger dropdown-toggle" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">监管报表
        <span class="caret"></span><span class="sr-only">Toggle Dropdown</span>
    </button>
    <ul class="dropdown-menu">
        <li><a href="#">备付金电子台账</a></li>
        <li><a href="#">网点资金调拨表</a></li>
        <li></li>
    </ul>
</div>
<h2 align=center>2018年备付金电子台账（一）</h2><br>
<table class="table table-striped table-bordered table-hover" font-size="10pt">
    <tr align=center><strong><td>日期</td><td>交易性质</td><td>交易时间</td><td>币种</td><td>金额</td><td>存入或提钞账户</td><td>备注</td><td>操作</td></strong></tr>
    {% for row in list %}
    <tr>
        <td align="center"><small>{{ row[0] }}</small></td>
        <td align="center"><small>{{ row[1] }}</small></td>
        <td align="center"><small>{{ row[2] }}</small></td>
        <td align="center"><small>{{ row[3] }}</small></td>
        <td align="right"><small>{{ row[4] }}</small></td>
        <td align="center"><small>{{ row[5] }}</small></td>
        <td align="center"><small>{{ row[6] }}</small></td>
        <td align=center><button type="button" class="btn btn-primary btn-xs">查看</button></td>
    </tr>
    {% endfor %}
</table>
{% endblock %}
