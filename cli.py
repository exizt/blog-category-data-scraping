#!/usr/bin/env python3

import argparse
from urllib.parse import urlparse, parse_qsl
import tldextract
import BlogCrawler


def main():
    """Console script for pip_chill"""

    parser = argparse.ArgumentParser(
        description="."
    )
    parser.add_argument(
        "--url",
        dest="url",
        help=".",
    )
    parser.add_argument(
        "--category",
        dest="category_id",
        help=".",
    )
    parser.add_argument(
        "--out",
        dest="file_name",
        default="output.txt",
        help=".",
    )
    parser.add_argument(
        "--child",
        action="store_true",
        dest="include_child",
        help=".",
    )
    parser.add_argument(
        "--test",
        action="store_true",
        dest="test",
        help=".",
    )
    args = parser.parse_args()
    # print(args)

    url = args.url

    # urlparse
    parse = urlparse(url)
    print(parse)

    qs = dict(parse_qsl(parse.query))
    # print(qs)

    netloc = parse.netloc
    platform = ''
    blog_id = ''
    if 'naver.com' in netloc:
        platform = 'naver'
        if 'PostList.naver' in parse.path:
            # https://blog.naver.com/PostList.naver?blogId=blog_id 형식일 때
            blog_id = qs['blogId']
        else:
            # https://blog.naver.com/blog_id 형식일 때
            temp = parse.path
            blog_id = temp.replace('/', '') # / 제거

    elif 'tistory.com' in netloc:
        platform = 'tistory'
        tld = tldextract.extract(url)
        # print(tld.subdomain)
        blog_id = tld.subdomain

    if len(platform) < 1:
        print("platform이 선택되지 않았습니다")
        exit()

    if len(blog_id) < 1:
        print("blog_id가 필요합니다")
        exit()

    # category_id = args.category_id
    # category_id = args.get('category_id', None)
    if args.category_id is None:
        print("category_id가 필요합니다")
        exit()
    if len(args.category_id) < 1:
        print("category_id가 필요합니다")
        exit()

    category_id = args.category_id

    if args.test:
        print(platform, blog_id, category_id)

    filename = args.file_name
    # include_child = False
    include_child = args.include_child

    if not args.test:
        # 데이터 프레임 생성
        df = BlogCrawler.read(platform, blog_id, category_id, include_child)
        # print(df[:5])
        # print(df['contents'])
        # conn = sqlite3.connect("blog.sqlite")
        # df.to_sql(f"naver_tt", con=conn, if_exists='replace')

        BlogCrawler.to_text(df, filename, reverse=True)


if __name__ == "__main__":
    main()
