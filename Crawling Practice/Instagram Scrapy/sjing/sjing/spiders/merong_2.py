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
    