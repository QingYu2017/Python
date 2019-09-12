```shell
Auth:Qing.Yu
Mail:1753330141@qq.com
 Ver:V1.0
Date:2019-09-12
```

### 摘要说明
网页资料，特别是PPT转图片并以公众号新闻方式分享的内容，难以长期保存和分类管理。  
使用爬虫，可以方便归集这些资料，必要的话，还能完成自动合并为PDF并转发邮件、存入指定目录、提交SVN等连续处理操作。  
复杂、长期的资料收集整理，可以使用Srapy统一处理，相对简单的情况下，使用轻量的requests和bs4库处理即可。  

微信内容示例  
![示例](https://github.com/QingYu2017/pic/blob/master/20190912111206.png)

### 处理流程
1. 准备：Windows/Linux，安装Python（推荐3.5+），使用pip安装requests、bs4库；
1. 使用bs4库解析页面内容，对解析出的图片链接；
1. 图片逐一下载，并顺序编号；

按文章标题分目录保存
![示例](https://github.com/QingYu2017/pic/blob/master/20190912111114.png)

目录中按先后顺序依次编号
![示例](https://github.com/QingYu2017/pic/blob/master/20190912111134.png)

### 参考资料
- 杨佩璐, 宋强. Python宝典[M]. 电子工业出版社, 2014.
- 佚名. Beautiful Soup 4.4.0 文档[EB／OL]. 2018. 

### 代码参考
```python
import os,sys,re,requests as r
from bs4 import BeautifulSoup as bs

#导入准备处理的文章链接
urls=[
'https://mp.weixin.qq.com/s?__biz=MzA5NDI5MDQwMg==&mid=502109991&idx=1&sn=10d566e855f099032411d5d7e619ac51&chksm=0849dfaa3f3e56bc24a0c6ece4be9ad03f33ef2ef5223c22fc3931202819a6ae67a0316752e5&mpshare=1&scene=1&srcid=0820ozQ64P3RmMk2Z2zwxQwg&sharer_sharetime=1568250006207&sharer_shareid=5db206eeaa12cdede20ef4815bcee5c8&key=60e020777f8f338a2d2595041876e9696475a52ac0bea755eba61bef4dda9cd1324eef08c99cb34486c61716c9da1b2600e081c0b54df4d5f4a27c8bb5fa524ee7bdaff53eba21aafc0d690f953aaf85&ascene=1&uin=MTY3OTYxNTkwMw%3D%3D&devicetype=Windows+10&version=62060844&lang=zh_CN&pass_ticket=MQNQ9VH4isixDqwvzYl7F1UC6c%2B6oseV1XOzl6guS30u%2B766nh31R6ZYivL7Zy0n',
'https://mp.weixin.qq.com/s?__biz=MzA5NDI5MDQwMg==&mid=502110139&idx=1&sn=a0f5631d8a5ae0ca6209f809dfcecc78&chksm=0849df363f3e562093594e889e962f6222d6de54c61a11d8a0e678c3877b299330e9a18329f4&mpshare=1&scene=1&srcid=0820HF7SUcmwiL8MRWqVH6Qu&sharer_sharetime=1568250017719&sharer_shareid=5db206eeaa12cdede20ef4815bcee5c8&key=2d030d495be8f43e3d321f5e190f5918d401309618b8533a93f3012adebc6976eebc752bcd4604c3124e833f9f44244f1fda3463257795d7036841f82569f005b2a305158629a7be53c7e3f2cc668e25&ascene=1&uin=MTY3OTYxNTkwMw%3D%3D&devicetype=Windows+10&version=62060844&lang=zh_CN&pass_ticket=MQNQ9VH4isixDqwvzYl7F1UC6c%2B6oseV1XOzl6guS30u%2B766nh31R6ZYivL7Zy0n',
'https://mp.weixin.qq.com/s?__biz=MzA5NDI5MDQwMg==&mid=502110147&idx=1&sn=affad451b71afa9798e7dcf1cc92edda&chksm=0849df4e3f3e56580cfe3e2eec20f33bacfcd230366a821ab197caae88e59dddc72207d1aeea&mpshare=1&scene=1&srcid=08208iLrVIvLtkqI8BOfNEdE&sharer_sharetime=1568250024723&sharer_shareid=5db206eeaa12cdede20ef4815bcee5c8&key=60e020777f8f338ad9e05de4e1cabe6056122ba6933e26878d74463f44c52a8eb121a57a14dcc27fb995517b515f1b3cff1e71435bb3e9c43460b362b795d445eb5dd57fe6040828670d245f7ee3c8bb&ascene=1&uin=MTY3OTYxNTkwMw%3D%3D&devicetype=Windows+10&version=62060844&lang=zh_CN&pass_ticket=MQNQ9VH4isixDqwvzYl7F1UC6c%2B6oseV1XOzl6guS30u%2B766nh31R6ZYivL7Zy0n',
'https://mp.weixin.qq.com/s?__biz=MzA5NDI5MDQwMg==&mid=502110148&idx=1&sn=0b06755ae98a16ec96f4af62a50e69b0&chksm=0849df493f3e565f970abb7f856cec02a67a34765a3fe834ecd96e548de2a0bfe77374518ec1&mpshare=1&scene=1&srcid=0820nSGaVJchNzkEgOVVU60g&sharer_sharetime=1568250032154&sharer_shareid=5db206eeaa12cdede20ef4815bcee5c8&key=60e020777f8f338a997eaf846e2c2d1078d95cfbe36fc54434b13d634bfa431f5bf3cb74c0a3feb7eafb48a82d03e7e3f17c9647ae6ba15d8c693e9c9850bd30c7af321e3eca06787d65cfcbd0bf0390&ascene=1&uin=MTY3OTYxNTkwMw%3D%3D&devicetype=Windows+10&version=62060844&lang=zh_CN&pass_ticket=MQNQ9VH4isixDqwvzYl7F1UC6c%2B6oseV1XOzl6guS30u%2B766nh31R6ZYivL7Zy0n',
'https://mp.weixin.qq.com/s?__biz=MzA5NDI5MDQwMg==&mid=502110142&idx=1&sn=d8b7298a87f951081667704d2dbec407&chksm=0849df333f3e5625771a674cfa4b35c53b7b4b6111ee37290eadb5b42f643b8b04c5de70603a&mpshare=1&scene=1&srcid=0820yAkFcrMLXgKngXzlQFop&sharer_sharetime=1568250039336&sharer_shareid=5db206eeaa12cdede20ef4815bcee5c8&key=60e020777f8f338aec30767e5d6c43ce6606d8ad362f7e80c392537dd9ca1993922dd5edb487806135d2d79806989d6f5d352d07bb309fc91320e88990d5d28101c132b8385c9454892abb6657ce96cf&ascene=1&uin=MTY3OTYxNTkwMw%3D%3D&devicetype=Windows+10&version=62060844&lang=zh_CN&pass_ticket=MQNQ9VH4isixDqwvzYl7F1UC6c%2B6oseV1XOzl6guS30u%2B766nh31R6ZYivL7Zy0n',
'https://mp.weixin.qq.com/s?__biz=MzA5NDI5MDQwMg==&mid=502110461&idx=1&sn=d17879cd732de69146f084e95a0ebfa4&chksm=0849d0703f3e5966df096cafd800a9873896070d03fa86373b704e993d51fdd2b01980344c7b&mpshare=1&scene=1&srcid=0820yyDvLMmKnsh0g00hhRq7&sharer_sharetime=1568250054487&sharer_shareid=5db206eeaa12cdede20ef4815bcee5c8&key=a8dbb24e2b14083a00fc795b7f5731d861ef2fd691e84aed5ee33ac60cadc5047248a32634e29c0cf28f748326221272b0ca9c3e7a7d2fc76759a4500e71c20a77f9d10afd123dbb94d916ea0163c0bc&ascene=1&uin=MTY3OTYxNTkwMw%3D%3D&devicetype=Windows+10&version=62060844&lang=zh_CN&pass_ticket=MQNQ9VH4isixDqwvzYl7F1UC6c%2B6oseV1XOzl6guS30u%2B766nh31R6ZYivL7Zy0n',
'https://mp.weixin.qq.com/s?__biz=MzA5NDI5MDQwMg==&mid=502110136&idx=1&sn=64ab1e76de1eb83950adab0503ac0404&chksm=0849df353f3e5623a18c6db29efb835b9da05b31d8fd4488cef1347f3d272a5cb84db8106dd3&mpshare=1&scene=1&srcid=0820p94Sz34hcPIJ7L2Ibt5I&sharer_sharetime=1568250072021&sharer_shareid=5db206eeaa12cdede20ef4815bcee5c8&key=2d030d495be8f43ef05906083fc1e73c9f52733e7cb79845017efe94d672e1e36bb7abe8baee123f6fbc5f1933d4479548f82f06db90a946352ee2437046fdb1e64a86ac8543254c54d758c69dcae952&ascene=1&uin=MTY3OTYxNTkwMw%3D%3D&devicetype=Windows+10&version=62060844&lang=zh_CN&pass_ticket=MQNQ9VH4isixDqwvzYl7F1UC6c%2B6oseV1XOzl6guS30u%2B766nh31R6ZYivL7Zy0n',
'https://mp.weixin.qq.com/s?__biz=MzA5NDI5MDQwMg==&mid=502110309&idx=1&sn=4fcde3d8f0a22dcf5ef7ffe7fedae6d2&chksm=0849d0e83f3e59fe036a181eff8899316f0f6d6395e814df5847672592d5813970eb7ce28548&mpshare=1&scene=1&srcid=0820qnyyHjKQ6Tyy3LKvSuAd&sharer_sharetime=1568250065188&sharer_shareid=5db206eeaa12cdede20ef4815bcee5c8&key=60e020777f8f338a12d01a391d1e86612e8fbb703d3835fbe56773b8c68a4b394d12884e74cd546334910fae0ed285286318fcb946fdde98050823ce9ad4d8b0f4efc51806114a7f09657bc82883b952&ascene=1&uin=MTY3OTYxNTkwMw%3D%3D&devicetype=Windows+10&version=62060844&lang=zh_CN&pass_ticket=MQNQ9VH4isixDqwvzYl7F1UC6c%2B6oseV1XOzl6guS30u%2B766nh31R6ZYivL7Zy0n',
]

#按照定义的文件名、链接、保存路径处理图片
def getImage(save_name,url,des_folder):
    src_f=r.get(url).content
    #des_f=url.split('/')[len(url.split('/'))-1]
    print(des_folder)
    print(save_name)
    if(not os.path.exists(des_folder)):
        os.mkdir(des_folder)
    with open(r'%s\%s'%(des_folder,save_name),'wb') as f:
        f.write(src_f)
        #print('Write %s complete'%save_name)

#解析文章，处理其中的图片
for url in urls:
    p=r.get(url)
    title = bs(p.content,'html.parser').find('h2',attrs={'class':'rich_media_title'})
    title = title.get_text().strip().replace(' ','').replace('|','-')
    pics = bs(p.content,'html.parser').find('div',attrs={'class':'rich_media_content'}).find_all('img')
    for i in range(len(pics)):
        getImage('%s.jpg'%('%05d'%(i+1)),pics[i].get('data-src'),title)
```
