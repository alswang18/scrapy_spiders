import scrapy
from selenium import webdriver
from scrapy.selector import Selector
from scrapy.http import Request
from selenium.common.exceptions import NoSuchElementException
from time import sleep
import re

class PcnSpiderSpider(scrapy.Spider):
    name = 'pcn_spider'
    allowed_domains = ['www.pcnc.com.ph/certified-ngos-list/']
    start_urls = ['http://www.pcnc.com.ph/certified-ngos-list/']

        
    def start_requests(self):
        print('start')
        url='http://www.pcnc.com.ph/certified-ngos-list/'
        yield Request(url, callback=self.parse)
        for i in range(2,41):
            url='http://www.pcnc.com.ph/certified-ngos-list/?sf_paged='+str(i)
            yield Request(url, callback=self.parse)
        
    def parse(self, response):
        rows = response.xpath('//tr')
        for i in range(1,len(rows)):
            NGO_Name=rows[i].xpath('td//text()')[0].extract()
            category=rows[i].xpath('td//text()')[2].extract()
            category=re.sub('\s+','',category)
            
            BIR_expiry_date=rows[i].xpath('td//text()')[3].extract()
            BIR_expiry_date=re.sub('\s+','',BIR_expiry_date)
            
            PCNC_expiry_date=rows[i].xpath('td//text()')[4].extract()
            PCNC_expiry_date=re.sub('\s+','',PCNC_expiry_date)
            yield { 
                'NGO_Name':NGO_Name, 
                'category':category, 
                'BIR_expiry_date':BIR_expiry_date,
                'PCNC_expiry_date':PCNC_expiry_date
               }
        