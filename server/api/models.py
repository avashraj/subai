from typing import List, Optional
from pydantic import BaseModel
from enum import Enum


class Difficulty(str, Enum):
    EASY = "Easy"
    MEDIUM = "Medium"
    HARD = "Hard"


class Question(BaseModel):
    text: str
    choices: List[str]
    answer: str


class Quiz(BaseModel):
    questions: List[Question]
    difficulty: Difficulty


class Req(BaseModel):
    lecture_id: Optional[str]
    question: str
