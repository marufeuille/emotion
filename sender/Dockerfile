FROM python:3.5
MAINTAINER Masahiro Ishii <marufeuille@gmail.com>
RUN apt update && apt -y upgrade && apt -y install git && pip install pika aliyun-log-python-sdk
COPY ./src /root/sender
CMD python3 /root/sender/index.py
