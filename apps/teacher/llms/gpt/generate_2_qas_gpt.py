from pydantic import BaseModel, __version__ as pydantic_version
from openai import OpenAI, version
import pandas as pd
import streamlit as st

openai_api_key = st.secrets.OPENAI_API_KEY


class QuestionAnswerPair(BaseModel):
    question_answer_pair_number: int
    question: str
    answer: str

class QuestionAnswerPairs(BaseModel):
    question_answer_pairs: list[QuestionAnswerPair]

def generate_2_qas_gpt(input, model="gpt-4o-mini"):
    client = OpenAI(api_key=openai_api_key)
    completion = client.beta.chat.completions.parse(
        model=model,
        messages=[
            {"role": "system", "content": "Erstelle eine Liste von Frage-Antwort-Paaren im strukturierten Format"},
            {"role": "user", "content": f"Erstelle eine Liste von Frage-Antwort-Paaren für den folgenden Text: {input}"}
        ],
        response_format=QuestionAnswerPairs,
    )

    response = completion.choices[0].message.parsed

    # print(response)

    list_qas = []
   # Beispiel, um auf die Daten zuzugreifen und sie auszugeben
    for pair in response.question_answer_pairs:
        list_qas.append({"question": pair.question, "answer": pair.answer})

    return list_qas
        
