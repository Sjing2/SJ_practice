import scrapy
import re
import time
import json
import requests

# 댓글 정보 : post_id(댓글이 달린 포스트 ID), insta_id(인스타그램 ID), reply(댓글 내용),
# hashtag(해시태그), tagging(태그한 사용자 아이디), crawling_time(수집시간),
# reply_time(댓글 달린 시간), heart(댓글별 좋아요 수)

class RelationSpider(scrapy.Spider):
    name = 'comment'

    # user 정보(username, id)
    inner_id = '2068136088'
    insta_id = 'merong_3429'

# 프로필 정보 추출
    def parse_profile(self, response):
        # 프로필 정보를 json 형식으로 받아옴
        profile_json = response.json()
        # 게시물 수 추출
        post_cnt = follower_json['data']['user']['edge_followed_by']['edges']
        user_id = RelationSpider.user_id

        # 개별 팔로워 추출해서 start에 팔로워, end에 대상 user_id 저장
        for follower in follower_lst:
            if not follower['node']['is_private']:
                yield {
                    'start': follower['node']['id'],
                    'end' : user_id
                }
            # 비공개 아이디는 어차피 필요없는 정보이기 때문에 제외하고 크롤링
            else:
                print('private_id!')

        # end_cursor 정보가 있어야 커서 내리면 나오는 다음 팔로워 목록으로 이동할 수 있음 
        try:
            end_cursor = follower_json['data']['user']['edge_followed_by']['page_info']['end_cursor']
        except:
            end_cursor = False

        # 다음 팔로워 목록 있으면 다음 팔로워 목록 url로 request하고 다시 팔로워 목록 추출
        if end_cursor:
            time.sleep(1)
            follower_url = 'https://www.instagram.com/graphql/query/?query_hash=c76146de99bb02f6415203be841dd25a&variables=%7B%22id%22%3A%22{}%22%2C%22first%22%3A13%2C%22after%22%3A%22{}%3D%3D%22%7D'.format(user_id, end_cursor[:-2])
            yield scrapy.Request(follower_url, callback=self.parse_follower)
        # 다음 팔로워 목록 없으면 팔로우 목록 추출 함수로 이동
        else:
            time.sleep(1)
            follow_url = 'https://www.instagram.com/graphql/query/?query_hash=d04b0a864b4b54837c0d870b0e77e076&variables=%7B%22id%22%3A%22{}%22%2C%22first%22%3A24%7D'.format(user_id)
            yield scrapy.Request(follow_url, callback=self.parse_follow)
