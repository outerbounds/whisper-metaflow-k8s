from metaflow import step, FlowSpec, resources

class MultiAudioTranscription(FlowSpec):
    @step
    def start(self):
        self.urls = [
        'https://upload.wikimedia.org/wikipedia/commons/4/4f/An_address_by_Opposition_Leader_Anthony_Albanese.ogg',
        'https://upload.wikimedia.org/wikipedia/commons/3/30/Bryan_-_The_Ideal_Republic.ogg',
        'https://upload.wikimedia.org/wikipedia/commons/b/ba/Watson_-_The_German_Peril.ogg']

        self.next(self.transcribe, foreach='urls')

    #@resources(cpu=12)
    @step
    def transcribe(self):
        import whisper

        print(f"### transcribing {self.input} ###")

        model_to_use = "tiny"
        # Transcribe to text using the "tiny" whisper model
        model = whisper.load_model(model_to_use)
        result = model.transcribe(self.input, fp16=False)
        print(result)

        self.next(self.join)

    @step
    def join(self, inputs):
        self.next(self.end)

    @step
    def end(self):
        pass

if __name__ == '__main__':
    MultiAudioTranscription()
