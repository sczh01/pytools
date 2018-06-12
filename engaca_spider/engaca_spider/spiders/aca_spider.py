#!python
#coding: utf-8

import scrapy
from scrapy.spiders import Spider
from scrapy.selector import Selector   
from scrapy.crawler import CrawlerProcess

import re
from engaca_spider.settings import starturl
from engaca_spider.items import  EngacaSpiderItem
from pprint import pprint
import json
import urllib
from urlparse import urljoin  
import jieba 

pro_list =[ i.strip().decode('utf-8')  for i in  open("pro_list.txt").readlines()]

class EngAcaSpider(Spider):
    '''
    '''
    name = "EngAca"
 
    #需要处理的http状态
    handle_httpstatus_list = [404,403]

    def start_requests(self):
        '''
        '''
        yield scrapy.Request(starturl,self.getnames)
        
    def getnames(self,response):
        '''
        '''
        if response.status == 403:
            print 'meet 403, sleep 600 seconds'
            import time
            time.sleep(600)
            yield scrapy.Request(response.url, callback=self.getnames)
        #404，页面不存在，直接返回即可
        elif response.status == 404:
            print 'meet 404, return'
        #正常处理
        else:
            print "second:",response.url
            self.logger.info('a response from %s',response.url)

            names_li=response.selector.xpath('//li[@class="name_list"]/a')
            for name_li in names_li:
                '''
                '''
                items=EngacaSpiderItem()
                items['name']=name_li.xpath("./text()").extract_first()  #unicode
                urlhref=name_li.xpath('./@href').extract_first()
                newurl=urljoin(response.url,urlhref)
                yield scrapy.Request(newurl,callback=self.getplaces,meta={'items':items})

    def getplaces(self,response):
        '''
        '''
        items = response.meta['items']

        # get first content;
        #  中英文 混用 .encode('gbk','ignore')  忽略英文空格
        ptext=response.selector.xpath('//div[@class="intro"]/p[1]/text()').extract_first()
        content=ptext.split(u'。')[1]        
        seg_list = jieba.cut(content)
        for place in seg_list:
            place=place.replace(u"省",'')
            place=place.replace(u"市",'')
            print "place:",place
            if place in pro_list:
                items['place']=place
                break
        else:
            items['place']='None'
        pprint(items)
 
        # for p in pro_list:
        #     print p,
        # raise "check place"
        yield items


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

process.crawl(EngAcaSpider)
process.start() # the script will block here until the crawling is finished