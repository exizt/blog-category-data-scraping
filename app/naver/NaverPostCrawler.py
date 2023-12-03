"""
네이버 포스트 본문 내용을 스크래핑
"""
import requests
from bs4 import BeautifulSoup

USER_AGENT = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 '
              'Safari/537.36')


def read_post(blog_id, post_id):
    url = f"https://m.blog.naver.com/{blog_id}/{post_id}"

    # 호출을 위장하기 위함.. 혹시 모르니까.
    headers = {
        'referer': f'https://m.blog.naver.com/{blog_id}',
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

    # container = soup.find("div", attrs={"class": "se-main-container"})
    container = soup.find("div", attrs={"id": "viewTypeSelector"})
    if container:
        texts = container.find_all(['p'])
        # text = soup.find("div", attrs={"class": "se-main-container"}).get_text()
        result = ''

        for text in texts:
            result += text.get_text()
            result += '\n'

        # text = text.replace("\n", "")  # 공백 제거
        # text = text.replace("\u200b", "\n")  # 제로 스페이스 제거
        result = result.replace("\u200b", "\n")  # 제로 스페이스 제거
        return result
    else:
        # print('div.se-main-container 가 없음')
        legacy_container = soup.find('div', attrs={'class': 'se_paragraph'})

        if legacy_container:
            for br in legacy_container.find_all("br"):
                br.replace_with("\n")
            # legacy_container = legacy_container.replace('<br>', '\n')

            return legacy_container.get_text()

        return ''
