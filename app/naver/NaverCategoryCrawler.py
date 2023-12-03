"""
네이버의 게시물 목록을 크롤링
"""
import requests
import json
from dateutil.parser import parse as date_parse
import pandas as pd
from pandas import DataFrame
import time
from urllib.parse import unquote_plus
from app.utils import LazyJSONDecoder


total_count = 0
USER_AGENT = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 '
              'Safari/537.36')


def collect(blog_id: str, category_no, include_child=False) -> DataFrame:
    """
    네이버 블로그 카테고리 글 목록을 가져오는 기능.
    :param blog_id: 블로그 아이디
    :param category_no: 카테고리 번호
    :param include_child: 자식 카테고리 포함 여부 (기본값 False)
    :return: DataFrame
    """
    # 페이지당 글 수
    per_page = 30
    df = collect_per_page(blog_id, category_no,
                          current_page=1, count_per_page=per_page, include_child_category=include_child)

    page_count = count_page(per_page)
    if page_count >= 2:
        for current_page in range(2, page_count+1):
            current_df = collect_per_page(blog_id, category_no,
                                          current_page=current_page,
                                          count_per_page=per_page, include_child_category=include_child)
            df = pd.concat([df, current_df], ignore_index=True)

            # 혹시 모르니까 sleep 추가
            time.sleep(0.5)
    return df


def count_page(per_page=5):
    global total_count
    if total_count % per_page > 0:
        rv = (total_count // per_page) + 1
    else:
        rv = total_count // per_page
    return rv


def collect_per_page(blog_id: str, category_no, current_page=1, count_per_page=5, include_child_category=False) -> DataFrame:
    """

    :param blog_id:
    :param category_no:
    :param current_page:
    :param count_per_page:
    :param include_child_category:
    :return:
    """
    print(f"collect_per_page [{blog_id}, {category_no}, {current_page}, {count_per_page}]")

    # 데이터 조회
    url = f"https://blog.naver.com/PostTitleListAsync.naver"

    # noinspection PyDictCreation
    params = {
        'blogId': blog_id,
        'currentPage': current_page,
        'categoryNo': category_no,
        'countPerPage': count_per_page
    }

    # 어쩔 때는 paraentCategoryNo 가 있고.. 어쩔 때는 없고..
    if include_child_category:
        params['parentCategoryNo'] = category_no

    # 호출을 위장하기 위함.. 혹시 모르니까.
    headers = {
        'referer': f'https://blog.naver.com/PostList.naver?blogId={blog_id}',
        'user-agent': USER_AGENT
    }

    # request http
    response = requests.get(url, params=params, headers=headers)

    # parse json
    data = json.loads(response.text, cls=LazyJSONDecoder)

    if current_page == 1:
        global total_count
        total_count = int(data['totalCount'])
        print(f"total: {total_count}")

    # 데이터 프레임으로 변경
    df_temp = pd.json_normalize(data["postList"])
    # 필요한 컬럼만 선택하기
    df = df_temp.loc[:, ['logNo', 'title', 'addDate']]

    # 바꿀 값들 변경
    for idx, row in df.iterrows():
        row['title'] = unquote_plus(row['title'])
        row['addDate'] = date_parse(row["addDate"])

    df.insert(0, 'blog_id', blog_id)
    df.rename(
        columns={
            'logNo': 'post_id',
            'addDate': 'created_at',
            'title': 'title'
        },
        inplace=True
    )
    return df
