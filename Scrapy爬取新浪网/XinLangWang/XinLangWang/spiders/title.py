import scrapy
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
# from urllib.request import urlopen
from scrapy.http import Request
# from hello.items import ZhaopinItem
# from scrapy.spiders import CrawlSpider, Rule
# from scrapy.linkextractors import LinkExtractor
from urllib.request import urlopen
#from urllib.request import Request
from bs4 import BeautifulSoup
from lxml import etree
from bson.objectid import ObjectId
import pymongo
client = pymongo.MongoClient(host="127.0.0.1")
db = client.XinLangWang            #库名dianping
collection = db.title

import redis
r = redis.Redis(host='127.0.0.1', port=6379, db=0)


class qidianClassSpider(scrapy.Spider):
    name = "title"
    allowed_domains = ["sina.com.cn"]  # 允许访问的域
    start_urls = [
        "http://www.sina.com.cn/",
    ]

    # #每爬完一个网页会回调parse方法
    # def parse(self, response):
    #     print(response.body.decode('utf-8'))
    def parse(self, response):
        ii=0
        hxs = HtmlXPathSelector(response)
        hxsObj = hxs.select('//div[@class="main-nav"]/div/ul/li/a')
        for secItem in hxsObj:
            titleName = secItem.select('text()').extract()
            titleUrl = secItem.select('@href').extract()
            if titleName ==[] or titleName==['更多']:
                pass
            else:
                print('===================')
                print(titleName[0])
                print(titleUrl[0])
                print("======================")
                ii+=1
                classid = collection.insert({'titlename': titleName[0], 'pid': None})
                urls = '%s,%s,%s' % (classid,titleUrl[0],ii)
                r.lpush('titleUrl', urls)

