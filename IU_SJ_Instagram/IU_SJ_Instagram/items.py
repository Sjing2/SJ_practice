import scrapy


class InstagramCrawlingItem(scrapy.Item):
    username = scrapy.Field()
    inner_id = scrapy.Field()
    reply = scrapy.Field()
    hashtag = scrapy.Field()
    reply_time = scrapy.Field()
    shortcode = scrapy.Field()
    end_cursor = scrapy.Field()


class UserProfSpiderItem(scrapy.Item):
    user_name = scrapy.Field()
    user_profile = scrapy.Field()
    post_short_codes = scrapy.Field()