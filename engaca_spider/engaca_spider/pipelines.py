# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class EngacaSpiderPipeline(object):
    def process_item(self, item, spider):
        return item



# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pprint import pprint
import codecs

class ShopinfoPipeline(object):
    def process_item(self, item, spider):
        return item



class JsonWithEncodingPipeline(object):
    '''保存到文件中对应的class
       1、在settings.py文件中配置
       2、在自己实现的爬虫类中yield item,会自动执行'''    
    def __init__(self):            
        
        self.file = codecs.open('result.txt', 'w', encoding='utf-8')  #保存为json文件
        line="name  place\n"

        self.file.write(line)#写入文件中
    def process_item(self, item, spider):
        '''
        '''
        keylist=['name','place']
        baseline=""
        for i in keylist:
            baseline+=item[i]+' '
        baseline+="\n"
        pprint(baseline)
        self.file.write(baseline)#写入文件中
    
    def spider_closed(self, spider):#爬虫结束时关闭文件
        self.file.close()