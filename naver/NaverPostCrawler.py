import requests
import json
import re
from dateutil.parser import parse as date_parse
import pandas as pd
from pandas import DataFrame
import time
import numpy as np
import urllib.request
from bs4 import BeautifulSoup


def read_post(blog_id, post_no):
    url = f"https://m.blog.naver.com/{blog_id}/{post_no}"

    # 호출을 위장하기 위함.. 혹시 모르니까.
    headers = {
        'referer': f'https://m.blog.naver.com/{blog_id}',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
    }

    # request http
    response = requests.get(url, headers=headers)

    # 데이터를 로드
    html_text = response.text

    # html 파싱 하고 어쩌고
    soup = BeautifulSoup(html_text, "html.parser")
    # soup = BeautifulSoup(html_text, "lxml")

    if soup.find("div", attrs={"class": "se-main-container"}):
        text = soup.find("div", attrs={"class": "se-main-container"}).get_text()
        
        # text = text.replace("\n", "")  # 공백 제거
        text = text.replace("\u200b", "\n")  # 제로 스페이스 제거
        return text
    else:
        return ''
