# Patech_Server

## LOCAL 내 실행법

### 선행조건:
MySQL 깔려있어야 함.

### 과정

MySQL에서 DB 생성

폴더 내 MySetting에 DB 정보 작성


    DATABASES = {
        'default' : {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'plant_db',
            'USER': 'root',
            'PASSWORD': '0000',
            'HOST': 'localhost',
            'PORT': '3306',
        }
    }



    
가상환경 실행

    python -m venv venv
    .\venv\Scripts\activate
    pip install -r requirements.txt

마이그래이션

    python manage.py makemigrations
    python manage.py migrate

서버실행

    python manage.py runserver 8000
