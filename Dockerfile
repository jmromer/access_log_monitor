FROM python:3.7.0-alpine

RUN apk update \
&& apk add \
build-base \
postgresql \
postgresql-dev \
libpq

RUN touch /var/log/access.log
RUN mkdir /usr/src/app/

WORKDIR /usr/src/app/
ADD . /usr/src/app/

COPY Pipfile .
RUN pip install -U pip pipenv
RUN pipenv install --dev

ENV PYTHONUNBUFFERED 1

COPY . .
