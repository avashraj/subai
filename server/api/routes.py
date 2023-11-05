from fastapi import APIRouter, UploadFile
from .models import Quiz, Difficulty, Question, Req
from .db import (
    connect_client,
    lecture_class_name,
    lecture_schema,
    convo_schema,
    convo_class_name,
)
from speechtotext.main import transcribe_audio_to_text
from datetime import datetime
import time
from nltk.tokenize import sent_tokenize
from random import shuffle

import nltk

nltk.download("punkt")


router = APIRouter()
client = connect_client()


# recv file,save_file, get text, insert text in db and return text
@router.post("/upload_file")
async def upload_file(file: UploadFile):
    # Save file
    save_path = f"api/upload/{int(time.mktime(datetime.timetuple(datetime.now())))}.mp3"
    with open(save_path, "wb") as f:
        f.write(file.file.read())

    # Get text
    text = transcribe_audio_to_text(save_path)
    sentences = [
        {"title": f"{idx}", "body": x} for idx, x in enumerate(sent_tokenize(text))
    ]

    # Delete previous objects, if any
    client.schema.delete_all()
    client.schema.create_class(lecture_schema)
    client.schema.create_class(convo_schema)
    # Batch addition of sentences
    client.batch.configure(batch_size=100, num_workers=3, dynamic=True)
    with client.batch as batch:
        for sentence in sentences:
            batch.add_data_object(sentence, lecture_class_name)

    return text


# Use Question and context to generate answer (RAG), and add to convo db
@router.post("/answer")
async def get_ans(r: Req):
    # TODO: Make this prompt good!
    generate_prompt = f"""Provide an answer to the question: {r.question} based on the given context with the following Rules:\n
    Rules:
    1. You are a teaching Chatbot.
    2. Answer Questions in simple words.
    3. Use only the given context for the answer.
    4. Keep the response Concise and Informative.  
    """

    response = (
        client.query.get(lecture_class_name, ["body"])
        .with_generate(grouped_task=generate_prompt)
        .with_near_text({"concepts": [r.question]})
        .with_limit(10)
        .do()
    )

    print(response)
    answer = response["data"]["Get"][lecture_class_name][0]["_additional"]["generate"][
        "groupedResult"
    ]

    client.data_object.create(
        {"question": r.question, "answer": answer}, convo_class_name
    )

    return {"text": answer}


# Return quiz
@router.get("/start_quiz", response_model=Quiz)
async def start_quiz():
    # Retrieve the lecture from the database
    lecture = client.class_(lecture_class_name)

    # Tokenize the lecture text into sentences
    sentences = sent_tokenize(lecture["body"])

    # Create a list to store the questions
    questions = []

    # For each sentence in the lecture
    for i, sentence in enumerate(sentences):
        # Use the sentence as the question
        question_text = sentence

        # Create a list of choices, using the current sentence as the correct answer
        # and three other random sentences as wrong answers
        choices = [
            sentence,
            sentences[(i + 1) % len(sentences)],
            sentences[(i + 2) % len(sentences)],
            sentences[(i + 3) % len(sentences)],
        ]
        shuffle(choices)

        # Add the question to the list
        questions.append(Question(text=question_text, choices=choices, answer=sentence))

    # Create a quiz with the generated questions
    quiz = Quiz(
        questions=questions, difficulty=Difficulty.EASY
    )  # Change the difficulty as needed

    return quiz
