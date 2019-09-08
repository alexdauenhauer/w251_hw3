FROM w251/cuda:dev-tx2-4.2.1_b97

ARG URL=http://169.44.201.108:7002/jetpacks/4.2.1

RUN apt-get update && apt install -y git pkg-config wget build-essential cmake unzip


WORKDIR /tmp
# RUN rm *.deb

RUN curl $URL/libopencv_3.3.1-2-g31ccdfe11_arm64.deb  -so libopencv_3.3.1-2-g31ccdfe11_arm64.deb
RUN curl $URL/libopencv-dev_3.3.1-2-g31ccdfe11_arm64.deb -so libopencv-dev_3.3.1-2-g31ccdfe11_arm64.deb
RUN curl $URL/libopencv-python_3.3.1-2-g31ccdfe11_arm64.deb -so libopencv-python_3.3.1-2-g31ccdfe11_arm64.deb

RUN apt install -y  libtbb-dev libavcodec-dev libavformat-dev libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev libgtk2.0-dev
RUN apt install -y libswscale-dev libv4l-dev
RUN dpkg -i *.deb

RUN apt install -y libcanberra-gtk-module libcanberra-gtk3-module libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev 

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

# load face detection code
WORKDIR /
RUN git clone https://github.com/alexdauenhauer/w251_hw3.git
WORKDIR /w251_hw3

RUN rm -f /tmp/*.deb

CMD git pull origin master
CMD python3 faceDetection.py