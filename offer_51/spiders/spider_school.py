# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy.http import Request
from django.http import response
from scrapy import item
from twisted.python.compat import items
from offer_51.items import Offer51Item
import csv
import sys
import urllib
import json
from selenium import webdriver
import cgi


class Spider_51(scrapy.Spider):
 
    name = "51spider"
    allowed_domains = ["51offer.com"]
    start_urls = ['https://www.51offer.com/']
    
    def parse(self, response):
        for page in range(1,2):
#            baseurl = 'https://www.51offer.com/school/uk-all-' 英国院校
#            baseurl = 'https://www.51offer.com/school/us-all-' 美国院校
#            baseurl = 'https://www.51offer.com/school/au-all-' 澳洲院校
            baseurl = 'https://www.51offer.com/school/sg-all-'
            listurl = baseurl + str(page)+ '.html?rankType=this_times'
#            print listurl
            yield Request(url=listurl,callback=self.parse_page,dont_filter=True)
        
             
    def parse_page(self,response):
        
        
        url = response.xpath("//li[@class='clearfix']/a/@href").extract()
#        print url
        for school_url in url:
#            print school_url
#            string_s = s.encode("utf-8")
          
            yield Request(url=school_url,callback=self.parse_detail,dont_filter=True)
            
            
    def parse_detail(self,response):
        
        url = response.url
               
        url1 =  url[31:]
        
        majorlisturl = 'https://www.51offer.com/school/specialty_'+ url1 + '?a=1'+'&pageNo=1' 
                            
        titlelist = response.xpath("//h1[@class='cname']/text()").extract()
        title =  titlelist[0].strip()

        hotmajorlist = response.xpath("//div[@class='rr']/text()").extract()
        
        if hotmajorlist:
             
            hotmajor = hotmajorlist[0].strip()
        else:
            hotmajor =''
        
       
#        IELTS_gradelist = response.xpath("//*[@id='school-introduction']/div[2]/div[1]/div/text()").extract()
        IELTS_gradelist = response.xpath("//*[@class='intro-lists']/div[2]/div[1]/text()").extract()
        if IELTS_gradelist:
            IELTS_grade = IELTS_gradelist[1].strip()
        else:
            IELTS_grade = ''
            
       
        QSranklist = response.xpath("//div[@class='rank-list']/div[2]/div[1]/text()").extract()
        if QSranklist:
            
    
            QSrank = QSranklist[0]
        else:
            QSrank = ''    
       
        
        Timeranklist = response.xpath("//div[@class='rank-list']/div[1]/div[1]/text()").extract()
        if Timeranklist:
            Timerank = Timeranklist[0]
            
        else:
            Timerank = ''

              
        item = Offer51Item()
        
        item['school_url'] = response.url
        item['title'] = title
        item['hotmajor'] = hotmajor   
        item['IELTS_grade'] = IELTS_grade
        item['QSrank'] = QSrank
        item['Timerank'] = Timerank
#        item['majorname'] = majorname.decode('unicode-escape')

           
        yield scrapy.Request(url=majorlisturl, callback=self.parse_major, meta={ 'item': item },dont_filter=True)
    
            
        
    def parse_major(self, response):  #当前页
        
        item = response.meta['item']  
                
        majornamelist = response.xpath("//div[@class='major-name']/a[1]/text()").extract()
        
        degreelist = response.xpath("//div[@class='major-tag']/a[1]/text()").extract()
            
        majortypelist = response.xpath("//div[@class='major-tag']/a[2]/text()").extract()
          
        majordetail = zip(majornamelist,degreelist,majortypelist)
        
        nextlink = ''.join(response.xpath("//a[@class='next']/@href").extract())  
        
        for major,degree,type in majordetail:
            
                     
            item['majorname'] = major
            item['degree'] = degree
            item['type'] = type
            
            websiteurllist = response.xpath("//div[@class='major-name']/a[1]/@href").extract()
        
            for websiteurl in websiteurllist:
                   
                yield scrapy.Request(url=websiteurl,callback=self.parse_website, meta={ 'item': item },dont_filter=True)#跳转到下一页

    
        if nextlink:
            
            yield scrapy.Request(url=nextlink,callback=self.parse_major,meta={ 'item': item },dont_filter=True)  #分页
        
                                                                                 
       
              
             
    def parse_website(self, response):
    
        item = response.meta['item']
        
        officalweb = response.xpath("//iframe[@id='majorframe']/@src").extract()
        
        item['weburl'] = officalweb[0]
        
        yield item
             
         
        



            
       
        
            
           
    
        
        
        
        
        
        
        
        
        
        
        