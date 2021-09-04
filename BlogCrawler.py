from naver import NaverBlogCrawler, NaverPostCrawler
from enum import Enum


class SupportPlatform(Enum):
    """
    지원되는 플랫폼에 대한 enum 리스트
    """
    Naver = 0
    Tistory = 1

    def __str__(self):
        return self.name

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_


def read_list_in_category(blog_platform, blog_id, category_id):
    platform = convert_platform_str(blog_platform)
    if platform == SupportPlatform.Naver:
        return NaverPostCrawler.read_post(blog_id, category_id)
    else:
        print('준비되지 않았습니다...')
        return False


def read_post(blog_platform, blog_id, post_id):
    platform = convert_platform_str(blog_platform)
    if platform == SupportPlatform.Naver:
        return NaverPostCrawler.read_post(blog_id, post_id)
    else:
        print('준비되지 않았습니다...')
        return False


def convert_platform_str(platform):
    """
    지원되는 플랫폼에 대한 형식(Enum)으로 전환 및 체크
    :param platform: str|int
    :return: SupportPlatform value
    """
    if type(platform) == str:
        p = platform.lower()
        if p == 'naver':
            return SupportPlatform.Naver
        elif p == 'tistory':
            return SupportPlatform.Tistory
        else:
            print('준비되지 않았습니다...')
            raise
    elif type(platform) == int:
        if SupportPlatform.has_value(platform):
            return platform
        else:
            print('준비되지 않았습니다...')
            raise
    else:
        raise
