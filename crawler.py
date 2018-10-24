import os

import requests
from bs4 import BeautifulSoup

file_path = 'episode_list.html'
url_episode_list = 'http://comic.naver.com/webtoon/list.nhn'

params = {
    'titleId': 703845,
}
if os.path.exists(file_path):
    html = open(file_path, 'rt').read()
else:
    # 저장되어 있지 않다면, requests를 사용해 HTTP GET요청
    response = requests.get(url_episode_list, params)
    # 요청 응답객채의 text속성값을 html변수에 할당
    html = response.text
    # 받은 텍스트 데이터를 HTML파일로 저장
    open(file_path, 'wt').write(html)

# BeautifulSoup클래스형 객체 생성 및 soup변수에 할당
soup = BeautifulSoup(html, 'lxml')

# div.detail > h2 (제목, 작가)dml
#   0번째 자식: 제목 텍스트
#   1번째 자식: 작가정보
h2_title = soup.select_one('div.detail > h2')
title = h2_title.contents[0].strip()
author = h2_title.contents[1].get_text(strip=True)
description = soup.select_one('div.detail > p').get_text(strip=True)

# print(desc.next_element)
# 위의 next_sibling과 같은 효과
print(title)
print(author)
print(description)

# 3. 에피소드 정보 목록을 가져오기
#   url_thumbnail:  썸네일 URL
#   title           제목
#   rating:         별점
#   created_date:   등록일
#   no:             에피소드 상세페이지의 고유 번호
#   각 에피소드들은 하나의 dict데이터
#   모든 에피소드들을 list에 넣는다


# 에피소드 목록을 담고 있는 table
table = soup.select_one('table.viewList')

# table내의 모든 tr요소 목록
tr_list = table.select('tr')

# 첫 번째 tr은 thead tr이므로 제외, tr_list의 [1:]부터 순서대로
for index, tr in enumerate(tr_list[1:]):
    # 에피소드에 해당하는 tr은 클래스가 없으므로,
    # 현재 순화중인 tr요소가 클래스 속성값을 가진다면 continue
    if tr.get('class'):
        continue
    print('=== {} === \n{}\n'.format(index, tr))

