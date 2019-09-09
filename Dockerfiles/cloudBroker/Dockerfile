FROM ubuntu

RUN apt-get update \
  && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    python3-pip \
    python3-setuptools \
    python3-dev \
    python3-numpy \
  && rm -rf /var/lib/apt/lists/*

RUN pip3 install paho-mqtt
RUN pip3 install ibm-cos-sdk

WORKDIR /
RUN git clone https://github.com/alexdauenhauer/w251_hw3.git
WORKDIR /w251_hw3

RUN git pull origin master

# CMD python3 saveToBucket.py
