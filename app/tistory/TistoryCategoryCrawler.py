"""
티스토리 게시물 목록을 크롤링
"""
import json
import time

import pandas as pd
import requests
from dateutil.parser import parse as date_parse
import datetime
from pandas import DataFrame

USER_AGENT = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 '
              'Safari/537.36')


def collect(blog_id: str, category_id, include_child=False) -> DataFrame:
    """
    티스토리 블로그 카테고리 글 목록을 가져오는 기능.
    :param blog_id: 블로그 아이디
    :param category_id: 카테고리 번호
    :param include_child: 자식 카테고리 포함 여부 (기본값 False)
    :return: DataFrame
    """
    # 페이지당 글 수
    per_page = 10  # 티스토리는 10개 고정인 듯함.
    page = 0
    df = None

    while True:
        current_df, is_last, next_page = collect_per_page(blog_id, category_id,
                                                          current_page=page, count_per_page=per_page,
                                                          include_child_category=include_child)
        if page == 0:
            df = current_df
        elif page >= 1:
            df = pd.concat([df, current_df], ignore_index=True)

        if is_last:
            break
        if next_page is None:
            break
        page += 1

        # 혹시 모르니까 sleep 추가
        time.sleep(0.5)

    return df


# noinspection PyUnusedLocal
def collect_per_page(blog_id: str, category_id, current_page=1, count_per_page=10,
                     include_child_category=False):
    """

    :param blog_id:
    :param category_id:
    :param current_page:
    :param count_per_page:
    :param include_child_category:
    :return:
    """
    print(f"collect_per_page [{blog_id}, {category_id}, {current_page}, {count_per_page}]")

    # 데이터 조회
    # url = f"https://{blog_id}.tistory.com/m/data/posts.json"
    url = f"https://{blog_id}.tistory.com/m/entries.json"

    # noinspection PyDictCreation
    # useServerOffset: true일 때는 첫번째를 생략함. false일 때는 생략하지 않음.
    params = {
        'page': current_page,
        'categoryId': category_id,
        'size': count_per_page,
        'useServerOffset': "false"
    }

    # 호출을 위장하기 위함.. 혹시 모르니까.
    headers = {
        'referer': f'https://{blog_id}.tistory.com/m/',
        'user-agent': USER_AGENT
    }

    # request http
    response = requests.get(url, params=params, headers=headers)

    # parse json
    # data = json.loads(response.text, cls=LazyDecoder)
    data = json.loads(response.text)
    # print(data)

    # 데이터 프레임으로 변경
    df_temp = pd.json_normalize(data['result']['items'])
    is_last = data['result']['isLast']
    next_page = data['result']['nextPage']

    # 필요한 컬럼만 선택하기
    df = df_temp.loc[:, ['id', 'title', 'published']]

    # 바꿀 값들 변경
    for idx, row in df.iterrows():
        # row['title'] = unquote_plus(row['title'])
        # row['published'] = date_parse(row["published"])
        # published : "5분 전", "2017. 12. 19."
        published = None
        if '분 전' in row['published'] or '시간 전' in row['published']:
            published = datetime.datetime.today()
        else:
            published = date_parse(row["published"])
        df.loc[idx, 'published'] = published

    df.insert(0, 'blog_id', blog_id)
    df.rename(
        columns={
            'id': 'post_id',
            'published': 'created_at',
            'title': 'title'
        },
        inplace=True
    )
    return df, is_last, next_page
