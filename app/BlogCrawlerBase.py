"""
블로그 데이터 스크래핑.
"""
from app.naver import NaverPostCrawler
from app.naver import NaverCategoryCrawler
from app.tistory import TistoryBlogCrawler, TistoryPostCrawler
from enum import Enum
import time
import random


