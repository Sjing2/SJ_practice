# user_id -->> username으로 변경

import scrapy
import json

class Change_Spider(scrapy.Spider):
    name = "change_id"

    # center_user_name = 'dadadajin_'
    ###################################################################################
    inner_id = '1451977165' # test - 200개 이상 포스트를 가진 user 크롤링(끊기는지 확인)
    ###################################################################################
    
    def start_requests(self):
        start_urls = 'https://www.instagram.com/graphql/query/?query_hash=bfa387b2992c3a52dcbe447467b4b771&variables=%7B%22id%22%3A%22{}%22%2C%22first%22%3A24%7D'.format(Change_Spider.inner_id)
        
        yield scrapy.Request(url=start_urls, callback=self.parse_username)

    def parse_username(self, response):
        user_json = response.json()
        edges = user_json['data']['user']['edge_owner_to_timeline_media']['edges']
        username = edges[0]['node']['owner']['username']

        yield username, print('유저이름은 :', username, '입니다')