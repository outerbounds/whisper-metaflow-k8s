import shlex
import subprocess
import json
from metaflow import step, FlowSpec, kubernetes, schedule, current, Flow


@schedule(hourly=True)
class SixMinVideoTranscription(FlowSpec):
    @step
    def start(self):
        self.urls = [
        'https://www.youtube.com/watch?v=uxtXEuK05-w',
        'https://www.youtube.com/watch?v=MgoZwkSXzGw',
        'https://www.youtube.com/watch?v=1iHeeMlOsyc']

        run = Flow(current.flow_name)[current.run_id]
        for u in self.urls:
            run.add_tag(u.split("v=")[-1])
        self.next(self.transcribe, foreach='urls')

    @step
    def transcribe(self):
        # For each of the inputs, call a function for transcribing using the 'tiny' or 'large' model.
        print(f"### transcribing {self.input} ###")
        self.next(self.tiny, self.large)

    @step
    def tiny(self):
        print(f"*** transcribing {self.input} with Whisper tiny model ***")
        cmd = 'python3 youtube_video_transcriber.py ' + self.input + " tiny"
        p = subprocess.run(shlex.split(cmd), capture_output=True)
        json_result = p.stdout.decode()
        print(json_result)
        self.result = json.loads(json_result)
        self.next(self.join)

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
    SixMinVideoTranscription()
