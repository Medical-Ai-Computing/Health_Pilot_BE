FROM python:3.10-slim
ENV PYTHONUNBUFFERED 1
RUN mkdir /healthpilot
WORKDIR /healthpilot

RUN apt-get update
RUN apt-get -y install gcc
RUN pip install --upgrade pip

# Install spaCy and download English language model
RUN pip install spacy && python -m spacy download en_core_web_sm

# USER app

COPY requirements.txt /healthpilot
RUN pip install -r /healthpilot/requirements.txt

COPY . /healthpilot

