from transformers import WhisperProcessor, WhisperForConditionalGeneration
from datasets import load_dataset

processor = WhisperProcessor.from_pretrained("openai/whisper-medium.en")
model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-medium.en")

print("model loaded successfully")