import scrapy
import re
import time
from bs4 import BeautifulSoup
import json
import requests

# 포스트 수집 시 필요한 내용 ↓
# post_id(포스트 ID), insta_id(인스타그램 ID), post_date(포스트 날짜), url, content(포스트 내용), media_url(사진, 동영상 url),
# hashtag(포스트 내 해시태그), region_tag(포스트의 장소태그), tagged(태그된 사람의 인스타 아이디), like_count(수집시 좋아요 수),
# view_count(수집시 조회수), crawling_time(수집시간), team_idx(팀 번호)

class PostSpider(scrapy.Spider):
    name = 'post'
    user_id = '1466227296'

    def parse_post(self, response):
        # 포스트 페이지를 json 형식으로 받아옴
        post_json = response.json()
        # 포스트_lst 추출
        post_lst = post_json['data']['user']['edge_owner_to_timeline_media']['edges']
         
        try:
            end_cursor = post_json['data']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor']
        except:
            end_cursor = False

        url = 'https://www.instagram.com/graphql/query/?query_hash=bfa387b2992c3a52dcbe447467b4b771&variables=%7B%22{}%7D'.format(end_cursor[:-2])
        yield scrapy.Request(url, callback=self.parse_post)


    # # post 수집
    # def post_collect(self, response):
    #     # 포스트를 json 형식으로 받아옴
    #     post_json = response.json()
    #     # 포스트 추출
    #     post_lst = follower_json['data']['user']['edge_followed_by']['edges']
    #     post_id = RelationSpider.user_id
    #     insta_id = 
    #     post_date = 
