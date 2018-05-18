# -*- coding: utf-8 -*-

# Scrapy settings for consumer project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'consumer'

SPIDER_MODULES = ['consumer.spiders']
NEWSPIDER_MODULE = 'consumer.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'consumer (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'consumer.middlewares.ConsumerSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   'consumer.middlewares.ConsumerDownloaderMiddleware': 543,
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
EXTENSIONS = {
    # 'scrapy.extensions.telnet.TelnetConsole': None,
    'consumer.patcher.NewspaperPatcher': 500,
    'consumer.scheduler_index.MakeSaveRequest': None,
}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'consumer.pipelines.ConsumerPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# 指定使用scrapy-redis的Scheduler
SCHEDULER = "scrapy_redis.scheduler.Scheduler"

# 在redis中保持scrapy-redis用到的各个队列，从而允许暂停和暂停后恢复
SCHEDULER_PERSIST = True

# 指定排序爬取地址时使用的队列，默认是按照优先级排序
# SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.SpiderPriorityQueue'
SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.FifoQueue'

DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"

ITEM_PIPELINES = {
    'consumer.pipelines.MongoPipeline': 400
    # 'scrapy_redis.pipelines.RedisPipeline': 400
}

# 序列化项目管道作为redis Key存储
REDIS_ITEMS_KEY = '%(spider)s:items'

# 指定用于连接redis的URL（可选）
# 如果设置此项，则此项优先级高于设置的REDIS_HOST 和 REDIS_PORT
# REDIS_URL = 'redis://127.0.0.1:6380'
REDIS_HOST = '127.0.0.1'
REDIS_PORT = '6380'

DEPTH_LIMIT = 5

# MONGODB 主机名
MONGODB_HOST = "127.0.0.1"
# MONGODB 端口号
MONGODB_PORT = 32679
# 数据库名称
MONGODB_DBNAME = "Extract_News"
# 存放数据的表名称
MONGODB_SHEETNAME = "Item"


CONCURRENT_REQUESTS = 100
