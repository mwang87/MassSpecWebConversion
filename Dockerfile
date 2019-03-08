FROM chambm/pwiz-skyline-i-agree-to-the-vendor-licenses:3.0.19056-6b6b0a2b4

MAINTAINER Mingxun Wang "mwang87@gmail.com"

RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential

RUN pip install ftputil
RUN pip install flask
RUN pip install gunicorn
RUN pip install requests

#RUN useradd mingxun
#USER mingxun

COPY . /app
WORKDIR /app
