import whisper

def transcribe_audio_to_text(audio_file_path):

    model = whisper.load_model("base")
    result = model.transcribe( audio_path, fp16=False)
    return result["text"]

