from app.naver import NaverCategoryCrawler
from app.naver import NaverPostCrawler


def test_read_list_in_category():
    blog_id = 'e2xist'
    category_no = '6'

    # 크롤링
    df = NaverCategoryCrawler.read_list_in_category(blog_id, category_no)

    # print(df)
    # if len(df) > 0:
    #     print('success')
    # else:
    #     print('failed')
    assert len(df) == 1


def test_read_post():
    blog_id = 'e2xist'
    post_id = '222474672614'

    actual = NaverPostCrawler.read_post(blog_id, post_id)
    # print(actual)
    # noinspection SpellCheckingInspection
    expected = "테스트 test\n2021. 8. 18. 12:43\n\t\n테스트 본문\n\n\n가나다라\n가나다라\n"
    assert actual == expected
