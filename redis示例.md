```python
# -*- coding: utf-8 -*-
#/root/Envs/v36/bin

import redis,requests

class obj_request():
    def __init__(self):
        self.url_id = 'baidu_sample'        #缺省url标识
        self.url='https://www.baidu.com'    #缺省url地址 
        self.headers={
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
            "Connection":"keep-alive",
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language":"zh-CN,zh;q=0.8"
            }                               #缺省包含浏览器信息的请求header，避免被反爬虫拦截
        self.redis_host = 'xx.xxx.xx.xxx'   #缺省redis服务器地址
        self.redis_port = 6379              #缺省redis端口
        self.redis_db = 0                   #缺省redis数据库

    def getPageContent(self):
        req = requests.get(
            self.url,
            headers = self.headers,
            )                               #通过requests发起访问请求
        self.obj_pagetContent = req.content #返回的页面内容写入对象的obj_pagecontent
    
    def push2redis(self):
        self.obj_redis = redis.StrictRedis(
            host = self.redis_host, 
            port = self.redis_port, 
            db = self.redis_db,
            )                               #创建redis连接
        self.obj_redis.hset(
            self.url_id,
            'url',self.url,
            )                               #存入url信息
        self.obj_redis.hset(
            self.url_id,'html',
            self.obj_pagetContent,
            )                               #存入页面内容
    
if __name__ == '__main__':                  #用例测试
    gold = url_requests()
    gold.url_id = 'GoldPrice'
    gold.url='http://www.sge.com.cn/sjzx/yshqbg'    
    gold.getPageContent()
    gold.push2redis()
    print(gold.obj_redis.hget('baidu_sample','url'))

```
