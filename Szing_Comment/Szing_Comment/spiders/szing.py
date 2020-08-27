import scrapy
import re
import time
import json
import requests
import datetime

# 댓글 정보 : inner_id(내구고유ID), reply(댓글 내용),
# hashtag(해시태그, 복수의 경우 콤마로 구분), reply_time(댓글 달린 시간),
# shortcode(댓글이 달린 포스트의 shortcode)

class Comment_Spider_1(scrapy.Spider):
    name = 'comment_1'

    # # user 정보(username, id)
    center_user_name = 'seni._.sen._.sen'
    inner_id = '13580068590'

    def start_requests(self):
        start_urls = 'https://www.instagram.com/graphql/query/?query_hash=bfa387b2992c3a52dcbe447467b4b771&variables=%7B%22id%22%3A%22{}%22%2C%22first%22%3A12%7D'.format(Comment_Spider_1.inner_id)
        yield scrapy.Request(url=start_urls, callback=self.comment_shortcode)


    def comment_shortcode(self, response):
        graphql = response.json()
        edges = graphql['data']['user']['edge_owner_to_timeline_media']['edges']

        shortcode_lst = []
        for edge in edges:
            shortcode_lst.append(edge['shortcode'])
            yield {'shortcode' : shortcode_lst}
        return