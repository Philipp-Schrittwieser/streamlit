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
def generate_1_text_gemini(model_name, topic):

    print("model_name_1_text_gemini", model_name)
    try:
        # Create the model
        generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 8192,
            "response_mime_type": "text/plain",
        }
        model = genai.GenerativeModel(model_name=model_name, generation_config=generation_config)

        # Das funktioniert viel besser als das komplexe Schema und auch für beide Modelle
        format = "{'properties': {'title': 'Themenüberschrift', 'content': 'Text über das Thema...'}}"
        
        prompt = f"""Erstelle einen strukturierten Lesetext zum Thema {topic} für SchülerInnen, die 14 Jahre alt sind.
        Antworte im JSON-Format mit GENAU dieser Struktur: {format} Nutze Markdown für die Formatierung."""

        print("prompt", prompt)
        
        response = model.generate_content(prompt)

        print("response", response)

        response_text = response.text.strip()
        
        # JSON-String bereinigen
        if response_text.startswith('```json'):
            response_text = response_text.replace('```json', '', 1)
        if response_text.endswith('```'):
            response_text = response_text[:-3]

        response_text = response_text.strip()
        
        # JSON parsen
        text_data = json.loads(response_text)
        print("text_data", text_data)
    
        content = text_data['properties']['content']
        
        print("content", content)
        
        return content
    
    except Exception as e:
        print("Error", e)
        print("model_name_1_text_gemini", model_name)
        return "error"
