FROM ubuntu:xenial
MAINTAINER Zach Musgrave <ztm@zachm.us>

RUN apt-get update
RUN apt-get install -y python3 python3-pip
RUN apt-get install -y libyaml-dev libpcre3-dev
RUN pip3 install --upgrade pip

ADD requirements.txt /code/requirements.txt
RUN pip3 install -Ur /code/requirements.txt

ADD . /code
WORKDIR /code

CMD uwsgi --ini emissary.uwsgi.ini --wsgi-file emissary/uwsgi.py
EXPOSE 8008
