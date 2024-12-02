from pydantic import BaseModel, __version__ as pydantic_version
import google.generativeai as genai
import pandas as pd
import streamlit as st
import json

# API-Key aus Umgebungsvariable laden
google_api_key = st.secrets.GOOGLE_API_KEY
genai.configure(api_key=google_api_key)

# Funktion zur Generierung von Frage-Antwort-Paaren
def generate_4_games_gemini(model_name, topic, game_type):

    if game_type != "Allgemein":
        add_game_type = f" und der Fokus liegt auf {game_type}."
    else:
        add_game_type = ""

    try:    
        model = genai.GenerativeModel(model_name)

        # Das funktioniert viel besser als das komplexe Schema und auch für beide Modelle
        format = "{'content': ['name': 'Name des Spiels', 'description': 'Kurze Beschreibung des Spiels']}"
        
        prompt = f"""Gib mir richtig coole und lustige Ideen für Lernspiele, die keine Vorbereitung erfordern und meine 14 Jährigen SuS richtig Spaß machen zum Thema: {topic} {add_game_type}. Antworte im JSON-Format mit GENAU dieser Struktur: {format}"""

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
        games_data = json.loads(response_text)

        print("games_data", games_data)
        
        # Antwortdaten extrahieren und zurückgeben
        markdown_text = games_data['content']
        return markdown_text
    
    except Exception as e:
        print("Error", e)
        print("model_name_3_grammar_gemini", model_name)
        return "error"
