# OpenAI Whisper on Metaflow

This repo contains files for running OpenAI Whisper as a flow on OB Platform.

| File           | Description |
|------------------|-------------|
| [Dockerfile](./Dockerfile)   | Dockerfile to create a docker image for running OpenAI Whisper |
| [Makefile](./Makefile)   | Makefile for building the docker image |
| [youtube_video_transcriber.py](./youtube_video_transcriber.py)   | CLI tool for creating a transcript of a given youtube URL and given model |
| [whisper_flow.py](./whisper_flow.py) | Metaflow flow for creating transcripts of using whispers tiny and large model s|

## How to run this flow?

- Create the docker image

```
$ make build
...
 => => writing image sha256:23be1b523a3404d8bee8e4c8ac29f7160ac7ad7090d48c567010a34cb9f2666e                                                           0.0s
 => => naming to docker.io/library/whisper-metaflow:v1alpha1                                                                                           0.0s
```

- Tag and push the docker image to a repository.

```
$ docker tag sha256:23be1b523a3404d8bee8e4c8ac29f7160ac7ad7090d48c567010a34cb9f2666e registry.gitlab.com/shri_javadekar/scratch/whisper-metaflow:latest
...

$ docker push registry.gitlab.com/shri_javadekar/scratch/whisper-metaflow
```

- Run the flow with this image

```
$ python3 whisper_flow.py run --with kubernetes:image=registry.gitlab.com/shri_javadekar/scratch/whisper-metaflow
```
  