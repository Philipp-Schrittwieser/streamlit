from pydantic import BaseModel, __version__ as pydantic_version
from openai import OpenAI, version
import pandas as pd
import streamlit as st

openai_api_key = st.secrets.OPENAI_API_KEY

class ReadersText(BaseModel):
    text: str

def generate_1_text_gpt(topic, model="gpt-4o-mini-2024-07-18"):
    client = OpenAI(api_key=openai_api_key)
    completion = client.beta.chat.completions.parse(
        model=model,
        messages=[
            {"role": "system", "content": "Erstelle einen Lesetext im strukturierten Format"},
            {"role": "user", "content": f"Erstelle einen Lesetext zum Thema: {topic} für SchülerInnen, die 14 Jahre alt sind."}
        ],
        response_format=ReadersText,
    )

    text = completion.choices[0].message.parsed.text  

    # print(text)

    return text

