# -*- coding: utf-8 -*-
"""
Created on Mon Jun 01 13:54:26 2023

Web crawling script for WebGoat to generate traffic and logs

@author: wroe1282
"""

#!/bin/python3
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.item import Item, Field
from scrapy.selector import Selector
#from scrapy.selector import HtmlXPathSelector
#from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.linkextractors import LinkExtractor
#from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.spiders import CrawlSpider, Rule
#from scrapy.utils.url import urljoin_rfc...,.
from urllib.parse import urljoin
#from sitegraph.items import SitegraphItem
from scrapy.utils.project import get_project_settings

from scrapy.http import Request
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

class SitegraphItem (Item):
	url=Field()
	linkedUrls=Field()



#POST login payload username=testuser&password=testuser
urlsArray=[
    'http://localhost:8080/WebGoat/login'
    'http://localhost:8080/WebGoat/welcome.mvc',
    'http://localhost:8080/webGoat/start.mvc#',
    'http://localhost:8080/WebGoat/start.mvc#lesson/MissingFunctionAC.lesson',
    'http://localhost:8080/WebGoat/start.mvc#lesson/SpoofCookie.lesson',
    'http://localhost:8080/WebGoat/start.mvc#lesson/WebWolfIntroduction.lesson',
    'http://localhost:8080/WebGoat/start.mvc#lesson/Cryptography.lesson',
    'http://localhost:8080/WebGoat/start.mvc#lesson/SqlInjection.lesson',
    'http://localhost:8080/WebGoat/start.mvc#lesson/InsecureDeserialization.lesson/3'
    
    ]
    
  




DOMAIN = 'localhost:8080/WebGoat/login'
URL = 'http://%s' % DOMAIN


class Spider4(scrapy.Spider):
    name = "MySpider"
      
    # urls to be fetched
    start_urls = [URL]
    
    def parse(self, response):
        csrf_token = response.xpath('//*[@name="csrf_token"]/@value').extract_first()
        inputs = response.css('form input')
        print( inputs)
 
        formdata = {}
        for input in inputs:
            name = input.css('::attr(type)').get()
            value = input.css('::attr(value)').get()
            formdata[name] = value
 
        formdata['csrf_token'] = csrf_token
        formdata['username'] = 'testuser'
        formdata['password'] = 'testuser'
 
    
       
        print(formdata)
        return scrapy.FormRequest.from_response(
            response,
            formdata = formdata,
            callback = self.parse_after_login
        )
 
    def parse_after_login(self, response):
        print ("logged in!!!!")
        #print(response.xpath('.//div[@class = "col-md-4"]/p/a/text()').get())
        
        #after login extract all links of that page
        link_extractor = LinkExtractor()
        links = link_extractor.extract_links(response)
        
        item=""
        #iterate over that links by sending to each a request
        for link in links:
            yield Request(url=link, meta={'item': item}, callback=self.parse_item_page)
        
        #for title in response.css('.oxy-post-title'):
        #for i in range(500):
        #    yield Request(URL + str(i), self.parse_tv)
        # for link in links:
        #     # parameters of link : url, text, 
        #     print (link.url)
        #     yield Request(link.url, callback=self.parse)
        #     #yield response.follow(link.url, self.parse)


s = get_project_settings()
s['FEED_FORMAT'] = 'csv'
s['LOG_LEVEL'] = 'INFO'
s['FEED_URI'] = 'Q1.csv'
s['LOG_FILE'] = 'Q1.log'


#process = CrawlerProcess(get_project_settings())


process = CrawlerProcess( 
 	settings={ 
        "USER_AGENT" : 'Mozilla/5.0 (X11; Linux x86_64; rv:7.0.1) Gecko/20100101 Firefox/7.7',
        "CONCURRENT_REQUESTS":'1'
        #"SPIDER_MODULES" : ['scrapy.spiders'],
        #"NEWSPIDER_MODULE" : 'scrapy.spiders',   
        #"FEED_URI": "C:\\Temp\\sitegraph.json",        
        #"FEEDS": { "items.json": {"format": "json"}}
        }
 	)

configure_logging()
settings = get_project_settings()

#process.crawl(Spider4)
#process.start()  # the script will block here until the crawling is finished

#Concurent execution of crawlers
runner = CrawlerRunner(settings)
runner.crawl(Spider4)#,domain="localhost:8080/webGoat/start.mvc")
d = runner.join()
d.addBoth(lambda _: reactor.stop())
reactor.run() 





