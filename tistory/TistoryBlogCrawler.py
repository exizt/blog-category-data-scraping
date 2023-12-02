"""
네이버의 게시물 목록을 크롤링
"""
import requests
import json
import re
from dateutil.parser import parse as date_parse
import pandas as pd
from pandas import DataFrame
import time
from urllib.parse import unquote_plus


total_count = 0


class LazyDecoder(json.JSONDecoder):
    """
    https://stackoverflow.com/questions/65910282/jsondecodeerror-invalid-escape-when-parsing-from-python
    JSONDecodeError; Invalid /escape 에 대한 조치
    """
    def decode(self, s, **kwargs):
        regex_replacements = [
            (re.compile(r'([^\\])\\([^\\])'), r'\1\\\\\2'),
            (re.compile(r',(\s*])'), r'\1'),
        ]
        for regex, replacement in regex_replacements:
            s = regex.sub(replacement, s)
        return super().decode(s, **kwargs)


def read_list_in_category(blog_id: str, category_id, include_child=False) -> DataFrame:
    """
    티스토리 블로그의 카테고리 글 목록을 가져오는 기능.
    :param blog_id: 블로그 아이디
    :param category_id: 카테고리번호
    :param include_child: 자식 카테고리 포함 여부 (기본값 False)
    :return: DataFrame
    """
    per_page = 10  # 티스토리는 10개 고정인 듯함.
    df = read_list_in_category_per_page(blog_id, category_id,
                                        current_page=1, count_per_page=per_page, include_child_category=include_child)

    page_total_count = count_page(per_page)
    if page_total_count >= 2:
        for current_page in range(2, page_total_count+1):
            current_df = read_list_in_category_per_page(blog_id, category_id,
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


def read_list_in_category_per_page(blog_id: str, category_id, current_page=1, count_per_page=10, include_child_category=False) -> DataFrame:
    print(f"read_list_in_category_per_page [{blog_id}, {category_id}, {current_page}, {count_per_page}]")
    # 데이터 조회
    url = f"https://{blog_id}.tistory.com/m/data/posts.json"

    # noinspection PyDictCreation
    params = {
        'page': current_page,
        'categoryId': category_id,
        'countPerPage': count_per_page,
        'type': 'post'
    }

    # 어쩔 때는 paraentCategoryNo 가 있고.. 어쩔 때는 없고..
    # if include_child_category:
    #    # params['parentCategoryNo'] = category_no

    # 호출을 위장하기 위함.. 혹시 모르니까.
    headers = {
        'referer': f'https://{blog_id}.tistory.com/m/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
    }
    # request http
    response = requests.get(url, params=params, headers=headers)

    # parse json
    # data = json.loads(response.text, cls=LazyDecoder)
    data = json.loads(response.text)

    if current_page == 1:
        global total_count
        total_count = int(data['totalCount'])
        print(f"total: {total_count}")

    # 데이터 프레임으로 변경
    df_temp = pd.json_normalize(data["list"])
    # 필요한 컬럼만 선택하기
    df = df_temp.loc[:, ['id', 'title', 'published']]

    # 바꿀 값들 변경
    for idx, row in df.iterrows():
        # row['title'] = unquote_plus(row['title'])
        row['published'] = date_parse(row["published"])

    df.insert(0, 'blog_id', blog_id)
    df.rename(
        columns={
            'id': 'post_id',
            'published': 'created_at',
            'title': 'title'
        },
        inplace=True
    )
    return df
