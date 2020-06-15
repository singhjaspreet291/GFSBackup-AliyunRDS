FROM ubuntu:latest
RUN apt-get update \
  && apt-get install -y vim python3 python3-pip python3-setuptools  mysql-client --no-install-recommends \
  && rm -rf /var/lib/apt/lists/* \
  && pip3 install wheel \
  && pip3 install oss2
ADD <scriptfiles> /home/
