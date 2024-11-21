from pydantic import BaseModel, __version__ as pydantic_version
from openai import OpenAI, version
import pandas as pd
import streamlit as st

input_text = """Klimawandel
Einleitung
Der Klimawandel ist ein wichtiges Thema, das jeden von uns betrifft. In diesem Text werden wir die Ursachen, die Auswirkungen und mögliche Lösungen des Klimawandels näher betrachten.

Was ist Klimawandel?
Der Klimawandel beschreibt die langfristigen Veränderungen des Klimas auf der Erde. Dies geschieht vor allem durch menschliche Aktivitäten, die zu einer Erhöhung der Treibhausgase in der Atmosphäre führen. Treibhausgase wie Kohlenstoffdioxid (CO2) und Methan (CH4) wirken wie eine Decke, die die Wärme in der Atmosphäre festhält.

Ursachen des Klimawandels
Die Hauptursachen des Klimawandels sind:

Fossile Brennstoffe: Wenn wir Kohle, Öl und Erdgas verbrennen, gelangen große Mengen CO2 in die Atmosphäre.
Abholzung: Bäume nehmen CO2 aus der Luft auf. Wenn Wälder gerodet werden, wird der gespeicherte Kohlenstoff wieder freigesetzt.
Industrie und Landwirtschaft: Diese Bereiche produzieren ebenfalls große Mengen an Treibhausgasen, beispielsweise durch die Verwendung chemischer Düngemittel und die Viehzucht.
Auswirkungen des Klimawandels
Der Klimawandel hat weltweit massive Auswirkungen:

Temperaturanstieg: Die Durchschnittstemperaturen auf der Erde steigen, was zu Hitzewellen führt.
Extreme Wetterereignisse: Häufigere Stürme, Überschwemmungen und Dürreperioden gefährden Menschen und die Umwelt.
Schmelzen der Pole: Gletscher und das Polareis schmelzen, was den Meeresspiegel ansteigen lässt und Küstenregionen gefährdet.
Biodiversität: Viele Tiere und Pflanzen können sich nicht schnell genug an die veränderten Bedingungen anpassen und sterben aus.
Lösungen gegen den Klimawandel
Es gibt viele Möglichkeiten, wie wir den Klimawandel bekämpfen können:

Erneuerbare Energien: Die Nutzung von Sonnen-, Wind- und Wasserkraft anstelle von fossilen Brennstoffen kann die CO2-Emissionen erheblich senken.
Energieeffizienz: Energiesparende Geräte und Maßnahmen zur Isolierung von Gebäuden helfen, den Energieverbrauch zu reduzieren.
Nachhaltige Mobilität: Der Umstieg von Auto auf Fahrrad oder öffentliche Verkehrsmittel reduziert den Ausstoß von Treibhausgasen.
Bewusstsein schaffen: Aufklärung über die Folgen des Klimawandels motiviert mehr Menschen, aktiv zu werden.
Fazit
Der Klimawandel ist eine der größten Herausforderungen unserer Zeit. Jeder Einzelne kann dazu beitragen, ihn abzubremsen. Durch bewusste Entscheidungen im Alltag und das Engagement in der Gemeinschaft können wir gemeinsam an einer besseren Zukunft arbeiten"""

dict_for_word = {}

# openai_api_key = st.secrets.OPENAI_API_KEY

class QuestionAnswerPair(BaseModel):
    question_answer_pair_number: int
    question: str
    answer: str

class QuestionAnswerPairs(BaseModel):
    question_answer_pairs: list[QuestionAnswerPair]

def generate_2_qas_gpt(input, model="gpt-4o-mini"):
    # client = OpenAI(api_key=openai_api_key)
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
        
