FROM python:3.7-buster

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get autoremove -y 

RUN apt-get install -y \
    gcc libssl-dev \
    libffi-dev build-essential \
    zlib1g-dev wget unzip cmake \
    python3-dev gfortran \
    libblas-dev liblapack-dev \
    libatlas-base-dev python-dev \
    libx11-dev python3 gcc \
    musl-dev g++ \
    libxml2 libxml2-dev \
    libxslt-dev postgresql-client libpq-dev

RUN apt-get clean


WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir psycopg2
RUN python -m pip install -U pip wheel setuptools

RUN pip install -r /app/requirements.txt

RUN source .env 

COPY . /app/
