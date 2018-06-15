# python_2018-3
创新实践2018年三月份

创新实践3

ifeng：基于scrapy-redis的凤凰网爬虫

consumer：负责爬虫组整个项目中的slave节点的整体逻辑和结构

entry：对新浪所有url获取的尝试


consumer
├── consumer
│   ├── general_redis.py	# 编写的一些Redis的增删改查操作。
│   ├── items.py	# 保存新闻id、URL、标题、发布时间、正文。
│   ├── middlewares.py	#下载中间件的保存位置。
│   ├── patcher.py	#newspaper的猴子补丁，编写成Scrapy Extensions 在 engine启动时进行补丁。
│   ├── pipelines.py	#mongopipeline，保存item和手动过滤垃圾页面
│   ├── scheduler_index.py		#每隔大约一小时将列表页、索引页再调度进requests队列，以Scrapy Extensions实现。
│   ├── settings.py	#Scrapy设置。
│   └── spiders
│       ├── consumer.py	# 解析部分，基本由谢毅鑫完成，我只负责逻辑结构，故不进行阐述。
│       └── downloadhtml.py	#简单下载html页面，爬取作为后期机器学习的训练集爬虫。
├── main.py
└── scrapy.cfg


ifeng
├── ifeng
│   ├── items.py  #保存新闻id、URL、标题、日期、时间、来源、正文。
│   ├── middlewares.py #本项目未使用。
│   ├── pipelines.py	#利用Scrapy-redis pipeline故没有编写。
│   ├── settings.py	#Scrapy设置上文件。
│   └── spiders	#爬虫文件夹。
│       └── news_spider.py	#凤凰网爬虫，解析内容。
├── main.py	#手动编写的爬虫运行入口，易于pycharm调试。
└── scrapy.cfg
