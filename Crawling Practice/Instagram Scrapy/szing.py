import scrapy


class SzingSpider(scrapy.Spider):
    name = 'szing'
    allowed_domains = ['example.com']
    start_urls = ['http://example.com/']

    def parse(self, response):
        pass
