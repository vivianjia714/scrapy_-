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
import sys
reload(sys)
sys.setdaulftencoding('utf-8')

class Spider_51(scrapy.Spider):
 
    name = "51spider"
    allowed_domains = ["51offer.com"]
    start_urls = ['https://www.51offer.com/']
    
    def parse(self, response):
        for page in range(1,5):
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
#        print url
        
        titlelist = response.xpath("//h1[@class='cname']/text()").extract()
        title =  titlelist[0].strip()
#        print title
        
        
        hotmajorlist = response.xpath("//div[@class='rr']/text()").extract()
        
        if hotmajorlist:
             
            hotmajor = hotmajorlist[0].strip()
        else:
            hotmajor =''
        
#        print hotmajor
        
#        IELTS_gradelist = response.xpath("//*[@id='school-introduction']/div[2]/div[1]/div/text()").extract()
        IELTS_gradelist = response.xpath("//*[@class='intro-lists']/div[2]/div[1]/text()").extract()
        if IELTS_gradelist:
            IELTS_grade = IELTS_gradelist[1].strip()
        else:
            IELTS_grade = ''
            
#        print IELTS_grade
        
        QSranklist = response.xpath("//div[@class='rank-list']/div[2]/div[1]/text()").extract()
        if QSranklist:
            
    
            QSrank = QSranklist[0]
        else:
            QSrank = ''    
#        print QSrank
        
        
        Timeranklist = response.xpath("//div[@class='rank-list']/div[1]/div[1]/text()").extract()
        if Timeranklist:
            Timerank = Timeranklist[0]
            
        else:
            Timerank = ''
#        print Timerank


#        school_logolist = response.xpath("//div[@class='school-logo']/img/@src").extract()
        
#        school_logo = school_logolist[0]
#        print school_logo

      
        item = Offer51Item()
        
        item['school_url'] = url 
        item['title'] = title
        item['hotmajor'] = hotmajor   
        item['IELTS_grade'] = IELTS_grade
        item['QSrank'] = QSrank
        item['Timerank'] = Timerank
#        item['school_logo'] = school_logo
        

        
     
        yield item
        
        
    