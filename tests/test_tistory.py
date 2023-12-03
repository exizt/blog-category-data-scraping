from app.tistory import TistoryCategoryCrawler, TistoryPostCrawler


def test_read_list_in_category():
    blog_id = 'e2xist-test'
    category_no = '1072932'

    # 크롤링
    df = TistoryCategoryCrawler.collect(blog_id, category_no)

    # print(df)
    # if len(df) > 0:
    #     print('success')
    # else:
    #     print('failed')
    assert len(df) == 1


def test_read_post():
    blog_id = 'e2xist-test'
    post_id = '1'

    actual = TistoryPostCrawler.read_post(blog_id, post_id)
    # print(actual)
    # noinspection SpellCheckingInspection
    expected = "\n테스트\n"
    assert actual == expected
