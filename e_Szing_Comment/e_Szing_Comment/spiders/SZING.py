import scrapy
import re
import time
import json
import requests
import datetime
import pandas as pd

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

        # shortcode_lst = []
        for edge in edges:
            # shortcode_lst.append(edge['node']['shortcode'])
            shortcode = edge['node']['shortcode']
            yield {'shortcode' : shortcode}
        return

class Comment_Spider_2(scrapy.Spider):
    name = 'comment_2'

    # try:
    #     df = pd.read_csv('shortcode_test.csv')
    #     shortcode_lst = list(map(str, list(np.unique(df))))
    # except:
    #     shortcode_lst = []

    url_format = 'https://www.instagram.com/graphql/query/?query_hash=bc3296d1ce80a24b1b6e40b1e72903f5&variables=%7B%22shortcode%22%3A%22{0}%22%2C%22first%22%3A12%7D'
    
    def __init__(self):
        post_data = pd.read_csv(r"C:\Users\sojeo\SJ_practice\Szing_Comment\shortcode_test.csv", encoding="utf-8") 
        self.shortcode_list = post_data['shortcode'].tolist()
        self.shortcode_count = 0

        self.start_urls = []
        for i in range(len(self.shortcode_list)):
            self.start_urls.append(self.url_format.format(self.shortcode_list[i]))

    def parse(self, response):
        r_json = response.json()
        item = InstagramCrawlingItem()
        for data in r_json['data']['shortcode_media']['edge_media_to_parent_comment']['edges']:
            item['text']=data['node']['text']
            item['innerid']=data['node']['owner']['id']
            item['username']=data['node']['owner']['username']
            item['shortcode']= self.shortcode_list[self.shortcode_count]
            yield item

            if int(data['node']['edge_threaded_comments']['count']) > 0:
                for in_data in data['node']['edge_threaded_comments']['edges']:
                    item['text']=in_data['node']['text']
                    item['innerid']=in_data['node']['owner']['id']
                    item['username']=in_data['node']['owner']['username']
                    item['shortcode']= self.shortcode_list[self.shortcode_count]
                    yield item

        end_cursor = json.loads(response.text)['data']['shortcode_media']['edge_media_to_parent_comment']['page_info']['end_cursor']

        if end_cursor != None:
            yield scrapy.Request('https://www.instagram.com/graphql/query/?query_hash=bc3296d1ce80a24b1b6e40b1e72903f5&variables={"shortcode":"' + self.shortcode + '","first":12'+',"after":"'+end_cursor+'"}', callback=self.parse)
        else:
            self.shortcode_count += 1