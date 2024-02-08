import scrapy
from cos_plusPro.items import CosPlusproItem

class SrcDataSpider(scrapy.Spider):
    name = "src_data"
    #allowed_domains = ["www.xxx.com"]
    start_urls = ["https://dimtown.com/cosplay/"]
    url = 'https://dimtown.com/cosplay/page%d'
    page_num = 2

    def new_parse(self, response):
        item = response.meta['item']
        img = response.xpath('//div[@class="content_left"]/p[3]/img')
        for img_src in img:
            src = img_src.xpath('./@src').extract_first()
            item['src'] = src
            yield item
    def parse(self, response):
        li_list = response.xpath('//ul[@class="update_area_lists cl"]/li')
        for li in li_list:
            new_page = li.xpath('./div[@class="kzpost-data"]/a/@href').extract_first()
            #图片集名称
            name = li.xpath('.//div[@class="posr-tit"]/text()').extract_first()
            item = CosPlusproItem()
            item['name'] = name
            #请求传参：meta={}就可以将meta对应字典的内容传给指定的回调函数
            yield scrapy.Request(new_page,callback=self.new_parse,meta={'item': item})
        if self.page_num <= 5:
            new_url = format(self.url % self.page_num)
            self.page_num += 1
            yield scrapy.Request(new_url,callback=self.parse)


