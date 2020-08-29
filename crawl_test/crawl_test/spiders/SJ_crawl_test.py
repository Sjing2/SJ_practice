import scrapy


class SjCrawlTestSpider(scrapy.Spider):
    name = 'SJ_crawl_test'
    allowed_domains = ['ecample.com']
    start_urls = ['http://ecample.com/']

    def parse(self, response):
        pass
