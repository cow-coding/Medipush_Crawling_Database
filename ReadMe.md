# Medipush Database Code

## Appropriate install environment

1. Python 3.8이상
2. Jupyter Notebook에서도 확인할 수 있습니다.
3. Google Colaboratory 기반으로 작선된 파이썬 코드입니다.


## 사용 라이브러리

1. Pymongo - MongoDB control Python Library
2. BeautifulSoup4 - Web Crawling Library
3. Pool, Manager - Multiprocessing Python Library


## Repository 설명
이 repository는 실제로 직접 구동을 하는 파일은 아닙니다. **(코드를 실행하지 마세요!!!)**  
프로젝트 진행을 할 때, 데이터베이스 구축을 위한 파이썬 실행코드입니다.  
Crawling_and_Making_DB.py가 실행 전반을 담고 있는 코드입니다.  
데이터베이스 구축 코드 내부에서 의약품 품목코드를 활용하는데, 의약품 품목코드가 담겨있는 파일이 med_code.csv입니다.  
med_code.csv를 Crawling_and_Making_DB.py와 같은 폴더에 넣어야합니다.  


## Code execution process
전체적인 코드 설명은 각주로 적어놨습니다.  
초반부에 데이터베이스와 연결부, 변수선언부, 품목코드 리딩파트를 제외하고 main문과 크롤링와 DB구축 함수만 간단하게 설명하겠습니다.

### main part
우선 main함수 내부에는 Pool과 Manager 라이브러리를 활용해서 multiprocessing 방식으로 크롤링을 진행했습니다.
전체 품목코드 개수가 44,469개가 있어서 전체 index를 0부터 44,469까지 넣어서 페이지 크롤링을 진행했습니다.

### crawling function part
크롤링과 데이터베이스 구축 함수는 크게 3가지를 수집했습니다.

1. 의약품명
2. 의약품 유효성분
3. 의약품의 위험정보 (DUR system)

각각의 페이지 태그 위치에서 데이터가 수집된다면 해당 부분 문자열 데이터를 불러옵니다.  
그 후 문자열 파싱을 통해서 데이터를 처리합니다.

그 후 최종적으로 페이지별로 데이터베이스에 데이터를 삽입합니다.

---
# 데이터 출처
- [식약처-의약품안전나라](https://nedrug.mfds.go.kr/index)
