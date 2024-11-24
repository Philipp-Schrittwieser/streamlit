from pydantic import BaseModel, __version__ as pydantic_version
from openai import OpenAI, version
import pandas as pd
import streamlit as st

openai_api_key = st.secrets.OPENAI_API_KEY

class QuizQuestion(BaseModel):
    number: int
    question: str
    answers: list[str]
    time_limit: int
    correct_answer: int

class QuizQuestions(BaseModel):
    questions: list[QuizQuestion]

def generate_quiz_gpt(content, num_questions=10, num_seconds=60, model="gpt-4o-mini"):
    client = OpenAI(api_key=openai_api_key)
    completion = client.beta.chat.completions.parse(
        model=model,
        messages=[
            {"role": "system", "content": "Erstelle Quiz-Fragen im strukturierten Format"},
            {"role": "user", "content": f"Erstelle {num_questions} Quizfragen zum Content, das time_limit ist immer {num_seconds} und correct_answer ist 1, 2, 3 oder 4: {content}, bitte variiere die richtige Antwort immer zwischen 1 und 4"}
        ],
        response_format=QuizQuestions,
    )

    questions = completion.choices[0].message.parsed.questions

    # number=1 question='Was steht die Abkürzung HTML für?' answers=['Hypertext Markup Language', 'High-level Text Markup Language', 'Hypertext Multi Language', 'Hyperlink and Text Markup Language'] time_limit=30 correct_answer=0

    # print(questions)

    # Convert to DataFrame
    df = pd.DataFrame([
        {
            'Number': q.number,
            'Question - max 120 characters': q.question,
            'Answer 1 - max 75 characters': q.answers[0],
            'Answer 2 - max 75 characters': q.answers[1],
            'Answer 3 - max 75 characters': q.answers[2],
            'Answer 4 - max 75 characters': q.answers[3],
            'Time limit (sec) – 5, 10, 20, 30, 60, 90, 120, or 240 secs': q.time_limit,
            'Correct answer(s) - choose at least one': q.correct_answer
        }
        for q in questions
    ])

    return df