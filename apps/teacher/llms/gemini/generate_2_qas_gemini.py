from pydantic import BaseModel, __version__ as pydantic_version
import google.generativeai as genai
import pandas as pd
import streamlit as st
import json

# API-Key aus Umgebungsvariable laden
google_api_key = st.secrets.GOOGLE_API_KEY
genai.configure(api_key=google_api_key)


## Class funktioniert nicht so gut, vor allem für mehrere Modelle
class QuestionAnswerPair(BaseModel):
    question_answer_pair_number: int
    question: str
    answer: str

class QuestionAnswerPairs(BaseModel):
    question_answer_pairs: list[QuestionAnswerPair]

# Funktion zur Generierung von Frage-Antwort-Paaren
def generate_2_qas_gemini(model_name, input_text, number_questions):

    print("model_name_2_qas_gemini", model_name)

    # Format entsprechend der QuestionAnswerPairs Klasse
    format = """{
        "question_answer_pairs": [
            {
                "question_answer_pair_number": 1,
                "question": "Beispielfrage?",
                "answer": "Beispielantwort"
            }
        ]
    }"""

    try:    
        model = genai.GenerativeModel(model_name)
        
        prompt = f"""Erstelle eine Liste von {number_questions} Frage-Antwort-Paaren im strukturierten Format für den folgenden Text: {input_text}
        Antworte im JSON-Format mit GENAU dieser Struktur: {format}"""

        print("prompt", prompt)

        response = model.generate_content(prompt)

        response_text = response.text.strip()

        print("response_text", response_text)
        
        # JSON-String bereinigen
        if response_text.startswith('```json'):
            response_text = response_text.replace('```json', '', 1)
        if response_text.endswith('```'):
            response_text = response_text[:-3]

        response_text = response_text.strip()
        
        # JSON parsen
        qas_data = json.loads(response_text)

        print("qas_data", qas_data)
        
        # Antwortdaten extrahieren und zurückgeben
        # ... existing code ...

        # Antwortdaten extrahieren und zurückgeben
        list_qas = []
        for pair in qas_data['question_answer_pairs']:
            list_qas.append({
                "question": pair['question'],
                "answer": pair['answer']
            })

        print("list_qas", list_qas)

        print("list_qas", list_qas)
        return list_qas
    
    except Exception as e:
        print("Error", e)
        print("model_name_2_qas_gemini", model_name)
        return "error"
