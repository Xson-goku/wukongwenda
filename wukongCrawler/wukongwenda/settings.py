#-*- coding: utf-8 -*-

import time

# Scrapy settings for wukongwenda project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'wukongwenda'

SPIDER_MODULES = ['wukongwenda.spiders']
NEWSPIDER_MODULE = 'wukongwenda.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'wukongwenda (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 48

LOG_LEVEL = 'DEBUG'

RETRY_HTTP_CODES = [500, 502, 503, 504, 400, 401, 403, 404, 406, 408, 429]

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 1.5
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
  'Accept-Language': 'en',
}

RANDOM_UA_TYPE = 'random'

EXTENSIONS = {}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'wukongwenda.middlewares.WukongwendaSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
	'srapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
	'wukongwenda.middlewares.RandomUserAgentMiddleware': 400,
	'scrapy.downloadermiddlewares.retry.RetryMiddleware': 90,
}
	# 'wukongwenda.middlewares.RandomProxy': 100,
	# 'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'wukongwenda.pipelines.MongoPipeline': 300,
}

LOG_FILE = 'wukongwenda/spider_log.log'#.format(int(time.time()))

MONGO_URL = 'mongodb://139.129.222.132:27017'
MONGO_DB = 'wukongwenda'
MONGO_COLLECTION = 'wukong_detail'

REDIS_HOST = ''
REDIS_PORT = 6379
REDIS_DB = 0
REDIS_PASSWORD = ''




