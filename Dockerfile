FROM python:3.10.12-alpine

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements/production.txt requirements.txt

RUN pip install pip --upgrade  && pip install -r requirements.txt

RUN mkdir -p /home/app

ENV HOME=/home/app

ENV APP_HOME=/home/app/web

WORKDIR $APP_HOME

COPY . .

CMD ["python", "main.py"]