from pydantic import BaseModel, __version__ as pydantic_version
import google.generativeai as genai
import pandas as pd
import streamlit as st
import json

# API-Key aus Umgebungsvariable laden
google_api_key = st.secrets.GOOGLE_API_KEY
genai.configure(api_key=google_api_key)

# Funktion zur Generierung von Frage-Antwort-Paaren
def generate_3_grammar_gemini(model_name, grammar_topic, number_exercises, exercises_type):

    print("model_name_3_grammar_gemini", model_name)

    # Format entsprechend der QuestionAnswerPairs Klasse
    format = """{
        "question_answer_pairs": [
            {
                "exercise_solution_pair_number": 1,
                "exercise": "Exercise task",
                "solution": "Solution"
            }
        ]
    }"""

    try:    
        model = genai.GenerativeModel(model_name)
        
        prompt = f"""Create a list of {number_exercises} Exercises and Solutions in structured format to practise EXACTLY the: {grammar_topic}
        Answer in JSON format with EXACTLY this structure: {format} {exercises_type}"""

        print("prompt", prompt)

        response = model.generate_content(prompt)

        response_text = response.text.strip()

        # print("response_text", response_text)
        
        # JSON-String bereinigen
        if response_text.startswith('```json'):
            response_text = response_text.replace('```json', '', 1)
        if response_text.endswith('```'):
            response_text = response_text[:-3]

        response_text = response_text.strip()
        
        # JSON parsen
        exercise_data = json.loads(response_text)

        # print("exercise_data", exercise_data)
        
        # Antwortdaten extrahieren und zurückgeben
        list_exercises = []
        for pair in exercise_data['question_answer_pairs']:
            list_exercises.append({
                "exercise": pair['exercise'],
                "solution": pair['solution']
            })

        print("list_exercises", list_exercises)

        return list_exercises
    
    except Exception as e:
        print("Error", e)
        print("model_name_3_grammar_gemini", model_name)
        return "error"
