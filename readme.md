# 블로그 카테고리 글 수집기

네이버, 티스토리 블로그의 특정한 블로그의 한 카테고리의 글을 수집할 수 있습니다. 

txt파일에 수집한 내용을 기록합니다. 게시글 등을 txt로 백업하거나, 소설 등을 백업하는 데에 적합합니다.

<br><br><br>

# 1. 라이선스
`MIT License`로 자유롭게 사용하실 수 있습니다.

<br><br><br>

# 2. 사용법
```python
import BlogCrawler

platform = 'naver'
# platform = 'tistory'
blog_id = '블로그아이디'
category_id = '카테고리번호'
filename = '저장할 파일명.txt'

df = BlogCrawler.read(platform, blog_id, category_id, False)

BlogCrawler.to_text(df, filename, reverse=True)
```

<br><br><br>

# 3. 코드에 대한 간략 설명
카테고리에 해당하는 글 목록을 우선적으로 수집합니다. 글 목록을 토대로 게시글의 본문을 하나씩 수집합니다.
차단을 방지하기 위해 몇 초간의 텀을 주기로 하나씩 수집합니다. 글이 많으면 시간이 좀 걸릴 수 있습니다. 

전부 수집이 되었다면 pandas 의 DataFrame 으로 반환합니다. 여기까지가 `BlogCrawler.read`의 기능입니다. 

수집한 DataFrame의 내용을 보기 좋게 txt파일로 저장하기 위해서
`BlogCrawler.to_text(df, filename, reverse=True)`을 이용합니다.

txt로 저장하지 않고, 데이터베이스에 넣거나 다양한 활용을 하시려면, DataFrame 값을 활용하시면 됩니다. 

<br><br><br>

# 사용된 파이썬 패키지
- requests : certifi, carset-normalizer, idna, urllib3
  - 웹 통신
- beautifulsoup4 : soupsieve
  - 응답된 html의 핸들링
- pandas : numpy, python-dateutil, pytz, six
  - dataframe으로 손쉽게 데이터 핸들링
- pytest : atomicwrites, attrs, colorama, iniconfig, packaging, pluggy, py, toml
  - TDD 디버깅 하려고 추가함.

<br><br><br>

# 연관 키워드, 연관 태그
네이버 블로그 카테고리 글 수집, 티스토리 블로그 카테고리 글 수집, 블로그 크롤링, 블로그 크롤러, 블로그 스크래핑
