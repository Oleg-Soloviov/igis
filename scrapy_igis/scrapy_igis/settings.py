BOT_NAME = 'scrapy_igis'

SPIDER_MODULES = ['scrapy_igis.spiders']
NEWSPIDER_MODULE = 'scrapy_igis.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'scrapy_igis (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'scrapy_igis.middlewares.ScrapyIgisSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'scrapy_igis.middlewares.MyCustomDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'scrapy_igis.pipelines.ScrapyIgisPipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True
# The initial download delay
AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# added by me
ITEM_PIPELINES = {'scrapy.pipelines.images.ImagesPipeline': 1}

IMAGES_STORE = '/home/oleg/PycharmProjects/igis/myproject/media/igis_udm'

MY_START_URLS = ['http://igis.ru/online?tip=9&city=%D0%90%D0%BB%D0%BD%D0%B0%D1%88%D0%B8', 'http://igis.ru/online?tip=9&city=%D0%91%D0%B0%D0%BB%D0%B5%D0%B7%D0%B8%D0%BD%D0%BE', 'http://igis.ru/online?tip=9&city=%D0%92%D0%B0%D0%B2%D0%BE%D0%B6', 'http://igis.ru/online?tip=9&city=%D0%92%D0%BE%D1%82%D0%BA%D0%B8%D0%BD%D1%81%D0%BA', 'http://igis.ru/online?tip=9&city=%D0%92%D0%BE%D1%82%D0%BA%D0%B8%D0%BD%D1%81%D0%BA%D0%B8%D0%B9+%D1%80%D0%B0%D0%B9%D0%BE%D0%BD', 'http://igis.ru/online?tip=9&city=%D0%93%D0%BB%D0%B0%D0%B7%D0%BE%D0%B2', 'http://igis.ru/online?tip=9&city=%D0%93%D1%80%D0%B0%D1%85%D0%BE%D0%B2%D0%BE', 'http://igis.ru/online?tip=9&city=%D0%94%D0%B5%D0%B1%D1%91%D1%81%D1%8B', 'http://igis.ru/online?tip=9&city=%D0%97%D0%B0%D0%B2%D1%8C%D1%8F%D0%BB%D0%BE%D0%B2%D0%BE', 'http://igis.ru/online?tip=9&city=%D0%98%D0%B3%D1%80%D0%B0', 'http://igis.ru/online?tip=9&city=%D0%9A%D0%B0%D0%BC%D0%B1%D0%B0%D1%80%D0%BA%D0%B0', 'http://igis.ru/online?tip=9&city=%D0%9A%D0%B0%D1%80%D0%B0%D0%BA%D1%83%D0%BB%D0%B8%D0%BD%D0%BE', 'http://igis.ru/online?tip=9&city=%D0%9A%D0%B5%D0%B7', 'http://igis.ru/online?tip=9&city=%D0%9A%D0%B8%D0%B7%D0%BD%D0%B5%D1%80', 'http://igis.ru/online?tip=9&city=%D0%9A%D0%B8%D1%8F%D1%81%D0%BE%D0%B2%D0%BE', 'http://igis.ru/online?tip=9&city=%D0%9A%D1%80%D0%B0%D1%81%D0%BD%D0%BE%D0%B3%D0%BE%D1%80%D1%81%D0%BA%D0%B8%D0%B9+%D1%80%D0%B0%D0%B9%D0%BE%D0%BD', 'http://igis.ru/online?tip=9&city=%D0%9C%D0%B0%D0%BB%D0%B0%D1%8F+%D0%9F%D1%83%D1%80%D0%B3%D0%B0', 'http://igis.ru/online?tip=9&city=%D0%9C%D0%BE%D0%B6%D0%B3%D0%B0', 'http://igis.ru/online?tip=9&city=%D0%9D%D1%8B%D0%BB%D0%B3%D0%B0', 'http://igis.ru/online?tip=9&city=%D0%A1%D0%B0%D1%80%D0%B0%D0%BF%D1%83%D0%BB', 'http://igis.ru/online?tip=9&city=%D0%A1%D0%B5%D0%BB%D1%82%D1%8B', 'http://igis.ru/online?tip=9&city=%D0%A1%D0%B8%D0%B3%D0%B0%D0%B5%D0%B2%D0%BE', 'http://igis.ru/online?tip=9&city=%D0%A1%D1%8E%D0%BC%D1%81%D0%B8', 'http://igis.ru/online?tip=9&city=%D0%A3%D0%B2%D0%B0', 'http://igis.ru/online?tip=9&city=%D0%A8%D0%B0%D1%80%D0%BA%D0%B0%D0%BD', 'http://igis.ru/online?tip=9&city=%D0%AE%D0%BA%D0%B0%D0%BC%D0%B5%D0%BD%D1%81%D0%BA%D0%BE%D0%B5', 'http://igis.ru/online?tip=9&city=%D0%AF%D0%BA%D1%88%D1%83%D1%80-%D0%91%D0%BE%D0%B4%D1%8C%D1%8F', 'http://igis.ru/online?tip=9&city=%D0%AF%D1%80']

import logging
FORMAT = '[%(filename)s:%(lineno)s] - %(levelname)s - %(message)s: %(asctime)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel('DEBUG')

fh = logging.FileHandler('log.txt')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(filename)s:%(lineno)s] - %(levelname)s - %(message)s: %(asctime)s')
fh.setFormatter(formatter)
logger.addHandler(fh)