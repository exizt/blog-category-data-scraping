import pytest
from naver import NaverBlogCrawler


def test_read_list():
    blog_id = 'e2xist'
    category_no = '6'

    # 크롤링
    df = NaverBlogCrawler.read_list_in_category(blog_id, category_no)

    print(df)
    # if len(df) > 0:
    #     print('success')
    # else:
    #     print('failed')
    assert len(df) > 0


# if __name__ == '__main__':
