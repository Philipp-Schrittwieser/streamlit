from pydantic import BaseModel
from openai import OpenAI
import pandas as pd
import streamlit as st
import json

openai_api_key = st.secrets.OPENAI_API_KEY

class QuizQuestion(BaseModel):
    number: int
    question: str
    answers: list[str]
    time_limit: int
    correct_answer: int

class QuizQuestions(BaseModel):
    questions: list[QuizQuestion]

def generate_quiz_gpt(content, num_questions=10, num_seconds=60, model="gpt-4o-mini-2024-07-18"):
    client = OpenAI(api_key=openai_api_key)
    
    messages = [
        {"role": "system", "content": "Create a quiz in JSON format with questions and answers, the correct answer should vary between 1 and 4"},
        {"role": "user", "content": f"Create {num_questions} quiz questions for the content, the time limit is always {num_seconds} and the correct answer is 1, 2, 3 or 4: {content}, the correct answer should vary! Please annswer in JSON using the following schema: {QuizQuestions.model_json_schema()}"}
    ]
    
    completion = client.chat.completions.create(
        model=model,
        messages=messages,
        response_format={"type": "json_object"},
    )

    print(f"Prompt: {messages}")

    result = json.loads(completion.choices[0].message.content)
    print(f"Result: {result}")

    questions = result['questions']

    df = pd.DataFrame([
        {
            'Number': q['number'],
            'Question - max 120 characters': q['question'],
            'Answer 1 - max 75 characters': q['answers'][0],
            'Answer 2 - max 75 characters': q['answers'][1],
            'Answer 3 - max 75 characters': q['answers'][2],
            'Answer 4 - max 75 characters': q['answers'][3],
            'Time limit (sec) – 5, 10, 20, 30, 60, 90, 120, or 240 secs': q['time_limit'],
            'Correct answer(s) - choose at least one': q['correct_answer']
        }
        for q in questions
    ])

    return df