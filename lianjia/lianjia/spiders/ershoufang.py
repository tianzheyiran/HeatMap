# -*- coding: utf-8 -*-
import scrapy

from lianjia.items import LianjiaItem
import json

class ErshoufangSpider(scrapy.Spider):
    name = 'ershoufang'
    allowed_domains = ['bj.lianjia.com']
    start_urls = ['https://bj.lianjia.com/xiaoqu/cro21/']

    def parse(self, response):
        baseurl = 'https://bj.lianjia.com'
        area = response.xpath('//div[@data-role="ershoufang"]/div[1]/a/@href').extract()
        for url in area:
            if "https" not in url:
                area_url = baseurl + url
            else:
                area_url = url
            yield scrapy.Request(url = area_url,callback=self.house_parse)

    def house_parse(self,response):
        meanPrice = response.xpath('//ul[@class="listContent"]//div[@class="totalPrice"]/span/text()').extract()
        xiaoqu = response.xpath('//ul[@class="listContent"]//div[@class="title"]/a/text()').extract()
        distinct = response.xpath('//div[@class="positionInfo"]/a[1]/text()').extract_first()

        item = LianjiaItem()
        for m,x in zip(meanPrice,xiaoqu):
            item['mean'] = m
            item['xiaoqu'] = x
            item['distinct'] = distinct

            yield item
        pagestr = response.xpath('//div[@class="page-box house-lst-page-box"]/@page-data').extract_first()

        totalPage = json.loads(pagestr)['totalPage']
        if totalPage > 1:
            for i in range(2,totalPage):
                url = 'https://bj.lianjia.com/xiaoqu/{}/pg{}/'.format(distinct,i)
                yield scrapy.Request(url=url,callback=self.house_parse)
