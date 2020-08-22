# Selenium으로 크롤링하기
# 인스타그램 크롤러 로그인버전

# !python --version

pwd

import pandas as pd
import numpy as np

## 라이브러리 import
## 라이브러리 : 필요한 도구
from selenium import webdriver  ## 라이브러리(모듈) 가져오라
from selenium.webdriver import ActionChains as AC
from tqdm import tqdm
from tqdm import tqdm_notebook
import re
from time import sleep
import time

## 데이터 수집할 키워드 지정
keywords = ["강아지"]
keywords[0]

# 크롤링 하기

## 크롬창 띄우기
driver = webdriver.Chrome("chromedriver.exe")  ## 크롬 드라이버 로드
driver.get("https://www.instagram.com/explore/tags/%EB%B0%A9%ED%96%A5%EC%A0%9C/?hl=ko")  # "#차량용방향제" 검색
time.sleep(5)

for keyword in keywords:
    dict = {}                                                       # 전체 데이터를 담을 딕셔너리 생성
    ### 사진 클릭
    CSS_tran="div.Nnq7C.weEfm"                         # 사진 버튼 정의 ("div.Nnq7C.weEfm")
    tran_button = driver.find_element_by_css_selector(CSS_tran)     # 사진 버튼 찾기
    AC(driver).move_to_element(tran_button).click().perform()       # 사진 버튼 클릭
    time.sleep(1)

    ### 크롤링 시작
    len_insta = 10   ### 몇 개 글을 크롤링 할건지

    for i in range(0, len_insta):    ### range : 숫자가 1씩하는 함수

        target_info = {}                                            # 사진별 데이터를 담을 딕셔너리 생성

        try:    ### 크롤링을 시도해라.
            ### 사진(pic) 크롤링 시작
            overlays1 = "div._2dDPU.CkGkG .FFVAD"                   # 사진창 속 사진   
            img = driver.find_element_by_css_selector(overlays1)    # 사진 선택
            pic = img.get_attribute('src')                          # 사진 url 크롤링 완료
            target_info['picture'] = pic
            ### print(target_info)

            ### 날짜(date) 크롤링 시작
            overlays2 = "div._2dDPU.CkGkG .c-Yi7 > time"                  # 날짜 지정
            datum2 = driver.find_element_by_css_selector(overlays2)     # 날짜 선택
            date = datum2.get_attribute('title')
    ###         get_attribute('title')                                    # 날짜 크롤링 완료
            target_info['date'] = date
            ### print(target_info)
            ### print(datalist)

            ### 좋아요(like) 크롤링 시작
            overlays3 = ".Nm9Fw"                                        # 리뷰창 속 날짜
            datum3 = driver.find_element_by_css_selector(overlays3)     # 리뷰 선택
            like = datum3.text                                          # 좋아요 크롤링 완료
            target_info['like'] = like
            ### print(target_info)

            ### 해시태그(tag) 크롤링 시작
            overlays4 = ".C7I1f.X7jCj"                                  # 태그 지정
            datum3 = driver.find_element_by_css_selector(overlays4)     # 태그 선택
            tag_raw = datum3.text
            tags = re.findall('#[A-Za-z0-9가-힣]+', tag_raw)            # ""#OOO"만 뽑아오기(OOO: 한글,숫자,영어,_)
            tag = ''.join(tags).replace("#"," ")                        # "#" 제거
            target_info['tag'] = tag
            ### print(target_info)

            dict[i] = target_info            ### 토탈 딕셔너리로 만들기

            print("{0}".format(i), tag)

            ### 다음장 클릭
            hit=0
            while hit < 1:                          ### 몇 번에 한번씩 크롤링할 것인지 숫자 지정
                hit+=1
                CSS_tran2="a._65Bje.coreSpriteRightPaginationArrow"             # 다음 버튼 정의
                tran_button2 = driver.find_element_by_css_selector(CSS_tran2)  # 다음 버튼 find
                AC(driver).move_to_element(tran_button2).click().perform()     # 다음 버튼 클릭
                time.sleep(2)

        except:  ### 에러가 나면 다음장을 클릭해라
            ### 다음장 클릭
            CSS_tran2="a._65Bje.coreSpriteRightPaginationArrow"             # 다음 버튼 정의
            tran_button2 = driver.find_element_by_css_selector(CSS_tran2)  # 다음 버튼 find
            AC(driver).move_to_element(tran_button2).click().perform()     # 다음 버튼 클릭
            time.sleep(2)

    print(dict)

    ### 판다스로 만들기 : 엑셀(테이블) 형식으로 만들기
    import pandas as pd
    result_df = pd.DataFrame.from_dict(dict, 'index')

    n = result_df['picture'].count()

    ### csv 형식(엑셀이랑 비슷한 파일)으로 저장
    result_df.to_csv("data/car_perfume({}).csv".format(keyword), encoding='euc-kr')

num_pic = len(result_df['picture'])
num_pic

## 이미지들 image 폴더에 다운받기
import urllib.request

for i in range(0, 50):
    try:
        index=result_df['picture'][i]
        urllib.request.urlretrieve(index, "image/{0}_{1}.jpg".format(date, i))        
    except:
        pass