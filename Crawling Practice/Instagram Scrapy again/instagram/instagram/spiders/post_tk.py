# 첫번째 페이지 --> https://www.instagram.com/graphql/query/?query_hash=bfa387b2992c3a52dcbe447467b4b771&variables=%7B%22id%22%3A%221437038730%22%2C%22first%22%3A24%7D
# 강원도 _hyeon_8
import scrapy
import json
import time
import re
import datetime

#### 로그인 과정은 필요없고, start_url에 center_id만 넣어주면 해당 id의 모든 post정보 크롤링 가능 ####
class Post_Spider(scrapy.Spider):
    name = "post"

    center_user_name = '_heeyas_day'
    inner_id = '1437038730'

    def start_requests(self):
        start_urls = 'https://www.instagram.com/graphql/query/?query_hash=bfa387b2992c3a52dcbe447467b4b771&variables=%7B%22id%22%3A%22{}%22%2C%22first%22%3A24%7D'.format(Post_Spider.inner_id)
        
        yield scrapy.Request(url=start_urls, callback=self.get_post)

    def get_post(self, response):
        graphql = response.json()
        edges = graphql['data']['user']['edge_owner_to_timeline_media']['edges']

        for edge in edges: # edge 안에서 가져와야 할 정보 추출
            node = edge['node']
            typename = node['__typename']

            # 추출할 정보 목록
            shortcode = node['shortcode'] # post_id
            insta_id = node['owner']['username']
            
            timestamp = node['taken_at_timestamp'] # timestamp 형식을 날짜-시간 형식으로 변환
            post_date = datetime.datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S')
            url = 'https://www.instagram.com/p/{}/'.format(shortcode) # post url

            content = node['edge_media_to_caption']['edges'][0]['node']['text'] # post 내용,, #전까지를 text로 보면 될듯,,
            try:
                hashtag = re.search('(#.+)', content).group()
            except:
                hashtag = None
            content = re.sub('(#.+)', '', content) # 공백제거 처리도 해주면 좋을듯
            content = re.sub('\n', '', content)

            # 사진, 동영상 url(복수일 경우 콤마로 구분)//사진, 동영상 복수처리
            media_url = []
            view_count = []
            try:
                if typename == 'GraphImage': # 이미지 혹은 동영상이 1개일 때
                    display_url = node['display_url']
                    media_url.append(display_url) # 중복되는 코드 줄이면 좋을듯
                elif typename == 'GraphSidecar': # 이미지 혹은 동영상이 여러개일 때
                    sidecar_edges = node['edge_sidecar_to_children']['edges']
                    for sidecar_edge in sidecar_edges:
                        side_node = sidecar_edge['node']
                        if side_node['__typename'] == 'GraphImage': # 이미지일때
                            display_url = side_node['display_url']
                            media_url.append(display_url)
                        elif side_node['__typename'] == 'GraphVideo': # 동영상일때
                            video_url = side_node['video_url']
                            media_url.append(video_url)
                            video_view_count = side_node['video_view_count']
                            view_count.append(video_view_count)
            except:
                pass

            try:
                region_tag = node['location']['name']
                # tagged = node['edge_media_to_tagged_user']['edges'][0]['node']['user']['username'] # 태그된 사람의 인스타 아이디
            except:
                region_tag = None
                # tagged = None

            like_count = node['edge_media_preview_like']['count']
            crawling_time = time.strftime('%Y-%m-%d %H:%M:%S')
            team_idx = 4

            yield {'shortcode' : shortcode,
                    'insta_id' : insta_id,
                    'inner_id' : Post_Spider.inner_id,
                    'post_date' : post_date,
                    'url' : url,
                    'content' : content,
                    'media_url' : media_url,
                    'hashtag' : hashtag,
                    'region_tag' : region_tag,
                    # 'tagged' : tagged,
                    'like_count' : like_count,
                    'view_count' : view_count,
                    'crawling_time' : crawling_time,
                    'team_idx' : team_idx
                    }
            print('post크롤링중...post크롤링중...post크롤링중...post크롤링중...')

        # end_cursor 추출
        try:
            end_cursor = graphql['data']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor']
            print('end_cursor :', end_cursor)
        except:
            end_cursor = None
        
        # 스크롤하고 다음 페이지 주소 가져오기
        if end_cursor:
            time.sleep(1)
            next_page = 'https://www.instagram.com/graphql/query/?query_hash=bfa387b2992c3a52dcbe447467b4b771&variables=%7B%22id%22%3A%22{}%22%2C%22first%22%3A13%2C%22after%22%3A%22{}%3D%3D%22%7D'.format(Post_Spider.inner_id, end_cursor[:-2])
            yield scrapy.Request(next_page, callback=self.get_post)