# 기본 이미지로 Ubuntu 22.04 사용
FROM python:3.10

# 비대화적인 프론트엔드로 설정 (Docker 내에서 사용자 입력 없이 설치 가능하게 함)
ENV DEBIAN_FRONTEND=noninteractive

# 필수 패키지 및 도구 설치
RUN apt-get update && apt-get install -y \
    build-essential \
    python3.10 \
    python3-pip \
    git \
    && rm -rf /var/lib/apt/lists/*

# Python 3.10을 python으로 사용 설정
RUN ln -s /usr/bin/python3.10 /usr/bin/python

# 애플리케이션 파일 추가
COPY . /app

# 작업 디렉토리 설정
WORKDIR /app

# 필요한 Python 패키지 설치
RUN pip install --no-cache-dir -r requirements.txt

# 또 다른 app 디렉토리로 작업 디렉토리 변경
WORKDIR /app/app

# 파일 병합 명령어 추가
RUN cat pth/model_best_5_part_* > pth/model_best_5.pth

# 애플리케이션 실행
CMD ["python", "main.py"]
