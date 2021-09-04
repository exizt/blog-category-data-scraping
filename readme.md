# 블로그 카테고리 글을 스크래핑

특정한 하나의 블로그의 하나의 카테고리에 해당하는 글을 스크래핑하는 기능을 구현

기록해두고 싶은 카테고리에 해당하는 글을 스크래핑해서 저장하는 것을 목적으로 하고 있습니다. 

주의) 코드는 아직 작업 중이고, 미완성입니다~


# 설치된 패키지
- requests : certifi, carset-normalizer, idna, urllib3
  - 웹 통신
- beautifulsoup4 : soupsieve
  - 응답된 html의 핸들링
- pandas : numpy, python-dateutil, pytz, six
  - dataframe으로 손쉽게 데이터 핸들링
- pytest : atomicwrites, attrs, colorama, iniconfig, packaging, pluggy, py, toml
  - 디버깅 하려고.


# 개발 노트
- sqlite로 저장하게 했다가, dataframe 으로 반환하는 형식으로 코드를 변경함
- 네이버 블로구 게시글을 크롤링하는 부분을 작업 중...
- 티스토리도 작업해야 하는데..
- 최종적으로는 네이버, 티스토리 두 개가 가능하도록 하는 것이 목표.