# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

from scrapy.item import Item, Field


class Offer51Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    #学校名称
    title = scrapy.Field()
    #链接
#    school_url = scrapy.Field()
    #雅思分数
#    IELTS_grade = scrapy.Field()
    #热门专业
#    hotmajor = scrapy.Field()
    #国内排名
#    Timerank = scrapy.Field()
    #世界排名
#    QSrank = scrapy.Field()
    
    enmajorname = scrapy.Field()
    
    cnmajorname = scrapy.Field()
        
    degreetype = scrapy.Field()
    
    englishtitle = scrapy.Field()
    
    officalurl = scrapy.Field()
    
    majortype = scrapy.Field()
#    weburl = scrapy.Field()
    #学校logo图片地址
#    school_logo = scrapy.Field()
    #图片
#    logoimage= scrapy.Field()
    pass