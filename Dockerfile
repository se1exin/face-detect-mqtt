FROM python:3.7

RUN apt-get update \
    && apt-get install -y python3-opencv

WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt

CMD python main.py
