# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import HtmlXPathSelector
# from scrapy.http import Request
# from urllib.request import urlopen
from scrapy.http import Request
# from hello.items import ZhaopinItem
# from scrapy.spiders import CrawlSpider, Rule
from time import sleep
# from scrapy.linkextractors import LinkExtractor

import pymongo

client = pymongo.MongoClient(host="127.0.0.1")
db = client.novel  # 库名dianping
collection = db.novelname

import redis  # 导入redis数据库

r = redis.Redis(host='127.0.0.1', port=6379, db=0)

ii = 0


class qidianNovelSpider(scrapy.Spider):
    name = "title2"
    allowed_domains = ["sina.com.cn"]  # 允许访问的域

    def __init__(self):
        # global pid
        # 查询reids库novelurl
        # qidianNovelSpider.start_urls=["https://www.qidian.com/all",]
        start_urls = []
        urlList = r.lrange('titleUrl', 0, -1)
        ii = 0
        self.dict = {}
        for item in urlList:
            itemStr = str(item, encoding="utf-8")
            arr = itemStr.split(',')
            classid = arr[0]
            url= arr[1]
            print(url)
            flag = arr[2]
            start_urls.append(url)
            self.dict[url] = {"classid": classid, "flag": flag}
           #self.dict[url] = {"classid": classid, "pid": pid, "num": 0}

        #print(start_urls)
        self.start_urls = start_urls

    def parse(self, response):
        classInfo = self.dict[response.url]
        #objectid = classInfo['classid']
        flag = classInfo['flag']
        hxs = HtmlXPathSelector(response)
        if flag == 1:
            hxsObj = hxs.select('//ul[@class="nav udv-clearfix"]/li/a')
            for secItem in hxsObj:
                className = secItem.select('text()').extract()
                classUrl = secItem.select('@href').extract()
                print(className[0])
                print(classUrl[0])
        else:
            pass


