FROM python:3.11-buster

RUN apt-get update \
    && apt-get install libgomp1 \
    && apt-get install -y gcc git

RUN pip install -U pip setuptools wheel
RUN pip install poetry==1.5.1

WORKDIR /app
RUN poetry config virtualenvs.create true \
    && poetry config virtualenvs.in-project true
