# 모여라 커넥터 API
신청곡을 받아 서버 컴퓨터에서 크롬으로 유투브 영상을 재생하는 API 서버입니다.   
DB 모델링과 Django와 Django RestFramework를 익히기 위한 토이 프로젝트입니다. 

기간 : 20.10.05 ~ 20.10.16

## 빌드 방법
```bash
# 레포지토리 클론
git clone https://github.com/kor-Chipmunk/moyeora_connector.git
cd moyeora_connector

# 파이썬 가상환경 라이브러리 설치
pip3 install virtualenv
virtualenv venv
source venv/bin/activate

# 의존성 라이브러리 설치
pip install -r requirements.txt

# DB 마이그레이트
python manage.py makemigrations
python manage.py migrate

# 서버 실행
python manage.py runserver

# 프로덕션 모드 실행
python manage.py runserver --settings=moyeora_connector.settings.production

```

## 제보
위 레포지토리의 Issues 탭을 활용해 주세요.

## 기여자
1. [kor-Chipmunk](https://www.github.com/kor-Chipmunk)
