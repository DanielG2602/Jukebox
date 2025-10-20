FROM python:3.11-slim

RUN apt-get update && \
    apt-get install -y ffmpeg libffi-dev && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./main.py" ]