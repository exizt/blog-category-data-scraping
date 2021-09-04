import requests
import json
import re
from dateutil.parser import parse as date_parse
import pandas as pd
import numpy as np
import sqlite3


class LazyDecoder(json.JSONDecoder):
    def decode(self, s, **kwargs):
        regex_replacements = [
            (re.compile(r'([^\\])\\([^\\])'), r'\1\\\\\2'),
            (re.compile(r',(\s*])'), r'\1'),
        ]
        for regex, replacement in regex_replacements:
            s = regex.sub(replacement, s)
        return super().decode(s, **kwargs)


def get_list_in_category(blog_id, category_no):

    # 데이터 조회
    url = f"https://blog.naver.com/PostTitleListAsync.naver?blogId={blog_id}&viewdate=&currentPage=3&categoryNo={category_no}&parentCategoryNo=&countPerPage=5"
    response = requests.get(url)
    data = json.loads(response.text, cls=LazyDecoder)

    total_count = data['totalCount']
    countPerPage = 5
    print(f"total: {total_count}")

    # 데이터 프레임으로 변경
    df_temp = pd.json_normalize(data["postList"])
    # 필요한 컬럼만 선택하기
    df = df_temp.loc[:, ['logNo', 'title', 'addDate']]

    # 바꿀 값들 변경
    for idx, row in df.iterrows():
        # print(date_parse(row['addDate']))
        row['addDate'] = date_parse(row["addDate"])

    # 커넥션 및 테이블로 저장
    conn = sqlite3.connect("blog.sqlite")
    df.to_sql(f"naver_{blog_id}_{category_no}", con=conn, if_exists='replace')

    print(df['logNo'])
