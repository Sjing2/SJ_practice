import scrapy


class InstagramCrawlingItem(scrapy.Item):
    innerid = scrapy.Field()
    date = scrapy.Field()
    tags = scrapy.Field()
    text = scrapy.Field()
    shortcode = scrapy.Field()
    end_cursor = scrapy.Field()
    image_url = scrapy.Field()

class UserProfSpiderItem(scrapy.Item):
    user_name = scrapy.Field()
    user_profile = scrapy.Field()
    post_short_codes = scrapy.Field()