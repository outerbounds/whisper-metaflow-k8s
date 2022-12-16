FROM --platform=linux/amd64 python:3.10-slim

RUN apt-get update -y && \
    apt-get install git -y

RUN apt-get install ffmpeg -y

RUN pip3 install git+https://github.com/openai/whisper.git
RUN pip3 install coolname
RUN pip3 install pytube
RUN pip3 install requests
RUN pip3 install awscli
RUN pip3 install boto3

RUN ln -s /usr/bin/python3 /usr/bin/python
COPY youtube_video_transcriber.py /

CMD ["python3"]
