import BlogCrawler


def test_platform():
    # platform_id = 'naver'

    platform_id = BlogCrawler.SupportPlatform.Naver
    t1 = BlogCrawler.convert_platform_id(platform_id)
    print(type(t1))

    platform_id = 'naver'
    t2 = BlogCrawler.convert_platform_id(platform_id)
    print(type(t2))

    assert t1 and t2
