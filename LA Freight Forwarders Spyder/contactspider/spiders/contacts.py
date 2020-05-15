# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from scrapy.selector import Selector
from scrapy.http import Request
from selenium.common.exceptions import NoSuchElementException
from time import sleep


class ContactsSpider(scrapy.Spider):
    name = 'contacts'
    allowed_domains = [
        'https://www.lacbffa.org/']

    def start_requests(self):
        self.driver = webdriver.Chrome(
            'C:\\Users\\alswa\\Desktop\\contactspider\\contactspider\\chromedriver')
        self.driver.get(
            'https://www.lacbffa.org/directory?current_page=1&sort_type=featured&search_for=company&asset_type=company_user&display_type=default')
        sel = Selector(text=self.driver.page_source)
        companies = sel.xpath(
            '//*[@class="col-xs-6"]/a[contains(text(),"Profile")]/@href').extract()
        pages = []
        while True:
            # try:
            sel = Selector(text=self.driver.page_source)
            if(sel.css('.btn.btn-info.page::text').extract_first() in pages):
                for company in companies:
                    print(len(companies))
                    url = 'https://www.lacbffa.org'+company
                    yield Request(url, callback=self.parse_contacts)
                self.driver.quit()
                break
            else:
                pages.append(
                    sel.css('.btn.btn-info.page::text').extract_first())
                companies.extend(sel.xpath(
                    '//*[@class="col-xs-6"]/a[contains(text(),"Profile")]/@href').extract())
                next_page = self.driver.find_element_by_xpath(
                    '//a[contains(text(),"Next")]').click()
                self.logger.info('sleeping')
                sleep(4)
            # except NoSuchElementException:
            #     self.logger.info('No More Pages')
            #     for company in companies:
            #         url = 'https://www.lacbffa.org'+company
            #         time.sleep(2)
            #         yield Request(url, callback=self.parse_contacts)
            #     self.driver.quit()
            #     break

    def parse_contacts(self, response):
        company_name = response.xpath(
            '//*[@id="about"]/h1/text()').extract_first()[6:]
        email = response.xpath(
            '//td[@class="contact-info-label"]/label[contains(text(),"Email")]/following-sibling::a/text()').extract_first()
        phone_number = response.xpath(
            '//td[@class="contact-info-label"]/label[contains(text(),"Phone")]/ancestor::td/text()').extract()[1].strip()
        fax_number = response.xpath(
            '//td[@class="contact-info-label"]/label[contains(text(),"Fax")]/ancestor::td/text()').extract()[1].strip()
        yield{
            'company_name': company_name,
            'email': email,
            'phone_number': phone_number,
            'fax_number': fax_number
        }
