FROM --platform=linux/amd64 nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04

RUN apt-get update -y && \
    apt-get install git -y

RUN apt-get install ffmpeg -y
RUN apt-get install curl -y

RUN apt install -y --no-install-recommends python3 python3-pip \
    && ln -sf python3 /usr/bin/python \
    && ln -sf pip3 /usr/bin/pip \
    && pip install --upgrade pip \
    && pip install wheel setuptools

RUN pip3 install git+https://github.com/openai/whisper.git
RUN pip3 install coolname
RUN pip3 install pytube
RUN pip3 install requests
RUN pip3 install awscli
RUN pip3 install boto3
RUN pip3 install torch
RUN pip3 install cuda-python
RUN pip3 install numba

# RUN ln -s /usr/bin/python3 /usr/bin/python

# This is required to avoid a crash in pytube
# https://stackoverflow.com/questions/75765213/pytube-attributeerror-nonetype-object-has-no-attribute-span-cipher-py
COPY cipher.py /usr/local/lib/python3.10/dist-packages/pytube/cipher.py

COPY youtube_video_transcriber.py /

CMD ["python3"]
