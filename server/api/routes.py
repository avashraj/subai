from fastapi import APIRouter, UploadFile
from .models import Quiz, Difficulty, Question, Req
from .db import connect_client, class_name, schema
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
    client.schema.delete_class(class_name)
    client.schema.create_class(schema)
    # Batch addition of sentences
    client.batch.configure(batch_size=100, num_workers=3, dynamic=True)
    with client.batch as batch:
        for sentence in sentences:
            batch.add_data_object(sentence, class_name)

    return text


# Use Question and context to generate answer (RAG)
@router.post("/answer")
async def get_ans(r: Req):
    # TODO: Make this prompt good!
    generate_prompt = f"""Provide an answer to the question: {r.question} based on the given context with the following Rules:\n
    Rules:
    1. You are a teaching Chatbot.
    2. Answer Questions like a teacher.
    3. Use only the given context for the answer.
    """

    response = (
        client.query.get(class_name, ["body"])
        .with_generate(grouped_task=generate_prompt)
        .with_near_text({"concepts": [r.question]})
        .do()
    )

    return {
        "text": response["data"]["Get"][class_name][0]["_additional"]["generate"][
            "groupedResult"
        ]
    }


# Return quiz
@router.get("/start_quiz", response_model=Quiz)
async def start_quiz():
    # return Quiz(
    #     difficulty=Difficulty.HARD,
    #     questions=[
    #         Question(text="sample question", choices=["1", "2", "3", "4"], answer="2")
    #     ],
    # )
    return await generate_quiz(lecture_id)


# Generate a quiz from a lecture
@router.get("/generate_quiz/{lecture_id}", response_model=Quiz)
async def generate_quiz(lecture_id: str):
    # Retrieve the lecture from the database
    lecture = client.class_(class_name).get_by_id(lecture_id)

    # Tokenize the lecture text into sentences
    sentences = sent_tokenize(lecture['body'])

    # Create a list to store the questions
    questions = []

    # For each sentence in the lecture
    for i, sentence in enumerate(sentences):
        # Use the sentence as the question
        question_text = sentence

        # Create a list of choices, using the current sentence as the correct answer
        # and three other random sentences as wrong answers
        choices = [sentence, sentences[(i+1)%len(sentences)], sentences[(i+2)%len(sentences)], sentences[(i+3)%len(sentences)]]
        shuffle(choices)
        
        # Add the question to the list
        questions.append(Question(text=question_text, choices=choices, answer=sentence))

    # Create a quiz with the generated questions
    quiz = Quiz(questions=questions, difficulty=Difficulty.EASY)  # Change the difficulty as needed

    return quiz


