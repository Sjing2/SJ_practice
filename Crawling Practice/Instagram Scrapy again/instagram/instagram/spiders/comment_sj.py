import scrapy
import re
import time
import json
import requests

# 댓글 정보 : inner_id(내구고유ID), reply(댓글 내용),
# hashtag(해시태그, 복수의 경우 콤마로 구분), reply_time(댓글 달린 시간),
# shortcode(댓글이 달린 포스트의 shortcode)

class Comment_Spider(scrapy.Spider):
    name = 'comment'

    # user 정보(username, id)
    center_user_name = 'seni._.sen._.sen'
    inner_id = '13580068590'

    def start_requests(self):
        start_urls = 'https://www.instagram.com/graphql/query/?query_hash=bfa387b2992c3a52dcbe447467b4b771&variables=%7B%22id%22%3A%22{}%22%2C%22first%22%3A12%7D'.format(Comment_Spider.inner_id)
        
        yield scrapy.Request(url=start_urls, callback=self.get_comment)

# 댓글 정보 추출
    def get_comment(self, response):
        # 댓글 정보를 json 형식으로 받아옴
        comment_json = response.json()
        # 댓글 내용 추출
        edges = comment_json['data']['user']['edge_owner_to_timeline_media']['edges']

        for edge in edges: # comment_txt 안에서 가져와야 할 정보 추출
            node = edge['node']

            shortcode = node['edge_media_to_caption']['shortcode']
            reply = node['edge_media_to_comment']['edges']['node']['text']
            created_at = node['edge_media_to_comment']['edges']['node']['created_at'] # created_at 형식을 날짜-시간 형식으로 변환
            reply_time = datetime.datetime.fromcreated_at(int(created_at)).strftime('%Y-%m-%d %H:%M:%S')
            url = 'https://www.instagram.com/p/{}/'.format(shortcode) # post url

            hashtag = []
            if '#' in reply:
                hashtag.append(reply)
            else:
                pass
        return
        

        #     # 추출할 정보 목록
        #     comment_id = node['id']
        #     insta_id = node['owner']['username']
            

        #     url = 'https://www.instagram.com/p/{}/'.format(post_id) # post url

        #     content = node['edge_media_to_caption']['edges'][0]['node']['text'] # post 내용,, #전까지를 text로 보면 될듯,,
        #     try:
        #         hashtag = re.search('(#.+)', content).group()
        #     except:
        #         hashtag = None
        #     content = re.sub('(#.+)', '', content) # 공백제거 처리도 해주면 좋을듯




        # # user_id = RelationSpider.user_id

        # # # end_cursor 정보가 있어야 커서 내리면 나오는 다음 팔로워 목록으로 이동할 수 있음 
        # # try:
        # #     end_cursor = comment_json['data']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor']
        # # except:
        # #     end_cursor = False

        # # # 다음 팔로워 목록 있으면 다음 팔로워 목록 url로 request하고 다시 팔로워 목록 추출
        # # if end_cursor:
        # #     time.sleep(1)
        # #     comment_url = 'https://www.instagram.com/graphql/query/?query_hash=c76146de99bb02f6415203be841dd25a&variables=%7B%22id%22%3A%22{}%22%2C%22first%22%3A13%2C%22after%22%3A%22{}%3D%3D%22%7D'.format(user_id, end_cursor[:-2])
        # #     yield scrapy.Request(follower_url, callback=self.parse_follower)
        # # # 다음 팔로워 목록 없으면 팔로우 목록 추출 함수로 이동
        # # else:
        # time.sleep(1)
        # comment_url = 'https://www.instagram.com/graphql/query/?query_hash=d04b0a864b4b54837c0d870b0e77e076&variables=%7B%22id%22%3A%22{}%22%2C%22first%22%3A24%7D'.format(user_id)
        # return scrapy.Request(comment_url, callback=self.parse_comment)