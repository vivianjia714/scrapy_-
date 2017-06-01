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
        for page in range(1,4):
#            baseurl = 'https://www.51offer.com/school/uk-all-' 英国院校
#            baseurl = 'https://www.51offer.com/school/us-all-' 美国院校
#            baseurl = 'https://www.51offer.com/school/au-all-' 澳洲院校
#            baseurl = 'https://www.51offer.com/school/sg-all-' 新加坡院校
#            baseurl = 'https://www.51offer.com/school/hk-all-' 香港院校
            baseurl = 'https://www.51offer.com/school/nz-all-'
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
        
        englishtitlelist = response.xpath("//span[@class='ename']/text()").extract()
        
        if englishtitlelist:
            englishtitle = englishtitlelist[0]
            
        else:
            englishtitle = ''
              
        item = Offer51Item()
        
#        item['school_url'] = response.url
        item['title'] = title
#        item['hotmajor'] = hotmajor   
#        item['IELTS_grade'] = IELTS_grade
#        item['QSrank'] = QSrank
#        item['Timerank'] = Timerank
        item['englishtitle'] = englishtitle
#        item['majorname'] = majorname.decode('unicode-escape')

           
        yield scrapy.Request(url=majorlisturl, callback=self.parse_major, meta={ 'item': item },dont_filter=True)
    
            
        
    def parse_major(self, response):
        
        item = response.meta['item']
                
        nextlink = 'majorlisturl'.join(response.xpath("//a[@class='next']/@href").extract())    
                              
        if nextlink:
            
#            print nextlink
            
            yield scrapy.Request(url=nextlink,callback=self.parse_major,meta={ 'item': item },dont_filter=True)        
                            
                                       
        websiteurllist = response.xpath("//div[@class='major-name']/a[1]/@href").extract()
      
        for websiteurl in websiteurllist:
        
            yield scrapy.Request(url=websiteurl,callback=self.parse_website, meta={ 'item': item },dont_filter=True)
            
        
              
             
    def parse_website(self, response):
    
        item = response.meta['item']
        
#        officalweb = response.xpath("//iframe[@id='majorframe']/@src").extract()
        
#        item['weburl'] = officalweb[0]
        
        enmajorname = response.xpath("//h2[@class='ename']/text()").extract()
        
#        print type(enmajorname[0].encode('utf-8'))
        
        cnmajorname = response.xpath("//h2[@class='ename']/i/text()").extract()
        
#        print type(cnmajorname[0].encode('utf-8'))
        
        degreetype = response.xpath("//div[@class='wrap']/p/span[1]/text()").extract()
        
#        print type(degreetype[0].encode('utf-8'))

        degreetype1 = degreetype[0][5:]

#        print degreetype1        
        officalurl = response.xpath("//iframe[@id='majorframe']/@src").extract()
        
        majortype = response.xpath("//div[@class='wrap']/p/span[2]/text()").extract()
        
        majortype1 = majortype[0][5:]
        
#        print majortype1.encode('gbk')
        
#        print officalurl[0]
        
        item['enmajorname'] = enmajorname[0].encode('utf-8')
        
        item['cnmajorname'] = cnmajorname[0].encode('utf-8')
        
        item['degreetype'] = degreetype1.encode('utf-8')
        
        item['officalurl'] = officalurl[0].encode('utf-8')
        
        item['majortype'] = majortype1.encode('utf-8')
        
        yield item
    
        



            
       
        
            
           
    
        
        
        
        
        
        
        
        
        
        
        