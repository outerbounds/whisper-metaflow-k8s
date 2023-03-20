#!/usr/bin/env python3

import sys
import json
import torch
from coolname import generate_slug

url = sys.argv[1]
model_to_use = sys.argv[2]
suffix = generate_slug(2)

def transcribe_video(url, output_path = './', filename = 'audio-' + suffix + '.mp3'):
    import whisper
    from pytube import YouTube
    import time
    import torch

    if torch.cuda.is_available():
        print(f"Using device: gpu")
    else:
        print(f"Using device: cpu")
    start = time.time()
    audio = YouTube(url).streams.get_audio_only()
    audio.download(output_path, filename)
    model = whisper.load_model(model_to_use)
    result = model.transcribe(output_path + filename, fp16=False)

    end = time.time()
    json_result = {}
    logprobs = []
    for s in result['segments']:
        logprobs.append(s['avg_logprob'])
    json_result['avg_logprob'] = sum(logprobs)/len(logprobs)
    json_result['duration_seconds'] = int(end - start)
    json_result['text'] = result['text']

    return json.dumps(json_result)

json_result = transcribe_video(url)
print(json_result)
