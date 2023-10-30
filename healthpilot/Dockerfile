FROM python:3.10-slim
ENV PYTHONUNBUFFERED 1
RUN mkdir /healthpilot
WORKDIR /healthpilot

RUN apt-get update
RUN apt-get -y install gcc
RUN pip install --upgrade pip
# RUN addgroup app && adduser --system --ingroup app app
# USER app

COPY requirements.txt /healthpilot
RUN pip install -r /healthpilot/requirements.txt

COPY . /healthpilot

