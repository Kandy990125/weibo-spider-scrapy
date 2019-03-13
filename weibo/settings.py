# coding=utf-8

BOT_NAME = 'weibo'

SPIDER_MODULES = ['weibo.spiders']
NEWSPIDER_MODULE = 'weibo.spiders'

# USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.54 Safari/536.5'
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.170 Safari/537.36'
'''
#把数据存到路径中的CSV文件中去
FEED_URI = u'file:///G:/MovieData/followinfo.csv'
FEED_FORMAT = 'CSV'
'''

#DOWNLOADER_MIDDLEWARES = {
    #"weibo.middleware.UserAgentMiddleware": 401,
 #   "weibo.middleware.CookiesMiddleware": 402,
#}
DOWNLOADER_MIDDLEWARES = {
#    'cnblogs.middlewares.MyCustomDownloaderMiddleware': 543,
    'weibo.middleware.RandomUserAgent': 1,
    'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 110,
    #'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
    # 'weibo.middleware.ProxyMiddleware': 100,
}

ITEM_PIPELINES = {
    #'weather2.pipelines.Weather2Pipeline': 300,
    'weibo.pipelines.MySQLStorePipeline': 300,
}


DOWNLOAD_DELAY =0.1   # 下载器间隔时间