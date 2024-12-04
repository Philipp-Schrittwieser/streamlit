from pydantic import BaseModel, __version__ as pydantic_version
import google.generativeai as genai
import streamlit as st
from pydantic import BaseModel, Field
import pandas as pd
import json

# API-Key aus Umgebungsvariable laden
google_api_key = st.secrets.GOOGLE_API_KEY
genai.configure(api_key=google_api_key)

# Modell-Definition
class QuizQuestion(BaseModel):
    number: int
    question: str
    answers: list[str] = Field(..., min_items=4, max_items=4)  # Genau 4 Antworten
    time_limit: int
    correct_answer: int

class QuizQuestions(BaseModel):
    questions: list[QuizQuestion]

# Funktion zur Generierung von Quizfragen
def generate_0_quiz_gemini(model_name, user_text, num_questions, time_limit, difficulty):
    print("model_name", model_name)
    # print("user_text", user_text)
    # print("num_questions", num_questions)
    # print("time_limit", time_limit)
    # print("difficulty", difficulty)
    try:

        add_difficulty = ""
        if difficulty == "Schwer":
            add_difficulty = "SCHWIERIGE"
        elif difficulty == "Mittel":
            add_difficulty = ""
        elif difficulty == "Leicht":
            add_difficulty = "LEICHTE"

        model = genai.GenerativeModel(model_name)
        
        prompt = f"Erstelle {num_questions} {add_difficulty} Quizfragen zum folgenden Inhalt. Das Zeitlimit ist immer {time_limit} Sekunden und die korrekte Antwort ist 1, 2, 3 oder 4: {user_text}. Bitte Antworte als JSON-Format mit GENAU folgender Struktur: {QuizQuestions.model_json_schema()}"
        
        response = model.generate_content(prompt)
        
        # Zugriff auf den Text-Inhalt
        response_text = response.text

        print(f"response_text: {response_text}")

        # Bereinige den JSON-String
        response_text = response.text.strip()
        if response_text.startswith('```json'):
            response_text = response_text.replace('```json', '', 1)
        if response_text.endswith('```'):
            response_text = response_text[:-4]
        response_text = response_text.strip()

        print(f"response_text: {response_text}")

        # Parse JSON-String
        quiz_data = json.loads(response_text)

        print(f"quiz_data: {quiz_data}")

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

        def clean_tag(text):
            text = str(text)
            if '<' in text and '>' in text:
                # Findet den Text zwischen < und >
                import re
                tag = re.search(r'<([^>]+)>', text)
                if tag:
                    # Ersetzt <tag> mit tag-tag und behält Rest des Texts
                    return text.replace(f'<{tag.group(1)}>', f'{tag.group(1)}-Tag')
            return text
        
        # Konvertierung in DataFrame
        df = pd.DataFrame([
            {
                'Number': clean_tag(str(q.number)),
                'Question - max 120 characters': clean_tag(q.question),
                'Answer 1 - max 75 characters': clean_tag(q.answers[0]), 
                'Answer 2 - max 75 characters': clean_tag(q.answers[1]),
                'Answer 3 - max 75 characters': clean_tag(q.answers[2]),
                'Answer 4 - max 75 characters': clean_tag(q.answers[3]),
                'Time limit (sec) – 5, 10, 20, 30, 60, 90, 120, or 240 secs': clean_tag(str(q.time_limit)),
                'Correct answer(s) - choose at least one': clean_tag(str(q.correct_answer))
            }
            for q in questions
        ])

        return df, False
    
    except Exception as e:
        print("Error", e)
        print("model_name_generate_quiz_gemini", model_name)
        return "error", True


# # Beispielaufruf
# content = example_text
# quiz_df = generate_quiz_questions(content)
# print("\nQuiz Fragen:")
# pd.set_option('display.max_columns', None)  # Zeigt alle Spalten
# pd.set_option('display.max_colwidth', None)  # Zeigt vollständigen Inhalt
# print(quiz_df)