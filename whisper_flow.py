import shlex
import subprocess
import json
from metaflow import step, FlowSpec, kubernetes


class TranscriptionFlow(FlowSpec):
    @step
    def start(self):
        self.urls = [
            'https://www.youtube.com/watch?v=hi1kmipRApg',
            'https://www.youtube.com/watch?v=i1ydhUkrlvw',
            'https://www.youtube.com/watch?v=S5I7987x2_I'
        ]        
        self.next(self.transcribe, foreach='urls')

    @step
    def transcribe(self):
        # For each of the inputs, call a function for transcribing using the 'tiny' or 'large' model. 
        print(f"### transcribing {self.input} ###")
        self.next(self.tiny, self.large)

    #@kubernetes(memory=1024, cpu=4, image="registry.gitlab.com/shri_javadekar/scratch/whisper-metaflow@sha256:d9beb3c2fc03e8c21eac006e16cb96042990855a1e76327b98e1440ab2ae898a")
    #@kubernetes(image="registry.gitlab.com/shri_javadekar/scratch/whisper-metaflow@sha256:d9beb3c2fc03e8c21eac006e16cb96042990855a1e76327b98e1440ab2ae898a")
    @step
    def tiny(self):
        print(f"*** transcribing {self.input} with Whisper tiny model ***")
        cmd = 'python3 youtube_video_transcriber.py ' + self.input + " tiny"
        p = subprocess.run(shlex.split(cmd), capture_output=True)
        json_result = p.stdout.decode()
        print(json_result)        
        self.result = json.loads(json_result)
        self.next(self.join)

    #@kubernetes(memory=15000, cpu=6, image="registry.gitlab.com/shri_javadekar/scratch/whisper-metaflow@sha256:d9beb3c2fc03e8c21eac006e16cb96042990855a1e76327b98e1440ab2ae898a")
    #@kubernetes(image="registry.gitlab.com/shri_javadekar/scratch/whisper-metaflow@sha256:d9beb3c2fc03e8c21eac006e16cb96042990855a1e76327b98e1440ab2ae898a")
    @step
    def large(self):
        print(f"*** transcribing {self.input} with Whisper large model ***")        
        cmd = 'python3 youtube_video_transcriber.py ' + self.input + " large"
        p = subprocess.run(shlex.split(cmd), capture_output=True)
        json_result = p.stdout.decode()
        print(json_result)
        self.result = json.loads(json_result)
        self.next(self.join)

    @step
    def join(self, inputs):
        print('tiny is %s' % inputs.tiny.result)
        print('large is %s' % inputs.large.result)
        print('isdiff %s' % inputs.tiny.result != inputs.large.result)
        self.next(self.postjoin)

    @step
    def postjoin(self, inputs):
        self.next(self.end)

    @step
    def end(self):
        pass

if __name__ == '__main__':
    TranscriptionFlow()
