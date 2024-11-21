from pydantic import BaseModel, __version__ as pydantic_version
import google.generativeai as genai
import streamlit as st
from pydantic import BaseModel
import pandas as pd
import json

# API-Key aus Umgebungsvariable laden
google_api_key = st.secrets.GOOGLE_API_KEY
genai.configure(api_key=google_api_key)

# Modell-Definition
class QuizQuestion(BaseModel):
    number: int
    question: str
    answers: list[str]
    time_limit: int
    correct_answer: int

class QuizQuestions(BaseModel):
    questions: list[QuizQuestion]

# Funktion zur Generierung von Quizfragen
def generate_quiz_gemini(content, num_questions=10, num_seconds=60, model_name='gemini-1.5-flash'):
    model = genai.GenerativeModel(model_name)
    
    prompt = f"Erstelle {num_questions} Quizfragen zum folgenden Inhalt. Das Zeitlimit ist immer {num_seconds} Sekunden und die korrekte Antwort ist 1, 2, 3 oder 4: {content}. Bitte Antworte als JSON-Format mit folgender Struktur: {QuizQuestions.model_json_schema()}"
    
    response = model.generate_content(prompt)
    
    # Zugriff auf den Text-Inhalt
    response_text = response.text

    # print(response_text)

    # Bereinige den JSON-String
    response_text = response.text.strip()
    if response_text.startswith('```json'):
        response_text = response_text.replace('```json', '', 1)
    if response_text.endswith('```'):
        response_text = response_text[:-4]
    response_text = response_text.strip()

    # print(response_text)

    # Parse JSON-String
    quiz_data = json.loads(response_text)

    # print(quiz_data)

    # Verwende die tatsächlichen Fragen
    questions = [
        QuizQuestion(
            number=q['number'],
            question=q['question'],
            answers=q['answers'],
            time_limit=q['time_limit'],
            correct_answer=q['correct_answer']
        ) for q in quiz_data['questions']
    ]
    
    # Konvertierung in DataFrame
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

# # Beispielaufruf
# content = example_text
# quiz_df = generate_quiz_questions(content)
# print("\nQuiz Fragen:")
# pd.set_option('display.max_columns', None)  # Zeigt alle Spalten
# pd.set_option('display.max_colwidth', None)  # Zeigt vollständigen Inhalt
# print(quiz_df)