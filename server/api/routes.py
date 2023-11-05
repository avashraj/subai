from fastapi import APIRouter, File, UploadFile
from .models import Quiz, Difficulty, Question, Answer, Req
from .db import connect_client, class_name
from speechtotext.main import transcribe_audio_to_text
from datetime import datetime
import time
from nltk.tokenize import sent_tokenize

import nltk

nltk.download("punkt")


router = APIRouter()
client = connect_client()


# recv file,save_file, get text, insert text in db and text with id
@router.post("/upload_file")
async def upload_file(file: UploadFile):
    # Save file
    save_path = f"api/upload/{int(time.mktime(datetime.timetuple(datetime.now())))}.mp3"
    with open(save_path, "wb") as f:
        f.write(file.file.read())
    print(save_path)
    # Get text
    text = transcribe_audio_to_text(save_path)
    sentences = [
        {"title": f"{idx}", "body": x} for idx, x in enumerate(sent_tokenize(text))
    ]

    # Batch addition of sentences
    client.batch.configure(batch_size=100, num_workers=3, dynamic=True)
    with client.batch as batch:
        for sentence in sentences:
            batch.add_data_object(sentence, class_name)

    return text


@router.post("/answer", response_model=Answer)
async def get_ans(r: Req):
    return Answer(text="test")


# Return quiz
@router.get("/start_quiz", response_model=Quiz)
async def start_quiz():
    return Quiz(
        difficulty=Difficulty.HARD,
        questions=[
            Question(text="sample question", choices=["1", "2", "3", "4"], answer="2")
        ],
    )
