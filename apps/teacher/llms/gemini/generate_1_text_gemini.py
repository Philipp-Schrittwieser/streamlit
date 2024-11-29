from pydantic import BaseModel, __version__ as pydantic_version
import google.generativeai as genai
import pandas as pd
import streamlit as st
import json

# API-Key aus Umgebungsvariable laden
google_api_key = st.secrets.GOOGLE_API_KEY
genai.configure(api_key=google_api_key)

class StructuredText(BaseModel):
    content: str

# Funktion zur Generierung eines strukturierten Lesetextes
def generate_1_text_gemini(topic, model_name='gemini-1.5-flash'):
    model = genai.GenerativeModel(model_name)
    
    prompt = f"""Erstelle einen strukturierten Lesetext zum Thema {topic} für SchülerInnen, die 14 Jahre alt sind.
    Antworte im JSON-Format mit dieser Struktur: {StructuredText.model_json_schema()}"""

    # print("prompt", prompt)
    
    response = model.generate_content(prompt)

    # print("response", response)

    response_text = response.text.strip()
    
    # JSON-String bereinigen
    if response_text.startswith('```json'):
        response_text = response_text.replace('```json', '', 1)
    if response_text.endswith('```'):
        response_text = response_text[:-3]

    response_text = response_text.strip()
    
    # JSON parsen
    text_data = json.loads(response_text)
    # print("text_data", text_data)
   
    content = text_data['properties']['content']['content']
    # print("content", content)
    
    return content
