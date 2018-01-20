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
import requests
from lxml import etree
from bson.objectid import ObjectId
# import pymongo
# client = pymongo.MongoClient(host="127.0.0.1")
# db = client.XinLangWang            #库名dianping
# collection = db.title
import  os
# import redis
# r = redis.Redis(host='127.0.0.1', port=6379, db=0)
import pandas

class qidianClassSpider(scrapy.Spider):
    name = "news"
    allowed_domains = ["sina.com.cn"]  # 允许访问的域
    start_urls = [
        "http://news.sina.com.cn/china/",
    ]

    # #每爬完一个网页会回调parse方法
    # def parse(self, response):
    #     print(response.body.decode('utf-8'))
    def parse(self, response):
        ii=0
        hxs = HtmlXPathSelector(response)
        hxsObj = hxs.select('//div[@ class="news-item  "]/h2/a')
        for secItem in hxsObj:
            titleName = secItem.select('text()').extract()
            titleUrl = secItem.select('@href').extract()
            print(titleName[0])
            print(titleUrl[0])
            request = Request(titleUrl[0], callback=lambda response: self.parse_subClass(response))
            yield request
            print("======================")
    def parse_subClass(self, response):
#--------------------------------------------------------------------------------------------------------------
        #hxs = HtmlXPathSelector(response)
        #hxsObj = hxs.select('//div[@class="page-content clearfix"]/div[@class="left"]/div[@class="article article_16"]/p')
        # for secItem in hxsObj:
        #     Content = secItem.select('text()').extract()
        #     ii = Content[0] + ii
        #     print(ii)
#----------------------------------------------------------------------------------------------------------------
        # html = response.body.decode('utf-8')
        # selector = etree.HTML(html)
        # dic = {}
        # dic['title'] = selector.xpath('//div[@class="page-header"]/h1[@id="artibodyTitle"]/text()')
        # dic['content']= selector.xpath('//div[@class="article article_16"]/p/text()')
        # dic['source']= selector.xpath('//span[@class="time-source" ]/text()')
        # dic['keyword'] = selector.xpath('//div[@class="article-keywords"]/a/text()')
#----------------------------------------------------------------------------------------------------------------
        html = response.body.decode('utf-8')
        html = str(html)
        soup=BeautifulSoup(html,"html.parser")
        dic = {}
        dic['title'] = soup.select('#artibodyTitle')[0].text
        dic['content'] = ''.join(soup.select('#artibody')[0].text.split())
        dic['source'] = soup.select('#navtimeSource')[0].text
        dic['keyword'] = soup.select('.article-keywords')[0].text
        print('------------------------')
        print(dic['title'])
        print(dic['content'])
        print(dic['source'])
        print(dic['keyword'])

        # return dic

