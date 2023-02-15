# OpenAI Whisper on Metaflow 👋

This repository will help you optimize Open AI's [Whisper](https://github.com/openai/whisper) in workflows run on the [Outerbounds Platform](https://outerbounds.com/blog/announcing-outerbounds-platform/). It builds on our earlier repository to help you [Get started with Whisper with Metaflow](https://github.com/outerbounds/whisper-metaflow). This implementation focuses on using Kubernetes resources to unlock new levels of scale and processing throughput. 

<img src="./static/Whisper-Cover.png" width=600> </img>

## Repository Overview

| File           | Description |
|------------------|-------------|
| [Dockerfile](./Dockerfile)   | Dockerfile to create a docker image for running OpenAI Whisper |
| [Makefile](./Makefile)   | Makefile for building the docker image |
| [youtube_video_transcriber.py](./youtube_video_transcriber.py)   | CLI tool for creating a transcript of a given YouTube URL and given model |
| [whisper_flow.py](./whisper_flow.py) | Metaflow flow for creating transcripts of using whispers tiny and large model s|

# Configure flow dependencies ⚙️

This section assumes you have Docker setup and running locally. If you don't have Docker installed, please follow the instructions [here](https://docs.docker.com/get-docker/).

## Create the docker image
With Docker running, build the image specified in the `./Dockerfile`. 

```
$ make build
...
 => => writing image sha256:23be1b523a3404d8bee8e4c8ac29f7160ac7ad7090d48c567010a34cb9f2666e                                                           0.0s
 => => naming to docker.io/library/whisper-metaflow:v1alpha1                                                                                           0.0s
```

## Tag and push the docker image to a repository.
Then tag the resultant image and push it to an image registry. In this example, we are using GitLab's container registry.
```
$ docker tag sha256:23be1b523a3404d8bee8e4c8ac29f7160ac7ad7090d48c567010a34cb9f2666e registry.gitlab.com/shri_javadekar/scratch/whisper-metaflow:latest
...

$ docker push registry.gitlab.com/shri_javadekar/scratch/whisper-metaflow
```

# Run the flow ▶️

<img src="./static/MLSys-02.png" width=600> </img>

## Running with Kubernetes resources
To unleash the power of the cloud with [Metaflow's Kubernetes decorator](https://docs.metaflow.org/scaling/remote-tasks/kubernetes), uncomment the lines with `@kubernetes` in the [flow code](./whisper_flow.py). Make sure to change the image argument to the container registry you just pushed to!
    
## Flow time!
After preparing your Kubernetes resources like you want, save the `./whisper_flow.py` file, and run this command from your terminal. 
```
$ python3 whisper_flow.py run --with kubernetes:image=registry.gitlab.com/shri_javadekar/scratch/whisper-metaflow
```
  
# Get Help 🤗
Please join us on [Slack](http://slack.outerbounds.co/) if you have questions about getting setup. The Metaflow community is responsive and happy to help!
