import whisper

audio_path = "sample1.flac"

model = whisper.load_model("base")
result = model.transcribe( audio_path, fp16=False)

with open("transcription_sample.txt", "w") as file:
    file.write(result["text"])


