FROM ubuntu:latest

RUN apt-get update
RUN apt-get -qyy install python-pip wget build-essential python-dev

RUN wget http://download.nanomsg.org/nanomsg-0.5-beta.tar.gz
RUN tar xzf nanomsg-0.5-beta.tar.gz && cd nanomsg-0.5-beta && ./configure && make && make install && ldconfig

RUN mkdir /myproject
COPY requirements.txt /myproject/requirements.txt

RUN rm -rf /nanomsg-0.5-beta*

WORKDIR /myproject
RUN pip install -r requirements.txt


