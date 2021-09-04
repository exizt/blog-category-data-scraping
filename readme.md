# 블로그 글을 크롤링

특정한 하나의 블로그를 선택하고, 하나의 카테고리를 선택해서. 해당하는 글을 크롤링하는 것을 목적으로 만들고 있습니다. 

설정 같은 것으로 '블로그 종류', '블로그 아이디', '카테고리 아이디'를 지정하면. 해당 글을 크롤링하는 것이죠. 

아직은 미완성이며, 코드 작업을 간간히 진행 중에 있습니다. 

최종적으로는 네이버 블로그, 티스토리 블로그에서 크롤링을 하는 기능을 구현할 예정이며. 이것을 cron 등의 스케쥴에 등록을 하면, 

하루 한 번 크롤링을 하는 기능을 할 수 있도록 하는 것이 목표입니다.

도커 컨테이너로도 구성을 해서, cron 셋팅이 가능하도록 하는 것도 좋은 활용법이 될 것 같네요.

아직 코드는 미완성입니다...



# 개발 노트
현재는 sqlite 로 저장하게 했는데...
단순히 DataFrame 으로 return만 하게 기능적으로 구성해도 될 것 같은데..


# 설치된 패키지
- requests : certifi, carset-normalizer, idna, urllib3
  - 웹 통신
- beautifulsoup4 : soupsieve
  - 응답된 html의 핸들링
- pandas : numpy, python-dateutil, pytz, six
  - dataframe으로 손쉽게 데이터 핸들링
- pytest : atomicwrites, attrs, colorama, iniconfig, packaging, pluggy, py, toml
  - 디버깅 하려고.
