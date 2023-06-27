import shlex
import subprocess
import json
from metaflow import step, FlowSpec, kubernetes, schedule, current, Flow
import time


class AudioTranscription(FlowSpec):
    @step
    def start(self):
        self.next(self.transcribe)

    @step
    def transcribe(self):
        import whisper

        url = 'https://upload.wikimedia.org/wikipedia/commons/4/4f/An_address_by_Opposition_Leader_Anthony_Albanese.ogg'
        print(f"### transcribing ###")

        model_to_use = "tiny"
        # Transcribe to text using the "tiny" whisper model
        model = whisper.load_model(model_to_use)
        result = model.transcribe(url, fp16=False)
        print(result)
        self.next(self.end)

    @step
    def end(self):
        pass

if __name__ == '__main__':
    AudioTranscription()
