FROM arm64v8/alpine

RUN apk update && apk add mosquitto-clients
RUN apk add git
RUN apk add python3 py3-pip

RUN pip3 install paho-mqtt

WORKDIR /
RUN git clone https://github.com/alexdauenhauer/w251_hw3.git
WORKDIR /w251_hw3

CMD python3 forwardMessage.py
