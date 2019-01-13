FROM python:3.5
MAINTAINER Masahiro Ishii <marufeuille@gmail.com>
RUN apt update && apt -y upgrade && apt -y install git && pip install opencv-python numpy keras tensorflow pika aliyun-log-python-sdk
COPY ./src /root/classifier
CMD python3 /root/classifier/index.py
