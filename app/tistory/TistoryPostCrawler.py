"""
네이버 포스트 본문 내용을 스크래핑
"""
import requests
from bs4 import BeautifulSoup

USER_AGENT = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 '
              'Safari/537.36')


def read_post(blog_id, post_id):
    url = f"https://{blog_id}.tistory.com/m/{post_id}"

    # 호출을 위장하기 위함.. 혹시 모르니까.
    headers = {
        'referer': f'https://{blog_id}.tistory.com/m/',
        'user-agent': USER_AGENT
    }

    # request http
    response = requests.get(url, headers=headers)

    # 데이터를 로드
    html_text = response.text

    # html 파싱 하고 어쩌고
    soup = BeautifulSoup(html_text, "html.parser")
    # soup = BeautifulSoup(html_text, "lxml")
    # contents = soup.select_one("div.se-main-container")

    container = soup.find("div", attrs={"class": "blogview_content"})
    if container:
        for br in container.find_all("br"):
            br.replace_with("\n")

        # 공감, 구독하기 버튼 영역
        for div in container.find_all('div', attrs={'class': 'container_postbtn'}):
            div.decompose()

        # 때때로 광고 영역
        for div in container.find_all('div', attrs={'class': 'revenue_unit_wrap'}):
            div.decompose()

        result = container.get_text()
        return result
    else:
        print('div.blogview_content 가 없음')
        return ''
