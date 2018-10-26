import os

import requests
from bs4 import BeautifulSoup


class Webtoon:
    def __init__(self, webtoon_id):
        self.webtoon_id = webtoon_id
        # webtoon 속성 채우기 위해 get_info() 실행
        # get_info 함수 결과 dict()

        info = self.get_info()
        self.title = info['title']
        self.author = info['author']
        self.description = info['description']

    def get_html(self):
        file_path = 'data/episode_list-{webtoon_id}.html'.format(webtoon_id=self.webtoon_id)
        # HTTP요청을 보낼 주소
        url_episode_list = 'http://comic.naver.com/webtoon/list.nhn'
        # HTTP요청시 전달할 GET Parameters
        params = {
            'titleId': self.webtoon_id,
        }

        # HTML파일이 로컬에 저장되어 있는지 검사
        if os.path.exists(file_path):
            # 저장되어 있다면 해당 파일을 읽어서 html변수에 할당
            html = open(file_path, 'rt').read()
        else:
            # 저장되어 있지 않다면, 해당 파일을 읽어서 html변수에 할당
            response = requests.get(url_episode_list, params)
            # 요청 응답객체의 text속성값을 html변수에 할당
            html = response.text
            # 받은 텍스트 데이터를 HTML파일로 저장
            open(file_path, 'wt').write(html)
        return html

    def  (self):

        """
        webtoon_id 매개변수를 이용하여
        웹툰 title, author, description을 딕셔너리 형태로 return
        :return: title, author, description 딕셔너리로
        """
        html = self.get_html()
        soup = BeautifulSoup(html, 'lxml')

        h2_title = soup.select_one('div.detail > h2')
        title = h2_title.contents[0].strip()
        author = h2_title.contents[1].get_text(strip=True)
        description = soup.select_one('div.detail > p').get_text(strip=True)

        # webtoon title, author, description
        # 딕셔너리 형태로 return
        webtoon_dict = {
            'title': title,
            'author': author,
            'description': description,
        }

        return webtoon_dict


if __name__ == '__main__':
    a = Webtoon(703845)
    print(a.title)
    print(a.author)
    print(a.description)
